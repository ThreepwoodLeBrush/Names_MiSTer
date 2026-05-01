#!/bin/bash

UV_DIR="$(cd "${0%/*}" && pwd)"

CPU_ARCH="$(uname -p)"
OS_KERNEL="$(uname -s)"

if [ "${OS_KERNEL,,}" = "linux" ]; then
    PLATFORM_SUFFIX="unknown-linux-gnu"
elif [ "${OS_KERNEL,,}" = "darwin" ]; then
    PLATFORM_SUFFIX="apple-darwin"
else
    >&2 echo "error: unrecognized OS kernel"
    exit 1
fi

echo "uv-${CPU_ARCH,,}-${PLATFORM_SUFFIX}"
