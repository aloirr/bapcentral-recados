---
id: R-20261120-110803-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: alta
tarefa: T-0010
responde_a: R-20261120-104729-alexandre
encerra: false
contrato: null
criado_em: 2026-11-20T11:08:03-04:00
---
# T-0010: o sábado-depósito tira 79 clientes da Máxima até janeiro; decisão antes do merge

## O que foi achado
- O código está pronto: PR #9 (modulo-rota, head 4e797721225b16fc475f4f803c9ebeaef8e95063) e PR #10 (testes, 34 testes, head ce816ddf4a2f8d32032fb44f0f51f471d1886d68). O CI está verde nos dois. O revisor-codigo está com eles.
- O gerador não perdeu nenhum cliente por erro.
- Na carteira fictícia, 94 dos 312 clientes ativos ficam sem compromisso na Máxima de 23/11 a 31/12. Os motivos, sem nomes:
  - 79: a única visita do mês caiu no sábado-depósito, que a regra aprovada tira do arquivo (37 de periodicidade 30, 39 de 45 e 3 de 14);
  - 12: conta 000040, fora por decisão;
  - 3: CNPJ interno, fora por decisão.
- Outro defeito, em outro arquivo (modulo-farois): a exportação real não repassa o nome do cliente ao gerador. Por isso o filtro de interno não funciona de verdade, e o cliente de visita semanal sai com a periodicidade da curva. Já está em correção num PR à parte, coberto pela regra aprovada.

## Decisão
Os 79 clientes do sábado-depósito: tirar do arquivo da Máxima ou exportar com a data final curta?
- (a) Manter como aprovado. Esses clientes ficam sem compromisso na Máxima até janeiro. Só faz sentido se o atendimento do sábado-depósito não passa pela Máxima.
- (b) Exportar também o sábado-depósito, com a mesma regra de data final curta. A duplicação já acaba com a data final curta, e nenhum cliente some da Máxima.

## Recomendação do gerente: (b)
- Motivo: a data final curta sozinha já resolve as repetições. Tirar o sábado-depósito deixa cerca de 1 em cada 4 clientes ativos sem compromisso na Máxima.
- Efeito no prazo: um ajuste pequeno no PR #9 e no PR #10, com mais uma revisão, cerca de 30 min. O merge sai às 12:45 em vez de 12:15.
- Se ele escolher (a): o merge segue às 12:15.
