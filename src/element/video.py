import cv2
import numpy as np
from typing import Optional, Tuple, overload, override
from pathlib import Path
from .base import BaseElement


class VideoElement(BaseElement):
  video: cv2.VideoCapture

  def __init__(self, src: str, start_time: Optional[int], end_time: Optional[int], fps: Optional[int], position: Optional[Tuple[float, float]], size: Optional[Tuple[int, int]], **kwargs):
    super().__init__(start_time, end_time, fps, position, size, **kwargs)
    self.video = cv2.VideoCapture(str(src))
    if start_time is not None:
      self.video.set(cv2.CAP_PROP_POS_FRAMES, start_time)

  def render(self, frame: np.ndarray) -> np.ndarray:
    video_frame = self._deal_video_frame()
    if video_frame is not None:
      if self.position is not None:
        x = int(self.position[0] * frame.shape[1])
        y = int(self.position[1] * frame.shape[0])
        frame[y:y + video_frame.shape[0], x:x + video_frame.shape[1]] = video_frame
      else:
        frame[:video_frame.shape[0], :video_frame.shape[1]] = video_frame
    return frame

  def dispose(self):
    super().dispose()
    self.video.release()

  def _deal_video_frame(self) -> Optional[np.ndarray]:
    video_frame = None
    if self.video.isOpened():
      ret, video_frame = self.video.read()
      if not ret:
        return None

      if self.size is not None:
        video_frame = cv2.resize(video_frame, self.size)

    return video_frame

  def available(self) -> bool:
    return self.video.isOpened()

class GreenScreenVideoElement(VideoElement):
  color: np.ndarray  # (3, )

  def __init__(self, src: str, color: Tuple[int, int, int], start_time: Optional[int], end_time: Optional[int], fps: Optional[int], position: Optional[Tuple[float, float]], size: Optional[Tuple[int, int]], **kwargs):
    super().__init__(src, start_time, end_time, fps, position, size, **kwargs)
    self.color = np.array(color).squeeze()

  def render(self, frame: np.ndarray):
    super().render(frame)

  def _deal_video_frame(self) -> Optional[np.ndarray]:
    video_frame = super()._deal_video_frame()
    if video_frame is not None:
      mask = self._green_screen_mask(video_frame)
      video_frame = video_frame * mask
    return video_frame

  def _green_screen_mask(self, frame: np.ndarray) -> np.ndarray:
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mask = np.abs(rgb - self.color).sum(axis=2, keepdims=True) > 5 / 255.    # background will be false
    return mask