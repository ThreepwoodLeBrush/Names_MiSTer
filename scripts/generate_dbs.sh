#!/usr/bin/env bash

SCRIPT_DIR="$(cd "${0%/*}" && pwd)"

"${SCRIPT_DIR}/uv/uv.sh" -q run -- python3 "${SCRIPT_DIR}/generate_dbs.py" "$@"
