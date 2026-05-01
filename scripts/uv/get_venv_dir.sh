#!/usr/bin/env bash

UV_DIR="$(cd "${0%/*}" && pwd)"
SCRIPTS_DIR="$(cd "${UV_DIR}/.." && pwd)"
UV_ARCH="$("${UV_DIR}/get_arch.sh")"

echo "${SCRIPTS_DIR}/.venv/${UV_ARCH}"
