# 1. Tanpa Hailo (CPU Only — Raspberry Pi 4/5)

Jalur ini menjalankan YOLO26 murni di CPU Pi. Cocok untuk deteksi ~7–15 FPS atau segmentation ringan (~3 FPS). Untuk real-time segmentation, lihat [`2-hailo.md`](2-hailo.md).

## 1.1 Prasyarat

```bash
# Pastikan 64-bit
uname -m          # harus: aarch64
# Pastikan OS
cat /etc/os-release   # Raspberry Pi OS Bookworm 64-bit direkomendasikan
```

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-venv python3-pip git libatlas-base-dev libopenblas-dev
```

## 1.2 Setup Environment

```bash
git clone <repo-ini>
cd yolo26-raspi

python3 -m venv .venv
source .venv/bin/activate

# Install dependensi CPU
bash scripts/setup_cpu.sh
```

## 1.3 Ekspor Model ke NCNN (Format Tercepat di ARM)

NCNN adalah format inference tercepat untuk Raspberry Pi. Ekspor sekali di komputer lain atau langsung di Pi.

```bash
# Aktifkan venv dulu
source .venv/bin/activate

# Ekspor YOLO26n (deteksi) ke NCNN
bash scripts/export_ncnn.sh detection nano

# Ekspor YOLO26n-seg (segmentasi) ke NCNN
bash scripts/export_ncnn.sh segmentation nano
```

Atau manual via Python:

```python
from ultralytics import YOLO

# Muat model PyTorch, ekspor ke NCNN
model = YOLO("yolo26n.pt")          # deteksi
# model = YOLO("yolo26n-seg.pt")    # atau segmentasi
model.export(format="ncnn", imgsz=640, half=False)
# Hasil: folder yolo26n_ncnn_model/ berisi *.bin & *.param
```

## 1.4 Jalankan Inferensi

### Deteksi (CPU)

```bash
python scripts/demo_detect.py \
  --model assets/yolo26n_ncnn_model \
  --source 0 \                    # 0 = webcam; bisa juga path gambar/video
  --conf 0.4
```

### Segmentasi (CPU)

```bash
python scripts/demo_seg.py \
  --model assets/yolo26n-seg_ncnn_model \
  --source 0 \
  --conf 0.4
```

## 1.5 Benchmark FPS

```bash
python scripts/benchmark_cpu.py --model assets/yolo26n_ncnn_model --runs 100
```

Contoh hasil nyata di **Pi 5 (FP32)**:

| Model | Format | mAP50-95 | Latensi | FPS |
|---|---|---|---|---|
| YOLO26n | ONNX | 40.1 | 128 ms | ~7.8 |
| YOLO26n | NCNN | 40.1 | **67 ms** | **~15** |
| YOLO26n | OpenVINO | 40.1 | 105 ms | ~9.5 |
| YOLO26s | NCNN | 47.8 | 220 ms | ~4.5 |

> Di Pi 4, FPS biasanya ~40–50% lebih rendah dari Pi 5.

## 1.6 Tips Optimasi CPU

1. **Gunakan NCNN, bukan ONNX/PyTorch** — perbedaan signifikan di ARM.
2. **Kurangi resolusi input** — `imgsz=416` atau `320` menaikkan FPS 2–3×, sedikit turunkan akurasi.
3. **Gunakan int8 quantization** jika butuh lebih cepat lagi (lihat `benchmark_cpu.py --int8`).
4. **Matikan thermal throttle** — pasang heatsink + kipas aktif; Pi 5 bisa turun drastis jika panas.
5. **Gunakan `libatlas`/`openblas`** untuk percepatan linear algebra di CPU.

## 1.7 Kapan Harus Pindah ke Jalur Hailo?

- Butuh **segmentasi real-time** (>10 FPS)
- Butuh **deteksi >30 FPS**
- Butuh **multi-stream** atau model lebih besar (YOLO26s/m)

→ Lanjut ke [`2-hailo.md`](2-hailo.md)
