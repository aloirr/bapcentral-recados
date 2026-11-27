# T-0037 — Farol de Fretes com edição na web: relato da sessão de tarefa

- **Sessão de tarefa:** https://claude.ai/code/session_01QvB2STi3xq4ykrr1HFRGBM (papel gerente-projetos, aberta pela sessão fixa).
- **Por que este arquivo:** o `send_message` à sessão fixa foi recusado ("só sessões do mesmo canal"), por isso o relato fica aqui.
- **Onde fica:** branch `gerente-projetos/T-0037-regras`, a mesma das RN-POS-007 a 010 no `03-regras.md`. Saiu da branch do engenheiro para manter um PR por dono.
- **Atualizado em:** 27/11/2026 (Manaus).

## Heads finais (prontos para PR; base f3c4569. O #147 só mexe no quadro)

| Branch | Head | Pareceres |
|---|---|---|
| `engenheiro-software/T-0037-desenho` | 0884880 | revisor-codigo: os 2 🟡 corrigidos (o relato saiu da branch; o contrato fala em líquido); corretor: RD-k corrigido |
| `modulo-farois/T-0037-fretes` | c53fc41 | revisor-codigo aprovado (o 🟢 de várias UFs foi feito); corretor: RD-j corrigido |
| `modulo-robo/T-0037-fretes` | 9175831 | revisor-codigo aprovado (o 🟢 de formatação foi feito) |
| `modulo-web/T-0037-fretes` | c8a2e32 | revisor-codigo, revisor-ux e design-de-marca aprovados; corretor: RD-f, RD-g e RD-h corrigidos |
| `testes/T-0037-fretes` | 43bb90a | revisor-codigo aprovado; corretor: RD-i corrigido |
| `gerente-projetos/T-0037-regras` | este commit | RN-POS-007 a 010 e este relato |

Rodada combinada dos 6 heads sobre o main:
- `compileall` OK;
- `pytest tests/`: 681 passam e 2 xpassed, sem falha;
- `pytest web/tests`: 411 passam (rodar separado do `tests/`, porque os dois têm um módulo `test_T0035_pacote_por_farol` com o mesmo nome);
- `smoke_processos`: só a falha conhecida [3];
- `smoke_relatorios`: o Fretes passa. Falham o DDR (falta a planilha de 11/2026; o main falha igual) e o [8] JANELAS (o ambiente não tem tkinter).

As correções dos achados ainda não passaram por uma segunda leitura do revisor-codigo e do corretor. São pequenas e estão listadas acima. Se o PR exigir parecer no head SHA, peça uma releitura rápida.

## Decisões (por delegação do po: "Aprove as telas e siga")

- **P1 A:** só o mês do pacote nas 4 abas.
- **P2 A:** o VLR FRETE (REAL) fica só no Farol de Entregas; o robô recusa o `frete_real` no Fretes.
- **P3 B:** o "% do faturado" passa a usar o faturado líquido de devolução. Na BAP inteira, NOV/26: 54,76% → 57,46%, pelas bases do repositório. MA: 90,5%.
- **P4 A:** o perfil `pos_venda` vê as 4 abas. Só o admin edita; o diretor vê só o Resumo.

## Pergunta em aberto

- **Futura (RN-GER-016):** tornar o `transportadoras_config.json` editável pela web? Só com o "autorizo" do Alexandre para esse arquivo. Na T-0037 ele é só lido.

## Pontos para o PR (gerente fixo)

- O `smoke_relatorios.py` regrava `RELATORIOS/painel_diretor_hist.json`, que é base congelada. O defeito é anterior à T-0037 e a correção fica com o testes. Depois de rodar o smoke, use `git restore`.
- O `docs/web/simulacoes/T-0037/sem-chave-cel.png` não mostra a mensagem, que fica abaixo da área visível. Ela aparece no `sem-chave-cel-inteira.png`.

- O DDR falha no `smoke_relatorios` porque falta a planilha de 11/2026; acontece igual no main. Incluir na lista de falhas conhecidas.
- Para depois (🟢):
  - um indício visual de que a grade do PC tem mais colunas (SLA e RESPONSÁVEL ficam no popup);
  - o logo e as fontes não carregam no PNG da simulação, porque ela abre por `file://` (`web/simular_*`). No site real estão certos.

## PNGs

Na branch `modulo-web/T-0037-fretes`, em `docs/web/simulacoes/T-0037/`:
- `resumo-pc.png` e `resumo-cel.png`;
- `notas-pc.png`, `notas-cel.png` e `notas-cel-inteira.png`;
- `editar-pc.png` e `editar-cel.png`;
- `sem-chave-pc.png`, `sem-chave-cel.png` e `sem-chave-cel-inteira.png`.

Todos em 1366 e 390 de largura, com deviceScaleFactor 2 e dados fictícios.
