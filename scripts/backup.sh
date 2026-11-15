#!/bin/bash
source /etc/sentinel-core.env
DATA=$(date +%Y-%m-%d_%H-%M)
NOME_ARQUIVO="backup_sentinel_$DATA.tar.gz"
DIRETORIO_ALVO="/srv/sentinel"

echo "📦 Compactando $DIRETORIO_ALVO..."
sudo tar -czf /tmp/$NOME_ARQUIVO $DIRETORIO_ALVO 2>/dev/null

echo "🔐 Criptografando backup..."
sudo gpg --batch --yes --passphrase "$GPG_PASSWORD" -c /tmp/$NOME_ARQUIVO

sudo rm /tmp/$NOME_ARQUIVO
echo "✅ Backup gerado: /tmp/${NOME_ARQUIVO}.gpg"
