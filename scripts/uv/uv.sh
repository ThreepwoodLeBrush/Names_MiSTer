#!/bin/bash

UV_DIR="$(cd "${0%/*}" && pwd)"
SCRIPTS_DIR="$(cd "${UV_DIR}/.." && pwd)"
BIN_DIR="$("${UV_DIR}/get_bin_dir.sh")"
export UV_PROJECT_ENVIRONMENT="$("${UV_DIR}/get_venv_dir.sh")"

"${BIN_DIR}/uv" --managed-python --project "${SCRIPTS_DIR}" "$@"
