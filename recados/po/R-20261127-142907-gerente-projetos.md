---
id: R-20261127-142907-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0023
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T14:29:07-04:00
---
# T-0023 entregue: PC só leitura em Garantias, Devoluções e NCC (a edição é pela web)

**No main:** #195 (adendo, fdc7110), #199 (garantias.gravar_contato, cd83e08), #200 (código, adc5027), #202 (testes, 7c3f3bd). Revisor de código, corretor, UX e marca aprovados; CI verde. O PR antigo #105 foi fechado (substituído).

**O que muda (RN-GER-012):** no PC, as telas de Garantias, Devoluções e NCC ficam só leitura; a edição é feita no site (web, já no ar desde a 0.7.0) e o robô grava no PC só acrescentando (regra 7). O "Salvar contato" da Garantia usa a função pública do pós-venda (grava só o que mudou).

**Como testar em 5 passos** (depois do "instale" ou da rotina das 06h30 no notebook):
1. No PC, abrir o Farol de Garantias: os campos de edição aparecem só para leitura.
2. Fazer o mesmo em Devoluções e NCC.
3. Editar uma garantia pelo site (admin ou pós-venda) e salvar.
4. Na próxima rodada do robô, conferir no PC que a edição chegou, sem apagar o que já estava.
5. No PC, usar "Salvar contato" numa garantia: só o contato muda; data de fechamento e status ficam como estavam.

**Para depois (🟢, sem pressa):** contraste do botão verde (MC-0012, sistema todo); "1 linhas" e fonte 8 numa tela; RN própria para a data de fechamento deduzida pelo gravar.
