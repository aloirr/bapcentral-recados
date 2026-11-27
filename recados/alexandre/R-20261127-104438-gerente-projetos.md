---
id: R-20261127-104438-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: normal
tarefa: T-0054
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:44:38-04:00
---
# T-0054: simulação da edição no Farol de Entregas para aprovar

**T-0054 (edição no Farol de Entregas): simulação para você aprovar por delegação.**

**Simulação** (dados fictícios: "CLIENTE TESTE 01", "MOTORISTA TESTE", NFs 9005xx; navegador em pt-BR; 1366 px e 390 px): `recados/anexos/T-0054/sim/`
- `posvenda-entregas-pc.png`: o pós-venda vê a coluna "Editar" nas Entregas (e nas Pendências dos meses anteriores, na mesma página).
- `posvenda-edicao-aberta-*`: o formulário com as 6 edições do PC.
  - O topo mostra a nota: "NF 900502 · CLIENTE TESTE 02 · MA".
  - Campos: ETAPA (lista), TRANSPORTADORA (lista), DT. PREVISTA, DT. REAL, RESPONSÁVEL e VLR FRETE (REAL).
- `posvenda-edicao-erro-varios-*`: um erro real do código ("RESPONSÁVEL (MOTORISTA): sem CPF, CNPJ, telefone ou e-mail."). O que foi digitado nos outros campos continua; só o campo recusado volta vazio e destacado.
- `posvenda-entregas-salvo-*`: depois de salvar, a linha mostra "Aguardando o PC" até o robô gravar.
- `gerente-entregas-*`: o gerente vê sem editar (P1 A); depois de uma edição, vê só a marca.
- `admin-entregas-depois-pc.png`: o admin vê igual ao pós-venda.
- `sugestao-*`: os dois últimos acertos de CSS que entram agora (a marca sem quebrar linha no PC e o campo recusado em destaque).

**Regras** (PR #178): RN-POS-011 nova. O pós-venda e o admin editam o Farol de Entregas e também "Notas com frete" no Fretes (P2 A). O gerente não edita (P1 A). O robô grava só acrescentando no diário (regra 7).

**Critérios da delegação:**
- dados fictícios ✅;
- revisor-ux aprovado no 69d6fcf, com 2 linhas de CSS já pedidas ao dono, sem outra rodada;
- marca: só tokens, sem hex novo (conferido pelo revisor-ux);
- revisor de código, corretor e testes começam agora, no head final.

**Ordem dos PRs depois da sua aprovação:** regras #178 → desenho #179 → web 0.12.0 → robô → testes.

**Importante:** a edição só aparece no site quando o robô do notebook estiver atualizado (meu R-20261127-104041). Até lá, nem o admin vê a coluna "Editar".
