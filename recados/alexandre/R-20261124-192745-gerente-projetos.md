---
id: R-20261124-192745-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0017
responde_a: R-20261124-192643-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T19:27:45-04:00
---
# Instale T-0017: pronto do lado do time; esperando o deploy v0.2.0 e a pasta compartilhada

Recebido o "instale". Situação às 19:30 (Manaus):
1. Deploy: /saude ainda responde versao 0.1.0. Falta o clique "Manual Deploy > Deploy latest commit" do Alexandre no Render (R-20261124-192615-gerente-projetos). A instalação só começa com /saude em 0.2.0.
2. Pasta: meu list_computer_folders está vazio. Assim que o Alexandre compartilhar "Regionais - Leandro" (app Claude no computador > Configurações > Claude Code > Remote Control) ela aparece aqui e eu peço o acesso; o Alexandre aprova o cartão.
3. Arquivos: os 3 não mudaram desde 73a8b4a (main c8a9267). SHA-256 completos para a conferência byte a byte:
   - bap_automation.py 2d12edcd283a6dade187a6ac493b08877d65b01f5ea777f2b9e928fc17b51a9b
   - bap_dados.py 52f764ff4d6e0d80cfce130f2622a1aed53bbc3acff918057e91ad761acba28f
   - relatorios_nucleo.py 7fc7ca395c9147b78b311bca317bd132977fb2884c078ce3557fbea771374a2a
4. Passos na pasta, quando conectada: criar SISTEMA BAP\BACKUP_RELATORIOS\ANTES_T0017_NOV2026 com cópia dos 3 arquivos atuais; copiar os 3 do main; conferir SHA-256 de cada um contra a lista acima; avisar por recado com os SHA lidos na pasta. Nenhum outro arquivo é tocado.
