import numpy as np
import numpy.typing as npt
import torch
from sklearn.preprocessing import OneHotEncoder


def get_num_idx(x_type) -> npt.NDArray[np.int_]:
    return np.where(x_type != "cat")[0]


def get_cat_idx(x_type) -> npt.NDArray[np.int_]:
    return np.where(x_type == "cat")[0]


def copy_x(x):
    if isinstance(x, np.ndarray):
        return x.copy()
    if isinstance(x, torch.Tensor):
        return torch.clone(x)
    raise NotImplementedError


def softargmax(x, dim=-1):
    # crude: assumes max value is unique
    # Can cause rounding errors
    beta = 100.0
    xx = beta * x
    sm = torch.nn.functional.softmax(xx, dim=dim)
    indices = torch.arange(x.shape[dim])
    y = torch.mul(indices, sm)
    result = torch.sum(y, dim)
    return result


class MinMaxScaler:
    def __init__(self) -> None:

        self.x_min = None
        self.x_max = None
        self.categories = None
        self.cat_idx = None
        self.encoder = None
        self.num_idx = []

    def fit(self, x, cat_idx=None, x_type=None):
        if isinstance(x, np.ndarray):
            nb_features = x.shape[1]
            self.cat_idx = cat_idx

            if self.cat_idx is None:
                if x_type is not None:
                    self.cat_idx = self.cat_idx = get_cat_idx(x_type)

            self.num_idx = range(nb_features)
            if self.cat_idx is not None:
                self.encoder = OneHotEncoder(sparse=False)
                self.encoder.fit(x[:, self.cat_idx])
                self.num_idx = [
                    e for e in self.num_idx if e not in self.cat_idx
                ]

            self.x_min = self.x_min
        else:
            raise NotImplementedError

        self.x_min = np.min(x[:, self.num_idx], axis=0)
        self.x_max = np.max(x[:, self.num_idx], axis=0)
        return self

    def transform(self, x):

        x_out = (x[:, self.num_idx] - self.x_min) / (self.x_max - self.x_min)
        if self.cat_idx is not None:
            x_cat = self.encoder.transform(x[:, self.cat_idx])
            x_out = np.concatenate(
                [
                    x_cat,
                    x_out,
                ],
                axis=1,
            )
        return x_out

    def inverse_transform(self, x):

        nb_features = x.shape[1]
        x_cat = x[:, 0 : nb_features - len(self.num_idx)]
        x_num = x[:, nb_features - len(self.num_idx) : nb_features]
        if isinstance(x, torch.Tensor):
            # process as tensor to preserve gradient
            x_num = x_num * (
                torch.Tensor(self.x_max) - torch.Tensor(self.x_min)
            ) + torch.Tensor(self.x_min)
            # Special case for binary features
            x_cat_encoded = torch.split(
                x_cat,
                [len(a) for a in self.encoder.categories_],
                1,
            )
            x_cat_softmax = [softargmax(a, 1) for a in x_cat_encoded]
            x_cat_unencoded = torch.stack(x_cat_softmax).swapaxes(0, 1)
            x_reversed = torch.zeros(
                (x.shape[0], x_num.shape[1] + x_cat_unencoded.shape[1])
            )
        else:
            # process as numpy
            x_num = x_num * (self.x_max - self.x_min) + self.x_min
            x_cat_unencoded = self.encoder.inverse_transform(x_cat)
            x_reversed = np.zeros(
                (x.shape[0], x_num.shape[1] + x_cat_unencoded.shape[1])
            )

        x_reversed[:, self.cat_idx] = x_cat_unencoded
        x_reversed[:, self.num_idx] = x_num

        return x_reversed
