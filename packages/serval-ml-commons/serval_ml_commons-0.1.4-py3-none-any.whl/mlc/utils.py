from typing import Any, Optional

import numpy as np
import numpy.typing as npt


def cut_in_batch(
    arr: npt.NDArray[Any],
    n_desired_batch: int = 1,
    batch_size: Optional[int] = None,
):

    if batch_size is None:
        n_batch = min(n_desired_batch, len(arr))
    else:
        n_batch = np.ceil(len(arr) / batch_size)
    batches_i = np.array_split(np.arange(arr.shape[0]), n_batch)

    return [arr[batch_i] for batch_i in batches_i]
