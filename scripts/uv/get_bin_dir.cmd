@echo off
setlocal

for /F "usebackq delims=" %%D in (`cd "%~dp0" ^& cd`) do set "UV_DIR=%%~D"
for /F "usebackq delims=" %%D in (`type "%UV_DIR%\.uv-version"`) do set "UV_VERSION=%%~D"
for /F "usebackq delims=" %%D in (`"%UV_DIR%\get_arch.cmd"`) do set "UV_ARCH=%%~D"

echo %UV_DIR%\%UV_VERSION%\%UV_ARCH%
