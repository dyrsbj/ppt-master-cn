# PPT Master CN — Codex 中文整合版

**一个 Codex Skill，提供中文企业 PPT 工作流并自动安装完整的官方 PPT Master 引擎。** 无须额外安装或单独调用 `$ppt-master`。

- Skill 入口：[`skills/ppt-master-cn/SKILL.md`](skills/ppt-master-cn/SKILL.md)
- 中文使用说明：[`skills/ppt-master-cn/README.md`](skills/ppt-master-cn/README.md)
- 中文内容与设计规范：[`skills/ppt-master-cn/references/chinese-deck-quality.md`](skills/ppt-master-cn/references/chinese-deck-quality.md)
- 固定上游版本：**v6.7.0**；下载完整官方 skill-only ZIP，并对照发布页 SHA-256 校验；不修改上游源码、署名及完整性校验。

## 一键安装（推荐）

在本机安装 Node.js 后：

```bash
npx skills add dyrsbj/ppt-master-cn
```

选择 `ppt-master-cn` 与 Codex。首次执行时：

```bash
python3 ~/.agents/skills/ppt-master-cn/scripts/bootstrap.py
```

Windows PowerShell：

```powershell
py -3 "$HOME\.agents\skills\ppt-master-cn\scripts\bootstrap.py"
```

之后在 Codex 使用：

```text
$ppt-master-cn 快速制作 12 页《企业 AI Agent 落地方案》，16:9，中文蓝白科技风，优先原生可编辑，并完成官方质量检查。
```

**独立安装 ≠ 离线内嵌**：仓库存放 Skill 与校验过的初始化器，首次运行下载约 22.5 MB 的官方发行 ZIP 并安装 Python 依赖；原生引擎保存到本 Skill 自身的 `vendor/ppt-master/`，无第二个 Skill 依赖。离线环境可先手动下载同一官方 ZIP，通过 `--archive` 安装，仍做校验。

## 开发与验证

```bash
python -m unittest discover -s skills/ppt-master-cn/tests -v
```

完整 PPT 生成端到端测试须在本地安装上游引擎及其依赖后执行。本仓库的无网络单元测试不冒充端到端通过。

## 原项目与版权

底层 PPT Master：<https://github.com/hugohe3/ppt-master>，Copyright (c) 2025–2026 Hugo He，MIT License。完整官方 LICENSE 与 SPONSORS 文件由初始化器保留在下载的运行时目录。本项目是独立中文整合入口，不代表官方发行。
