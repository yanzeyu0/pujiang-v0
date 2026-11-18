# V0 最小 Kivy APK —— 打包、装机、验证步骤

这一包只干一件事：验证 Kivy 原生界面能不能在你的鸿蒙 7 + 卓易通容器里跑起来。
不通就换 Flutter 鸿蒙原生，不用再往下写任何代码，避免白干。

源码位置（Windows）：
`C:\Users\Administrator\WorkBuddy\2026-11-18-09-04-22\pujiang-agent\v0-kivy-test\`

里面几个文件：`main.py`（界面）、`buildozer.spec`（打包配置）、`一键打包.bat`、`build_in_wsl.sh`（自动打包脚本）。

---

## 零、最省事的办法：两个脚本，按次序双击（推荐）

> 说明：你的 Windows 自带的是**旧版 WSL**，`wsl --install` 那条路（商店下载 + `--web-download` 参数）都走不通，会报"连接被重置"或"无效的分发名称"。所以已改成**离线安装**：微软直链下载安装包 + 本地安装，完全绕开商店和版本兼容问题。已验证三个下载地址国内可达。

**第一步 —— 装 WSL + Ubuntu（只需做一次）**

1. 找到 `v0-kivy-test\StepA_InstallWSL_Offline.bat`，**右键 -> 以管理员身份运行**。
2. 它会：启用 Windows 的 WSL 功能 -> 从微软直链下载 Ubuntu 离线包（约 500MB）和 WSL2 内核 -> 本地安装。全程不碰商店。
3. 跑完提示 `Ubuntu install DONE` 后：
   - **重启电脑**；
   - 重启后从开始菜单打开一次「Ubuntu 22.04」，设置 Linux 用户名和密码（只需这一次，输密码时屏幕不显示是正常的，直接输完回车）；
   - 看到命令行提示符就说明 Ubuntu 能用了。

**第二步 —— 编译 APK**

1. 找到 `v0-kivy-test\一键打包.bat`，**右键 -> 以管理员身份运行**。
2. 它检测到 Ubuntu 后全自动：装依赖 -> 编译 -> 把 APK 拷到上级 `pujiang-agent\` 目录。首次编译 20~50 分钟，耐心等。
3. 看到 `BUILD DONE` 就成了；中途报错把 **ERROR 那几行** 截图发我。

> Android SDK 走 `dl.google.com`，已验证可达，不是瓶颈。想手动一步步来 / 脚本出问题，再看下面第二节起的详细步骤。

---

## 一、为什么要在 WSL 里打包

Buildozer 只能在 Linux 下跑，Windows 本机不能直接编 APK。
用 Windows 自带的 WSL2（Ubuntu 22.04）就行，不用装虚拟机、不用买服务器。

---

## 二、装 WSL2（一次性，约 10 分钟）

1. 按 `Win` 键，输入 `powershell`，右键「以管理员身份运行」。
2. 粘贴执行：

```powershell
wsl --install -d Ubuntu-22.04
```

3. 重启电脑。重启后会自动弹出 Ubuntu 窗口，让你设 Linux 用户名和密码（随便设，跟 Windows 无关，记住即可）。
4. 如果没自动弹，管理员 PowerShell 里再执行一次 `wsl -d Ubuntu-22.04`。

---

## 三、在 Ubuntu 里装打包依赖（一次性，约 10 分钟）

在 Ubuntu 窗口里逐条执行（可以整段粘）：

```bash
sudo apt update
sudo apt upgrade -y
```

```bash
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
  autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
  libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
  build-essential
