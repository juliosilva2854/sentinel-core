# Topologia da Rede

```mermaid
graph TD
    A[Kali Linux / Windows Attacker] -->|SSH Brute Force| B(UFW Firewall)
    B -->|Bloqueado| C{Fail2ban}
    C -->|Bane IP| D[Ubuntu Server 22.04]
    E[Windows Admin] -->|Chave SSH + Porta 2222| D
    D --> F[Dashboard Flask / Grafana]
    D --> G[Telegram Bot API]
    D --> H[Pastas Samba / ACLs]