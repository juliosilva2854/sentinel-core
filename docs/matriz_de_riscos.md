# Matriz de Riscos

| Ameaça | Probabilidade | Impacto | Mitigação Implementada |
| :--- | :--- | :--- | :--- |
| Força Bruta SSH | Alta | Alto | Fail2ban + SSH Key Auth |
| Acesso não autorizado a arquivos | Média | Alto | Samba ACLs + Permissões POSIX |
| Ransomware (Criptografia de dados) | Baixa | Crítico | Backup Imutável (Rclone + GPG) |
| Modificação de arquivos do sistema | Média | Alto | Monitoramento com AIDE e Auditd |
| Malware em arquivos compartilhados | Alta | Médio | ClamAV escaneando a pasta pública |