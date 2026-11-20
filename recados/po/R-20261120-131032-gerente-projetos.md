---
id: R-20261120-131032-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: normal
tarefa: T-0001
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-20T13:10:32+00:00
---
# T-0001: resultado da conferência e pedido do teste po ↔ gerente

Resultado da T-0001 (conferência da montagem), rodada na BapCentral-GP em 20/11/2026:

- Crit. 1 ✅ `node --test` (CLI + guardiões): 139/139 verdes.
- Crit. 2 ½ leitura ✅ (`caixa` e `pendencias` leem o aloirr/bapcentral-recados; token fora das saídas). Gravação pela CLI ❌: 403 do proxy. Este recado foi gerado pela CLI e gravado pela integração do GitHub, com a autorização do Alexandre (opção 1). A gravação de vez, com `git push` pelo clone, vai por PR de governança (opção 2).
- Crit. 3 ⏸ precisa da sessão BapCentral-PO: o po envia um `aviso` de teste ao gerente-projetos; eu leio, respondo com `--encerra` e você confere a resposta.
- Crit. 4 ✅ guardião: po bloqueado em `relatorios_nucleo.py`; modulo-farois liberado.
- Crit. 5 ⏸ o Alexandre abre uma issue pelo formulário "Recado" no aloirr/bapcentral-recados; confiro na próxima ronda.
- Crit. 6 ✅ `verificar --por-dono` limpo.
