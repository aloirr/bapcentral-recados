---
id: R-20261127-131307-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0054
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T13:13:07-04:00
---
# T-0054 entregue: edição do Farol de Entregas no site (web 0.14.0)

**No main:** #179 (desenho, 4d7c86d), #190 (web 0.14.0, dba9963), #191 (robô, 50475d0), #194 (testes, b4c92ab). Revisor de código, corretor, UX e marca aprovados no head final; CI verde. /saude mostra 0.14.0.

**O que é (RN-POS-011):** nas abas Entregas e Pendências dos meses anteriores, o admin e o pós-venda editam ETAPA, TRANSPORTADORA, DT. PREVISTA, DT. REAL, RESPONSÁVEL e VLR FRETE (REAL), com as listas e datas do PC. O gerente vê sem editar (P1 A). O pós-venda também edita "Notas com frete" do Fretes (P2 A, quando a T-0037 entrar). O robô grava no PC só acrescentando no _EDICOES_POS_VENDA (regra 7).

**Como testar em 5 passos:**
1. Antes: o robô do notebook precisa estar atualizado (ATUALIZAR_DO_GITHUB.bat; hoje ele manda só 5 faróis). Sem isso, o botão "Editar" não aparece.
2. Entrar no site como admin ou pós-venda e abrir o Farol de Entregas: aparece "Editar" nas linhas.
3. Editar uma nota (ex.: DT. REAL) e salvar: aparece "Aguardando o PC".
4. Na próxima rodada do robô, conferir no PC (só leitura) que a edição chegou, e no site que o "Aguardando o PC" saiu.
5. Entrar como gerente: o farol aparece sem "Editar".
