# Troubleshooting — Masalah Umum

## CPU Only

### `ModuleNotFoundError: No module named 'ultralytics'`
```bash
source .venv/bin/activate
pip install -r requirements-cpu.txt
```

### FPS jauh lebih rendah dari tabel benchmark
- Pastikan **64-bit OS** (`uname -m` = `aarch64`)
- Pastikan pakai **NCNN**, bukan ONNX/PyTorch
- Cek thermal: `vcgencmd measure_temp` — jika >80°C, throttling aktif. Pasang heatsink/kipas.
- Pastikan power supply resmi Pi 5 (5V/5A); brown-out menurunkan clock CPU.

### `libatlas` / `libopenblas` error saat install
```bash
sudo apt install -y libatlas-base-dev libopenblas-dev liblapack-dev
pip install --no-cache-dir -r requirements-cpu.txt
```

### Webcam tidak terbuka (`--source 0`)
```bash
# Cek device video
ls /dev/video*
# Install dependensi kamera
sudo apt install -y v4l-utils
# Test
libcamera-hello   # Pi Camera
fswebcam /dev/video0   # USB cam
```

### Model NCNN tidak ditemukan
Pastikan ekspor menghasilkan folder `*_ncnn_model/` berisi file `.bin` dan `.param`. Path ke folder, bukan ke file `.pt`.

---

## Hailo

### `hailortcli scan` tidak menemukan device
1. Pastikan AI HAT+ terpasang di slot M.2 Pi 5, lalu reboot.
2. Cek kernel module: `lsmod | grep hailo` — jika kosong, `sudo modprobe hailo_pci`
3. Cek dmesg: `dmesg | grep -i hailo`
4. Update firmware: `sudo hailortcli fw-update` (jika tersedia)
5. Cek slot M.2 & fisik koneksi.

### Compile HEF gagal (DFC error)
- Pastikan ONNX opset ≥ 13 dan input shape tetap (bukan dinamis).
- Beberapa layer YOLO26 mungkin belum didukung DFC versi lama — update `hailo-all` ke versi terbaru.
- Untuk segmentasi, pastikan output mask head ter-export dengan benge. Gunakan `--verbose` saat compile untuk lihat layer bermasalah.
- Jika tetap gagal, coba `yolo26n-seg` varian lebih kecil atau laporkan ke Hailo support dengan log DFC.

### FPS Hailo jauh di bawah 50
- Pastikan bukan bottleneck preprocessing CPU — kurangi resolusi kamera input, atau pindahkan preprocessing ke thread terpisah.
- Cek `hailortcli monitor` untuk utilisasi NPU.
- Pastikan tidak ada fallback diam-diam ke CPU (cek log error SDK).

### Akurasi turun banyak setelah INT8
- Recompile HEF dengan **calibration dataset** yang representatif (200–1000 gambar domain kamu), bukan default COCO.
- Gunakan parameter PTQ lebih hati-hati di DFC (lihat `compile_hef.md`).

### `hailo_sdk` module not found
```bash
# SDK hanya tersedia setelah setup_hailo.sh, dan di Python 3.9–3.11
python3 --version
pip install hailo-all --extra-index-url https://library.hailo.ai/simple/
```

---

## Umum

### Out of memory (OOM)
- Kurangi `imgsz` ke 416 atau 320.
- Tutup aplikasi lain; di Pi, browser + browser tabs memakan RAM besar.
- Untuk Hailo, pastikan cukup RAM untuk buffer preprocessing.

### Butuh lebih cepat tapi akurasi boleh turun
1. Turunkan input ke 320×320
2. Pakai varian `n` (nano)
3. Naikkan `conf` threshold (kurangi jumlah deteksi)
4. Di CPU: pastikan NCNN + int8
