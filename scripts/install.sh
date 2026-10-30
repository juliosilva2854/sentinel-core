#!/bin/bash

# --- Variáveis de Cores ANSI ---
VERDE='\033[0;32m'
VERMELHO='\033[0;31m'
AZUL='\033[0;34m'
AMARELO='\033[0;33m'
NC='\033[0m' # Sem Cor

# --- Banner Inicial ---
clear
echo -e "${AZUL}"
cat << "EOF"
=============================================================
   🛡️  SENTINEL CORE - SECURE INFRASTRUCTURE DEPLOYMENT 🛡️
=============================================================
EOF
echo -e "${NC}"

# --- Funções de Log ---
log_info() { echo -e "[ ${AZUL}i${NC} ] $1"; }
log_ok()   { echo -e "[ ${VERDE}✔${NC} ] $1"; }
log_erro() { echo -e "[ ${VERMELHO}✖${NC} ] $1"; }

# --- Verifica se é root ---
if [ "$EUID" -ne 0 ]; then 
  log_erro "Por favor, execute este script como root (sudo ./install.sh)"
  exit 1
fi

log_info "Iniciando atualização do sistema..."
apt-get update -y && apt-get upgrade -y
log_ok "Sistema atualizado."

log_info "Instalando pacotes essenciais (UFW, Fail2ban, Samba, ClamAV)..."
apt-get install -y ufw fail2ban samba clamav auditd lynis
log_ok "Pacotes base instalados."

log_info "Aplicando Hardening de SSH e Firewall..."
# Chama o script secundário de hardening
bash scripts/hardening.sh
log_ok "Hardening aplicado."

log_info "Configurando Fail2ban..."
# Copia a configuração customizada
cp configs/jail.local /etc/fail2ban/jail.local
systemctl restart fail2ban
log_ok "Fail2ban ativo e monitorando."

echo -e "\n${VERDE}=============================================================${NC}"
echo -e "${VERDE}   ✅ SENTINEL CORE PRONTO E BLINDADO PARA OPERAÇÃO! ✅${NC}"
echo -e "${VERDE}=============================================================${NC}"