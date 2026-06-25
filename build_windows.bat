@echo off
setlocal

cd /d "%~dp0"

set "PYTHON_EXE=python"
if exist "%~dp0venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
)

echo [1/4] Using Python: %PYTHON_EXE%
"%PYTHON_EXE%" --version
if errorlevel 1 goto :error

echo [2/4] Installing package and build dependencies...
"%PYTHON_EXE%" -m pip install -e ".[build]"
if errorlevel 1 goto :error

echo [3/4] Cleaning previous build output...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist BlockDodge.spec del /q BlockDodge.spec

echo [4/4] Building single-file executable...
"%PYTHON_EXE%" -m PyInstaller ^
    --noconfirm ^
    --clean ^
    --onefile ^
    --windowed ^
    --name BlockDodge ^
    --collect-data blockdodge ^
    --hidden-import tkinter ^
    "%~dp0src\blockdodge\__main__.py"
if errorlevel 1 goto :error

echo.
echo Build completed: dist\BlockDodge.exe
exit /b 0

:error
echo.
echo Build failed.
exit /b 1
