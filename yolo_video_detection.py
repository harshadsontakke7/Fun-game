import argparse
from pathlib import Path

import cv2
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="YOLO object detection on video")
    parser.add_argument("--video", required=True, help="Video path or webcam index (e.g. 0)")
    parser.add_argument("--cfg", required=True, help="Path to YOLO .cfg file")
    parser.add_argument("--weights", required=True, help="Path to YOLO .weights file")
    parser.add_argument("--names", required=True, help="Path to class names file")
    parser.add_argument("--output", help="Optional output video file path")
    parser.add_argument("--conf-threshold", type=float, default=0.5, help="Confidence threshold")
    parser.add_argument("--nms-threshold", type=float, default=0.4, help="NMS threshold")
    parser.add_argument("--input-size", type=int, default=416, help="YOLO input size")
    return parser.parse_args()


def load_classes(names_path):
    with open(names_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def create_capture(video_source):
    if video_source.isdigit():
        return cv2.VideoCapture(int(video_source))
    return cv2.VideoCapture(video_source)


def main():
    args = parse_args()

    names_path = Path(args.names)
    classes = load_classes(names_path)
    rng = np.random.default_rng(42)
    colors = rng.integers(0, 255, size=(max(len(classes), 1), 3), dtype=np.uint8)

    net = cv2.dnn.readNetFromDarknet(args.cfg, args.weights)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

    capture = create_capture(args.video)
    if not capture.isOpened():
        raise RuntimeError(f"Unable to open video source: {args.video}")

    writer = None
    window_name = "YOLO Object Detection"

    while True:
        has_frame, frame = capture.read()
        if not has_frame:
            break

        height, width = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(
            frame, 1 / 255.0, (args.input_size, args.input_size), swapRB=True, crop=False
        )
        net.setInput(blob)
        detections = net.forward(output_layers)

        boxes = []
        confidences = []
        class_ids = []

        for output in detections:
            for detection in output:
                scores = detection[5:]
                class_id = int(np.argmax(scores))
                confidence = float(scores[class_id])

                if confidence < args.conf_threshold:
                    continue

                center_x, center_y, box_w, box_h = detection[:4] * np.array(
                    [width, height, width, height]
                )
                x = int(center_x - box_w / 2)
                y = int(center_y - box_h / 2)
                boxes.append([x, y, int(box_w), int(box_h)])
                confidences.append(confidence)
                class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, args.conf_threshold, args.nms_threshold)

        if len(indices) > 0:
            for idx in indices.flatten():
                x, y, w, h = boxes[idx]
                class_id = class_ids[idx]
                label = classes[class_id] if class_id < len(classes) else f"class_{class_id}"
                color = tuple(int(c) for c in colors[class_id % len(colors)])

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(
                    frame,
                    f"{label}: {confidences[idx]:.2f}",
                    (x, max(y - 10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2,
                )

        if args.output and writer is None:
            fps = capture.get(cv2.CAP_PROP_FPS)
            if fps <= 0:
                fps = 30.0
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(args.output, fourcc, fps, (width, height))

        if writer is not None:
            writer.write(frame)

        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    capture.release()
    if writer is not None:
        writer.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
