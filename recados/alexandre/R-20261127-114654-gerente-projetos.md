---
id: R-20261127-114654-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: normal
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T11:46:54-04:00
---
# Complemento 4 da passagem: T-0036 #177 em 915ed5d

Complemento 4 da passagem R-20261127-111237. Esta sessão continua parada. Vi que o main já está no a042d7c, com o #180 mesclado pelo gerente que assumiu.

**T-0036:** o PR #177 (`testes/T-0036-testes-v2`) está no head **915ed5d**, sem conflito, com o main f6c4b00 mesclado.
- **Testes, só v2 sem o robô:** 1046 ✅, 0 ❌ em `tests/`; 602 ✅ em `web/tests`.
- **Testes, v2 com o robô #159 c8209a1:** 1069 ✅, 0 ❌.
- **Pacote:** medido como o robô mede, em JSON compacto: 15,02 MiB, dentro da margem de 80%. Entrou também um teste novo do maior farol no formato 2, abaixo de 80% de 8 MB.
- **Próximo passo:** CI do #177 → merge. Depois, revisor do delta do robô c8209a1 → update do #159 → merge → entrega.
