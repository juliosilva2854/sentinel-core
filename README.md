# 🛡️ Sentinel Core - Secure Infrastructure & DevSecOps Lab

![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Shell Script](https://img.shields.io/badge/Shell_Script-121011?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Security](https://img.shields.io/badge/Security-Hardening-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=for-the-badge)

O **Sentinel Core** é um laboratório de infraestrutura corporativa focado em **DevSecOps**, automação e segurança defensiva. O projeto simula a implantação de um servidor Linux (Ubuntu Server) blindado, com serviços de rede essenciais e monitoramento centralizado via Web e ChatOps.

## 🎯 Objetivos do Projeto
- **Hardening:** Aplicação de CIS Benchmarks (SSH, Firewall UFW).
- **Defesa Ativa:** Fail2ban, monitoramento de integridade (AIDE) e antivírus (ClamAV).
- **Automação:** Instalação e configuração via scripts Bash idempotentes e Docker.
- **Observabilidade:** Dashboard interativo em Python/Flask e alertas em tempo real no Telegram.

## 🏗️ Arquitetura e Stack Tecnológica
- **Sistema Operacional:** Ubuntu Server 22.04 LTS
- **Serviços de Rede:** Samba 4 (AD DC), DNS/DHCP (dnsmasq)
- **Segurança:** UFW, Fail2ban, ClamAV, AIDE, Lynis, Trivy
- **Aplicações:** Python (Flask, psutil), Docker, Docker Compose
- **Integrações:** Telegram API, Rclone (Backup Criptografado)

## 📂 Estrutura do Repositório
```text
sentinel-core/
├── scripts/       # Scripts Bash de automação e Hardening
├── configs/       # Arquivos de configuração (sshd_config, jail.local, etc.)
├── dashboard/     # Aplicação Web (Flask) para gestão e monitoramento
├── bot/           # Bot de Telegram (ChatOps e Alertas)
├── docs/          # Documentação, Topologia e Matriz de Riscos
└── docker-compose.yml

🚀 Como Iniciar (Futuro)
(Instruções de deploy serão adicionadas na conclusão da fase de scripts)

Clone o repositório.

Execute o instalador mestre: sudo ./scripts/install.sh.

Autor: Julio Cesar - LinkedIn | GitHub