import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
from .base import BaseElement


class ImageElement(BaseElement):
  image: np.ndarray
  isPng: bool

  def __init__(self, element_config, work_dir: Path, fps: float, resolution: Tuple[int, int]):
    super().__init__(element_config, work_dir, fps, resolution)
    src: Path = self.work_dir / element_config['path']
    self.image = cv2.imread(src.as_posix(), cv2.IMREAD_UNCHANGED)
    if self.size is not None:
      self.image = cv2.resize(self.image, self.size)
    self.isPng = (src.as_posix().endswith('.png') or src.as_posix().endswith('.PNG')) and self.image.shape[2] == 4

  def render(self, frame: np.ndarray) -> np.ndarray:
    if self.image is not None:
      if self.isPng:
        # TODO: debug this part
        cv2.addWeighted(self.image[:, :, 3], 1, frame[:self.image.shape[0], :self.image.shape[1], :],
                         1, 0, frame[:self.image.shape[0], :self.image.shape[1], :])
      else:
        if self.position is not None:
          x = int(self.position[0] * frame.shape[1])
          y = int(self.position[1] * frame.shape[0])
          frame[y:y + self.image.shape[0], x:x + self.image.shape[1]] = self.image
        else:
          frame[:self.image.shape[0], :self.image.shape[1], :] = self.image
    return frame

  def dispose(self):
    super().dispose()

  def available(self) -> bool:
    return self.image is not None