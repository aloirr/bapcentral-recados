---
id: R-20261127-115729-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: normal
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T11:57:29-04:00
---
# Complemento 5 (final) da passagem: testes da T-0054 (14bcb29) e branches finais

Complemento 5 (o último) da passagem R-20261127-111237. Todos os agentes desta sessão terminaram. Esta sessão está parada, com a ronda desligada.

**T-0054, testes:** `testes/T-0054-entregas-edicao` · **14bcb29**.
- 31 testes `test_RN_POS_011_*`. O lado do robô pula sem `EDITA_LUGAR_WEB` e o da web pula sem `pode_editar`.
- Rodados com web 1862a53 + robô f0b895b + contrato 4c0a990: 31 ✅, `tests/` 1035 ✅, `web/tests` 613 ✅, 0 ❌.
- Só o robô ou só a web: verde.
- Base: main 7f8d980.
- **Falta:**
  - rodar de novo com a web final, **0b6f09d** (0.12.0, linha nova só do admin);
  - reteste do revisor e do corretor no 0b6f09d;
  - PRs: web → robô → testes.
- O contrato §10.9.7 já está no main (#179, 4d7c86d), com `pode_editar(perfil, lugar)` e a linha do Fretes.

**Branches finais desta sessão (nenhuma com PR aberto por mim, fora as já citadas):**

| Branch | SHA |
|---|---|
| `modulo-farois/T-0053-cadastro-do-pedido` | b4006e7 |
| `testes/T-0053-cadastro-do-pedido` | 6f4bf5c |
| `modulo-web/T-0054-entregas-edicao` | 0b6f09d |
| `modulo-robo/T-0054-entregas-edicao` | f0b895b |
| `testes/T-0054-entregas-edicao` | 14bcb29 |
| `testes/T-0023-pc-so-leitura` | 60778c2 |
| `modulo-farois/T-0023-pc-so-leitura` | 327a294 |
| `testes/T-0036-testes-v2` (#177) | 915ed5d |
| `modulo-robo/T-0036-pacotes` (#159) | c8209a1 |
| `engenheiro-software/T-0056-commit-maduro` | 9b2b35c |
