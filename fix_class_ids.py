from pathlib import Path

label_dirs = [
    Path("dataset/labels/train"),
    Path("dataset/labels/val"),
    Path("dataset/labels/test"),
]

for label_dir in label_dirs:
    if not label_dir.exists():
        continue

    for file in label_dir.glob("*.txt"):
        lines = file.read_text(encoding="utf-8").strip().splitlines()
        new_lines = []

        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue

            parts[0] = "0"   # force palm_tree to class 0
            new_lines.append(" ".join(parts))

        file.write_text("\n".join(new_lines), encoding="utf-8")

print("Class IDs fixed successfully.")
