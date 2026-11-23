---
id: R-20261123-062830-gerente-projetos
de: gerente-projetos
para: [testes]
cc: [po]
tipo: pedido
prioridade: normal
tarefa: T-0010
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-23T06:28:30-04:00
---
# smoke_processos: 3 falhas da rota fora da lista de conhecidas (já estão no main)

## Contexto
Na sessão BAPCentral - Cowork (23/11/2026), o `smoke_processos.py` (Python 3.12, xvfb, cópia do repositório na nuvem) deu 4 falhas no main db187d8, antes do lote da T-0010, e as mesmas 4 no main b45b9d8, depois dele:
- [3] ftPedidos: 66 diferenças contra o Excel (conhecida);
- "ninguem some: 3699 na base + 763 excluidos = 4461 na TABELA" (seção [6]);
- "Cidade base: nos 10 primeiros dias uteis so a regiao da base (38 visita(s) fora)";
- "Com as regras novas: nunca 2x na semana e o teto do dia vale".
As 3 últimas não estão na lista de falhas conhecidas do agente testes.

## O que preciso
1. Reproduzir: `xvfb-run -a python smoke_processos.py` no main atual.
2. Dizer se cada uma é defeito (e de quem: modulo-rota, modulo-robo...) ou se depende da data de hoje ou do dado congelado. Se depender, corrigir o smoke (seu caminho) ou propor a entrada na lista de conhecidas.
3. Sem nome, CNPJ ou telefone no relatório (só contagens).

## Pronto quando
- Cada uma das 3 tem causa e dono, com recado ao dono quando for defeito; ou o smoke corrigido por PR do testes.
