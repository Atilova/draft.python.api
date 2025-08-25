#!/bin/sh
set -e

is_secrets_found=false

for secret_file in /run/secrets/*.env; do
    if [ -f "$secret_file" ]; then
        echo "Loading environment from $secret_file"
        export $(grep -v '^#' "$secret_file" | xargs)
        is_secrets_found=true
    fi
done

if [ "$is_secrets_found" = false ]; then
    echo "No secrets found in /run/secrets/*.env"
fi

exec "$@"
