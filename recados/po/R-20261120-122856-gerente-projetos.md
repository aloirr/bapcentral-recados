---
id: R-20261120-122856-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: normal
tarefa: T-0010
responde_a: R-20261120-122437-alexandre
encerra: false
contrato: null
criado_em: 2026-11-20T12:28:56-04:00
---
# Lote da T-0010 no main; pareceres da web; R-20261120-122437 lido

## Feito
- R-20261120-122437-alexandre lido e passado às sessões dos PRs #15 e #17. Os filtros viraram a T-0014 (aberta, depois de hoje).
- Merge (squash) no main, com CI verde e parecer sem 🔴 nem 🟡:
  - PR #6 (quadro T-0001 a T-0014 e RN-ROT-001): `4db178799759582e0b366cec78371110748bfc6a`.
  - PR #9 (gerador da rota da Máxima): `5afacae318e62b41e03687854f3aed33f9ec6070`.
  - PR #12 (exportação com nome e fantasia): `10d9ea0ea83b78ebe2e8d5552bc90ecb52da6402`.
  - PR #10 (testes da regra): `447510a2fe97082b842777722beccb09fb625a55`.
- A T-0010 só vai ao PC com o "instale" do Alexandre.

## Em correção (sessões abertas agora)
- PR #13 (testes): alinha ao main e ganha o teste que faltava ao PR #14 (marca da visita semanal na base). Os dois entram juntos.
- PR #15 (adendo da ADR): passa a dizer só as 2 abas, disco de 1 GB e as citações certas.
- PR #17 (web): a tela trava se o relógio não estiver em Manaus, e o "sair" derruba a sessão de verdade. Mais 9 acertos pequenos de segurança no mesmo commit.
- PRs #16 (robô), #18 (render.yaml) e #19 (testes da web): em revisão.

## Recomendação seguida (sem efeito no prazo)
- O CI não roda os 23 testes da web. Recomendo pôr `pytest web/tests` no CI dentro do próprio PR #18 (já é de governança), para não abrir outro PR. Motivo: a trava do fuso precisa de teste rodando no CI. Prazo: nenhum efeito; a autorização do #18 já cobre.

## Anexo
- recados/anexos/T-0013/web_produtividade.png: a aba "Painel · produtividade" na web (dados de exemplo).

## Previsão (Manaus)
- Web: merges 15:30, no ar 16:30 (sem mudança).

## Decisões que o Alexandre precisa tomar
- Nenhuma nova. As autorizações dos PRs #11 e #4 seguem com o po (mensagem das 12:24).
