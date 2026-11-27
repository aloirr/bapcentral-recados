---
id: R-20261127-012526-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: pergunta
prioridade: normal
tarefa: T-0025
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T01:25:26-04:00
---
# 3 perguntas ao Alexandre (fila das 06h): TOTAL A PAGAR do diretor, telefone na garantia e estado nas Devoluções/NCC

Origem: o desenho do engenheiro-software, registrado pelo gerente (decisão 3 A). Branch `engenheiro-software/T-0023-T-0025-contrato`. Fica em fila para as 06h. A recomendação é a primeira opção em todas.

1. **T-0025, o TOTAL A PAGAR para o diretor.** Hoje ele só existe nas abas Vendedores e Supervisores, e o diretor só vê o Resumo. Do jeito que está, o diretor não vê o TOTAL A PAGAR.
   - (A) Um cartão "TOTAL A PAGAR" no Resumo, visível só para admin, gerente e diretor. *(recomendada)*
   - (B) O diretor passa a ver também as abas Vendedores e Supervisores.
   - (C) Fica só para admin e gerente.

2. **T-0023, Garantias: quem preenche o telefone de contato do cliente.**
   - (A) Só no PC, como hoje. O site não mostra nem recebe telefone (regra 6). *(recomendada)*
   - (B) Um campo no site, só de escrita, que vai para o PC sem aparecer na tela. Isso abre exceção à regra 6.

3. **T-0023, filtro por estado nas Devoluções e na NCC.**
   - (A) Pela filial da nota, a mesma regra do faturamento (RN-GER-006). *(recomendada)*
   - (B) Pela UF do cliente, como nos PRs antigos.

**Previsões, em horas de agente:**
- T-0023 v2: cerca de 12 h.
- T-0025 v2: cerca de 20 h. A tela de edição dos parâmetros das campanhas tem 6 abas.

O código começa depois que a T-0033 entrar no main, porque depende da grade e da casca BC3. As perguntas acima não seguram o início.
