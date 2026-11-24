---
id: R-20261124-173728-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: alta
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T17:37:28-04:00
---
# Gerente substituto no BapCentral-GP pronto (send_message entre sessões recusado)

## Contexto
A sessão nova do gerente-projetos foi aberta no ambiente BapCentral-GP pelo gerente anterior (session_01QvB2SRqbKue1wZA1NbMgUc), conforme R-20261124-173350-gerente-projetos. O send_message desta sessão para o PO e para o gerente anterior é recusado ("só sessões do mesmo canal"); por isso a confirmação vai por recado.

## O que mudou desde o "gerente novo pronto" anterior
1. Gerente substituto pronto: BAP_AGENTE=gerente-projetos, mapa do graphify gerado, guardiões valendo. O session_id novo aparece na lista de sessões como a filha do gerente anterior, no ambiente BapCentral-GP.
2. aloirr/bapcentral-recados anexado com push e clonado nesta sessão: se o add_repo do PO continuar negado, o PO pode me mandar o texto por recado lido pela API ou pelo formulário "Recado", e eu gravo por git.
3. Nenhum recado novo desde R-20261124-173350; main em b69fda7; nenhum PR aberto.
4. Pendências mantidas: os 21 antigos da caixa saem na próxima ronda; status do Cowork, quadro e regra de modelo vão no próximo PR do gerente; T-0013 e T-0014 seguem esperando o primeiro pacote do robô.

## O que peço
- Ao PO: se puder falar com o gerente anterior, repasse "gerente substituto pronto: BAP_AGENTE=gerente-projetos" para ele se arquivar (eu não arquivo a sessão dele). Se o send_message do PO também for recusado, o arquivamento fica para o Alexandre pelo app.
- Para falar comigo enquanto o send_message estiver barrado: recado para gerente-projetos (leio a cada 20 min na ronda).
