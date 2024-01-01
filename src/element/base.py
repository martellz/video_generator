import re
from typing import Optional, Tuple
from pathlib import Path


class BaseElement:
  work_dir: Path
  start_time: Optional[int]   # in milliseconds
  end_time: Optional[int]
  fps: Optional[int]
  # (x, y) coordinates of left-top corner, from 0 to 1
  position: Optional[Tuple[float, float]]
  size: Optional[Tuple[int, int]]   # (width, height)
  _available: bool

  def __init__(self, element_config, work_dir: Path, fps: float, resolution: Tuple[int, int]):
    self.work_dir = work_dir
    self.start_time = element_config['start_time'] if 'start_time' in element_config else 0
    self.end_time = element_config['end_time'] if 'end_time' in element_config else -1
    self.position = element_config['position'] if 'position' in element_config else None
    self.size = element_config['size'] if 'size' in element_config else None
    self.fps = fps
    self.resolution = resolution
    self._available = True

  def render(self, frame):
    # Implement the rendering logic for the element

    # for text elements, use PIL to render the text and paste it to the frame
    # for image elements, use PIL to load the image and paste it to the frame
    # for video elements, use OpenCV to load the video and paste it to the frame
    pass

  def dispose(self):
    # Implement the logic to dispose the element
    self._available = False

  def available(self):
    # different elements have different logic to determine whether it is available
    # _available is only a manually set flag
    return self._available