# T-0052 — parecer de marca (design-de-marca)

- Branch `modulo-web/T-0052-painel-cartoes`, head **2df92cd** (diff `web/app`, 4 arquivos).
- Base: `docs/marca/manual.md` §4 (paleta em tokens), §5 (tipografia), §7 (aplicações, BC3). Prints antes e depois (PC 1366 px e celular 390 px, dados fictícios) e `MEDICAO.md`.
- **Parecer: liberado com ajustes** (1 🟡, nenhum 🔴). Vale para o head 2df92cd.

## Achados

| ID | Onde | Tipo | Fere | Gravidade | Correção | Dono |
|---|---|---|---|---|---|---|
| 🟡 MC-0052-1 | `web/app/static/estilo.css:121` (`.rc-valor`) | tipografia | §5: "Número de destaque (faixa, cartão)" = **22 px / 700**; "o mesmo papel usa sempre o mesmo tamanho" | média (visível ao Diretor nos 8 cartões) | `font-size:1.5rem` (24 px, o tamanho do título da tela) → `font-size:1.375rem` (22 px). A regra é anterior à T-0052, mas agora vira o padrão dos 8 cartões; mudança de 1 linha, cabe no `.rc-topo` de 138 px | modulo-web |
| 🟢 MC-0052-2 | `estilo.css:119-120` (`.rc-rot` .8rem/700; `.rc-leg` .85rem) | tipografia | §5 (escala 11/12/14 e pesos) | baixa | Fora da escala, mas **anterior** à T-0052. Fica para a auditoria de consistência: `.rc-rot` → 11 px/600 maiúsculas +4%; `.rc-leg` → 12 px/400. Não segura este PR | modulo-web (depois) |
| 🟢 MC-0052-3 | `estilo.css:132` e `painel.html` (`.rc-faixa.vazia`) | cor | §4 | — | Conferido. A faixa vazia reservada herda o fundo `--c-e8f0e4` e o filete `--c-cfdccb` da faixa com dados: lê como parte do topo do cartão. **Nenhum hex novo** no diff; tokens já existentes. A classe `.vazia` não colide com `.rolagem-dados.vazia` (l. 599) | — |

## Conferido sem achado
- Cor: o valor grande em `--texto` sobre `--c-e8f0e4`, com contraste alto. Os anéis MTD e MÊS seguem com os tons de farol só no farol.
- Hierarquia: título → valor → legenda → faixa → gráfico, igual nos 8 cartões e nos 4 da Produtividade. A faixa e o gráfico começam na mesma altura em cada linha (MEDICAO.md).
- A faixa do BC3 continua com o degradê `--faixa-inicio` → `--faixa-fim` e o texto branco (§7). Agora leva só quando, DU e filtro. Tirar os números da faixa é decisão de produto (RD-0063), não de marca.
- Celular (390 px): o valor grande cabe ao lado dos anéis, sem corte.
