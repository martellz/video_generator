from typing import Optional, Tuple


class BaseElement:
  start_time: Optional[int]   # in milliseconds
  end_time: Optional[int]
  fps: Optional[int]
  # (x, y) coordinates of left-top corner, from 0 to 1
  position: Optional[Tuple[float, float]]
  size: Optional[Tuple[int, int]]   # (width, height)

  def __init__(self, start_time: Optional[int], end_time: Optional[int], fps: Optional[int], position: Optional[Tuple[float, float]], size: Optional[Tuple[int, int]], **kwargs):
    self.start_time = start_time
    self.end_time = end_time
    self.fps = fps
    self.position = position
    self.size = size
    # Additional attributes can be passed as keyword arguments
    self.attributes = kwargs

  def render(self, frame):
    # Implement the rendering logic for the element

    # for text elements, use PIL to render the text and paste it to the frame
    # for image elements, use PIL to load the image and paste it to the frame
    # for video elements, use OpenCV to load the video and paste it to the frame
    pass

  def dispose(self):
    # Implement the logic to dispose the element
    pass
