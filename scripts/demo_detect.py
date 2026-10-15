#!/usr/bin/env python3
import argparse
from ultralytics import YOLO

def main():
    ap = argparse.ArgumentParser(description="YOLO26 Detection (CPU/NCNN)")
    ap.add_argument('--model', required=True, help='Path to *_ncnn_model folder or .pt')
    ap.add_argument('--source', default='0', help='0 for webcam, image/video/rtsp path')
    ap.add_argument('--conf', type=float, default=0.4)
    ap.add_argument('--iou', type=float, default=0.45)
    ap.add_argument('--imgsz', type=int, default=640)
    ap.add_argument('--show', action='store_true')
    args = ap.parse_args()

    src = 0 if args.source == '0' else args.source
    model = YOLO(args.model)
    model.predict(
        source=src,
        conf=args.conf,
        iou=args.iou,
        imgsz=args.imgsz,
        show=args.show,
        verbose=False,
        stream=True
    )

if __name__ == '__main__':
    main()
