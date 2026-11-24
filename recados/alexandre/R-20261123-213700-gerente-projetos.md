---
id: R-20261123-213700-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0014
responde_a: R-20261123-213000-alexandre
encerra: false
contrato: null
criado_em: 2026-11-23T21:37:00-04:00
---
# T-0014: bap_automation.py instalado na produção; web de volta no ar com token novo

## Instalação (pasta "Regionais - Leandro")
- Backup: SISTEMA BAP\BACKUP_RELATORIOS\ANTES_T0014_NOV2026\bap_automation.py (361.095 bytes, SHA-256 10fc23f5…, conferido depois de gravado).
- Instalado: bap_automation.py do main 3623986 (375.368 bytes, SHA-256 5eac3409…), conferido byte a byte depois de gravado.
- O arquivo antigo era a versão da migração (99fc41c) com uma diferença local; o novo leva junto a T-0013 (passo 4f, envio do pacote para a web) e a T-0014 (visões por estado).
- Os 12 módulos que o robô importa já estavam iguais ao main (instalação da T-0010); nada mais foi trocado.

## Atenção
- A versão antiga tinha a senha do robô escrita no código (valor não citado aqui). A nova só lê do cofre do Windows (serviço BAP_TOOLS) ou da variável BAP_SENHA. Qualquer máquina que rode o robô sem o cofre gravado vai falhar no login.
- O cofre foi gravado pelo Alexandre no notebook desktop-prukjf6. No notebook que vai rodar o robô, o cofre precisa ser gravado de novo (está no prompt de instalação entregue ao Alexandre).
- Recomendação ao Alexandre: trocar a senha do robô no BAP Tools quando puder, porque ela ficou em texto aberto na pasta do OneDrive.

## Web
- Depois da troca dos segredos o deploy falhou uma vez (BAP_WEB_TOKEN vazio na primeira colagem). O Alexandre colou o token novo e o site voltou.
- /saude às 21:35 (Manaus): status ok, versão 0.1.0, tz_ok true, ultimo_pacote null.

## Como testar em 5 passos
1. No notebook do robô, rodar o instalar_bap.bat e gravar o cofre (prompt do Alexandre, passo 4).
2. Colar o token novo no BAP_WEB_TOKEN do Render e salvar.
3. Rodar o robô uma vez pelo atalho "Automacao BAP".
4. Ver no /saude o ultimo_pacote preenchido.
5. Abrir o Painel na web, escolher um estado e comparar com o farol do PC.
