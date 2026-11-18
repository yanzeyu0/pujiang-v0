[app]
title = 蒲江房产V0验证
package.name = pujiang_v0
package.domain = org.pujiang

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,otf

version = 0.1
requirements = python3,kivy==2.3.1

orientation = portrait
fullscreen = 0

# V0 不联网，不申请任何权限
android.permissions =

# 只编 arm64，鸿蒙手机就是 arm64，能显著缩短首次编译时间
android.arch = arm64-v8a

# 安卓 5.0 起都能装，兼容卓易通容器
android.api = 35
android.minapi = 21

android.skip_update = False
android.accept_sdk_license = True

# 用 pip 安装的稳定版 p4a，不去 GitHub 拉 develop 分支（避免国内网络失败）
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 0
