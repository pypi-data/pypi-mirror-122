import numpy as np

from typing import Optional


class SeedMixin:
    """Adds working with ._seed and ._original_seed for reproducibility"""
    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value: int):
        self._original_seed = value
        self._seed = value

    def reset_seed(self):
        self._seed = self._original_seed
        return self

    def set_seed(self, value: Optional[int]):
        if value is None:
            value = np.random.randint(100000)
        self.seed = value
        return self
