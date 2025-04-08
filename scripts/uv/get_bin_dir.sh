#!/bin/bash

UV_DIR="$(cd "${0%/*}" && pwd)"
UV_VERSION="$(cat "${UV_DIR}/.uv-version")"
UV_ARCH="$("${UV_DIR}/get_arch.sh")"

echo "${UV_DIR}/${UV_VERSION}/${UV_ARCH}"
