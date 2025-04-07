#!/usr/bin/env bash
# Copyright (c) 2021 José Manuel Barroso Galindo <theypsilon@gmail.com>

set -euo pipefail

pushd "${0%/*}/.." > /dev/null

export GIT_MERGE_AUTOEDIT=no

echo "Regenerating Names TXT files:"
echo
./scripts/generate_names_txt_files.sh
echo
echo

echo "Regenerating Names CSV:"
echo
./scripts/generate_names_csv.sh
echo
echo

git add names*

if ! git diff --staged --quiet --exit-code --ignore-space-at-eol names*; then
    echo "There are changes to commit."
    echo

    if [[ "$GIT_PUSH" == "true" ]]; then
        git commit -m "BOT: Regenerated files."
        git push origin master
        SHA=$(git rev-parse --verify HEAD)
        echo
        echo "New files deployed (${SHA})."
    else
        SHA=
    fi

    ./scripts/generate_dbs.sh "${SHA}"

    if [[ "$GIT_PUSH" == "true" ]]; then
        echo
        echo "New dbs deployed."
    fi
else
    echo "Nothing to be updated."
fi

popd > /dev/null