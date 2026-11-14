#!/bin/bash

# --- Variáveis de Cores ANSI ---
VERDE='\033[0;32m'
AZUL='\033[0;34m'
NC='\033[0m' # Sem Cor

# --- Variáveis do Backup ---
DATA=$(date +%Y-%m-%d_%H-%M)
NOME_ARQUIVO="backup_sentinel_$DATA.tar.gz"
DIRETORIO_ALVO="/srv/sentinel" # Onde estão as pastas do RH e Financeiro
SENHA_GPG="SenhaSuperSecretaDoBackup2026" # Em produção, use uma variável de ambiente!

echo -e "${AZUL}[ i ] Iniciando rotina de backup criptografado...${NC}"

# 1. Compacta a pasta
echo -e "${AZUL}[ i ] Compactando a pasta /srv/sentinel...${NC}"
sudo tar -czf /tmp/$NOME_ARQUIVO $DIRETORIO_ALVO 2>/dev/null

# 2. Criptografa o arquivo com GPG (Simula proteção contra Ransomware)
echo -e "${AZUL}[ i ] Criptografando o arquivo com GPG...${NC}"
sudo gpg --batch --yes --passphrase "$SENHA_GPG" -c /tmp/$NOME_ARQUIVO

# 3. Remove o arquivo não criptografado (Segurança)
sudo rm /tmp/$NOME_ARQUIVO

echo -e "${VERDE}[ ✔ ] Backup concluído com sucesso!${NC}"
echo -e "${VERDE}[ ✔ ] Arquivo gerado: /tmp/${NOME_ARQUIVO}.gpg${NC}"

# Simulação de envio para a nuvem (Rclone)
echo -e "${AZUL}[ i ] (Simulação) Enviando para a nuvem via Rclone...${NC}"
# rclone copy /tmp/${NOME_ARQUIVO}.gpg remote:backups/
