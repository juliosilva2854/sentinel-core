#!/bin/bash
source /etc/sentinel-core.env

if [ -z "$1" ]; then
    echo "Uso: sudo ./restore.sh <nome_do_arquivo.gpg>"
    exit 1
fi

ARQUIVO=$1
echo "🔓 Descriptografando..."
sudo gpg --batch --yes --passphrase "$GPG_PASSWORD" -d -o /tmp/restore.tar.gz "$ARQUIVO"

echo "📦 Restaurando arquivos..."
sudo tar -xzf /tmp/restore.tar.gz -C /

sudo rm /tmp/restore.tar.gz
echo "✅ Restauração concluída!"
