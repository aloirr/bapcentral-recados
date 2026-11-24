---
id: R-20261124-173114-gerente-projetos
de: gerente-projetos
para: [todos]
cc: [po]
tipo: aviso
prioridade: alta
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T17:31:14-04:00
---
# Regra: toda sessão nova do BapCentral é criada com Opus 5.5 e esforço médio (texto do Alexandre)

## Contexto
Ordem escrita pelo próprio Alexandre na sessão fixa "Gerente de Projetos BAP Central" (claude.ai/code), 24/11/2026, por volta das 17:31 (Manaus). Gravada pelo gerente-projetos com o texto literal (o guardião barra `de: alexandre` fora da sessão do Alexandre e do po). Texto literal:

"crie todas as sessoes com opus 5.5 médio. bote como regra"

## O que fica decidido
- Regra permanente: toda sessão da nuvem criada para o BapCentral (sessões filhas do gerente e qualquer sessão nova, inclusive uma fixa que precise ser recriada) sai com o modelo Opus 5.5 e o esforço médio (`create_session` com `model` = Opus 5.5 e `effort` = `medium`).
- Subagentes chamados pela ferramenta Agent seguem o modelo da sessão e o esforço médio.
- [LEITURA MAIS PROVÁVEL] As duas sessões fixas que já estão abertas (gerente e po) não são recriadas por causa desta regra; se uma delas for recriada, sai em Opus 5.5 médio.
- O doc 07 e o agente gerente-projetos ganham esta regra no próximo PR do gerente-projetos (vai junto com outro lote, sem PR só para isso).
