import logging
import uuid
from typing import Any, Dict, Optional, Union

import numpy as np
import numpy.typing as npt
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset

from mlc.models.model import Model

logger = logging.getLogger(__name__)


class BaseModelTorch(Model):
    def __init__(
        self,
        name: str,
        objective: str,
        batch_size: int,
        epochs: int,
        early_stopping_rounds: int,
        learning_rate: float,
        val_batch_size: int = 100000,
        class_weight: Union[str, Dict[int, str]] = None,
        force_device: str = None,
        is_text: bool = False,
        weight_decay=0,
        **kwargs: Dict[str, Any],
    ) -> None:
        super().__init__(
            name=name,
            objective=objective,
            batch_size=batch_size,
            epochs=epochs,
            early_stopping_rounds=early_stopping_rounds,
            learning_rate=learning_rate,
            val_batch_size=val_batch_size,
            class_weight=class_weight,
            weight_decay=weight_decay,
            **kwargs,
        )
        self.force_device = force_device
        self.device = self.get_device()
        self.objective = objective
        self.batch_size = batch_size
        self.epochs = epochs
        self.early_stopping_rounds = early_stopping_rounds
        self.learning_rate = learning_rate
        self.force_train = False
        self.val_batch_size = val_batch_size
        self.class_weight = class_weight
        self.is_text = is_text
        self.weight_decay = weight_decay

    def to_device(self) -> None:
        logger.debug(f"On Device: {self.device}")
        self.model.to(self.device)

    def get_device(self):
        if self.force_device is not None:
            device = self.force_device
        else:
            if torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"
        return torch.device(device)

    def eval(self) -> None:
        self.force_train = False

    def train(self) -> None:
        self.force_train = True

    def fit(
        self,
        x: npt.NDArray[np.float_],
        y: Union[npt.NDArray[np.int_], npt.NDArray[np.float_]],
        x_val: Optional[npt.NDArray[np.float_]] = None,
        y_val: Optional[
            Union[npt.NDArray[np.int_], npt.NDArray[np.float_]]
        ] = None,
        reset_weight: bool = True,
    ):
        model_id = uuid.uuid4()
        if reset_weight:
            self.reset_all_weights()

        optimizer = optim.AdamW(
            filter(lambda p: p.requires_grad, self.model.parameters()),
            lr=self.learning_rate,
            weight_decay=self.weight_decay,
        )

        if x_val is None:
            (
                _,
                count_idx,
                count,
            ) = np.unique(y, return_counts=True, return_index=True)
            if np.sum(count == 1) > 0:
                to_delete = count_idx[np.where(count == 1)[0]]
                x = np.delete(x, to_delete, axis=0)
                y = np.delete(y, to_delete, axis=0)

            x, x_val, y, y_val = train_test_split(
                x, y, test_size=0.2, random_state=42, stratify=y
            )

        if self.is_text:
            x = torch.tensor(x).int()
            x_val = torch.tensor(x_val).int()
        else:
            x = torch.tensor(x).float()
            x_val = torch.tensor(x_val).float()

        y = torch.tensor(y)
        y_val = torch.tensor(y_val)

        class_weight = self.class_weight
        if class_weight is not None:
            if self.class_weight == "balanced":
                class_weight = torch.Tensor(
                    1 - torch.unique(y, return_counts=True)[1] / len(y)
                )
            else:
                class_weight = torch.Tensor(self.class_weight)

        if self.objective == "regression":
            loss_func = nn.MSELoss()
            y = y.float()
            y_val = y_val.float()
        elif self.objective == "classification":
            loss_func = nn.CrossEntropyLoss(weight=class_weight)
        else:
            if class_weight is not None:
                class_weight = torch.Tensor(class_weight[1] / class_weight[0])
            loss_func = nn.BCEWithLogitsLoss(pos_weight=class_weight)
            y = y.float()
            y_val = y_val.float()

        train_dataset = TensorDataset(x, y)

        val_dataset = TensorDataset(x_val, y_val)

        train_loader = DataLoader(
            dataset=train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=0,
        )
        val_loader = DataLoader(
            dataset=val_dataset,
            batch_size=self.val_batch_size,
            shuffle=True,
            num_workers=0,
        )
        min_val_loss = float("inf")
        min_val_loss_idx = 0

        loss_history = []
        val_loss_history = []

        for epoch in range(self.epochs):
            for i, (batch_x, batch_y) in enumerate(train_loader):

                out = self.model(batch_x.to(self.device))

                if (
                    self.objective == "regression"
                    or self.objective == "binary"
                ):
                    out = out.squeeze()

                loss = loss_func(out, batch_y.to(self.device))
                loss_history.append(loss.item())
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                logger.debug(f"Batch {i}")

            # Early Stopping
            if self.early_stopping_rounds > 0:
                val_loss = 0.0
                val_dim = 0
                with torch.no_grad():
                    for val_i, (batch_val_x, batch_val_y) in enumerate(
                        val_loader
                    ):
                        out = self.model(batch_val_x.to(self.device))

                        if (
                            self.objective == "regression"
                            or self.objective == "binary"
                        ):
                            out = out.squeeze()

                        val_loss += loss_func(
                            out, batch_val_y.to(self.device)
                        ).item()
                        val_dim += 1

                val_loss /= val_dim
                val_loss_history.append(val_loss)

                logger.debug("Epoch %d, Val Loss: %.5f" % (epoch, val_loss))

                if val_loss < min_val_loss:
                    min_val_loss = val_loss
                    min_val_loss_idx = epoch

                    # Save the currently best model
                    self.save(f"tmp/best_{model_id}.model")

                if min_val_loss_idx + self.early_stopping_rounds < epoch:
                    logger.debug(
                        "Validation loss has not improved for %d steps!"
                        % self.early_stopping_rounds
                    )
                    logger.debug("Early stopping applies.")
                    break

        self.model.__hash__()
        # Load best model
        if self.early_stopping_rounds > 0:
            self.load(f"tmp/best_{model_id}.model")
        return loss_history, val_loss_history

    def predict(self, x):
        if self.objective == "regression":
            self.predictions = self.predict_helper(x)
        else:
            self.predict_proba(x)
            self.predictions = np.argmax(self.prediction_probabilities, axis=1)

        return self.predictions

    def predict_proba(self, x: np.ndarray) -> np.ndarray:
        probas = self.predict_helper(x)

        # If binary task returns only probability for the true class,
        # adapt it to return (N x 2)
        if probas.shape[1] == 1:
            probas = np.concatenate((1 - probas, probas), 1)

        self.prediction_probabilities = probas
        return self.prediction_probabilities

    def predict_helper(self, x, load_all_gpu: bool = False):

        if self.force_train:
            self.model.train()
        else:
            self.model.eval()

        if self.is_text:
            x = torch.tensor(x).int()
        else:
            x = torch.tensor(x).float()

        if load_all_gpu:
            x = x.to(self.device)

        test_dataset = TensorDataset(x)
        test_loader = DataLoader(
            dataset=test_dataset,
            batch_size=self.val_batch_size,
            shuffle=False,
            num_workers=0,
        )
        predictions = []
        with torch.no_grad():
            for batch_x in test_loader:
                if load_all_gpu:
                    preds = self.model(batch_x[0])
                else:
                    preds = self.model(batch_x[0].to(self.device))

                if self.objective == "binary":
                    preds = torch.sigmoid(preds)
                torch.cuda.synchronize()
                predictions.append(preds.detach().cpu().numpy())
        return np.concatenate(predictions)

    def save(self, path: str) -> None:
        torch.save(self.model.state_dict(), path)

    def load(self, path: str) -> None:
        state_dict = torch.load(path)
        self.model.load_state_dict(state_dict)

    def get_model_size(self) -> int:
        model_size = sum(
            t.numel() for t in self.model.parameters() if t.requires_grad
        )
        return model_size

    def reset_all_weights(self) -> None:
        """
        refs:
            - https://discuss.pytorch.org/t/how-to-re-set-alll-parameters-in
            -a-network/20819/6
            - https://stackoverflow.com/questions/63627997/reset-parameters
            -of-a-neural-network-in-pytorch
            - https://pytorch.org/docs/stable/generated/torch.nn.Module.html
        """

        @torch.no_grad()
        def weight_reset(m: nn.Module) -> None:
            # - check if the current module has reset_parameters & if it's
            # callabed called it on m
            reset_parameters = getattr(m, "reset_parameters", None)
            if callable(reset_parameters):
                m.reset_parameters()

        # Applies fn recursively to every submodule see:
        # https://pytorch.org/docs/stable/generated/torch.nn.Module.html
        self.model.apply(fn=weight_reset)
