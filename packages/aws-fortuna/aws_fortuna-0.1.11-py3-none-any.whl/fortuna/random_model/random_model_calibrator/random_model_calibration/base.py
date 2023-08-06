import abc
import collections
import logging
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Tuple

import jax
import jax.numpy as jnp
from flax import jax_utils
from flax.core import FrozenDict
from flax.training.common_utils import stack_forest
from jax import lax, random, value_and_grad
from jax._src.prng import PRNGKeyArray
from jax.tree_util import tree_map
from optax._src.base import PyTree
from tqdm import trange
from tqdm.std import tqdm as TqdmDecorator

from fortuna.data.loader import DataLoader
from fortuna.training.mixin import (InputValidatorMixin,
                                    WithCheckpointingMixin,
                                    WithEarlyStoppingMixin)
from fortuna.training.train_state import TrainState
from fortuna.typing import Array, Batch, Path, Status
from fortuna.utils.builtins import HashableMixin


class RandomModelCalibratorABC(
    HashableMixin,
    WithCheckpointingMixin,
    WithEarlyStoppingMixin,
    InputValidatorMixin,
    metaclass=abc.ABCMeta,
):
    def __init__(
        self,
        *args,
        predict_fn: Callable[[jnp.ndarray], jnp.ndarray],
        save_checkpoint_dir: Optional[Path] = None,
        save_every_n_steps: Optional[int] = None,
        keep_top_n_checkpoints: int = 2,
        disable_calibration_metrics_computation: bool = False,
        eval_every_n_epochs: int = 1,
        **kwargs,
    ):
        super(RandomModelCalibratorABC, self).__init__(*args, **kwargs)
        self.predict_fn = predict_fn
        self.save_checkpoint_dir = save_checkpoint_dir
        self.save_every_n_steps = save_every_n_steps
        self.keep_top_n_checkpoints = keep_top_n_checkpoints
        self.disable_calibration_metrics_computation = disable_calibration_metrics_computation
        self.eval_every_n_epochs = eval_every_n_epochs
        self.multi_device = False

    def calibration_step(
        self,
        state: TrainState,
        train_batch: Batch,
        calib_batch: Batch,
        fun: Callable,
        rng: PRNGKeyArray,
        n_train_data: int,
        n_calib_data: int,
        kwargs: FrozenDict[str, Any] = FrozenDict(),
    ) -> Tuple[TrainState, Dict[str, Any]]:
        # ensure to use a different key at each step
        model_key = random.fold_in(rng, state.step)

        grad_fn = value_and_grad(
            lambda params: self.calibration_loss_step(
                fun,
                params,
                train_batch,
                calib_batch,
                state.mutable,
                model_key,
                n_train_data,
                n_calib_data,
                state.calib_params,
                state.calib_mutable,
                kwargs,
            ),
            has_aux=True,
        )
        (loss, aux), grad = grad_fn(state.params)
        grad, loss = self.sync_gradients_and_loss(grad, loss)

        state = state.apply_gradients(grads=grad, mutable=aux["mutable"])
        return (
            state,
            {
                "loss": loss,
                "outputs": aux["outputs"],
                "logging_kwargs": aux["logging_kwargs"],
            },
        )

    @abc.abstractmethod
    def validation_step(
        self,
        state: TrainState,
        batch: Array,
        fun: Callable,
        rng: PRNGKeyArray,
        n_data: int,
        metrics: Optional[Tuple[Callable[[jnp.ndarray, Array], float], ...]] = None,
        kwargs: FrozenDict[str, Any] = FrozenDict(),
    ) -> Dict[str, jnp.ndarray]:
        pass

    def calibration_step_end(
        self,
        current_epoch: int,
        state: TrainState,
        aux: Dict[str, Any],
        calib_batch: Batch,
        metrics: Optional[Tuple[Callable[[jnp.ndarray, Array], float], ...]],
    ) -> Dict[str, jnp.ndarray]:
        if (
            self.save_checkpoint_dir is not None
            and self.save_every_n_steps is not None
            and current_epoch % self.save_every_n_steps == 0
        ):
            self.save_checkpoint(
                state, self.save_checkpoint_dir, keep=self.keep_top_n_checkpoints
            )
        calibration_losses_and_metrics = {"loss": aux["loss"]}

        if aux["logging_kwargs"] is not None:
            for k, v in aux["logging_kwargs"].items():
                calibration_losses_and_metrics[k] = v

        if not self.disable_calibration_metrics_computation and metrics is not None:
            preds = self.predict_fn(aux["outputs"])
            if self.multi_device:
                calibration_batch_metrics = self.compute_metrics(
                    preds.reshape((preds.shape[0] * preds.shape[1],) + preds.shape[2:]),
                    calib_batch[1].reshape(
                        (calib_batch[1].shape[0] * calib_batch[1].shape[1],) + calib_batch[1].shape[2:]
                    ),
                    metrics,
                )
            else:
                calibration_batch_metrics = self.compute_metrics(preds, calib_batch[1], metrics)
            for k, v in calibration_batch_metrics.items():
                calibration_losses_and_metrics[k] = v
        return calibration_losses_and_metrics

    def calibration_epoch_end(
        self, calibration_losses_and_metrics_current_epoch: List[Dict[str, jnp.ndarray]]
    ) -> Dict[str, float]:
        return self._get_mean_losses_and_metrics(
            calibration_losses_and_metrics_current_epoch
        )

    def validation_epoch_end(
        self,
        validation_losses_and_metrics_current_epoch: List[Dict[str, jnp.ndarray]],
        state: TrainState,
    ) -> Dict[str, float]:
        validation_losses_and_metrics_current_epoch = self._get_mean_losses_and_metrics(
            validation_losses_and_metrics_current_epoch
        )
        # early stopping
        improved = self.early_stopping_update(
            validation_losses_and_metrics_current_epoch
        )
        if improved and self.save_checkpoint_dir:
            self.save_checkpoint(state, self.save_checkpoint_dir, force_save=True)
        return validation_losses_and_metrics_current_epoch

    def calibrate(
        self,
        rng: PRNGKeyArray,
        state: TrainState,
        fun: Callable,
        training_dataloader: DataLoader,
        training_dataset_size: int,
        calibration_dataloader: DataLoader,
        calibration_dataset_size: int,
        n_epochs: int = 1,
        metrics: Optional[Tuple[Callable[[jnp.ndarray, Array], float], ...]] = None,
        validation_dataloader: Optional[DataLoader] = None,
        validation_dataset_size: Optional[int] = None,
        verbose: bool = True,
        unravel: Optional[Callable[[any], PyTree]] = None,
        **kwargs,
    ) -> Tuple[TrainState, Status]:
        calibration_kwargs = FrozenDict(kwargs)
        if validation_dataloader:
            assert (
                validation_dataset_size is not None
            ), "`validation_dataset_size` is required when `validation_dataloader` is provided."

        calibration_losses_and_metrics = collections.defaultdict(list)
        validation_losses_and_metrics = collections.defaultdict(list)

        state, dataloaders, rng = self.on_calib_start(
            state, [training_dataloader, calibration_dataloader, validation_dataloader], rng
        )
        training_dataloader, calibration_dataloader, validation_dataloader = dataloaders

        progress_bar = trange(n_epochs, desc="Epoch")
        for epoch in progress_bar:
            # calibration loop
            (
                state,
                calibration_losses_and_metrics_current_epoch,
                calibration_batch_metrics_str,
            ) = self._calibration_loop(
                epoch,
                fun,
                metrics,
                rng,
                state,
                training_dataloader,
                training_dataset_size,
                calibration_dataloader,
                calibration_dataset_size,
                calibration_kwargs,
                verbose,
                progress_bar,
            )
            # keep track of calibration losses and metrics [granularity=epoch]
            for k in calibration_losses_and_metrics_current_epoch.keys():
                calibration_losses_and_metrics[k].append(
                    calibration_losses_and_metrics_current_epoch[k]
                )

            # validation loop
            if self.should_perform_validation(validation_dataloader, epoch):
                # performance evaluation on the whole validation dataset
                state = self.on_validation_start(state)
                (
                    validation_losses_and_metrics_current_epoch,
                    validation_epoch_metrics_str,
                ) = self._validation_loop(
                    fun=fun,
                    metrics=metrics,
                    rng=rng,
                    state=state,
                    calibration_kwargs=calibration_kwargs,
                    validation_dataloader=validation_dataloader,
                    validation_dataset_size=validation_dataset_size,
                    verbose=verbose,
                    unravel=unravel,
                )
                if verbose:
                    logging.info(
                        f"Epoch: {epoch + 1} | " + validation_epoch_metrics_str
                    )
                # keep track of calibration losses and metrics [granularity=epoch] and check for early stopping
                for k in validation_losses_and_metrics_current_epoch.keys():
                    validation_losses_and_metrics[k].append(
                        validation_losses_and_metrics_current_epoch[k]
                    )
                # check for early stopping
                if self.is_early_stopping_active and self._early_stopping.should_stop:
                    logging.info("[Early Stopping] Stopping calibration...")
                    break

        # aggregate
        calibration_status = {
            k: jnp.array(v) for k, v in calibration_losses_and_metrics.items()
        }
        validation_status = {
            k: jnp.array(v) for k, v in validation_losses_and_metrics.items()
        }
        status = dict(**calibration_status, **validation_status)

        state = self.on_calib_end(state)
        return state, status

    def _calibration_loop(
        self,
        current_epoch: int,
        fun: Callable,
        metrics: Optional[Tuple[Callable[[jnp.ndarray, Array], float], ...]],
        rng: PRNGKeyArray,
        state: TrainState,
        training_dataloader: DataLoader,
        training_dataset_size: int,
        calibration_dataloader: DataLoader,
        calibration_dataset_size: int,
        calibration_kwargs: FrozenDict[str, Any],
        verbose: bool,
        progress_bar: TqdmDecorator,
    ) -> Tuple[TrainState, Dict[str, float], str]:
        calibration_losses_and_metrics_epoch_all_steps = []
        calibration_batch_metrics_str = ""
        for step, (train_batch, calib_batch) in enumerate(zip(training_dataloader, calibration_dataloader)):
            # forward and backward pass
            state, aux = self.calibration_step(
                state,
                train_batch,
                calib_batch,
                fun,
                rng,
                training_dataset_size,
                calibration_dataset_size,
                calibration_kwargs,
            )
            # compute calibration losses and metrics for the current batch
            calibration_losses_and_metrics_current_batch = self.calibration_step_end(
                current_epoch=current_epoch,
                state=state,
                aux=aux,
                calib_batch=calib_batch,
                metrics=metrics,
            )
            # keep track of calibration losses and metrics [granularity=batch]
            calibration_losses_and_metrics_epoch_all_steps.append(
                calibration_losses_and_metrics_current_batch
            )
            # logging
            if verbose:
                calibration_batch_metrics_str = " | ".join(
                    [
                        f"{m}: {round(float(v), 5)}"
                        for m, v in calibration_losses_and_metrics_current_batch.items()
                    ]
                )
                progress_bar.set_description(
                    f"Epoch: {current_epoch + 1} | " + calibration_batch_metrics_str,
                    refresh=True,
                )

        # compute calibration losses and metrics avg for the current epoch + other ops (if needed)
        calibration_losses_and_metrics_current_epoch = self.calibration_epoch_end(
            calibration_losses_and_metrics_epoch_all_steps
        )

        return (
            state,
            calibration_losses_and_metrics_current_epoch,
            calibration_batch_metrics_str,
        )

    def _validation_loop(
        self,
        fun: Callable,
        metrics: Optional[Tuple[Callable[[jnp.ndarray, Array], float], ...]],
        rng: PRNGKeyArray,
        state: TrainState,
        calibration_kwargs: FrozenDict[str, Any],
        validation_dataloader: DataLoader,
        validation_dataset_size: int,
        verbose: bool = True,
    ) -> Tuple[Dict[str, float], str]:
        validation_losses_and_metrics_epoch_all_steps = []
        validation_epoch_metrics_str = ""
        for batch in validation_dataloader:
            validation_losses_and_metrics_current_batch = self.validation_step(
                state,
                batch,
                fun,
                rng,
                validation_dataset_size,
                metrics,
                calibration_kwargs,
            )
            validation_losses_and_metrics_epoch_all_steps.append(
                validation_losses_and_metrics_current_batch
            )
        # compute validation losses and metrics for the current epoch
        validation_losses_and_metrics_current_epoch = self.validation_epoch_end(
            validation_losses_and_metrics_epoch_all_steps, state
        )
        # logging
        if verbose:
            validation_epoch_metrics_str = " | ".join(
                [
                    f"{m}: {round(float(v), 5)}"
                    for m, v in validation_losses_and_metrics_current_epoch.items()
                ]
            )
        return validation_losses_and_metrics_current_epoch, validation_epoch_metrics_str

    def _get_mean_losses_and_metrics(
        self, losses_and_metrics: List[Dict[str, jnp.ndarray]]
    ) -> Dict[str, float]:
        losses_and_metrics = stack_forest(losses_and_metrics)
        losses_and_metrics = tree_map(lambda x: x.mean(), losses_and_metrics)
        return losses_and_metrics

    def should_perform_validation(
        self, validation_dataloader: Optional[DataLoader], epoch: int
    ) -> bool:
        return (
            validation_dataloader is not None
            and self.eval_every_n_epochs > 0
            and epoch % self.eval_every_n_epochs == 0
        )

    @staticmethod
    def sync_gradients_and_loss(
        grad: jnp.ndarray, loss: jnp.ndarray
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
        return grad, loss

    def on_calib_start(
        self,
        state: TrainState,
        dataloaders: List[DataLoader],
        rng: PRNGKeyArray,
    ) -> Tuple[TrainState, List[DataLoader], PRNGKeyArray]:
        return state, dataloaders, rng

    def on_calib_end(self, state: TrainState) -> TrainState:
        self.save_checkpoint(
            state,
            save_checkpoint_dir=self.save_checkpoint_dir,
            keep=self.keep_top_n_checkpoints,
            force_save=True,
        )
        return state

    def on_validation_start(self, state: TrainState) -> TrainState:
        return state

    def compute_metrics(
        self,
        preds: Array,
        targets: Array,
        metrics: Optional[Tuple[Callable[[jnp.ndarray, Array], float], ...]],
    ) -> Dict[str, float]:
        metrics_vals = {}
        for metric in metrics:
            metrics_vals[metric.__name__] = metric(preds, targets)
        return metrics_vals


class JittedMixin:
    @partial(jax.jit, static_argnums=(0, 3, 5, 6, 7))
    def calibration_step(
        self,
        state: TrainState,
        batch: Batch,
        fun: Callable,
        rng: PRNGKeyArray,
        n_data: int,
        unravel: Optional[Callable[[any], PyTree]] = None,
        kwargs: FrozenDict[str, Any] = FrozenDict(),
    ) -> Tuple[TrainState, Dict[str, Any]]:
        return super().calibration_step(state, batch, fun, rng, n_data, unravel, kwargs)

    @partial(jax.jit, static_argnums=(0, 3, 5, 6, 7, 8))
    def validation_step(
        self,
        state: TrainState,
        batch: Batch,
        fun: Callable,
        rng: PRNGKeyArray,
        n_data: int,
        metrics: Optional[Tuple[Callable[[jnp.ndarray, Array], float], ...]] = None,
        unravel: Optional[Callable[[any], PyTree]] = None,
        kwargs: FrozenDict[str, Any] = FrozenDict(),
    ) -> Dict[str, jnp.ndarray]:
        return super().validation_step(
            state, batch, fun, rng, n_data, metrics, unravel, kwargs
        )


class MultiDeviceMixin:
    all_reduce_mean = jax.pmap(lambda x: lax.pmean(x, "x"), "x")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.multi_device = True

    @staticmethod
    def _add_device_dim_to_input_dataloader(dataloader: DataLoader) -> DataLoader:
        def _reshape_input_batch(batch):
            n_devices = jax.local_device_count()
            if batch.shape[0] % n_devices != 0:
                raise ValueError(
                    f"The size of all batches must be a multiple of {n_devices}, that is the number of "
                    f"available devices. Please set an appropriate batch size in the data loader."
                )
            single_input_shape = batch.shape[1:]
            # reshape to (local_devices, device_batch_size, *single_input_shape)
            return batch.reshape((n_devices, -1) + single_input_shape)

        class DataLoaderWrapper:
            def __init__(self, dataloader):
                self.dataloader = dataloader

            def __iter__(self):
                dataloader = map(
                    lambda batch: tree_map(_reshape_input_batch, batch), self.dataloader
                )
                dataloader = jax_utils.prefetch_to_device(dataloader, 2)
                yield from dataloader

        return DataLoaderWrapper(dataloader) if dataloader is not None else dataloader

    @staticmethod
    def sync_mutable(state: TrainState) -> TrainState:
        return (
            state.replace(mutable=MultiDeviceMixin.all_reduce_mean(state.mutable))
            if state.mutable is not None
            else state
        )

    @staticmethod
    def sync_gradients_and_loss(
        grads: jnp.ndarray, loss: jnp.ndarray
    ) -> Tuple[jnp.ndarray, jnp.ndarray]:
        grad = lax.pmean(grads, axis_name="batch")
        loss = lax.pmean(loss, axis_name="batch")
        return grad, loss

    def save_checkpoint(
        self,
        state: TrainState,
        save_checkpoint_dir: Path,
        keep: int = 1,
        force_save: bool = False,
        prefix: str = "checkpoint_",
    ) -> None:
        state = self.sync_mutable(state)
        state = jax.device_get(tree_map(lambda x: x[0], state))
        return super(MultiDeviceMixin, self).save_checkpoint(
            state, save_checkpoint_dir, keep, force_save, prefix
        )

    def on_calib_start(
        self, state: TrainState, dataloaders: List[DataLoader], rng: PRNGKeyArray
    ) -> Tuple[TrainState, List[DataLoader], PRNGKeyArray]:
        state, dataloaders, rng = super(MultiDeviceMixin, self).on_calib_start(
            state, dataloaders, rng
        )
        state = jax_utils.replicate(state)
        dataloaders = [
            self._add_device_dim_to_input_dataloader(dl) for dl in dataloaders
        ]
        model_key = random.split(rng, jax.local_device_count())
        return state, dataloaders, model_key

    def on_calib_end(self, state: TrainState) -> TrainState:
        state = super(MultiDeviceMixin, self).on_calib_end(state)
        return jax.device_get(tree_map(lambda x: x[0], state))

    @partial(jax.pmap, axis_name="batch", static_broadcasted_argnums=(0, 3, 5, 6, 7))
    def calibration_step(
        self,
        state: TrainState,
        batch: Batch,
        fun: Callable,
        rng: PRNGKeyArray,
        n_data: int,
        unravel: Optional[Callable[[any], PyTree]] = None,
        kwargs: FrozenDict[str, Any] = FrozenDict(),
    ) -> Tuple[TrainState, Dict[str, Any]]:
        return super().calibration_step(state, batch, fun, rng, n_data, unravel, kwargs)

    def calibration_step_end(
        self,
        current_epoch: int,
        state: TrainState,
        aux: Dict[str, Any],
        batch: Batch,
        metrics: Optional[Tuple[Callable[[jnp.ndarray, Array], float], ...]],
        kwargs: FrozenDict[str, Any] = FrozenDict(),
    ) -> Dict[str, jnp.ndarray]:
        calibration_losses_and_metrics = super(MultiDeviceMixin, self).calibration_step_end(
            current_epoch, state, aux, batch, metrics, kwargs
        )
        return tree_map(lambda x: x.mean(), calibration_losses_and_metrics)

    def on_validation_start(self, state: TrainState) -> TrainState:
        state = super(MultiDeviceMixin, self).on_validation_start(state)
        state = self.sync_mutable(state)
        return state

    @partial(jax.pmap, axis_name="batch", static_broadcasted_argnums=(0, 3, 5, 6, 7, 8))
    def validation_step(
        self,
        state: TrainState,
        batch: Batch,
        fun: Callable,
        rng: PRNGKeyArray,
        n_data: int,
        metrics: Optional[Tuple[Callable[[jnp.ndarray, Array], float], ...]] = None,
        unravel: Optional[Callable[[any], PyTree]] = None,
        kwargs: FrozenDict[str, Any] = FrozenDict(),
    ) -> Dict[str, jnp.ndarray]:
        validation_losses_and_metrics = super().validation_step(
            state, batch, fun, rng, n_data, metrics, unravel, kwargs
        )
        return lax.pmean(validation_losses_and_metrics, axis_name="batch")
