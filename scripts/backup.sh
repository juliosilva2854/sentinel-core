#!/bin/bash

# --- Variáveis ---
DATA=$(date +%Y-%m-%d_%H-%M)
ARQUIVO_BACKUP="backup_sentinel_$DATA.tar.gz"
DIRETORIO_ALVO="/etc /var/www /home/compartilhado" # Pastas a serem salvas
SENHA_GPG="SenhaForteParaOBackup123" # Em produção, use variáveis de ambiente

echo "🔄 Iniciando rotina de backup..."

# 1. Compacta os arquivos
tar -czf /tmp/$ARQUIVO_BACKUP $DIRETORIO_ALVO 2>/dev/null

# 2. Criptografa o arquivo (Simula backup seguro contra Ransomware)
gpg --batch --yes --passphrase "$SENHA_GPG" -c /tmp/$ARQUIVO_BACKUP

# 3. Remove o arquivo não criptografado (segurança)
rm /tmp/$ARQUIVO_BACKUP

echo "✅ Backup concluído: /tmp/${ARQUIVO_BACKUP}.gpg"
echo "📤 (Simulação) Enviando para a nuvem via Rclone..."
# rclone copy /tmp/${ARQUIVO_BACKUP}.gpg remote:backups/