---
id: R-20261127-111431-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: normal
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T11:14:31-04:00
---
# Complemento da passagem: T-0054 web 0b6f09d e corretor da T-0053

Complemento da passagem R-20261127-111237. Esta sessão continua parada, sem merge e sem frente nova.

- **T-0054, web:** `modulo-web/T-0054-entregas-edicao` · **0b6f09d**. Tem o merge do main com a web 0.12.0, a linha nova só do admin no `novo_tela`, no GET `?novo=1` e no `editar_novo` (com o teste `test_RN_POS_011_linha_nova_so_do_admin`) e o RD-0255. `pytest web/tests`: 616 ✅. Falta o reteste do revisor de código e do corretor nesse SHA.
- **T-0053, corretor no b4006e7:** 4 achados abertos para o modulo-farois, RD-0256 a 0259, e 1 só de docstring, o RD-0260. Estão em `recados/anexos/T-0053/redundancias.md`. Seguram o lote. A RN-GER-019 (3874b3a) saiu sem achado.
