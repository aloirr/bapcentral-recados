---
id: R-20261124-080200-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0016
responde_a: R-20261124-075000-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T08:02:00-04:00
---
# T-0016: rota por lugar com sábado sem repetição e cidade base; smoke da rota limpo; instalado

## Merges (CI verde em cada head)
- #41 `a0f1ec2` — tarefa T-0016, quadro e RN-ROT-002/003 no doc 03 (gerente-projetos).
- #40 `af3b8cf` — `planner_nucleo.py` (modulo-rota): na roteirização por lugar, os 10 primeiros dias úteis só para a região da base; o sábado do depósito perde o cliente que já tem visita de seg a sex na semana (com aviso); sábado que já passou não é reescrito.
- #42 `dd7e85d` — `smoke_processos.py` e `tests/test_T0016_rota_lugar.py` (testes).

## Simulação aprovada (novembro, config congelada, mês inteiro)
- Cliente 2x na semana: 80 → 0. Fora da base nos 10 primeiros dias úteis: 18 → 0.
- Sábado 07/11: 2.314 → 2.237. Dia útil: 1.877 → 1.874. Clientes visitados no mês: 2.984 → 2.984.

## Testes
- pytest 149/149. `smoke_processos`: só a falha conhecida (ftPedidos, 66 diferenças); "ninguém some", "cidade base" e "nunca 2x na semana" ok.
- Revisão própria do gerente antes do merge achou e corrigiu 1 ponto (o sábado que já passou não pode ser reescrito).

## Produção
- `planner_nucleo.py` de `af3b8cf` instalado na pasta "Regionais - Leandro"; backup em SISTEMA BAP\BACKUP_RELATORIOS\ANTES_T0016_NOV2026 (conferido); instalado idêntico byte a byte ao main.
- A rota gravada de novembro só muda no próximo recálculo; os dias que já passaram ficam como estão.

## Próximo
- T-0004: o smoke_processos pode virar bloqueante no CI (governança, `.github/workflows/ci.yml`): PR com "Agente: alexandre", merge só com o "autorizo" do Alexandre.

## Como testar em 5 passos
1. No PC, abrir o Planner BAP e recalcular a rota de um vendedor do interior.
2. Ver no aviso da rota se apareceu "visita(s) ... saíram do sábado".
3. Conferir que nos 10 primeiros dias úteis do mês só aparece a cidade base e as cidades até 50 km.
4. Conferir que nenhum cliente está num dia da semana e no sábado da mesma semana.
5. Fayga e Rodrigo continuam com a base na segunda e terça e o interior de quarta em diante.
