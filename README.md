# PPT Master CN — Codex 中文整合版

**一个 Codex Skill，提供中文企业 PPT 工作流，并在首次使用时初始化完整的官方 PPT Master 生成引擎。**

- 技术来源：[hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)（固定 **v6.7.0**）
- 本仓库 Skill：[skills/ppt-master-cn/SKILL.md](skills/ppt-master-cn/SKILL.md)
- 中文排版规范：[chinese-deck-quality.md](skills/ppt-master-cn/references/chinese-deck-quality.md)
- 引擎初始化脚本：[bootstrap.py](skills/ppt-master-cn/scripts/bootstrap.py)
- 安装完**只需调用 `$ppt-master-cn`**，无需额外安装或单独调用官方 `$ppt-master`

## 1. 给 Codex 安装（推荐，全局生效）

以下步骤可用于 **Codex CLI / Codex 桌面端**。先在本机安装：

- [Node.js](https://nodejs.org/)（用于 `npx`）
- **Python 3.10 或更新版本**（需包含 pip）
- 能连接 GitHub，首次安装引擎时需要下载官方发行包

在终端确认：

```bash
node --version
npx --version
python --version
```

macOS/Linux 如果没有 `python` 命令，可运行 `python3 --version`；Windows 也可以用 `py -3 --version`。

### 第一步：安装 Skill

Windows 打开 **PowerShell**，macOS/Linux 打开 **Terminal**，执行：

```bash
npx skills add dyrsbj/ppt-master-cn --skill ppt-master-cn -a codex -g
```

这里：
- `--skill ppt-master-cn`：只选这个 Skill；
- `-a codex`：明确安装给 Codex；
- `-g`：按当前 `skills` CLI 的**全局安装**方式处理，让个人的多个项目可复用。

安装时如仍有交互提示，按照提示确认。**不要把该命令输入 Codex 对话框**：它是操作系统终端命令。

> 想只对当前项目生效？去掉 `-g`，并先进入那个项目的根目录再执行相同命令。该项目中的 Codex 才会看到这个 Skill。

### 第二步：首次初始化官方 PPT 生成引擎

**安装 Skill** 与 **下载引擎及 Python 依赖** 是两个步骤。Skill 已包含初始化程序，不需要安装第二个 Skill。

不同安装器/版本可能会把个人 Skill 放在 `~/.agents/skills/` 或 `~/.codex/skills/`。请先参考安装命令最终显示的路径；以下命令会自动查找这两个常见目录。

**Windows PowerShell**（整段复制执行）：

```powershell
$skill = @(
  "$HOME\.agents\skills\ppt-master-cn",
  "$HOME\.codex\skills\ppt-master-cn"
) | Where-Object { Test-Path (Join-Path $_ "scripts\bootstrap.py") } | Select-Object -First 1
if (-not $skill) { throw "找不到 ppt-master-cn；请查看上一步的安装输出并确认实际目录。" }

py -3 (Join-Path $skill "scripts\bootstrap.py")
py -3 (Join-Path $skill "scripts\bootstrap.py") --check
```

**macOS/Linux**（整段复制执行）：

```bash
SKILL_DIR=""
for dir in "$HOME/.agents/skills/ppt-master-cn" "$HOME/.codex/skills/ppt-master-cn"; do
  if [ -f "$dir/scripts/bootstrap.py" ]; then SKILL_DIR="$dir"; break; fi
done
if [ -z "$SKILL_DIR" ]; then
  echo "找不到 ppt-master-cn，请核对上一步显示的安装路径"; exit 1
fi

python3 "$SKILL_DIR/scripts/bootstrap.py"
python3 "$SKILL_DIR/scripts/bootstrap.py" --check
```

初始化器会做以下工作：
1. 下载 [官方 v6.7.0 Skill 发行包](https://github.com/hugohe3/ppt-master/releases/tag/v6.7.0)（约 22.5 MB）；
2. 校验固定的 SHA-256，解压到**本 Skill 自己的** `vendor/ppt-master/` 目录；
3. 执行上游要求的完整性和署名校验；
4. 使用当前 Python 环境的 pip 安装依赖，并验证引擎可用。

若第二条 `--check` 命令显示“上游引擎完整性验证通过”，表示**下载及完整性校验通过**；这不代表已经做过 PPT 实际导出测试。

> 如果你的 Python 因系统包管理策略禁止直接使用 pip，请先激活 Python 虚拟环境，再使用该环境的 Python 执行初始化脚本；依赖会安装到对应环境。

### 第三步：在 Codex 中使用

重新打开 Codex 或开启一个新会话，在聊天中输入：

```text
$ppt-master-cn

请做一份 10 页《企业 AI Agent 平台建设方案》PPT。
中文、16:9、蓝白科技风，面向管理层汇报。
图表、文字和架构图尽可能用原生可编辑元素，禁止编造数据。
按所选工作流执行质量检查，输出 PPTX。
```

如果 Skill 列表里看不到 `ppt-master-cn`，先确认安装路径下确实存在 `SKILL.md`，然后重启 Codex；若同时安装了项目级和全局同名 Skill，请只保留需要的那一份。

## 2. 不用 npx：手动安装

适合 Node.js 或 `npx` 不可用的场景。先克隆仓库：

```bash
git clone --depth 1 https://github.com/dyrsbj/ppt-master-cn.git
```

**Windows PowerShell**：

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills" | Out-Null
Copy-Item -Path ".\ppt-master-cn\skills\ppt-master-cn" -Destination "$HOME\.agents\skills\ppt-master-cn" -Recurse -Force
py -3 "$HOME\.agents\skills\ppt-master-cn\scripts\bootstrap.py"
py -3 "$HOME\.agents\skills\ppt-master-cn\scripts\bootstrap.py" --check
```

**macOS/Linux**：

```bash
mkdir -p "$HOME/.agents/skills"
cp -R ./ppt-master-cn/skills/ppt-master-cn "$HOME/.agents/skills/ppt-master-cn"
python3 "$HOME/.agents/skills/ppt-master-cn/scripts/bootstrap.py"
python3 "$HOME/.agents/skills/ppt-master-cn/scripts/bootstrap.py" --check
```

重新打开 Codex，即可使用 `$ppt-master-cn`。如果上述克隆命令在已存在的 `ppt-master-cn` 文件夹中失败，请选择一个新的空工作目录重试。

## 3. 常见问题

**Q：还要安装官方 `$ppt-master` 吗？**  
**不用。** 当前整合版在同一个 Skill 内下载并保留官方引擎。它仍依赖首次联网下载及 Python 第三方依赖，并不是完全离线的单文件程序。

**Q：遇到 `npx` / `node` 不存在？**  
先安装 Node.js，并重新打开终端。如果无法安装 Node.js，可按“手动安装”一节使用 Git。

**Q：找不到 `python` 或 pip？**  
安装 Python 3.10+，确保能运行 `py -3`（Windows）或 `python3`（macOS/Linux）。可用 `python -m pip --version` 检查 pip。

**Q：GitHub 下载超时或网络无法访问？**  
在能访问 GitHub Releases 的网络上下载官方 [`ppt-master-skill-v6.7.0.zip`](https://github.com/hugohe3/ppt-master/releases/download/v6.7.0/ppt-master-skill-v6.7.0.zip)，转移到本机，然后运行初始化脚本并附加 `--archive <压缩包绝对路径>` 参数。程序仍会校验 SHA-256，不能随意换成其他版本的 ZIP。

**Q：是否所有 PPT 对象都能原生编辑？**  
不保证。原生文本、图形和图表可编辑性取决于实际页面元素、上游转换支持及所选工作流；应在最终文件中检查，而非仅靠提示词承诺。

**Q：能否无须任何额外费用生成 PPT？**  
Skill 自身与 MIT 上游代码可以本地安装；但是某些图片生成、联网素材、TTS 或其他模型服务可能有费用/授权要求。按官方工作流及具体所选服务而定。

## 4. 开发与验证

无网络单元测试：

```bash
python -m unittest discover -s skills/ppt-master-cn/tests -v
```

真实的 PPT 生成端到端测试，仍需完成首次引擎初始化并运行实际制作请求；**单元测试不代表端到端生成已经验证**。

## 5. 版权与声明

官方项目：[hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)；Copyright (c) 2025–2026 Hugo He，MIT License。完整官方许可证与署名文件由初始化器保留，本项目不修改或绕过上游完整性保护。**PPT Master CN 是非官方的中文整合入口**。
