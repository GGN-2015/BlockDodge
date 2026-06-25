# BlockDodge

BlockDodge 是一个纯 Python / pygame 实现的三赛道躲避游戏。玩家控制德克萨斯在三条赛道之间移动，躲避飞来的剑，收集 BUFF，并尽量坚持到终点。

本项目改编自 [atoposyz/BlockDodge](https://github.com/atoposyz/BlockDodge)。原项目是 C# / WinForms 实现；当前仓库已经整理为纯 Python 包，并保留运行所需的图片、音频和关卡配置资源。

## 环境要求

- Python 3.10 或更高版本
- pygame 2.6.1

项目已在 Windows + Python 3.13.12 下验证。

## 使用 pip 安装

推荐先创建虚拟环境：

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
```

从当前源码目录安装：

```powershell
.\venv\Scripts\python.exe -m pip install -e .
```

如果只想按普通包方式安装当前目录，也可以使用：

```powershell
python -m pip install .
```

安装完成后会得到 `blockdodge` 命令。

也可以直接从 GitHub 安装当前项目：

```powershell
python -m pip install git+https://github.com/GGN-2015/BlockDodge.git
```

如果需要可编辑开发安装，先克隆仓库再安装：

```powershell
git clone https://github.com/GGN-2015/BlockDodge.git
cd BlockDodge
python -m pip install -e .
```

## 运行游戏

Windows：

```powershell
.\venv\Scripts\blockdodge.exe
```

也可以用模块方式运行：

```powershell
.\venv\Scripts\python.exe -m blockdodge
```

macOS / Linux：

```bash
python3 -m venv venv
./venv/bin/python -m pip install -e .
./venv/bin/blockdodge
```

## 操作方式

- `W` 或方向键 `↑`：移动到上一条赛道
- `S` 或方向键 `↓`：移动到下一条赛道
- 鼠标：点击菜单、开始、暂停、重置、排行榜、返回等按钮

选择模式并点击“开始游戏”后，键盘移动才会生效。

## 游戏模式

- 关卡模式：读取内置 `demo2.txt` 关卡配置，播放 `music.wav`。
- 随机模式：随机生成发射物轨道，播放 `endless.wav`。

游戏保留了原版的主菜单、帮助页、状态栏、排行榜窗口、道具效果、计分和 BGM 时机，并改为跨平台 Python 实现。

## Windows 打包为单个 exe

仓库提供了 Windows 批处理脚本：

```powershell
.\build_windows.bat
```

脚本会自动：

1. 优先使用当前目录的 `venv\Scripts\python.exe`，否则使用系统 `python`。
2. 执行 `pip install -e ".[build]"` 安装游戏和打包依赖。
3. 使用 PyInstaller 打包。
4. 生成单文件可执行程序：

```text
dist\BlockDodge.exe
```

如果希望手动安装打包依赖：

```powershell
.\venv\Scripts\python.exe -m pip install -e ".[build]"
```

## 项目结构

```text
pyproject.toml
build_windows.bat
src/blockdodge/
  app.py
  assets.py
  constants.py
  effects.py
  entities.py
  rank.py
  state.py
  transmitter.py
  ui.py
  config/
  resources/
```

运行资源位于 `src/blockdodge/resources`，关卡配置位于 `src/blockdodge/config`。

排行榜文件首次使用时会复制到用户目录：

```text
~/.blockdodge/rank.txt
```

这样可以避免修改安装目录中的包资源，同时保留玩家分数。

## 开发检查

语法检查：

```powershell
.\venv\Scripts\python.exe -m compileall src\blockdodge
```

无窗口启动检查：

```powershell
$env:SDL_VIDEODRIVER='dummy'
$env:SDL_AUDIODRIVER='dummy'
.\venv\Scripts\python.exe -c "from blockdodge.app import BlockDodgeApp; import pygame; app=BlockDodgeApp(''); app.start_random_mode(); app.quit(); app._destroy_tk(); pygame.quit(); print('ok')"
```
