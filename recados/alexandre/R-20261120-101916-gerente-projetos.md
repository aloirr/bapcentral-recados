---
id: R-20261120-101916-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0005
responde_a: R-20261120-101842-alexandre
encerra: false
contrato: null
criado_em: 2026-11-20T10:19:16-04:00
---
# Recomendação do gerente: corrigir o gerador da rota para a Máxima

## Decisão
Corrigir o gerador do JSON da rota para a Máxima (entrega R-20261120-101532-gerente-projetos)?

## Recomendação do gerente: (a), abrir a tarefa do modulo-rota com a simulação primeiro
- **Motivo:** a correção (data final = próxima visita + periodicidade − 1) é segura nos dois casos.
  - Se a Máxima repete cada linha até a data final, a correção acaba com os compromissos repetidos.
  - Se a Máxima não repete, cada linha continua gerando uma visita só e nada muda.
- **Confirmar antes com a Máxima: não é preciso.** Como a correção é segura nos dois casos, não pede trabalho manual dele.
  - A dúvida sobre a remessa nova apagar a antiga também não muda a correção: ela só diz se o problema dobra.
  - Se ele quiser a confirmação mesmo assim, ela depende de alguém perguntar à Máxima, e isso é manual.
- **Efeito no prazo:**
  - nenhum nas outras tarefas: é tarefa nova, do modulo-rota, em caminho que não colide;
  - a simulação (a planilha de mentira, com os números de antes e de depois) sai em cerca de 1 h depois do sim;
  - o código vem depois da simulação aprovada e só vai ao PC com o "instale".

## Se ele escolher (b), deixar como está
- Nada muda. A agenda pode continuar acumulando compromissos repetidos, se a suposição estiver certa.
