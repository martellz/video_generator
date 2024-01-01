import argparse
import json
from pathlib import Path
from src.framework import VideoGenerator


def main(config_path):
  with open(config_path) as f:
    config = json.load(f)

  video_generator = VideoGenerator(
      config,
      Path(config_path).parent,  # work_dir (current directory)
      output_fn='output.mp4',
      fps=30,
      resolution=(1080, 1920)
  )

  video_generator.generate_video()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', help='config.json file path')
  args = parser.parse_args()

  main(args.config)