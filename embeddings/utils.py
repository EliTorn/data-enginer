import numpy as np


def blob_to_vec(blob):
    return np.frombuffer(blob, dtype=np.float32)
