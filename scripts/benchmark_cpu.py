#!/usr/bin/env python3
import argparse
import time
import numpy as np
from ultralytics import YOLO

def main():
    ap = argparse.ArgumentParser(description="Benchmark YOLO26 di CPU (NCNN/ONNX)")
    ap.add_argument('--model', required=True)
    ap.add_argument('--runs', type=int, default=100)
    ap.add_argument('--warmup', type=int, default=20)
    ap.add_argument('--imgsz', type=int, default=640)
    args = ap.parse_args()

    model = YOLO(args.model)
    dummy = np.zeros((args.imgsz, args.imgsz, 3), dtype=np.uint8)

    print(f"[WARMUP] {args.warmup} frames...")
    for _ in range(args.warmup):
        _ = model(dummy, imgsz=args.imgsz, verbose=False)

    times = []
    print(f"[BENCH] {args.runs} frames...")
    for _ in range(args.runs):
        t0 = time.perf_counter()
        _ = model(dummy, imgsz=args.imgsz, verbose=False)
        times.append((time.perf_counter() - t0) * 1000.0)

    times = np.array(times)
    print("=== CPU BENCHMARK ===")
    print(f"Model: {args.model}")
    print(f"Runs: {args.runs} | Warmup: {args.warmup}")
    print(f"Mean:   {times.mean():.2f} ms")
    print(f"Median: {np.median(times):.2f} ms")
    print(f"Min:    {times.min():.2f} ms")
    print(f"Max:    {times.max():.2f} ms")
    print(f"FPS:    {1000.0/times.mean():.2f}")
    print("======================")

if __name__ == '__main__':
    main()
