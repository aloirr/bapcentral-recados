---
id: R-20261128-002739-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: status
prioridade: alta
tarefa: null
responde_a: R-20261128-002520-alexandre
encerra: false
contrato: null
criado_em: 2026-11-28T00:27:39-04:00
---
# PAUSA da BAP Central: estado final para retomar

Pedido: "pause o bap central e o catalogo. ACELERE 1000% o ERP." Não sai mais nada novo: nenhuma tarefa, PR, merge nem sessão. As sessões filhas foram paradas no ponto seguro e arquivadas. Do catálogo, nada estava rodando por este gerente.

## No ar / no main (seguro para a rotina das 06h30 de 28/11)
- **T-0060 lote 1, ENTREGUE no main:** #228, #231, #230, #234, #235, #229, #236, #223, #225, #233 e #226 (último 8118bd0). A rotina das 06h30 instala os .py, e o Executivo passa a projetar com hoje contando: no pacote de 27/11, 146.673 ÷ 18 × 19 ≈ R$ 154,8 mil. A web muda com o pacote do robô novo. Pareceres do revisor-codigo e do corretor-redundancias sem achado em aberto no head de cada PR; simulação aprovada pelo po (R-20261127-230959-po).
- **Entregues em 27/11:** T-0055, T-0053, T-0054, T-0056, T-0023, T-0036, T-0045 lotes 1 e 2, T-0057, T-0058, T-0013, T-0014, a T-0059 regra (#218, #219, #222, #227) e o quadro (#232).
- **Web no ar:** 0.16.0. O deploy é automático no merge (R-20261127-235921-alexandre).
- **T-0045:** a senha da Máxima foi preenchida no Render (R-20261128-001639-alexandre). O cron roda das 06h00 às 21h50. A agenda e o diagnóstico seguem desligados até o ok do Alexandre no site.

## Ficou no meio (nada pela metade no main)
- **T-0037 (Farol de Fretes):** o #204 (robô) está no main e vai para o PC às 06h30. Ficaram abertos:
  - o #205 (web, head 0a11b00, ainda 0.15.0, a renumerar para 0.17.0);
  - o #169 (testes estritos, head 279a65f, vermelho até o #205 entrar).
- **T-0060 lote 2:** peças e cadastros do Metas até ontem; corte do Espelho (TMA, jornada, 1.074 × 990); conversão 8,2 × 9%; DU parcial das visitas; TOP 30; "mês fechado" do Executivo e da parcial; real linha a linha no PDF da parcial com as colunas de RV de volta; os 🟢 de docstring; e quem grava RELATORIOS/painel_diretor_hist.json na suíte. A **T-0048** entra junto.
- **T-0059 parte 2** (telas da web na regra 12, com as decisões 49 e 50), com a T-0046 e a T-0047 junto. Também a **T-0050** (decisão 69).
- **Migração** (T-0025, T-0038 a T-0044) e **T-0049**: datas do R-20261127-194317 e do quadro (#232). Todas passam a contar a partir da retomada.
- **Nota no ADR 0001** ("aprovo deploy" substituído pelo deploy automático), do engenheiro-software.
- **A conferir:** T-0051, os PRs antigos da T-0025 (#93, #98, #100, #107) e as entregas da T-0045 lote 1 e da T-0056.
- **Backlog do Alexandre (R-20261128-001535):** rodar o conferir_pedidos.py.

## Para retomar
1. O Alexandre escreve "retome a BAP Central".
2. Eu confiro o /saude: o lote novo depois das 06h30 e o cron das visitas.
3. Primeiro a T-0037: o #205 traz o main, passa a 0.17.0 e recebe os pareceres; depois o #169.
4. Depois, em 2 frentes: T-0059 parte 2 + T-0050 (web) e T-0060 lote 2 + T-0048 (faróis).
5. Por último, a migração, com as datas refeitas a partir do dia da retomada.
