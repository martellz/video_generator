import cv2
import numpy as np
from typing import Optional, Tuple
from .base import BaseElement


class ImageElement(BaseElement):
  image: np.ndarray
  isPng: bool

  def __init__(self, src: str, start_time: Optional[int], end_time: Optional[int], fps: Optional[int], position: Optional[Tuple[float, float]], size: Optional[Tuple[int, int]], **kwargs):
    super().__init__(start_time, end_time, fps, position, size, **kwargs)
    self.image = cv2.imread(str(src), cv2.IMREAD_UNCHANGED)
    if self.size is not None:
      self.image = cv2.resize(self.image, self.size)
    self.isPng = (src.endswith('.png') or src.endswith('.PNG')) and self.image.shape[2] == 4

  def render(self, frame: np.ndarray) -> np.ndarray:
    if self.image is not None:
      if self.position is not None:
        x = int(self.position[0] * frame.shape[1])
        y = int(self.position[1] * frame.shape[0])
        frame[y:y + self.image.shape[0], x:x + self.image.shape[1]] = self.image
      else:
        frame[:self.image.shape[0], :self.image.shape[1]] = self.image
    return frame

  def dispose(self):
    super().dispose()

  def available(self) -> bool:
    return self.image is not None