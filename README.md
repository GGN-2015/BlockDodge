# BlockDodge

BlockDodge is now a pure Python version of the original WinForms game. It uses
`pygame` for the game window, drawing, keyboard input, and background music.

The player controls Texas on three lanes, dodging swords and collecting special
items until reaching the goal.

## Requirements

- Python 3.10 or newer
- `pygame==2.6.1`

Python 3.13 is supported. The included project was verified with Python 3.13.12.

## Install

Create and activate a virtual environment, then install the package:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -e .
```

On macOS or Linux:

```bash
python3 -m venv venv
./venv/bin/python -m pip install -e .
```

## Run

After installation:

```powershell
.\venv\Scripts\blockdodge.exe
```

Or run it as a module:

```powershell
.\venv\Scripts\python.exe -m blockdodge
```

On macOS or Linux:

```bash
./venv/bin/blockdodge
```

## Controls

- `W` or `Up`: move to the lane above
- `S` or `Down`: move to the lane below
- Mouse: click menu and game buttons

Movement only works after a mode has been selected and the game has started.

## Game Modes

- Level mode: uses the bundled `demo2.txt` track and `music.wav`.
- Random mode: generates a random track and uses `endless.wav`.

The game keeps the original main menu, help pages, status panel, pause/reset
buttons, rank window, item effects, scoring, and music timing as closely as
possible in a cross-platform Python implementation.

## Project Layout

```text
pyproject.toml
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

The package includes all runtime assets under `src/blockdodge/resources` and
track files under `src/blockdodge/config`.

Rank data is copied on first use to:

```text
~/.blockdodge/rank.txt
```

This keeps installed package files read-only while preserving player scores.

## Development Checks

```powershell
.\venv\Scripts\python.exe -m compileall src\blockdodge
```

For a quick import and startup check:

```powershell
$env:SDL_VIDEODRIVER='dummy'
$env:SDL_AUDIODRIVER='dummy'
.\venv\Scripts\python.exe -c "from blockdodge.app import BlockDodgeApp; import pygame; app=BlockDodgeApp(''); app.start_random_mode(); app.quit(); app._destroy_tk(); pygame.quit(); print('ok')"
```

## Migration Note

The old C#/.NET WinForms project files have been removed. This repository now
contains only the Python package and the runtime resources needed by that
package.
