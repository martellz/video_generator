import cv2
import numpy as np
import json

from typing import Optional, Tuple, List
from pathlib import Path
from .element import BaseElement, ImageElement, VideoElement, GreenScreenVideoElement

# debug
import matplotlib.pyplot as plt


class VideoGenerator:
  def __init__(self, config: dict, work_dir: Path, output_fn: str, fps: float=30, resolution: Tuple[int, int]=(1080, 1920)):
    self.config = config
    self.fps = fps
    self.resolution = resolution
    self.elements: List[BaseElement | ImageElement | VideoElement | GreenScreenVideoElement] = []

    # self.write_video_flag = True  # TODO: set to False when change generate_video() to generator or async function
    self.video_writer = cv2.VideoWriter(
      output_fn,
      cv2.VideoWriter_fourcc(*'MP4V'),
      self.fps,
      (self.resolution[1], self.resolution[0])
    )

    element: BaseElement | ImageElement | VideoElement | GreenScreenVideoElement
    for element_config in self.config['elements']:
      ElementClass = BaseElement
      if element_config['type'] == 'image':
        ElementClass = ImageElement
      elif element_config['type'] == 'video':
        ElementClass = VideoElement
      elif element_config['type'] == 'green_screen_video':
        ElementClass = GreenScreenVideoElement

      element = ElementClass(
        element_config,
        work_dir,
        self.fps,
        self.resolution
      )

      self.add_element(element)

    # find end time of the video by finding the maximum end time of all elements
    self.end_time = 0.
    for element in self.elements:
      if element.end_time is not None:
        self.end_time = max(self.end_time, element.end_time)

    print(self)

  def __repr__(self) -> str:
    return '<VideoGenerator: fps: {}, resolution: {}, end_time: {}, elements: {}>'.format(
      self.fps,
      self.resolution,
      self.end_time,
      self.elements
    )

  def add_element(self, element):
    self.elements.append(element)

  def generate_video(self):
    current_time = 0.
    frame_count = 0

    while True:
      frame_count += 1
      current_time += 1 / self.fps
      if current_time > self.end_time:
        break

      frame = np.zeros((*self.resolution, 4), dtype=np.uint8)
      for element in self.elements:
        if element.available():

          if element.start_time <= current_time:
            if element.end_time is None:
              # if end_time is None, render the element until the end of the video
              frame = element.render(frame)
            else:
              if element.end_time >= current_time:
                frame = element.render(frame)
              else:
                element.dispose()
          else:
            element.dispose()

      # plt.imshow(frame)
      # plt.show()
      self.video_writer.write(frame[..., :3])

    self.video_writer.release()
    print(f'Generated {frame_count} frame:s')