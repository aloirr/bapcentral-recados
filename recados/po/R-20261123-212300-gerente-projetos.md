---
id: R-20261123-212300-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0013
responde_a: R-20261123-210500-alexandre
encerra: false
contrato: null
criado_em: 2026-11-23T21:23:00-04:00
---
# Deploy v0.1.0 da BAP Central no Render: no ar

## O que foi feito
- Blueprint `bap-central` criado pelo navegador a partir do `render.yaml` do main (aloirr/bapcentral, branch main). Sync no commit 3623986.
- Serviço web `bap-central`: Python 3, plano Starter, gerenciado pelo Blueprint, disco de 1 GB criado. Build e deploy em 1 min 3 s, status Live.
- Endereço: https://bap-central.onrender.com
- Os 4 segredos foram digitados pelo Alexandre; o gerente-projetos não viu nem gravou nenhum valor.

## Conferência (23/11/2026, 21:20 Manaus)
- `/saude`: status ok, versão 0.1.0, hora_manaus 2026-11-23 21:20:55, tz America/Manaus, tz_ok true, telas_bloqueadas false, ultimo_pacote null (esperado: o robô ainda não mandou pacote).
- `/` redireciona para `/login`, título "Entrar · BAP AUTOPARTS".

## Pendências
1. **Segredos expostos em print:** os dois valores aleatórios gerados no PowerShell apareceram num print enviado na conversa. Recomendação feita ao Alexandre: trocar BAP_WEB_TOKEN (comando que grava o token novo direto no cofre do Windows e copia para a área de transferência) e SESSION_SECRET (botão Generate do Render), depois "Save, rebuild and deploy". Nenhum valor neste recado.
2. **Cofre do Windows no PC do robô:** senha do robô (serviço BAP_TOOLS) e endereço/token da web (serviço BAP_WEB, usuários `url` e `token`). Só o Alexandre faz.
3. **Instalação do bap_automation.py da T-0014 na produção:** aguarda o "instale" do Alexandre (backup ANTES_T0014_NOV2026 e conferência byte a byte).
4. Depois disso: primeiro pacote do robô e conferência do Painel na web contra o farol de origem.

## Como testar em 5 passos
1. Abrir https://bap-central.onrender.com/saude e ver `"status":"ok"` e `"tz_ok":true`.
2. Abrir https://bap-central.onrender.com e entrar com o usuário e a senha inicial de administrador.
3. Trocar a senha inicial quando a tela pedir.
4. Depois do cofre gravado e do robô instalado, rodar o robô e ver `ultimo_pacote` preenchido no `/saude`.
5. Abrir o Painel na web e comparar os números com o farol do PC.
