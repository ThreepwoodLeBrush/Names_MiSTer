@echo off
setlocal

set SCRIPTS_DIR=%~dp0
set SCRIPTS_DIR=%SCRIPTS_DIR:~0,-1%

setlocal
rem # NOTE: uv unsets SCRIPTS_DIR
call "%SCRIPTS_DIR%\uv\uv.cmd" -q run -- python "%SCRIPTS_DIR%\generate_dbs.py" %*
endlocal
