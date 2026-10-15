Put the .png files in the same directory as the .py file and enjoy :)

## YOLO object detection from video

Use `yolo_video_detection.py` to run YOLO (Darknet format) on a video stream.

### Requirements

- Python 3
- `opencv-python`
- `numpy`
- YOLO files: `.cfg`, `.weights`, and class names `.names`

### Run

```bash
python yolo_video_detection.py \
  --video input.mp4 \
  --cfg yolov3.cfg \
  --weights yolov3.weights \
  --names coco.names \
  --output output.mp4
```

Use `--video 0` to run from webcam.
