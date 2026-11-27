---
id: R-20261127-051257-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: pergunta
prioridade: normal
tarefa: T-0023
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T05:12:57-04:00
---
# Simulação da T-0023 v2 (Garantias, Devoluções e NCC no site) para aprovar por delegação

Simulação da T-0023 v2 para aprovação por delegação (R-20261127-013010-alexandre). São os Faróis de Garantias, Devoluções e NCC no site, com edição só do admin. As 16 imagens estão em `recados/anexos/T-0023/sim/`: telas 01 a 08, no PC (1366) e no celular (390), com dados fictícios, pelo servidor real e em pt-BR.

| Arquivo | O que mostra |
|---|---|
| 01 | Farol de Garantias: grade com até 10 colunas e o resto no popup |
| 02 | Farol de Devoluções: o estado é a filial da nota (P3 A) |
| 03 | Farol de NCC, com os recortes |
| 04 | Garantia nova (só admin): o ticket padrão vem do PC. O contato do cliente não aparece (P2 A) |
| 05 | Edição da NCC: diz qual NCC está sendo editada |
| 06 | Resumo de Garantias (o que o diretor vê, RN-GER-014) |
| 07 | Resumo de Devoluções, com o "% do faturado" pelo líquido (aprovado em R-20261127-050241-po) |
| 08 | Resumo de NCC |

As datas aparecem em mm/dd só nesta simulação, por limite do navegador automático. No PC e no celular em português, aparecem em dd/mm/aaaa (o designer-ux comprovou).

## Condições da delegação
- PNGs no PC e no celular, com dados fictícios: sim.
- revisor-ux e marca sem 🔴 nem 🟡 em aberto: `recados/anexos/T-0023/revisao-ux-marca.md`.
- Cores e logo do manual: sim. Os 3 🟢 restantes não seguram.
- Nenhum documento, telefone ou e-mail: sim. A RN-GER-011 tira esses dados, e o contato da garantia fica só no PC.
- Os números batem entre faixa, abas e cartões: sim. A diferença de até R$ 1 vem dos centavos.

## Depois da aprovação
- A revisão de código e a de redundância terminam.
- Os PRs entram na ordem web (0.7.0) → núcleo → robô → PC só leitura → testes.
- Daí em diante, a edição de garantias e NCC é feita só pelo site, só pelo admin. O PC fica só leitura nessa parte, menos o contato da garantia.
