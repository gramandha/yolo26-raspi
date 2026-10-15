#!/bin/bash
# Setup environment Hailo untuk Raspberry Pi 5 + AI HAT+

set -e

echo "[INFO] Install HailoRT, firmware, SDK & dependencies..."
sudo apt update

# Install Hailo repository & packages (versi umum; cek hailo.ai untuk version terbaru)
# Referensi: https://hailo.ai/developer-zone/
echo "[INFO] Menambahkan Hailo apt repo (jika belum)..."
curl -fsSL https://repo.hailo.ai/hailo/public.key | sudo gpg --dearmor -o /usr/share/keyrings/hailo-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hailo-archive-keyring.gpg] https://repo.hailo.ai/hailo/debian stable main" | sudo tee /etc/apt/sources.list.d/hailo.list >/dev/null
sudo apt update

echo "[INFO] Install hailo-all & tools..."
sudo apt install -y \
  hailo-all \
  hailortcli \
  hailo-model-zoo \
  v4l-utils

# Load kernel module
echo "[INFO] Loading Hailo kernel module..."
sudo modprobe hailo_pci || true

# Persist
echo "hailo_pci" | sudo tee /etc/modules-load.d/hailo.conf >/dev/null

# Set permission
echo "[INFO] Setting udev rules..."
sudo usermod -aG hailo "$(whoami)"

echo "[INFO] Upgrade pip & install Python deps..."
pip install --upgrade pip wheel setuptools
pip install -r requirements-hailo.txt

echo "[OK] Hailo environment siap."
echo "[INFO] Silakan reboot, lalu jalankan: hailortcli scan"
echo "[INFO] Setelah reboot, login kembali agar group 'hailo' aktif."
