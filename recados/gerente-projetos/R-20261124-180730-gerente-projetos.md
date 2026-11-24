---
id: R-20261124-180730-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:07:30-04:00
---
# Parecer do designer-ux: Farol de Inadimplência, head 9211d8b — 🟢 pode mostrar

> Parecer do designer-ux (subagente do gerente-projetos; gravado pelo gerente sem alteração, pela limitação do --de no coord.mjs).

# Reteste de UX: T-0017, Farol de Inadimplência, simulação PC × site

- Revisor: designer-ux · 24/11/2026
- Branch `origin/modulo-web/T-0017-farois-web`, **head 9211d8b**. Substitui o parecer do head 0b00e43 e vale só para este head.
- Prints refeitos às 22:05 e conferidos:
  - sim-web-real-pc.png;
  - sim-web-real-am.png;
  - sim-web-real-cel.png, conferido inteiro, de cima a baixo (780×11758, em 7 trechos).

## Veredito: 🟢 Pode mostrar ao Alexandre. Nenhum 🔴 em aberto.

## Os 4 🔴 do parecer anterior: corrigidos e conferidos no print

**R1. Filtro de estado. ✔**
- O aviso agora diz "Cartões: AM. Resumo e gráficos: BAP inteira." (`render.py:139` e `:330`).
- O título do resumo virou "Resumo gerencial · BAP inteira" quando há filtro (`farol.html:31`).
- O selo some na BAP inteira.
- O R$ 92.893 do cartão e o R$ 400.388 do resumo agora aparecem cada um com o seu rótulo.

**R2. Cor dos cartões. ✔**
- "A vencer em 7 dias" e os itens `info` do resumo ficaram cinza, iguais ao PC (`estilo.css:69` e `:77`).
- O vermelho (Em atraso, Inadimplência, Acima de 90) e o verde (Recuperado) estão mantidos.

**R3. Gráficos dia a dia. ✔**
- A base das barras está alinhada, e os números dos dias aparecem inteiros.
- Conferido nos 3 gráficos dia a dia (Em atraso, Recebido, Vencido), a 390 px e a 1366 px (`estilo.css:89` e `:107`).

**R4. Nomes das filiais no celular. ✔**
- A 390 px, todos os nomes aparecem inteiros: SÃO LUIS, BELÉM, MANAUS, MATOGROSSO, BOA VISTA, SANTARÉM, MACAPÁ (`estilo.css:106`, `.gb-rotv` com 310 px).

**Extra A1. ✔**
- O Recuperado no filtro AM mostra "—" com "só na BAP inteira" (`render.py:140`).

## Conferência do celular inteiro (390 px)

- Topo, chips de estado (44 px), mini-barras nos cartões e resumo: legíveis.
- Semana a semana e mês a mês (Em atraso, Recebido, Vencido): rótulos e valores inteiros.
- Faixa de atraso: rótulos inteiros.
- Recuperado dia a dia: datas e valores inteiros.
- Em atraso por vendedor: legível.
- Nenhum texto cortado ou sobreposto.
- Nenhum dado pessoal: vendedores fictícios, sem cliente nem CNPJ.

## 🟡 Ficam para depois (não bloqueiam)

1. **Vazio abaixo das datas no "Recuperado dia a dia".**
   - A altura fixa de 310 px do `.gb-rotv` também vale para esse gráfico e para a faixa de atraso, e deixa uma faixa vazia abaixo das datas no celular.
   - Melhor deixar a altura acompanhar o tamanho do rótulo.
2. **Trilho do "Em atraso por vendedor" com comprimento variável.**
   - O trilho cinza muda de tamanho conforme a largura do valor (Vendedor 02 e 07, `estilo.css` `.hb-l`).
   - Fixar a largura da coluna do valor.
3. **Pendências do parecer anterior, sem mudança:**
   - A2: cartão diferente do Painel e do PC (faixa verde-clara + bolinha);
   - A3: buracos na grade dos cartões (2+1 / 3 na BAP inteira; 5+1 no AM);
   - A4: barra "A VENCER" vermelha na faixa de atraso;
   - A5: "MATOGROSSO" e "SÃO LUIS" sem espaço e acento (vêm do pacote do PC);
   - A6: resumo repete os cartões, e a data aparece duas vezes;
   - A7: página longa no celular (~5.900 px);
   - A8: mini-barras em ordens diferentes.

## Para a apresentação ao Alexandre

- Mostrar lado a lado: sim-pc-tela.png × sim-web-real-pc.png, depois sim-web-real-am.png, depois sim-web-real-cel.png.
- Vale perguntar a ele sobre a A2 (cartão igual ao do Painel) e a A3 (grade), que são decisão de layout.
