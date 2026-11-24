---
id: R-20261124-183034-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:30:34-04:00
---
# Parecer do designer-ux: PR #48 head 18d65d9 — 🟢

> Parecer do designer-ux (subagente do gerente-projetos; gravado pelo gerente sem alteração, pela limitação do --de no coord.mjs).

# Reteste de UX (3ª rodada): T-0017, PR #48, Farol de Inadimplência

- Revisor: designer-ux · 24/11/2026
- Branch `origin/modulo-web/T-0017-farois-web`, **head 18d65d9**. Substitui o parecer do head 9211d8b e vale só para este head.
- Prints das 22:28/22:29 conferidos:
  - sim-web-real-pc.png (1366 px);
  - sim-web-real-am.png (filtro AM);
  - sim-web-real-cel.png (390 px, conferido inteiro: 780×11886, em 7 trechos).
- Mudanças vindas do corretor-redundancias (RD-0003 e RD-0004):
  - `render.py:139-141`: aviso e texto de estado sem dado;
  - `render.py:322-333`;
  - `farol.html:9` e `:32`;
  - `_estados.html`: as barrinhas por estado agora são o mesmo componente do Painel.

## Veredito: 🟢 Pode mostrar ao Alexandre. O 🔴 1 continua resolvido.

## O 🔴 1: com o filtro AM, fica claro que o Resumo é da BAP inteira?

**Sim, e o texto pode ficar como está.** Motivos:
- O chip "AM" aceso já diz que os cartões são de AM. Repetir "Cartões: AM." no aviso era redundante; aceito o RD.
- "Resumo e gráficos: BAP inteira." fica entre o chip e os cartões. Quem filtra lê antes de chegar a qualquer número.
- A diferença entre o cartão (R$ 92.893) e o resumo (R$ 400.388) passa a ter explicação na tela.
- A 1366 px, aviso, cartões e o começo do resumo cabem na mesma tela.
- O selo no título do Resumo repetia o aviso. Pode sair.

**🟡 Opcional, sem repetição (para o corretor também aceitar), se o Alexandre achar o resumo longe do aviso no celular:**
- Com filtro de estado, trocar o título "Resumo gerencial" por **"Resumo da BAP inteira"**.
- Ao mesmo tempo, encurtar o aviso para **"Gráficos: BAP inteira."**
- Cada informação continua num lugar só, e o rótulo fica junto do número que ele explica.
- Não é pré-requisito para a apresentação.

## Os outros pontos da mudança

- **Estado sem nenhum recorte** (`render.py:322-325` e `:333`):
  - os cartões mostram "—" sem dica, e há um aviso só: "Sem números de UF neste pacote. Resumo e gráficos: BAP inteira.";
  - é correto e curto;
  - não há print desse caso: conferi só pelo código. 🟢
- **Dica por cartão só quando faltam alguns cartões:** no AM, só o "Recuperado no mês" mostra "—" e "só na BAP inteira". 🟢
- **"Baixado do ERP em 24/11/2026 17:52"** (`farol.html:9`), junto da faixa global "Dados de 24/11/2026 18:28 (horário de Manaus)":
  - agora são dois horários diferentes, do ERP e do pacote. Não é repetição, então 🟢;
  - 🟡 para depois: avaliar se o usuário precisa dos dois. O que ele usa para agir é a hora do ERP.
- **Barrinhas por estado nos cartões** (`_estados.html`, o mesmo componente do Painel): ganharam em consistência com o Painel.
  - 🟡 Os valores ficaram maiores e quase encostam entre si: "R$ 107,8 / R$ 111,1 / R$ 92,9", no celular e a 1366 px.
  - Ainda se leem, porque a quebra de linha mantém "mil" embaixo.
  - Para depois: um pouco mais de espaço entre as colunas dentro do cartão.

## Celular inteiro (390 px): sem regressão

- Topo, chips de 44 px, cartões e resumo: legíveis.
- Dia a dia (Em atraso, Recebido, Vencido): base alinhada, dias inteiros.
- Semana a semana e mês a mês: valores e rótulos inteiros.
- Faixa de atraso e Por filial: rótulos inteiros (SÃO LUIS ... MACAPÁ).
- Recuperado dia a dia e Em atraso por vendedor: legíveis.
- Nenhum texto cortado ou sobreposto. Nenhum dado pessoal.

## 🟡 Pendências que seguem para depois (sem mudança)

- Espaço vazio abaixo das datas no "Recuperado dia a dia" (`.gb-rotv` de 310 px).
- Trilho do "por vendedor" com comprimento variável.
- A2 a A8 do primeiro parecer:
  - cartão do farol diferente do `.rc` do Painel;
  - buracos na grade dos cartões;
  - barra "A VENCER" vermelha;
  - nomes de filial sem acento ou espaço;
  - resumo que repete os cartões;
  - página longa no celular;
  - ordem das barrinhas por estado.
