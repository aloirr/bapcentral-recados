---
id: R-20261127-073205-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: pergunta
prioridade: normal
tarefa: T-0037
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T07:32:05-04:00
---
# Simulação v2 da T-0037 (Farol de Fretes) para aprovar por delegação

A simulação v2 da **T-0037** (Farol de Fretes no site, com a edição de "Notas com frete" só pelo admin) está pronta. Peço que aprove por delegação (R-20261127-013010-alexandre).

**Onde está:** `recados/anexos/T-0037/sim-v2/`, PC 1366 e celular 390, dados fictícios, servidor real; o `LEIAME.md` diz o que cada imagem mostra.
- 01 Resumo (no celular, também a 360 px)
- 02 a 05 abas Notas, Por UF, Por cidade, Por transportadora
- 06 popup da nota
- 07 edição pelo admin
- 08 farol da rota no celular, para mostrar que o âmbar de "atenção" continua

**O que o diretor e o gerente veem no Resumo:**
- **Cartões** iguais aos do PC.
- **Gráfico** de 12 meses na largura toda, nas cores do manual.
- **Tabelas** Por UF, Por cidade e Por transportadora do mês (NOV/26), com TOTAL. O total bate com o cartão "Notas com frete".
- **Duas frases curtas:** "<UF> concentra P% do valor das notas com frete." e "<transportadora> leva P% do valor."

**Mudanças que a revisão trouxe (informe ao Alexandre):**
- **"Sem transportadora" × "Sem acompanhamento":** o cartão "Sem transportadora" contava 1 e a tabela somava 2, porque juntava a nota sem acompanhamento. Agora a tabela separa a linha "Sem acompanhamento", e o cartão bate com a tabela. Isso vale também no PC.
- **Rótulos claros, no PC e no site:** "(sem)" virou "Sem UF", "Sem cidade / MA", "SERRA BONITA / Sem UF" e "Sem transportadora".
- **Gráfico:** saiu do azul, que não é cor do manual. O site agora só aceita cores do manual e traduz as cores antigas do PC.

**Critérios da delegação, conferidos:**
- dados fictícios;
- revisor-ux aprovado no reteste 2, sem 🔴 nem 🟡;
- marca dentro do parecer do revisor-ux: só tokens do manual;
- o número bate: TOTAL das 3 tabelas = cartões = aba Notas (9 notas, R$ 85.950, frete R$ 2.565);
- nas bases reais de NOV/26: BAP 54,76% → 57,46% (P3 B, % sobre o faturado líquido).

**Perfis:** admin edita; gerente, analista e pós-venda leem; diretor vê só o Resumo.

**Depois da aprovação:** os PRs na ordem testes → contrato → web 0.9.0 → faróis e robô na mesma janela. O robô e os faróis chegam ao PC pela rotina das 06h30 seguinte. Previsão: hoje à tarde.
