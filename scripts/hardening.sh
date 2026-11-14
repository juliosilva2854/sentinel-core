#!/bin/bash

# 1. Configuração do SSH
cp configs/sshd_config /etc/ssh/sshd_config
systemctl restart sshd

# 2. Configuração do Firewall (UFW)
ufw default deny incoming
ufw default allow outgoing
ufw allow 2222/tcp  # Nova porta do SSH
ufw allow 80/tcp    # HTTP (Para o Dashboard)
ufw allow 443/tcp   # HTTPS
ufw --force enable

# 3. Bloqueio de IPs maliciosos (Regra de exemplo)
# echo "deny 192.168.0.100" >> /etc/hosts.deny