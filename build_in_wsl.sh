#!/bin/bash
# 在 Ubuntu / WSL 内一键装依赖 + 编译 APK，由 一键打包.bat 调用
# 参数 $1 = APK 要拷贝回 Windows 的目标目录（wslpath 格式）
set -e

OUT_DIR="${1:-$HOME}"
echo "===================================================="
echo " V0 auto build inside Ubuntu"
echo " output dir: $OUT_DIR"
echo "===================================================="

echo "[1/5] apt update + install build deps..."
export DEBIAN_FRONTEND=noninteractive
sudo apt update -y
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
  autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
  libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
  build-essential

echo "[2/5] install buildozer (Tsinghua mirror)..."
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install --user --upgrade pip
pip3 install --user buildozer
pip3 install --user "Cython<3"

echo "[3/5] accept Android SDK licenses..."
export PATH="$HOME/.local/bin:$PATH"
yes | ~/.local/bin/buildozer android update_sdk || true

echo "[4/5] building APK (first time 20-50 min)..."
cd ~/pujiang_v0
~/.local/bin/buildozer -v android debug

echo "[5/5] copying APK back to Windows..."
APK=$(ls ~/pujiang_v0/bin/*.apk 2>/dev/null | head -1)
if [ -z "$APK" ]; then
  echo "ERROR: no APK found in bin/. Build may have failed."
  exit 1
fi
cp "$APK" "$OUT_DIR/"
echo "DONE. APK copied to: $OUT_DIR/$(basename "$APK")"
