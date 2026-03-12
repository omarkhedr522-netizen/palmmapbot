from ultralytics import YOLO

class TreeDetector:
    def __init__(self, model_path=r"runs\detect\runs\palm_tree_bootstrap3\weights\best.pt", confidence_threshold=0.5):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def detect_tree(self, image_path):
        results = self.model(image_path, verbose=False)
        boxes = results[0].boxes

        if boxes is None or len(boxes) == 0:
            return {
                "has_tree": False,
                "confidence": 0.0
            }

        max_confidence = 0.0

        for box in boxes:
            conf = float(box.conf[0])
            if conf > max_confidence:
                max_confidence = conf

        return {
            "has_tree": max_confidence >= self.confidence_threshold,
            "confidence": max_confidence
        }
