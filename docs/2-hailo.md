# 2. Dengan Hailo-8 / Hailo-8L (NPU — Raspberry Pi 5)

Jalur ini menjalankan YOLO26 deteksi dan segmentasi di **NPU Hailo-8**, mencapai **50+ FPS** untuk keduanya. Butuh hardware accelerator Hailo.

## 2.1 Hardware yang Didukung

| Hardware | Chip | Catatan |
|---|---|---|
| **Hailo AI HAT+** (official) | Hailo-8L atau Hailo-8 | Pasang di slot M.2 Pi 5 — disarankan |
| Hailo-8 M.2 module | Hailo-8 | Modul terpisah, butuh carrier board |

> **Wajib**: Raspberry Pi 5 + AI HAT+ atau Hailo-8 M.2. Pi 4 TIDAK didukung untuk AI HAT+.

## 2.2 Install Hailo Runtime + Firmware

```bash
# 1. Pasang HAT+ secara fisik, lalu reboot
sudo reboot

# 2. Clone repo & install runtime
git clone <repo-ini>
cd yolo26-raspi
bash scripts/setup_hailo.sh

# 3. Verifikasi perangkat terdeteksi
hailortcli scan
# Harus menampilkan: Hailo8/8L device detected
```

`setup_hailo.sh` akan:
- Install `hailo-all` (HailoRT + firmware + DFC)
- Install `hailo-model-zoo`
- Load kernel module & set permission device
- Install Python SDK (`hailo_sdk` / `hailortcli`)

## 2.3 Dua Cara Mendapatkan Model HEF

### Cara A — Gunakan Model Zoo (cepat, model umum)

Untuk YOLO versi lama yang sudah tersedia di Model Zoo (mis. YOLOv8-seg), compile langsung:

```bash
# Contoh: compile yolov8s-seg ke HEF
hailo model compiler --model yolov8s-seg --hw_arch hailo8
```

Daftar model: `hailo model zoo list`

### Cara B — Compile YOLO26 sendiri (disarankan untuk YOLO26)

YOLO26 belum tersedia default di Model Zoo, jadi compile sendiri via ONNX → DFC:

```bash
# 1. Ekspor YOLO26 ke ONNX (di komputer yang punya GPU/CPU cukup)
python -c "
from ultralytics import YOLO
YOLO('yolo26n.pt').export(format='onnx', imgsz=640, opset=13)
YOLO('yolo26n-seg.pt').export(format='onnx', imgsz=640, opset=13)
"

# 2. Compile ONNX → HEF dengan DFC (Data Flow Compiler)
hailo model compiler \
  --onnx yolo26n.onnx \
  --hw_arch hailo8 \
  --output-dir assets/hef/

hailo model compiler \
  --onnx yolo26n-seg.onnx \
  --hw_arch hailo8 \
  --output-dir assets/hef/
```

Langkah detail & parameter tuning: [`scripts/hailo/compile_hef.md`](../scripts/hailo/compile_hef.md)

> **Catatan INT8**: compile default menggunakan PTQ INT8 dengan calibration images. Siapkan ~200–1000 gambar representatif domain kamu untuk akurasi terbaik.

## 2.4 Jalankan Inferensi via NPU

### Deteksi (Hailo-8)

```bash
python scripts/hailo/detect_hailo.py \
  --hef assets/hef/yolo26n.hef \
  --source 0 \
  --conf 0.4
```

### Segmentasi (Hailo-8)

```bash
python scripts/hailo/seg_hailo.py \
  --hef assets/hef/yolo26n-seg.hef \
  --source 0 \
  --conf 0.4
```

## 2.5 Benchmark Hasil Nyata (Pi 5 + Hailo-8)

Dari riset EdgeLane-SEG (2026), YOLO26-SEG di Pi 5 + Hailo-8:

| Konfigurasi | Latensi | FPS | Efisiensi | Power |
|---|---|---|---|---|
| Pi 5 CPU only (YOLO26-SEG) | 340 ms | 2.9 | 0.53 FPS/W | 5–6 W |
| Pi 5 + Movidius VPU | 290 ms | 3.5 | 0.77 FPS/W | 4–5 W |
| **Pi 5 + Hailo-8 (INT8)** | **19–20 ms** | **50–52** | **18.85 FPS/W** | 2.5–3 W |

Deteksi (non-seg) juga di kisaran serupa atau lebih tinggi dengan Hailo-8.

## 2.6 Catatan Penting

1. **Akselerasi CPU vs NPU**: preprocessing (decode, resize) tetap di CPU Pi — pastikan cukup headroom CPU.
2. **INT8 vs FP32**: HEF Hailo selalu INT8. Akurasi turun sedikit (~0.5–1% mAP) vs FP32, tapi tidak signifikan untuk kebanyakan use case.
3. **Thermal**: AI HAT+ punya heatsink; pastikan aliran udara baik agar NPU dan CPU tidak throttle.
4. **Lisensi SDK**: Hailo SDK proprietary — hanya untuk perangkat Hailo, tidak untuk redistribute.

## 2.7 Checklist Deploy

- [ ] Pi 5 + AI HAT+ terpasang fisik
- [ ] `hailortcli scan` menampilkan device
- [ ] Model HEF berhasil di-compile
- [ ] `detect_hailo.py` / `seg_hailo.py` jalan dengan FPS sesuai target
- [ ] Thermal & power stabil untuk operasi jangka panjang
