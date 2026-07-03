#!/bin/sh
set -e
 
if ! command -v ssh-keygen >/dev/null 2>&1; then
    apk add --no-cache openssh-keygen
fi
 
if ! command -v python3 >/dev/null 2>&1; then
    apk add --no-cache python3 py3-pip
    pip install --break-system-packages requests
fi
 
KEY_PATH="/data/keys/ssh_host_rsa_key"
 
mkdir -p /data/keys
 
if [ ! -f "$KEY_PATH" ]; then
    ssh-keygen -t rsa -b 4096 -f "$KEY_PATH" -N ""
fi
 
cp /auth_proxy.py /tmp/auth_proxy.py
chmod +x /tmp/auth_proxy.py
 
exec rclone serve sftp \
    --addr :2022 \
    --auth-proxy /tmp/auth_proxy.py \
    --key "$KEY_PATH" \
    --vfs-cache-mode off \
    --dir-cache-time 5s \
    -vv
 
