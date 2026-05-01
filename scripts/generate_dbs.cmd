@echo off
setlocal

for /F "usebackq delims=" %%D in (`cd "%~dp0" ^& cd`) do set "SCRIPTS_DIR=%%~D"

setlocal
rem # NOTE: uv unsets SCRIPTS_DIR
call "%SCRIPTS_DIR%\uv\uv.cmd" -q run -- python "%SCRIPTS_DIR%\generate_dbs.py" %*
endlocal
