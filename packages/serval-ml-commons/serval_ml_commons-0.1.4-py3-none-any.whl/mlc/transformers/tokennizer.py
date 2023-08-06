from typing import Any, Dict, Union

import numpy as np
import pandas as pd
import torch
from numpy import typing as npt
from transformers import DistilBertTokenizer

from mlc.transformers.transformer import Transformer


def initialize_distilbert_transform(max_token_length):
    """Adapted from the Wilds library, available at:
    https://github.com/p-lambda/wilds"""
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

    def transform(text):
        tokens = tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=max_token_length,
            return_tensors="pt",
        )
        x = torch.stack((tokens["input_ids"], tokens["attention_mask"]), dim=2)
        x = torch.squeeze(x, dim=0)  # First shape dim is always 1
        return x

    return transform


class TokenizerTransformer(Transformer):
    def __init__(self, max_token_length: int, **kwargs: Any):
        super().__init__(name="tokenizer", **kwargs)
        self.max_token_length = max_token_length
        self.transform_f = initialize_distilbert_transform(
            self.max_token_length
        )

    def fit(
        self,
        x: Union[npt.NDArray[np.float_], pd.DataFrame],
        y: Union[npt.NDArray[np.int_], pd.Series] = None,
    ) -> Transformer:
        # Pre-fitted, hence empty
        return self

    def transform(
        self, x: Union[npt.NDArray[np.float_], pd.DataFrame]
    ) -> Union[npt.NDArray[np.float_], pd.DataFrame]:

        return self.transform_f(x.values.reshape(-1).tolist()).reshape(
            x.shape[0], -1
        )

    def load(self, path: str) -> None:
        # Pre-fitted, out of our scope
        pass

    def save(self, path: str) -> None:
        # Pre-fitted, out of our scope
        pass

    def get_params(self, deep: bool) -> Dict[str, Any]:
        del deep
        return {"max_token_length": self.max_token_length}
