---
id: R-20261127-112637-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: normal
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T11:26:37-04:00
---
# Complemento 2 da passagem: testes da T-0053 (6f4bf5c)

Complemento 2 da passagem R-20261127-111237. Esta sessão continua parada.

- **T-0053, testes:** `testes/T-0053-cadastro-do-pedido` · **6f4bf5c**.
  - 13 testes `test_RN_GER_019_*`, que pulam com motivo quando o `relatorios_nucleo` não tem a regra.
  - Com o b4006e7: suíte 1018 ✅, 0 ❌.
  - smoke igual ao do main.
  - Isso fecha o 🔴2 do revisor de código.
  - Falta só o modulo-farois fechar os RD-0256 a 0259 do corretor; depois vêm os PRs (#180 → testes → faróis).
- **Smoke:** as 3 falhas do "Farol DDR" já acontecem no main e não estão na lista de falhas conhecidas do agente testes. Essa lista é de governança e fica com o Alexandre.