```

```bash
pip3 install --user --upgrade pip
pip3 install --user buildozer
pip3 install --user "Cython<3"
```

验证装好了：

```bash
~/.local/bin/buildozer --version
```

能打印版本号就 OK。（如果提示找不到命令，用 `python3 -m buildozer --version` 也行。）

---

## 四、把源码拷进 Ubuntu 并打包

**关键：不要直接在 `/mnt/c` 下编译**，跨文件系统又慢又容易出权限错。拷到 Linux 自己的家目录。

```bash
cp -r /mnt/c/Users/Administrator/WorkBuddy/2026-11-18-09-04-22/pujiang-agent/v0-kivy-test ~/pujiang_v0
cd ~/pujiang_v0
```

开始打包：

```bash
~/.local/bin/buildozer -v android debug
```

说明：

- 第一次打包要下载 Android SDK + NDK + Python-Android，约 1～2 GB，视网速 **20～50 分钟**，中途一堆日志是正常的。
- 如果卡在下载或报网络错，重跑同一条命令即可，已下载的部分会续用。
- 出现 `Build succeeded` 就成功。
- 以后改了 `main.py` 再打包，只需 2～5 分钟。

产物在：

```
~/pujiang_v0/bin/pujiang_v0-0.1-arm64-v8a-debug.apk
```

---

## 五、把 APK 弄回 Windows

在 Ubuntu 里：

```bash
cp ~/pujiang_v0/bin/*.apk /mnt/c/Users/Administrator/WorkBuddy/2026-11-18-09-04-22/pujiang-agent/
```

回到 Windows，文件在：

```
C:\Users\Administrator\WorkBuddy\2026-11-18-09-04-22\pujiang-agent\pujiang_v0-0.1-arm64-v8a-debug.apk
```

---

## 六、装进卓易通（鸿蒙 7 手机）

1. 把这个 APK 传到手机。三种方式任选：
   - 微信「文件传输助手」发给自己，手机上点开 -> 右上角「…」-> 用其他应用打开 -> 选「卓易通」。
   - USB 数据线拷到手机存储，用手机文件管理器找到 APK -> 打开方式选「卓易通」。
   - 已开 USB 调试的话，电脑 PowerShell 里 `adb install 完整路径\xxx.apk`（adb 需在卓易通里授权）。
2. 卓易通里会弹出安装确认，点安装。
3. 如果提示「未知来源」，去卓易通设置里允许安装外部 APK。
4. 装完桌面上出现「蒲江房产V0验证」图标，点开。

---

## 七、验证清单（逐项打勾，决定走不走 Kivy）

| 序号 | 看什么 | 通过标准 |
|---|---|---|
| 1 | 标题中文 | 显示「蒲江房产带看作战系统」，不是方块/乱码 |
| 2 | 色块 | 蓝、橙、绿三条色块清晰显示 |
| 3 | 触摸 | 点「点我验证」，下方状态变成 `[OK] 触摸正常 / 第 1 次…` |
| 4 | 输入 | 点输入框能弹键盘，改字后点按钮，状态里显示新文字 |
| 5 | 旋转 | 手机横过来竖过来，布局不重叠、不裁切 |
| 6 | 稳定性 | 反复开关 10 次，不黑屏不闪退 |

**6 项全过** -> 告诉我「V0 通过」，我立刻按 P0 -> P1 往下做。
**任何一项不过** -> 把不通过的现象原样告诉我（黑屏？中文方块？点按钮没反应？闪退？），顺手记一下卓易通的 Android 版本（卓易通设置里能看到），我据此决定是调 Kivy 兼容性还是直接改 Flutter 鸿蒙原生。

---

## 八、常见坑（遇到了照做）

- `buildozer: command not found` -> 用 `~/.local/bin/buildozer` 全路径，或 `python3 -m buildozer`。
- 报 `Cython` 相关编译错 -> 执行 `pip3 install --user "Cython<3"` 后重跑。
- 下载 SDK 卡住 -> 重跑 `buildozer -v android debug`，断点续传。
- 打包成功但安装失败 -> 确认 APK 是 `arm64-v8a` 版本，别用错架构。
- 打开就黑屏 -> 大概率是 OpenGL ES 兼容问题，记下现象即可，别自己折腾。
