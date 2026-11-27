---
id: R-20261127-113021-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: normal
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T11:30:21-04:00
---
# Complemento 3 da passagem: testes da T-0023 (60778c2)

Complemento 3 da passagem R-20261127-111237. Esta sessão continua parada.

- **T-0023, testes do PC só leitura:** `testes/T-0023-pc-so-leitura` · **60778c2**.
  - Teste novo `tests/test_T0023_pc_so_leitura.py` (12 casos `test_RN_GER_012_*`, que pulam no main com o motivo).
  - Dois checks do smoke corrigidos e o `test_T0021` ajustado.
  - Com o 327a294: 1014 ✅, 0 ❌. O smoke fica com 294 ok e só as falhas que já existem no main.
  - Isso fecha o 🟡1 do revisor.
- **O que falta na T-0023:**
  - o adendo no desenho T-0023 (engenheiro): aceitei que o corpo de gravação fosse apagado, que é o 🟡2;
  - opcional para o modulo-farois: remover o `_trocou_cliente` e o `vars_cli`, que ficaram sem uso;
  - depois disso: corretor → PRs (testes → faróis) → fechar o #105 → entrega.
