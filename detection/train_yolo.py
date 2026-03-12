from ultralytics import YOLO

def main():
    model = YOLO("yolov8n.pt")

    model.train(
        data="dataset/data.yaml",
        epochs=40,
        imgsz=640,
        batch=8,
        project="runs",
        name="palm_tree_bootstrap"
    )

if __name__ == "__main__":
    main()
