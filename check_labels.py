from pathlib import Path

label_dir = Path("dataset/labels/train")
bad_files = []

for file in label_dir.glob("*.txt"):
    content = file.read_text(encoding="utf-8").strip()

    if not content:
        bad_files.append((file.name, "EMPTY"))
        continue

    for line in content.splitlines():
        parts = line.strip().split()

        if len(parts) != 5:
            bad_files.append((file.name, f"WRONG_PARTS: {line}"))
            break

        try:
            cls_id = int(parts[0])
            values = list(map(float, parts[1:]))
        except:
            bad_files.append((file.name, f"NON_NUMERIC: {line}"))
            break

        if cls_id != 0:
            bad_files.append((file.name, f"BAD_CLASS_ID: {line}"))
            break

        if not all(0 <= v <= 1 for v in values):
            bad_files.append((file.name, f"OUT_OF_RANGE: {line}"))
            break

print(f"Checked {len(list(label_dir.glob('*.txt')))} label files")
print(f"Bad files found: {len(bad_files)}")

for name, reason in bad_files[:20]:
    print(name, "->", reason)
