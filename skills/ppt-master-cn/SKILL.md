---
name: ppt-master-cn
description: 中文 Codex PowerPoint 制作 Skill。用于生成、修改、重建、模板化 PPTX，包括企业汇报、技术架构、培训和图表。首次自动安装官方 PPT Master v6.7.0 引擎，无需另装 $ppt-master。
---

# PPT Master CN — 单 Skill 入口

**路径规则**：使用 Codex 提供的本 SKILL.md 的绝对位置定义 CN_SKILL_DIR；不得猜测工作目录。官方运行时的绝对路径为 `CN_SKILL_DIR/vendor/ppt-master`（官方称 SKILL_DIR）。

## 初始化
1. 如果 `vendor/ppt-master/SKILL.md` 不存在，用 Python 3.10+ 执行 `python "<CN_SKILL_DIR>/scripts/bootstrap.py"`；首次需联网、下载固定版本和安装依赖。Windows 如没有 python 命令可用 `py -3`。
2. 如果安装失败，明确报告并停止，不得用简化的 PPT 脚本伪装为完成。
3. 如果已安装，执行 `python "<CN_SKILL_DIR>/scripts/bootstrap.py" --check`；失败就停止。

## 官方执行流程（强制）
1. 阅读 `<CN_SKILL_DIR>/vendor/ppt-master/SKILL.md`。
2. 立刻运行 `python "<CN_SKILL_DIR>/vendor/ppt-master/scripts/attribution_guard.py"`。非零即停止，不得修改、绕过或修复官方保护。
3. 依据官方 `workflows/routing.md` 选择唯一顶层 route 和 profile；严格加载该 route 的权威文档、依赖文件、规定步骤。
4. 尊重所有标为 BLOCKING 的用户确认节点，不得跳过；不提前进入后续阶段。
5. 只在官方路线允许的策划阶段阅读 `references/chinese-deck-quality.md` 并应用其中文企业汇报规范。如果与上游要求冲突，以上游为准。

## 内容质量
- 默认简体中文、16:9，但以用户指定模板和要求优先。
- 一页一个清晰任务，标题尽可能表达论断；架构图、业务流程、数据图表采用正确的视觉关系。
- 不伪造业绩、ROI、引用、研究或数据；需要的来源和假设标注清楚。
- 优先原生可编辑文本、形状、表格、图表；不把图片包装成可编辑对象来宣传。
- 勿擅自将内部文档、用户资料发往外部服务。

## 交付与验收
运行官方当前路线要求的 SVG 质量检查、PPTX 编译、交付验证。明确告知导出路径、页数、比例、可编辑性、检查结果及限制；失败时如实报告。

## 示例
`$ppt-master-cn 快速制作 8 页中文《企业 AI Agent 平台建设方案》，蓝白科技风，原生可编辑，禁止编造数据，完成质量检查后交付 PPTX。`

## Attribution
Original PPT Master: https://github.com/hugohe3/ppt-master ; Copyright (c) 2025–2026 Hugo He; MIT. 本 Skill 是第三方中文集成层，官方文件完整下载并保留 LICENSE、SPONSORS 和原始完整性检查。
