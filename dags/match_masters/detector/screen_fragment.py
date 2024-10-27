from dataclasses import dataclass
from typing import Tuple, Dict

import numpy as np


@dataclass
class ScreenFragment:
    top: int
    bottom: int
    left: int
    right: int
    expected_images: Dict[str, np.ndarray]

    def mid(self) -> Tuple[int, int]:
        return (self.left + self.right) // 2, (self.top + self.bottom) // 2

    def extract(self, screen: np.ndarray) -> np.ndarray:
        return screen[self.top:self.bottom, self.left:self.right]
