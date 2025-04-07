@echo off
setlocal enabledelayedexpansion

rem # Please keep this script in sync with the corresponding Bash script.

cd "%~dp0.."

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

    if "!GIT_PUSH!" == "true" (
        echo git commit -m "BOT: Regenerated files."
        echo git push origin master
        for /F "usebackq delims=" %%s in (`git rev-parse --verify HEAD`) do set SHA=%%s
        echo.
        echo New files deployed ^(!SHA!^).
    ) else (
        set SHA=
    )

    call ".\scripts\generate_dbs.cmd" "!SHA!" || set "RETURN_CODE=!ERRORLEVEL!" && goto :ERROR

    if "!GIT_PUSH!" == "true" (
        echo.
        echo New dbs deployed.
    )
) else (
    echo Nothing to be updated.
)
goto :EOF


:ERROR
echo error: non-zero code (%RETURN_CODE%) returned by internal call.
exit /B %RETURN_CODE%
