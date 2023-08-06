import numpy as np
import numpy.typing as npt
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    mean_squared_error,
    roc_auc_score,
)

from mlc.metrics.metric import Metric


def transaction_cost(y, y_s) -> float:
    (tn, fp, fn, tp) = confusion_matrix(y, y_s)
    return (((tp + fp) * 5.0) + (fn * 60.0) + (tn * 0)) / 60


str2pred_classification_metric = {
    "f1": f1_score,
    "mcc": matthews_corrcoef,
    "error_rate": lambda y, y_s: 1 - accuracy_score(y, y_s),
    "class_error": lambda y, y_s: 1 - (y == y_s).astype(int),
    "accuracy": lambda y, y_s: accuracy_score(y, y_s),
    "confusion_matrix": lambda y, y_s: confusion_matrix(y, y_s),
    "balanced_accuracy": lambda y, y_s: balanced_accuracy_score(y, y_s),
    "transaction_cost": transaction_cost,
}
str2proba_classification_metric = {
    "auc": lambda y, y_s: roc_auc_score(y, y_s[:, -1]),
    "proba_error": lambda y, y_s: 1 - y_s[np.arange(len(y)), y],
    "y_scores": lambda y, y_s: y_s,
}

str2regression_metric = {
    "rmse": lambda y, y_s: mean_squared_error(y, y_s, squared=True)
}


class PredClassificationMetric(Metric):
    def __init__(self, metric_name: str):
        self.metric_name = metric_name

    def compute(
        self, y_true: npt.NDArray[np.generic], y_score: npt.NDArray[np.generic]
    ) -> npt.NDArray[np.generic]:
        return str2pred_classification_metric[self.metric_name](
            y_true, y_score
        )


class ProbaClassificationMetric(Metric):
    def __init__(self, metric_name: str):
        self.metric_name = metric_name

    def compute(
        self, y_true: npt.NDArray[np.generic], y_score: npt.NDArray[np.generic]
    ) -> npt.NDArray[np.generic]:
        return str2proba_classification_metric[self.metric_name](
            y_true, y_score
        )


class RegressionMetric(Metric):
    def __init__(self, metric_name: str):
        self.metric_name = metric_name

    def compute(
        self, y_true: npt.NDArray[np.generic], y_score: npt.NDArray[np.generic]
    ) -> npt.NDArray[np.generic]:
        return str2regression_metric[self.metric_name](y_true, y_score)
