from typing import Union

import numpy as np
import numpy.typing as npt

from mlc.metrics.metric import Metric
from mlc.models.model import Model


def default_model_prediction(
    model: Model, x: npt.NDArray[np.float_]
) -> Union[npt.NDArray[np.int_], npt.NDArray[np.float_]]:
    if model.objective in ["regression"]:
        return model.predict(x)
    if model.objective in ["binary", "classification"]:
        return model.predict_proba(x)
    raise NotImplementedError


def compute_metric(
    model: Model,
    metric: Metric,
    x: npt.NDArray[np.float_],
    y: npt.NDArray[Union[np.float_, np.int_]],
) -> npt.NDArray[np.generic]:

    y_score = default_model_prediction(model, x)
    return metric.compute(y, y_score)
