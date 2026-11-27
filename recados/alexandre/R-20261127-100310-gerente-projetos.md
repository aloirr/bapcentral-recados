---
id: R-20261127-100310-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0054
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:03:10-04:00
---
# T-0054: edição no Farol de Entregas, plano e previsão

**T-0054:** edição no Farol de Entregas do site. Recebi o R-20261127-100158-alexandre.

**Plano** (o mesmo modelo do Farol de Pedidos e do Fretes: a tela no site; o robô do PC grava só acrescentando linha, regra 7):
1. **Desenho** (engenheiro-software, já começou):
   - inventário das edições que o pós-venda faz hoje no Farol de Entregas do PC (campos, quem pode, onde grava);
   - o que a web reaproveita do `/editar` e da fila que já existem;
   - o acréscimo no contrato;
   - a regra.
2. **Regras:** RN nova, se precisar. Eu escrevo no 03-regras.
3. **Web** (modulo-web, 0.12.0): a edição no Farol de Entregas, no PC e no celular. Simulação antes, em PNG, a 1366 px e 390 px, com dados fictícios, para você aprovar por delegação.
4. **Robô** (modulo-robo): ler a fila e gravar no `_EDICOES_POS_VENDA`, só acrescentando linha.
5. **Testes:** condicionais primeiro e obrigatórios depois, para o CI ficar verde em qualquer ordem de PR.

Revisões de código, UX, marca e redundância antes de cada merge, como sempre.

**Previsão:**
- desenho até umas 11h30 de Manaus;
- simulação para você até umas 14h;
- no ar no site no fim da tarde de hoje, se a simulação for aprovada sem voltas;
- a gravação pelo robô começa quando o robô novo for instalado no PC (rotina das 06h30, regra 11), ou seja, amanhã cedo.

**Perguntas ao Alexandre:** se aparecer alguma, vai com a recomendação e o padrão adotado, sem travar.
