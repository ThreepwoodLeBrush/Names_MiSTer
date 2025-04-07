@echo off
setlocal

for /F "usebackq delims=" %%D in (`cd "%~dp0" ^& cd`) do set "UV_DIR=%%~D"
for /F "usebackq delims=" %%D in (`cd "%UV_DIR%\.." ^& cd`) do set "SCRIPTS_DIR=%%~D"
for /F "usebackq delims=" %%D in (`"%UV_DIR%\get_bin_dir.cmd"`) do set "BIN_DIR=%%~D"
for /F "usebackq delims=" %%D in (`"%UV_DIR%\get_venv_dir.cmd"`) do set "UV_PROJECT_ENVIRONMENT=%%~D"

"%BIN_DIR%\uv.exe" --managed-python --project "%SCRIPTS_DIR%" %*
