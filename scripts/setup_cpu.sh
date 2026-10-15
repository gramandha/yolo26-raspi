#!/bin/bash
# Setup environment CPU-only untuk Raspberry Pi OS 64-bit (Bookworm)

set -e

echo "[INFO] Menginstall dependensi CPU-only..."
sudo apt update
sudo apt install -y \
  python3-venv \
  python3-pip \
  git \
  libatlas-base-dev \
  libopenblas-dev \
  liblapack-dev \
  libjpeg-dev \
  zlib1g-dev \
  libssl-dev \
  build-essential \
  cmake \
  pkg-config \
  v4l-utils \
  libgl1 \
  libglib2.0-0

echo "[INFO] Upgrade pip..."
pip install --upgrade pip wheel setuptools

echo "[INFO] Install Python package dari requirements-cpu.txt..."
pip install -r requirements-cpu.txt

echo "[OK] CPU environment siap. Aktifkan venv: source .venv/bin/activate"
