# Compile YOLO26 ONNX -> HEF (Hailo Dataflow Compiler)

Panduan mengubah graf ONNX YOLO26 menjadi `.hef` yang bisa dijalankan di NPU Hailo-8/8L.

## 1) Prasyarat

- ONNX hasil ekspor Ultralytics: `yolo26n.onnx`, `yolo26n-seg.onnx`
- Folder calibration: `assets/calib/` berisi ~100-500 gambar JPG/PNG representatif domain kamu
- `hailo-all` / Data Flow Compiler sudah terinstall (`bash scripts/setup_hailo.sh`)

Ekspor ONNX:

```bash
python3 -c "from ultralytics import YOLO; YOLO('yolo26n.pt').export(format='onnx', imgsz=640, opset=13, simplify=True)"
python3 -c "from ultralytics import YOLO; YOLO('yolo26n-seg.pt').export(format='onnx', imgsz=640, opset=13, simplify=True)"
```

## 2) Compile via CLI

Deteksi:

```bash
hailo model compiler \
  --onnx models/yolo26n.onnx \
  --hw_arch hailo8 \
  --calib-path assets/calib/ \
  --output-dir models/hef/
```

Segmentasi:

```bash
hailo model compiler \
  --onnx models/yolo26n-seg.onnx \
  --hw_arch hailo8 \
  --calib-path assets/calib/ \
  --output-dir models/hef/
```

Ganti `--hw_arch hailo8` menjadi `hailo8l` bila memakai Hailo-8L (26 TOPS).

## 3) Verifikasi HEF

```bash
hailortcli parse-hef models/hef/yolo26n.hef
hailortcli parse-hef models/hef/yolo26n-seg.hef
```

Perhatikan nama output layer (bbox, scores, classes, mask coeffs). Nama-nama ini dipakai untuk postprocessing di `detect_hailo.py` / `seg_hailo.py`.

## 4) Parameter Penting DFC

| Flag | Fungsi |
|---|---|
| `--hw_arch` | Target chip: `hailo8` atau `hailo8l` |
| `--calib-path` | Set gambar untuk kuantisasi INT8 (PTQ) |
| `--performance` | Optimasi throughput |
| `--classes` | Jumlah kelas (deteksi) |

## 5) Tips

- Selalu pakai `opset=13` dan `simplify=True` saat ekspor ONNX.
- Pastikan input statis (imgsz tetap), hindari dynamic shape.
- Kalau ada layer unsupported, update `hailo-all` ke versi terbaru lalu compile ulang.
- Compile bisa makan 5-20 menit di Pi; lebih cepat di PC x86 dengan DFC.
