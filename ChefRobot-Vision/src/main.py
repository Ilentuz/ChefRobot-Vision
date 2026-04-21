"""Real-time webcam detection for food and kitchen categories only."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Final

import cv2
from ultralytics import YOLOWorld

MODEL_NAME: Final[str] = "yolov8m-world.pt"
WINDOW_NAME: Final[str] = "Roboruka Vision"
CAMERA_INDEX: Final[int] = 0
CONFIDENCE_THRESHOLD: Final[float] = 0.35
IOU_THRESHOLD: Final[float] = 0.45
QUIT_KEY: Final[str] = "q"
LOGS_DIRECTORY_NAME: Final[str] = "logs"
LOG_FILE_NAME: Final[str] = "vision.log"
LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

TARGET_LABELS: Final[tuple[str, ...]] = (
    "apple",
    "banana",
    "orange",
    "broccoli",
    "carrot",
    "tomato",
    "cucumber",
    "bell pepper",
    "potato",
    "onion",
    "garlic",
    "eggplant",
    "avocado",
    "strawberry",
    "blueberry",
    "raspberry",
    "blackberry",
    "egg",
    "bowl",
    "cup",
    "mug",
    "plate",
    "fork",
    "knife",
    "spoon",
    "chopping board",
    "cutting board",
    "pan",
    "pot",
    "bottle",
)


def configure_logger() -> logging.Logger:
    """Create and return application logger for vision pipeline."""
    logger: logging.Logger = logging.getLogger("vision_detector")
    if logger.handlers:
        return logger

    logs_dir: Path = Path(LOGS_DIRECTORY_NAME)
    logs_dir.mkdir(parents=True, exist_ok=True)
    file_handler: logging.FileHandler = logging.FileHandler(
        logs_dir / LOG_FILE_NAME,
        encoding="utf-8",
    )
    formatter: logging.Formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger


def normalize_label(label: str) -> str:
    """Normalize model label for stable filtering and display."""
    return label.strip().lower()


def should_display_detection(label: str) -> bool:
    """Return True if a label is allowed by project requirements."""
    return normalize_label(label) in TARGET_LABELS


def draw_detection(
    frame: Any,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    label: str,
    confidence: float,
) -> None:
    """Draw one accepted detection on frame."""
    color: tuple[int, int, int] = (0, 180, 0)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    caption: str = f"{label}: {confidence:.2f}"
    cv2.putText(
        frame,
        caption,
        (x1, max(y1 - 10, 20)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
        cv2.LINE_AA,
    )


def run_realtime_detection() -> None:
    """Run webcam stream and display only allowed object classes."""
    logger: logging.Logger = configure_logger()
    logger.info("Initializing YOLO World model: %s", MODEL_NAME)
    model: YOLOWorld = YOLOWorld(MODEL_NAME)
    model.set_classes(list(TARGET_LABELS))

    camera: cv2.VideoCapture = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        logger.error("Cannot open webcam at index %s", CAMERA_INDEX)
        raise RuntimeError(f"Cannot open webcam at index {CAMERA_INDEX}")

    logger.info("Webcam stream started")
    try:
        while True:
            success: bool
            frame: Any
            success, frame = camera.read()
            if not success:
                logger.error("Failed to read frame from webcam")
                raise RuntimeError("Failed to read frame from webcam")

            prediction_result = model.predict(
                source=frame,
                conf=CONFIDENCE_THRESHOLD,
                iou=IOU_THRESHOLD,
                verbose=False,
            )[0]
            boxes = prediction_result.boxes
            names: dict[int, str] = prediction_result.names

            if boxes is not None:
                for box in boxes:
                    confidence: float = float(box.conf[0].item())
                    class_id: int = int(box.cls[0].item())
                    label: str = normalize_label(names[class_id])
                    if not should_display_detection(label):
                        continue
                    x1, y1, x2, y2 = (int(value) for value in box.xyxy[0].tolist())
                    draw_detection(frame, x1, y1, x2, y2, label, confidence)

            cv2.imshow(WINDOW_NAME, frame)
            if cv2.waitKey(1) & 0xFF == ord(QUIT_KEY):
                logger.info("Stop key pressed, shutting down")
                break
    except (RuntimeError, cv2.error) as exc:
        logger.exception("Vision loop failed: %s", exc)
        raise
    finally:
        camera.release()
        cv2.destroyAllWindows()
        logger.info("Webcam stream closed")


if __name__ == "__main__":
    run_realtime_detection()
