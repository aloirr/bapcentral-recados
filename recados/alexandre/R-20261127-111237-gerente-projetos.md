---
id: R-20261127-111237-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: alta
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T11:12:37-04:00
---
# Passagem ao gerente que assumiu: estado desde a RETOMADA; esta sessão para

# Passagem para o gerente que assumiu (R-20261127-110804): o que mudou desde a RETOMADA das 10h51

Li o R-20261127-110804 e o R-20261127-111139-po. **Esta sessão (BapCentral-GP, na nuvem) para agora.** Não faço mais merge, não começo frente nova e a minha ronda está desligada. Os agentes que já estavam rodando terminam e só dão push nas branches abaixo, sem PR e sem merge.

## Entrou no main depois da RETOMADA (main 4d7c86d)
- #181: testes do Painel (66b0d95) e #182: web 0.10.1 (a86aa85). **T-0052 entregue** (R-20261127-105222); o /saude já dá 0.10.1.
- #178: RN-POS-011, com RN-POS-010 e as decisões P1 e P2 A (7f8d980).
- #179: desenho e contrato §10.9.7 da T-0054 (4d7c86d).

## Estado de cada frente (branch · SHA · o que falta)
- **T-0053** (aprovada pelo po; UX e marca ok):
  - código `modulo-farois/T-0053-cadastro-do-pedido` · **b4006e7**. Revisor de código sem 🔴 nem 🟡 no reteste. Fretes, Entregas, Devoluções e Saldo saem idênticos ao main; o escopo ficou só na família do Farol de Pedidos.
  - regras PR #180 · **3874b3a** (RN-GER-019 final).
  - Falta:
    - os testes `testes/T-0053-cadastro-do-pedido` (agente em curso, ainda sem push);
    - o corretor (agente em curso, parecer em `recados/anexos/T-0053/redundancias.md`);
    - depois, os PRs: #180 → testes → faróis.
- **T-0054** (aprovada pelo po; print final e marca ok):
  - robô `modulo-robo/T-0054-entregas-edicao` · **f0b895b**, aprovado pelo revisor;
  - web `modulo-web/T-0054-entregas-edicao` · c9feadb.
  - Falta, com o agente em curso: o merge do main (conflito de versão; a web vai como 0.12.0), "linha nova só do admin" no caminho do novo, com teste, e o RD-0255 (linhas em branco). Depois, o reteste do revisor e do corretor no head novo.
  - Testes `testes/T-0054-entregas-edicao`: agente em curso.
  - PRs: web → robô → testes.
- **T-0036:** PR #177 `testes/T-0036-testes-v2` · 102d879. O agente em curso faz o merge do main e passa a medir o pacote como o robô mede.
  - Robô #159 · c8209a1, com as colunas duplicadas corrigidas.
  - Falta: revisor do delta do robô → merge do #177 → update do #159 → merge.
- **T-0023:** testes `testes/T-0023-pc-so-leitura` (agente em curso). Código `modulo-farois/T-0023-pc-so-leitura` · 327a294, revisor com 0 🔴.
  - Falta o adendo no desenho, porque aceitei que o corpo de gravação foi apagado.
- **T-0056:** `engenheiro-software/T-0056-commit-maduro` · 9b2b35c. O CI fica vermelho até o testes ajustar `limite_1_commit_com_1h` e criar os 16 casos de `docs/desenho/T-0056.md`.
  - Depois: revisor → PR → "instale" do Alexandre.
- **T-0037:** igual à RETOMADA (web 0f941d5 · testes ccb7950 · contrato bcb5582 · faróis 94c6391 · robô 5d13276). Falta o merge do main no robô e nos faróis, mais as revisões finais.
- **T-0045:** aguarda a frase do Alexandre (R-20261127-102456).
- **Robô do notebook antigo** (o /saude ainda mostra 5 faróis): aguarda o ATUALIZAR_DO_GITHUB.bat e as 3 linhas do log (R-20261127-104041).
- **T-0055:** é a mesma do R-20261127-110732. A prioridade fica com o Alexandre (ver R-20261127-111139-po).

## Agentes desta sessão ainda rodando (só dão push, nada de PR nem merge)
- testes T-0036;
- testes T-0053;
- testes T-0023;
- testes T-0054;
- modulo-web T-0054;
- corretor T-0053.

Os pareceres vão para `recados/anexos/T-00xx/`. Antes de assumir cada frente, confira se a branch parou de mudar.
