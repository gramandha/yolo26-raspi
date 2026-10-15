#!/bin/bash
# Ekspor YOLO26 ke NCNN — format inference tercepat untuk ARM/Pi
#
# Penggunaan:
#   bash scripts/export_ncnn.sh detection nano       # yolo26n.pt
#   bash scripts/export_ncnn.sh segmentation small   # yolo26s-seg.pt
#
# Args:
#   $1 = detection | segmentation
#   $2 = nano | small | medium | large | x | (varian lain)

set -e

TYPE="${1:-detection}"
SIZE="${2:-nano}"

if [ "$TYPE" = "segmentation" ]; then
  MODEL="yolo26${SIZE}-seg.pt"
else
  MODEL="yolo26${SIZE}.pt"
fi

echo "[INFO] Ekspor $MODEL ke NCNN (imgsz=640)..."

python3 - <<EOF
from ultralytics import YOLO

model = YOLO("$MODEL")          # auto-download jika belum ada
path = model.export(format="ncnn", imgsz=640, half=False)
print("[OK] Hasil ekspor:", path)
EOF

echo "[OK] Selesai. Folder *_ncnn_model bisa dipakai demo_detect.py / demo_seg.py"
