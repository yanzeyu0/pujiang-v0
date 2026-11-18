# 用 GitHub Actions 云端编译 APK（替代本地 WSL）

你本地 WSL 装不上、Windows 又编不了 Kivy APK（python-for-android 依赖 sh 库，只支持 Linux）。所以改用 **GitHub 免费云服务器** 编译——你只需在网页上点几下，APK 自动编好并下载回来。

## 一句话原理

把代码推到 GitHub 仓库 → GitHub 的 Ubuntu 云服务器自动跑 buildozer 编出 APK → 你在网页上下载。

---

## 第一步：注册 GitHub（没有账号的话）

1. 打开 https://github.com 注册账号（邮箱 + 用户名 + 密码即可）。
2. 注册完登录。

> 如果你已经能打开 github.com 并能登录，跳过这步。

---

## 第二步：建仓库并上传代码（我帮你生成脚本，你双击就行）

我做了个 `上传到GitHub.bat`，它会自动把当前 `v0-kivy-test` 目录推到一个新仓库。但需要你先提供一个 **Personal Access Token**（相当于密码）。

**获取 Token：**

1. 登录 GitHub 后打开：https://github.com/settings/tokens
2. 点 **Generate new token (classic)**
3. Note 随便填，比如 `pujiang`；Expiration 选 90 天
4. 勾选 `repo` 和 `workflow` 两个权限
5. 拉到最下面点 **Generate token**
6. **复制那串 `ghp_` 开头的字符串**（只显示一次，务必复制保存）

---

## 第三步：运行上传脚本

1. 编辑 `上传到GitHub.bat`，把里面的 `你的GitHub用户名` 和 `你的Token` 换成你自己的。
2. 双击运行，等待提示上传完成。

---

## 第四步：触发编译 + 下载 APK

1. 打开你的仓库页面：`https://github.com/你的用户名/pujiang-v0`
2. 点顶部 **Actions** 标签
3. 左侧点 **Build V0 APK**，右侧点 **Run workflow** → **Run workflow**（绿色按钮）
4. 等它跑完（约 15~25 分钟，首次要下载 SDK/NDK）
5. 跑完后，在 Actions 页面底部 **Artifacts** 里点 **pujiang-v0-apk** 下载 zip
6. 解压得到 `pujiang_v0-0.1-arm64-v8a-debug.apk`

---

## 第五步：装进卓易通验证

APK 下载后，按 `README.md` 第六节装进卓易通，对照 6 项验证清单。

---

## 常见问题

- **打不开 github.com**：换浏览器、用手机热点、或稍后重试（网络抖动）。GitHub 在国内有时不稳。
- **Actions 没有 Run workflow 按钮**：确认仓库里 `.github/workflows/build-apk.yml` 文件存在（上传脚本会自动带上）。
- **编译失败**：把 Actions 里的报错日志截图发我。
- **Token 泄露/忘记**：去 settings/tokens 里删掉重建一个即可。
