# 🛡️ Sentinel Core - Enterprise SIEM & DevSecOps Lab

![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Bash](https://img.shields.io/badge/Shell_Script-121011?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Security](https://img.shields.io/badge/Security-Hardening-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

O **Sentinel Core** é um laboratório de infraestrutura corporativa focado em **DevSecOps**, automação e segurança defensiva. O projeto simula a implantação de um servidor Linux (Ubuntu Server) blindado, atuando como um SIEM (Security Information and Event Management) para monitoramento de ameaças em tempo real.

## 🚀 Funcionalidades Principais

- **SOC Dashboard (Web):** Painel interativo em Python/Flask com métricas de CPU, RAM, Rede, Top Processos e Terminal de Logs em tempo real.
- **Hardening (CIS Benchmarks):** SSH restrito a chaves (porta 2222), bloqueio de root, Firewall UFW (Default Deny).
- **Defesa Ativa (IPS):** Fail2ban configurado para banir IPs após tentativas de força bruta.
- **Compartilhamento Seguro (Samba):** Estrutura de arquivos com Access-Based Enumeration (ABE) e permissões rigorosas (RH vs Financeiro).
- **Disaster Recovery:** Rotina de backup compactada e criptografada com GPG, e script de restauração em 1 comando.
- **Antivírus (ClamAV):** Proteção em tempo real na pasta compartilhada (com teste EICAR validado).

## 🏗️ Arquitetura do Projeto

```mermaid```
graph TD
    A["Atacante"] -->|"Ataque SSH"| B["Firewall UFW"]
    B -->|"Bloqueado"| C["Fail2ban"]
    C -->|"Bane IP"| D["Ubuntu Server"]
    E["Administrador"] -->|"Acesso Seguro"| D
    D --> F["Dashboard Web"]
    D --> G["Pastas Samba"]
    D --> H["Backup GPG"]

📂 Estrutura do Repositório
text
sentinel-core/
├── scripts/       # Automação Bash (Hardening, Backup, Restore)
├── dashboard/     # Aplicação Web (Flask, Chart.js, HTML/CSS)
├── configs/       # Arquivos de configuração (sshd_config, jail.local, smb.conf)
├── docs/          # Documentação e Diagramas
└── .github/       # CI/CD (GitHub Actions)
⚙️ Como Executar a Automação
Clone o repositório:

bash
git clone https://github.com/juliosilva2854/sentinel-core.git
cd sentinel-core
Dê permissão de execução aos scripts:

bash
chmod +x scripts/*.sh
Execute o instalador mestre (como root):

bash
sudo ./scripts/install.sh
Inicie o Dashboard (via Systemd):

bash
sudo systemctl start sentinel-dashboard
👨‍💻 Autor
Julio Cesar

LinkedIn

GitHub

Projeto desenvolvido para a disciplina de Sistemas Operacionais de Redes - UNINOVE.
