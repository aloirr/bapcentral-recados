---
id: R-20261120-101532-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0005
responde_a: R-20261120-101118-alexandre
encerra: true
contrato: null
criado_em: 2026-11-20T10:15:32-04:00
---
# T-0005: o gerador da rota para a Máxima repete compromissos (com uma suposição sobre a Máxima)

## Entregue
- Verificação feita pelo modulo-rota, só lendo o código e simulando com 12 clientes fictícios. Nada foi alterado.
- **Resposta: sim, erra.** Mas depende de uma suposição sobre a Máxima: que ela repete cada linha a cada periodicidade até a data final. O código e os docs não confirmam isso.
- **Por quê** (`planner_nucleo.py`, função `linhas_protheus`, linhas 6228–6279):
  - sai uma linha por visita, e não uma por cliente: um cliente semanal vira 4 ou 5 linhas no mês;
  - todas as linhas valem de 2000-01-01 até 3000-01-01. O 3000 foi pedido pela Máxima em 07/10;
  - a periodicidade vem da curva do cliente: 7, 14, 30 ou 45 dias.
- **Números da simulação** (12 clientes: 4 semanais, 4 quinzenais e 4 mensais):
  - o JSON sai com 32 linhas, as 32 visitas pretendidas;
  - nas segundas de novembro, os mesmos 4 clientes semanais viram 8, 12, 16 e 20 compromissos;
  - até 31/12 são 184 compromissos, contra 32 visitas;
  - com a remessa antiga ainda ativa, tudo dobra: 344 no total;
  - com a proposta não aplicada (data final = próxima visita + periodicidade − 1), dá exatamente 32 compromissos, no máximo 4 por dia;
  - o crescimento bate com o caso real de 09/11: 17, 22 e 27 compromissos para 12 clientes.
- **Em quais casos:**
  - semanal: é o pior caso, já a partir da 2ª semana;
  - quinzenal: o cliente aparece em dobro em alguns dias;
  - mensal: não erra em novembro, mas repete nos meses seguintes;
  - remessa antiga ativa: dobra tudo;
  - sábado-depósito: volta 45 dias depois;
  - inativo: já não entra desde 10/11;
  - CNPJ interno e conta 000040: o filtro não foi achado no planner, e isso não foi confirmado.

## Em andamento
- nada nesta tarefa. A T-0005 fica concluída com esta entrega.

## O que o time pede a você
- Duas perguntas só a Máxima responde: se ela repete cada linha pela periodicidade até a data final, e se a remessa nova apaga a antiga.
- Corrigir o gerador é decisão sua (nenhuma correção sem nova decisão).

## Próximo passo
- Se você decidir corrigir, abro uma tarefa do modulo-rota com a proposta acima, simulada antes (PNG ou planilha de mentira), como manda a regra "Simule".

## Como testar em 5 passos
1. Abrir `planner_nucleo.py` nas linhas 6182–6185 e 6272–6273: as datas 2000-01-01 e 3000-01-01 são fixas.
2. Na mesma função (6228–6279), ver que sai uma linha por visita.
3. Exportar o JSON de um vendedor com clientes semanais.
4. Contar as linhas do mesmo cliente: 4 ou 5 no mês.
5. Na Máxima, ver a agenda desse cliente na 3ª ou 4ª semana: se aparecer repetido, a suposição se confirma.
