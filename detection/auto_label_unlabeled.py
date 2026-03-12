from ultralytics import YOLO
from pathlib import Path
import shutil

# Your trained model
model = YOLO(r"runs\detect\runs\palm_tree_bootstrap2\weights\best.pt")

unlabeled_dir = Path("dataset/unlabeled")
train_img_dir = Path("dataset/images/train")
train_lbl_dir = Path("dataset/labels/train")

CONF_THRESHOLD = 0.5

image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

added = 0
skipped = 0

for img_path in unlabeled_dir.iterdir():
    if img_path.suffix.lower() not in image_extensions:
        continue

    results = model(str(img_path), verbose=False)
    boxes = results[0].boxes

    if boxes is None or len(boxes) == 0:
        skipped += 1
        continue

    lines = []

    for box in boxes:
        conf = float(box.conf[0])

        if conf < CONF_THRESHOLD:
            continue

        cls = int(box.cls[0])
        xywh = box.xywhn[0].tolist()

        line = f"{cls} {xywh[0]:.6f} {xywh[1]:.6f} {xywh[2]:.6f} {xywh[3]:.6f}"
        lines.append(line)

    if lines:
        new_img = train_img_dir / img_path.name
        new_lbl = train_lbl_dir / f"{img_path.stem}.txt"

        shutil.copy2(img_path, new_img)

        with open(new_lbl, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        added += 1
    else:
        skipped += 1

print(f"Auto labeling complete. Added: {added}, Skipped: {skipped}")
