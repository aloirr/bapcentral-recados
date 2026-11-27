---
id: R-20261127-094034-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: normal
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T09:40:34-04:00
---
# T-0052: Painel Executivo, plano e previsão

T-0052 aberta: Painel Executivo no site, com o valor grande em todos os cartões e os cartões no mesmo padrão e nível. Recebi o R-20261127-093750-alexandre.

**Causa provável, achada no código:**
- Os 3 primeiros cartões de cada aba (Faturamento Líquido, Positivação e Pedidos Faturados, na aba Resultado) mandam o valor grande para a faixa do topo da página e tiram o valor do cartão.
- Foi uma escolha antiga contra número repetido (RD-0063). Por isso o cartão parece "em branco".
- Os desníveis vêm da linha de legenda, que só alguns cartões têm (ex.: "projeção do mês" no Faturamento de Peças). Ela empurra a faixa de comparação e o gráfico para baixo.

**O que vai mudar (modulo-web, já trabalhando):**
- o valor grande volta para todos os cartões, no PC e no celular, nas abas Resultado e Produtividade;
- a mesma estrutura em todos: título, valor, legenda, faixa de comparação e gráfico, com cada parte na mesma altura entre os cartões da linha;
- o número não aparece duas vezes na tela. A faixa do topo deixa de repetir os 3 números, ou o time explica a escolha na simulação;
- nenhum número é recalculado: o valor continua vindo pronto do PC, o mesmo do farol de origem.

**Simulação antes do PR (regra 10):** PNG antes e depois, a 1366 px e a 390 px, com dados fictícios e a medição das alturas. Mando para você aprovar por delegação, depois do revisor-ux e do design-de-marca.

**Previsão:** a simulação em 1h30, até umas 11h15 de Manaus. Com a sua aprovação, o PR e o merge saem em mais 1 h, e o site já fica no ar.

Os outros trabalhos seguem em paralelo: T-0050 (PRs #173 a #175), T-0037 (testes prontos, falta uma decisão de marca sobre uma cor), T-0023, T-0036 e T-0045.
