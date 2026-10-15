#!/usr/bin/env python3
import argparse
import cv2
import time

try:
    from hailo_platform import HEF, Device, VDevice
except Exception:
    raise SystemExit("Error: hailo_platform not found. Install hailort first")

def main():
    ap = argparse.ArgumentParser(description="YOLO26 Segmentation (Hailo-8)")
    ap.add_argument("--hef", required=True)
    ap.add_argument("--source", default="0")
    ap.add_argument("--conf", type=float, default=0.4)
    ap.add_argument("--iou", type=float, default=0.45)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--fps", action="store_true")
    args = ap.parse_args()

    src = 0 if args.source == "0" else args.source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open source: {args.source}")

    hef = HEF(args.hef)
    devices = Device.scan()
    if not devices:
        raise RuntimeError("No Hailo device found. Run: hailortcli scan")

    prev = time.time(); cnt = 0; fps = 0.0
    try:
        with VDevice(devices[0]) as target:
            with target.create_infer_model(hef) as model:
                model.set_batch_size(1)
                while True:
                    ret, frame = cap.read()
                    if not ret: break
                    cnt += 1
                    now = time.time()
                    if now - prev >= 1.0:
                        fps = cnt/(now-prev); cnt=0; prev=now
                        if args.fps: print(f"[FPS] {fps:.2f}")
                    if args.show:
                        cv2.putText(frame, f"Hailo SEG | FPS: {fps:.1f}", (10,25),
                                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255),2)
                        cv2.imshow("YOLO26-SEG (Hailo)", frame)
                        if cv2.waitKey(1)&0xFF==27: break
    finally:
        cap.release(); cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
