#!/usr/bin/env bash
# Copyright (c) 2021 José Manuel Barroso Galindo <theypsilon@gmail.com>

set -euo pipefail

export GIT_MERGE_AUTOEDIT=no
git config --global user.email "theypsilon@gmail.com"
git config --global user.name "The CI/CD Bot"

echo "Regenerating Names TXT files:"
echo
./scripts/generate_names_txt_files.py
echo
echo

echo "Regenerating Names CSV:"
echo
./scripts/generate_names_csv.py
echo
echo

git add names*

if ! git diff --staged --quiet --exit-code --ignore-space-at-eol ; then
    echo "There are changes to commit."
    echo
    git commit -m "BOT: Regenerated files."
    git push origin master
    echo
    echo "New files deployed."
else
    echo "Nothing to be updated."
fi
