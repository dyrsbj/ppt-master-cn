# PPT Master CN：Codex 安装与使用

> 完整的 Agent 对话安装提示词与手动安装说明请查看[仓库首页 README](../../README.md)。
>
> 本目录是 `ppt-master-cn` Skill 本体，包括 `SKILL.md`、`scripts/bootstrap.py`、中文规范以及测试。它能作为**单个 Skill 安装**，不需要再单独安装 `$ppt-master`。

## 先试试：直接让 Agent 帮你安装（首选）

无需先运行终端命令。在 **Codex / Claude Code / 其他有本地文件读写和命令执行权限的 Agent 对话框** 输入：

```text
帮我安装这个 Skill：https://github.com/dyrsbj/ppt-master-cn
```

如果 Agent 不清楚安装路径，可以使用更详细的指令：

```text
请帮我将 https://github.com/dyrsbj/ppt-master-cn 中的
skills/ppt-master-cn 安装到你当前 Agent 支持的个人 Skills 目录。
先阅读 README、SKILL.md 和 scripts/bootstrap.py，安装后运行
bootstrap.py 初始化官方引擎并执行 bootstrap.py --check 验证。
不需要额外安装 $ppt-master。完成后告诉我安装目录和验证结果；
没有文件系统或终端权限时请说明限制并给出手动操作命令。
```

需要 Node.js / Python 或授权时，Agent 应明确说明。**仅复制仓库不算完成**，首次引擎下载、依赖安装以及 `--check` 检查均须成功。不支持本地 Skills 或无法执行命令的普通网页聊天 Agent 不能代替用户在电脑上安装。

更完整的“一句话安装 / 推荐完整指令 / 命令行备用安装”见 [仓库首页 README](../../README.md)。

---

## 一、通过 npx 安装给 Codex（备用）

前提：Node.js（含 npx）、Python 3.10+（含 pip），首次初始化需能下载 GitHub Release。

在 **Windows PowerShell / macOS 或 Linux 终端**中执行（不是 Codex 对话框）：

```bash
npx skills add dyrsbj/ppt-master-cn --skill ppt-master-cn -a codex -g
```

参数说明：`--skill` 指定 Skill，`-a codex` 指定 Codex，`-g` 表示全局生效；如果只安装给当前项目，去掉 `-g`，在项目根目录运行。

## 二、初始化引擎（只需首次）

安装器版本不同时，实际安装位置可能是 `~/.agents/skills/ppt-master-cn` 或 `~/.codex/skills/ppt-master-cn`。以安装命令显示的路径为准。

### Windows PowerShell

```powershell
$skill = @(
  "$HOME\.agents\skills\ppt-master-cn",
  "$HOME\.codex\skills\ppt-master-cn"
) | Where-Object { Test-Path (Join-Path $_ "scripts\bootstrap.py") } | Select-Object -First 1
if (-not $skill) { throw "找不到 Skill，请检查上一步的安装输出。" }
py -3 (Join-Path $skill "scripts\bootstrap.py")
py -3 (Join-Path $skill "scripts\bootstrap.py") --check
```

### macOS / Linux

```bash
SKILL_DIR=""
for dir in "$HOME/.agents/skills/ppt-master-cn" "$HOME/.codex/skills/ppt-master-cn"; do
  if [ -f "$dir/scripts/bootstrap.py" ]; then SKILL_DIR="$dir"; break; fi
done
if [ -z "$SKILL_DIR" ]; then echo "找不到 Skill，请检查安装输出"; exit 1; fi
python3 "$SKILL_DIR/scripts/bootstrap.py"
python3 "$SKILL_DIR/scripts/bootstrap.py" --check
```

初始化会下载官方 PPT Master **v6.7.0** ZIP，校验 SHA-256、验证上游完整性并安装 Python 依赖。无需安装独立的 `$ppt-master` Skill。下载超时可先获取官方 ZIP，使用 `--archive <文件绝对路径>`。

## 三、在 Codex 使用

重启 Codex 或重新打开会话，输入：

```text
$ppt-master-cn
制作 10 页《企业 AI Agent 平台建设方案》PPT，中文、16:9、蓝白科技风。
文字、图表、架构图尽可能原生可编辑，禁止编造数据；
按官方工作流完成质量检查后输出 PPTX。
```

若 Codex 不显示该 Skill，核对安装目录下是否有 `SKILL.md`，确认没有多个同名安装副本，并重启 Codex。

## 四、更多说明

- **手动安装、不使用 npx**：[根 README 的手动安装章节](../../README.md#2-不用-npx手动安装)。
- **常见错误和离线安装**：[根 README 常见问题](../../README.md#3-常见问题)。
- **测试**：`python -m unittest discover -s skills/ppt-master-cn/tests -v`。
- **声明**：本 Skill 是非官方整合层，保留 Hugo He 官方 [PPT Master](https://github.com/hugohe3/ppt-master) 的 MIT 许可证、署名及完整性验证。初始化通过不代表已做 PPT 端到端生成测试。
