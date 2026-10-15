#!/usr/bin/env python3
import argparse
import cv2
import time
from datetime import datetime

try:
    from hailo_platform import HEF, Device, VDevice, HailoRTException
except Exception as e:
    raise SystemExit("Error: hailo_platform not found. Install hailort first (bash scripts/setup_hailo.sh)")

def main():
    ap = argparse.ArgumentParser(description="YOLO26 Detection (Hailo-8)")
    ap.add_argument("--hef", required=True, help="Path to .hef file")
    ap.add_argument("--source", default="0", help="Camera index or video/image path")
    ap.add_argument("--conf", type=float, default=0.4)
    ap.add_argument("--iou", type=float, default=0.45)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--show", action="store_true", help="Show window")
    ap.add_argument("--fps", action="store_true", help="Print FPS")
    args = ap.parse_args()

    src = 0 if args.source == "0" else args.source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open source: {args.source}")

    try:
        hef = HEF(args.hef)
        devices = Device.scan()
        if not devices:
            raise RuntimeError("No Hailo device found. Run: hailortcli scan")
        print(f"[HAILO] Device detected: {len(devices)} | Using HEF: {args.hef}")
    except Exception as e:
        cap.release()
        raise

    prev_time = time.time()
    frame_count = 0
    fps = 0.0

    try:
        with VDevice(devices[0]) as target:
            with target.create_infer_model(hef) as model:
                model.set_batch_size(1)
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frame_count += 1
                    # TODO: Full preprocessing + inference + postprocessing sesuai output HEF
                    cur = time.time()
                    dt = cur - prev_time
                    if dt >= 1.0:
                        fps = frame_count / dt
                        frame_count = 0
                        prev_time = cur
                        if args.fps:
                            print(f"[FPS] {fps:.2f}")

                    if args.show:
                        cv2.putText(frame, f"Hailo DET | FPS: {fps:.1f}", (10, 25),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.imshow("YOLO26-DET (Hailo)", frame)
                        if cv2.waitKey(1) & 0xFF == 27:
                            break
    except Exception as e:
        print(f"[ERR] {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("[INFO] Stopped")

if __name__ == "__main__":
    main()
