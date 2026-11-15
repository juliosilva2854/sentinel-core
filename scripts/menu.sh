#!/bin/bash

while true; do
    clear
    echo -e "\e[1;34m=========================================\e[0m"
    echo -e "\e[1;37m       🛡️  SENTINEL CORE - ADMIN MENU     \e[0m"
    echo -e "\e[1;34m=========================================\e[0m"
    echo -e "\e[1;32m1)\e[0m Ver status do Firewall (UFW)"
    echo -e "\e[1;32m2)\e[0m Ver IPs Banidos (Fail2ban)"
    echo -e "\e[1;32m3)\e[0m Ver logs de autenticação (SSH)"
    echo -e "\e[1;32m4)\e[0m Rodar Backup Manual"
    echo -e "\e[1;31m0)\e[0m Sair"
    echo -e "\e[1;34m=========================================\e[0m"
    read -p "Escolha uma opção: " opt

    case $opt in
        1) sudo ufw status verbose; read -p "Pressione Enter para continuar...";;
        2) sudo fail2ban-client status sshd; read -p "Pressione Enter para continuar...";;
        3) sudo tail -n 10 /var/log/auth.log; read -p "Pressione Enter para continuar...";;
        4) sudo ~/sentinel-core/scripts/backup.sh; read -p "Pressione Enter para continuar...";;
        0) echo "Saindo..."; exit;;
        *) echo -e "\e[1;31mOpção inválida!\e[0m"; sleep 1;;
    esac
done
