---
id: R-20261126-235924-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0035
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-26T23:59:24-04:00
---
# T-0035 entregue (site 0.4.0 no ar); T-0033 aprovada no UX; 3 respostas pendentes

# Status 00h00 (27/11): T-0035 no main e no ar; T-0033 aprovada pelo designer-ux

## Marco: T-0035, pacote por farol, entregue
- No main: #131 (ADR 0003 e contrato), #132 (web 0.4.0), #133 (robô), #134 (testes).
- **Site no ar com a versão 0.4.0.** O `/saude` mostra a memória (pico de 64 MB de um limite de 512 MB) e o pacote atual convertido.
- O robô novo chega ao PC pela rotina diária das 06h30, que confere: commit com 2 h ou mais, CI verde e versão da web igual à do site. A partir daí ele manda farol a farol (gzip), e o farol que falhar mostra os dados da rodada anterior; com mais de 26 h, aparece o selo "Desatualizado" (§4.4 A).
- Provas:
  - 4 combinações robô × web com as bases congeladas;
  - 47 cartões iguais;
  - 552 testes da raiz e 331 da web;
  - revisor-codigo aprovado;
  - designer-ux aprovou o selo nas cores do manual.

## Como testar em 5 passos
1. Abra https://bap-central.onrender.com/saude: versão 0.4.0, com `pacote` e `memoria`.
2. Depois da rodada do robô de amanhã (a partir das 07h), abra os faróis: os números são os mesmos do PC.
3. No `/saude`, o `lote` muda a cada rodada e o `origem` deixa de ser "convertido".
4. Se um farol falhar, ele continua com os dados anteriores; com mais de 26 h, aparece o selo amarelo "Desatualizado".
5. A memória fica bem abaixo dos 512 MB.

## Também no main hoje
- #82 (testes das parciais), #129 (manual da marca aprovado), #130 (travas de teste do lote 2).

## Aguardando você
| Item | Recado | Resposta pronta |
|---|---|---|
| Simulação T-0024 (5 faróis do lote 2) | R-20261126-225201 | "1 A" |
| Simulação T-0033 (revisão geral) | R-20261126-232717 | "1 A". O designer-ux já aprovou a versão final (3c6419d); o revisor-codigo e o corretor-redundancias revisam agora |
| T-0045 visitas da Máxima no site (5 decisões) | R-20261126-224331 | "1 A, 2 A, 3 A, 4 A, 5 B" |

## Previsões (sem mudança)
- T-0033: PRs logo depois do seu "1 A" e das revisões, ~01h30.
- T-0034 (página inicial): simulação 27/11 12h.
