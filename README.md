# YOLO26 di Raspberry Pi — Deteksi & Segmentasi (Tanpa & Dengan Hailo)

Panduan langkah-demi-langkah menjalankan **YOLO26** (deteksi `YOLO26n/s/...` dan segmentasi `YOLO26n-seg/...`) di Raspberry Pi, dalam dua skenario:

| Skenario | Hardware | Hasil (Pi 5, 640×640, FP32/INT8) |
|---|---|---|
| **Tanpa Hailo** (CPU only) | Raspberry Pi 4/5 | Deteksi ~7–8 FPS (YOLO26n, NCNN); Seg ~3 FPS |
| **Dengan Hailo** (NPU) | Pi 5 + Hailo-8 / Hailo-8L AI HAT+ | Deteksi 50+ FPS; Seg **50–52 FPS** (INT8) |

> Segmentation real-time di Pi murni **tidak memadai** — butuh NPU seperti Hailo-8.

## Struktur Repository

```
yolo26-raspi/
├── README.md
├── docs/
│   ├── 1-cpu-only.md          # Skema tanpa Hailo (NCNN/ONNX/OpenVINO)
│   ├── 2-hailo.md             # Skema dengan Hailo-8 (HailoRT + HEF)
│   └── troubleshooting.md     # Masalah umum & solusi
├── scripts/
│   ├── setup_cpu.sh           # Install environment CPU (Pi OS 64-bit)
│   ├── setup_hailo.sh         # Install HailoRT, firmware, model zoo
│   ├── export_ncnn.sh         # Ekspor PyTorch → NCNN (format tercepat di ARM)
│   ├── demo_detect.py         # Demo deteksi (CPU, PyTorch/NCNN)
│   ├── demo_seg.py            # Demo segmentasi (CPU)
│   ├── benchmark_cpu.py       # Benchmark FPS/latensi di perangkat
│   └── hailo/
│       ├── compile_hef.md     # Cara compile YOLO26 → HEF (DFC)
│       ├── detect_hailo.py    # Demo deteksi via Hailo-8 (hailo_sdk)
│       └── seg_hailo.py       # Demo seg via Hailo-8
├── requirements-cpu.txt
├── requirements-hailo.txt
└── .gitignore
```

## Pilih Jalur Cepat

**Baru mulai? Ikuti urutan ini:**

1. Siapkan OS: **Raspberry Pi OS (64-bit, Bookworm)** — arsitektur `arm64` wajib.
2. **Tanpa Hailo** → ikuti [`docs/1-cpu-only.md`](docs/1-cpu-only.md)
3. **Dengan Hailo** → ikuti [`docs/2-hailo.md`](docs/2-hailo.md)
4. Ada error? → [`docs/troubleshooting.md`](docs/troubleshooting.md)

## Peringatan Lisensi

- **Ultralytics YOLO26**: lisensi non-permissive untuk sebagian model (cek `ultralytics` — sebagian besar di bawah AGPL-3.0 / komersial). Untuk produk komersial, beli lisensi Ultralytics.
- **Hailo SDK / Model Zoo**: proprietary — hanya untuk perangkat Hailo.
- Pastikan kepatuhan lisensi sebelum deploy produksi.

## Referensi

- [Ultralytics Raspberry Pi Guide](https://docs.ultralytics.com/guides/raspberry-pi)
- [Hailo AI HAT+ / Model Zoo](https://hailo.ai/developer-zone/)
- Benchmark CPU Pi 5: YOLO26n ONNX 128 ms (≈7.8 FPS), NCNN ≈67 ms (≈15 FPS)
- Benchmark Hailo-8: YOLO26-SEG 19–20 ms (≈50–52 FPS, INT8)
