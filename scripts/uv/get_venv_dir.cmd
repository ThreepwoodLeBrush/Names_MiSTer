@echo off
setlocal

for /F "usebackq delims=" %%D in (`cd "%~dp0" ^& cd`) do set "UV_DIR=%%~D"
for /F "usebackq delims=" %%D in (`cd "%UV_DIR%\.." ^& cd`) do set "SCRIPTS_DIR=%%~D"
for /F "usebackq delims=" %%D in (`"%UV_DIR%\get_arch.cmd"`) do set "UV_ARCH=%%~D"

echo %SCRIPTS_DIR%\.venv\%UV_ARCH%
