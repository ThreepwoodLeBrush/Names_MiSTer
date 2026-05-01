@echo off
setlocal enabledelayedexpansion

rem # Please keep this script in sync with the corresponding Bash script.

cd "%~dp0.."

echo Running mypy
rem # Switch to 'scripts' folder so mypy will find pyproject.toml
pushd .\scripts > nul
call .\uv\uv.cmd -q run -- python -m mypy .\ || set "RETURN_CODE=!ERRORLEVEL!" && goto :ERROR
popd > nul
echo.

set GIT_MERGE_AUTOEDIT=no

echo Regenerating Names TXT files:
echo.
call ".\scripts\generate_names_txt_files.cmd" || set "RETURN_CODE=!ERRORLEVEL!" && goto :ERROR
echo.
echo.

echo Regenerating Names CSV:
echo.
call ".\scripts\generate_names_csv.cmd" || set "RETURN_CODE=!ERRORLEVEL!" && goto :ERROR
echo.
echo.

git add names*

git diff --staged --quiet --exit-code --ignore-space-at-eol names*
if not "!ERRORLEVEL!" == "0" (
    echo There are changes to commit.
    echo.

    echo git commit -m "BOT: Regenerated files."
    echo git push origin master
    for /F "usebackq delims=" %%s in (`git rev-parse --verify HEAD`) do set SHA=%%s

    echo.
    echo New files deployed ^(!SHA!^).

    call ".\scripts\generate_dbs.cmd" "!SHA!" || set "RETURN_CODE=!ERRORLEVEL!" && goto :ERROR

    echo.
    echo New dbs deployed.
) else (
    echo Nothing to be updated.
)
goto :EOF


:ERROR
echo error: non-zero code (%RETURN_CODE%) returned by internal call.
exit /B %RETURN_CODE%
