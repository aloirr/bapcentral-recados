---
id: R-20261127-055046-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: aviso
prioridade: normal
tarefa: T-0036
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T05:50:46-04:00
---
# Correção: a faixa do site já mostra só a data; quem diverge é o checklist do revisor-ux

Correção de uma frase minha nos recados R-20261127-052537 e R-20261127-053643, sobre a faixa "Dados de".

**O que eu disse (errado):** que o site mostra "Dados de dd/mm/aaaa hh:mm" na faixa e que isso contraria a §4.1 da `tela-bc3.md`.

**O que é verdade (conferido no código pelo engenheiro-software):**
- Na faixa, o site mostra só a data: "24/11/2026 08:30" no PC e "24/11 08:30" no celular.
- O texto inteiro, "Dados de …, horário de Manaus", aparece só quando se para o mouse em cima (`title`).
- A §4.1 já dizia exatamente isso, e os testes da web exigem isso.
- Quem diz outra coisa é o checklist do revisor-ux (`.claude/agents/revisor-ux.md`, linha 40: "Dados de … (Manaus)").

**Efeito na decisão:** nenhum. A sua decisão (R-20261127-054626, manter como está no site) continua valendo, e o site não muda.
- O engenheiro deixou a §4.1 mais explícita, citando a sua decisão (PR do desenho da T-0036).
- Falta alinhar o checklist do revisor-ux. Como é arquivo de governança (`.claude/**`), essa correção vai na fila de governança do Alexandre, junto com o render.yaml e o donos.json da T-0045.

Desculpe a imprecisão.
