# PPT Master CN for Codex

这是**单 Skill 安装的中文整合入口**。不需要另外安装 `$ppt-master`，首次运行自动下载官方 v6.7.0 完整 Skill 运行时到本目录 `vendor/ppt-master`。

### 安装
在项目根目录执行 `npx skills add dyrsbj/ppt-master-cn`，选择 Codex 和 `ppt-master-cn`。

或将本文件所在目录复制到：
- Windows：`%USERPROFILE%\.agents\skills\ppt-master-cn`
- macOS/Linux：`~/.agents/skills/ppt-master-cn`

首次初始化：
```bash
python3 ~/.agents/skills/ppt-master-cn/scripts/bootstrap.py
python3 ~/.agents/skills/ppt-master-cn/scripts/bootstrap.py --check
```
Windows PowerShell:
```powershell
py -3 "$HOME\.agents\skills\ppt-master-cn\scripts\bootstrap.py"
py -3 "$HOME\.agents\skills\ppt-master-cn\scripts\bootstrap.py" --check
```
首次需 Python 3.10+、GitHub 下载访问和 pip。亦可下载官方 ZIP 后 `python scripts/bootstrap.py --archive /path/to/ppt-master-skill-v6.7.0.zip`。此流程会严格核验 SHA-256 和作者完整性门禁。

### Codex
```text
$ppt-master-cn 快速制作12页中文企业AI平台汇报，16:9，蓝白科技风，图表和文字尽可能原生可编辑。
```

### 说明
**独立安装不等于完全离线嵌入。** 当前仓库提供独立 Skill 入口、下载器和中文规范，而不是把官方 22.5 MB 引擎直接提交到 Git。初始化后上游引擎驻留本 Skill 的 vendor 内，因此没有第二个 Skill 依赖。普通 PPT 工作流可能仍需用户授权的图片、模型等网络资源。

固定官方包：https://github.com/hugohe3/ppt-master/releases/tag/v6.7.0

官方引擎 Copyright (c) 2025–2026 Hugo He, MIT License；原作者权利和许可证保留。本整合不代表上游官方。通过 `python -m unittest discover -s skills/ppt-master-cn/tests -v` 运行无需网络的单元测试；真正的 PPT 生成端到端检验必须在安装依赖后执行。
