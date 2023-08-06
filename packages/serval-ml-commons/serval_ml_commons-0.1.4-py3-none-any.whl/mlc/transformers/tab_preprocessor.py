from typing import Any, Dict, Union

import numpy as np
import numpy.typing as npt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from mlc.transformers.transformer import Transformer


class TabPreprocessor(Transformer):
    def __init__(
        self,
        feature_type: pd.Series,
        scale: bool,
        one_hot_encode: bool,
        **kwargs: Dict[str, Any],
    ) -> None:
        super().__init__(
            name="tab_preprocessor",
            feature_type=feature_type,
            scale=scale,
            one_hot_encode=one_hot_encode,
            **kwargs,
        )
        self.scale = scale
        self.one_hot_encode = one_hot_encode
        cat = feature_type == "cat"
        self.cat_idx = np.where(cat)[0]
        self.num_idx = np.where(~cat)[0]
        self.std_scaler = StandardScaler()
        self.cat_encoder = OneHotEncoder(
            sparse=False, handle_unknown="ignore", drop="if_binary"
        )
        self.do_scale = (len(self.num_idx) > 0) and scale
        self.do_one_hot_encode = (len(self.cat_idx) > 0) and one_hot_encode

    def fit(
        self,
        x: Union[npt.NDArray[np.float_], pd.DataFrame],
        y: Union[npt.NDArray[np.int_], pd.Series] = None,
    ) -> Transformer:
        if isinstance(x, pd.DataFrame):
            x = x.to_numpy()
        if self.do_scale:
            self.std_scaler.fit(x[:, self.num_idx])
        if self.do_one_hot_encode:
            self.cat_encoder.fit(x[:, self.cat_idx])

        return self

    def transform(
        self, x: Union[npt.NDArray[np.float_], pd.DataFrame]
    ) -> Union[npt.NDArray[np.float_], pd.DataFrame]:
        # def transform(self, X):
        if isinstance(x, pd.DataFrame):
            x = x.to_numpy()
        x = x.copy()
        if self.do_scale:
            x[:, self.num_idx] = self.std_scaler.transform(x[:, self.num_idx])
        if self.do_one_hot_encode:
            new_x1 = x[:, self.num_idx]
            new_x2 = self.cat_encoder.fit_transform(x[:, self.cat_idx])
            x = np.concatenate([new_x1, new_x2], axis=1)

        return x

    def inverse_transform(
        self, x: Union[npt.NDArray[np.float_], pd.DataFrame]
    ) -> Union[npt.NDArray[np.float_], pd.DataFrame]:
        if isinstance(x, pd.DataFrame):
            x = x.to_numpy()
        x = x.copy()
        if self.do_one_hot_encode:
            cat_x = x[:, len(self.num_idx) :]
            cat_x = self.cat_encoder.inverse_transform(cat_x)

            new_x = np.empty((len(x), len(self.num_idx) + len(self.cat_idx)))
            new_x[:, self.num_idx] = x[:, : len(self.num_idx)]
            new_x[:, self.cat_idx] = cat_x
            x = new_x

        if self.do_scale:
            x[:, self.num_idx] = self.std_scaler.inverse_transform(
                x[:, self.num_idx]
            )

        return x

    def load(self, path: str) -> None:
        raise NotImplementedError

    def save(self, path: str) -> None:
        raise NotImplementedError


def get_tab_transformer(
    metadata: pd.DataFrame, scale: bool, one_hot_encode: bool
) -> ColumnTransformer:
    cat_index = metadata["type"] == "cat"
    cat_features = metadata[cat_index]["feature"]
    num_features = metadata[~cat_index]["feature"]

    transformers = []
    if scale:
        transformers.append(("num", StandardScaler(), num_features))
    if one_hot_encode:
        transformers.append(
            (
                "cat",
                OneHotEncoder(
                    sparse=False, handle_unknown="ignore", drop="if_binary"
                ),
                cat_features,
            )
        )

    return ColumnTransformer(
        transformers=transformers,
        sparse_threshold=0,
        remainder="passthrough",
        n_jobs=-1,
    )
