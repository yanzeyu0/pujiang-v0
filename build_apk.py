#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
蒲江房产带看作战系统 - V0 Windows 原生打包
================================================
不依赖 WSL / 不依赖 Docker / 不依赖微软商店。

原理：python-for-android (Kivy 官方安卓打包后端) 原生支持 Windows，
直接在 Windows 上调用它编译 arm64 APK。

依赖（脚本会自动下载到 pujiang-agent\v0-kivy-test\toolchain\）：
  - JDK 17 (清华源)
  - Android cmdline-tools + SDK (dl.google.com)
  - python-for-android (清华 pypi 源)
"""
import os
import sys
import shutil
import subprocess
import zipfile
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
# 工具链放到盘符根短路径，规避 Windows 260 字符路径限制
# （项目路径本身较长，深目录 + 长 jar 名会超出限制）
TOOLCHAIN = Path("C:/pjtool")
JDK_ZIP = TOOLCHAIN / "jdk17.zip"
JDK_DIR = TOOLCHAIN / "jdk17"
SDK_DIR = TOOLCHAIN / "android-sdk"
CMDTOOLS_ZIP = TOOLCHAIN / "cmdline-tools.zip"
CMDTOOLS_DIR = SDK_DIR / "cmdline-tools" / "latest"
P4A_DIR = TOOLCHAIN / "p4a"
DIST_DIR = BASE / "dist"

# 清华源加速
PYPI = "https://pypi.tuna.tsinghua.edu.cn/simple"
JDK_URL = ("https://mirrors.tuna.tsinghua.edu.cn/Adoptium/17/jdk/x64/windows/"
           "OpenJDK17U-jdk_x64_windows_hotspot_17.0.21_9.zip")
CMDTOOLS_URL = ("https://dl.google.com/android/repository/"
                "commandlinetools-win-11076708_latest.zip")

def sh(cmd, **kw):
    print("  RUN:", cmd if isinstance(cmd, str) else " ".join(cmd))
    return subprocess.run(cmd, shell=isinstance(cmd, str), check=True, **kw)

def download(url, dest, desc):
    print(f"[下载] {desc}")
    print(f"       {url}")
    if dest.exists():
        print("       已存在，跳过")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        urllib.request.urlretrieve(url, tmp)
        tmp.rename(dest)
    finally:
        if tmp.exists():
            tmp.unlink()

def unzip(src, dst):
    print(f"[解压] {src.name} -> {dst}")
    with zipfile.ZipFile(src) as z:
        z.extractall(dst)

def main():
    print("=" * 60)
    print(" 蒲江房产 V0 - Windows 原生打包")
    print("=" * 60)
    TOOLCHAIN.mkdir(parents=True, exist_ok=True)

    # 1. JDK
    if not JDK_DIR.exists():
        download(JDK_URL, JDK_ZIP, "JDK 17 (清华源)")
        print("[解压] JDK ...")
        # 先解压到短路径，规避 Windows 260 字符路径限制
        short_tmp = TOOLCHAIN / "_tmp_jdk"
        if short_tmp.exists():
            shutil.rmtree(str(short_tmp))
        with zipfile.ZipFile(JDK_ZIP) as z:
            z.extractall(short_tmp)
        # 解压出的目录名带版本号，重命名为 jdk17
        for d in short_tmp.glob("jdk-17*"):
            if d.is_dir():
                shutil.move(str(d), str(JDK_DIR))
                break
        if not JDK_DIR.exists():
            # 兜底：直接把 tmp 内容搬为 jdk17
            shutil.move(str(short_tmp), str(JDK_DIR))
        else:
            shutil.rmtree(str(short_tmp))
    java_bin = JDK_DIR / "bin" / "java.exe"
    if not java_bin.exists():
        # 若目录结构不同，回退搜索
        for d in TOOLCHAIN.glob("**/bin/java.exe"):
            java_bin = d
            break
    print("[OK] JDK:", java_bin)

    # 2. Android cmdline-tools
    if not (CMDTOOLS_DIR / "bin" / "sdkmanager.bat").exists():
        download(CMDTOOLS_URL, CMDTOOLS_ZIP, "Android cmdline-tools")
        print("[解压] cmdline-tools ...")
        # 先解压到短路径，规避 Windows 260 字符路径限制
        short_tmp = TOOLCHAIN / "_tmp_cmdline"
        if short_tmp.exists():
            shutil.rmtree(str(short_tmp))
        with zipfile.ZipFile(CMDTOOLS_ZIP) as z:
            z.extractall(short_tmp)
        # 解压出的内部是 cmdline-tools 目录
        inner = short_tmp / "cmdline-tools"
        if inner.exists():
            CMDTOOLS_DIR.parent.mkdir(parents=True, exist_ok=True)
            if CMDTOOLS_DIR.exists():
                shutil.rmtree(str(CMDTOOLS_DIR))
            shutil.move(str(inner), str(CMDTOOLS_DIR))
            shutil.rmtree(str(short_tmp))
        else:
            # 兜底：把整个 tmp 内容搬过去
            CMDTOOLS_DIR.parent.mkdir(parents=True, exist_ok=True)
            for item in short_tmp.iterdir():
                shutil.move(str(item), str(CMDTOOLS_DIR.parent))
            shutil.rmtree(str(short_tmp))
    print("[OK] cmdline-tools")

    # 3. 安装 Android SDK 组件
    sdkmanager = CMDTOOLS_DIR / "bin" / "sdkmanager.bat"
    env = dict(os.environ)
    env["JAVA_HOME"] = str(JDK_DIR)
    print("[安装] Android SDK 组件 (platform + build-tools + NDK)...")
    print("       这一步会下载约 1-2GB，请耐心等待")
    sh([str(sdkmanager),
        "--sdk_root=" + str(SDK_DIR),
        "platforms;android-35",
        "build-tools;34.0.0",
        "platform-tools",
        "ndk;25.2.9519653"], env=env)
    print("[接受] Android SDK licenses (预写哈希文件，避免交互卡死)...")
    # 直接预写 license 哈希文件，绕开 sdkmanager 在 Windows 上的交互式 stdin 转发问题
    lic_dir = SDK_DIR / "licenses"
    lic_dir.mkdir(parents=True, exist_ok=True)
    _LICENSES = {
        "android-sdk-license": "24333f8a63b6825ea9c5514f83c2829b004d1fee",
        "android-sdk-preview-license": "d56f5187479451eabf01fb78af6dfcb131a6481e",
        "android-googletv-license": "601085b94cd77f0b54ff86406957099ebe79c4d6",
        "android-sdk-arm-dbt-license": "33b6a2b64607f11b759f320ef9dff4ae5c47d97a",
    }
    for name, h in _LICENSES.items():
        (lic_dir / name).write_text(h + "\n", encoding="ascii")
    print("       license 已预写:", ", ".join(_LICENSES))

    # 4. 安装 python-for-android 及其依赖
    #    注意：p4a pin 了 wheel~=0.43.0，该版本不支持 Python 3.13，
    #    导致 pip 直接排除 p4a（"from versions: none"）。解法：
    #    用 --no-deps 装 p4a，再单独装依赖（新版 wheel 替代 0.43）。
    print("[安装] python-for-android ...")
    P4A_URL = ("https://pypi.org/simple")
    ALIYUN = "https://mirrors.aliyun.com/pypi/simple/"
    try:
        sh([sys.executable, "-m", "pip", "install",
            "-i", P4A_URL, "--no-deps", "python-for-android==2026.5.9"])
    except subprocess.CalledProcessError:
        print("       p4a 已装或无需重装，继续")
    sh([sys.executable, "-m", "pip", "install",
        "-i", ALIYUN,
        "appdirs", "colorama", "jinja2", "sh", "meson", "ninja",
        "build", "toml", "packaging", "setuptools", "wheel",
        "cython<3", "kivy==2.3.1"])

    # 5. 编译 APK
    print("[编译] APK (arm64-v8a) ...")
    app_dir = BASE
    env = dict(os.environ)
    env["ANDROID_SDK_ROOT"] = str(SDK_DIR)
    env["ANDROID_NDK_HOME"] = str(SDK_DIR / "ndk" / "25.2.9519653")
    env["JAVA_HOME"] = str(JDK_DIR)
    env["ANDROID_HOME"] = str(SDK_DIR)
    DIST_DIR.mkdir(exist_ok=True)
    sh([sys.executable, "-m", "pythonforandroid.toolchain", "apk",
        "--bootstrap=sdl2",
        "--dist_name=pujiang_v0",
        "--name=PuJiangV0",
        "--version=0.1",
        "--package=org.pujiang.pujiang_v0",
        "--arch=arm64-v8a",
        "--android_api=35",
        "--requirements=python3,kivy==2.3.1",
        "--permission=",
        "--private=" + str(app_dir),
        "--orientation=portrait",
        "--release",
        "--output=" + str(DIST_DIR / "pujiang_v0-0.1-arm64-v8a.apk")],
       env=env)

    print()
    print("=" * 60)
    print(" 完成！APK 在:")
    print(" ", DIST_DIR / "pujiang_v0-0.1-arm64-v8a.apk")
    print("=" * 60)

if __name__ == "__main__":
    main()
