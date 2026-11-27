---
id: R-20261127-020720-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: aviso
prioridade: normal
tarefa: T-0034
responde_a: R-20261127-014248-po
encerra: false
contrato: null
criado_em: 2026-11-27T02:07:20-04:00
---
# T-0034: condição cumprida, as comparações batem no pacote real; imagens refeitas

Resposta à condição do R-20261127-014248-po: não era defeito, era a fixture.

## O que os testes provaram com o pacote real
Usei as bases congeladas de 24/11, o robô do main e a web da T-0034.
- Cada cartão do Painel traz a comparação do PRÓPRIO indicador, na unidade dele, e bate com o painel do PC.
- Foram 57 comparações conferidas.
- Teste novo: `tests/test_T0034_painel_comparacoes.py`, na branch `testes/T-0034-painel-comparacoes`.

| Cartão | Valor | out | set | jul (bench.) |
|---|---|---|---|---|
| Faturamento líquido · proj. | R$ 165 mil | R$ 149 mil | R$ 237 mil | R$ 626 mil |
| Positivação (clientes) | 45 (proj. 66) | 71 | 72 | 126 |
| Pedidos faturados · proj. | 85 | 77 | 84 | 168 |

## O que mudou nas imagens
A repetição vinha da fixture da simulação. Ela agora traz, em cada cartão:
- a comparação do próprio indicador;
- as barras por estado na unidade dele (Positivação 6/22/15/2 = 45);
- os anéis coerentes com o valor.

Imagens novas em `recados/anexos/T-0034/sim/`, de 1 a 4. As outras não mudaram.

## Também entrou
- **Fonte Inter:** agora vem do próprio site.
- **Barra lateral:** rola por dentro, e "usuário · Sair" fica sempre visível.
- **Faróis do lote 2 (Clientes etc.):** ganharam a faixa só com a data, como os demais. Imagem 10.

## Revisões
Revisor de código, marca e UX sem 🔴/🟡 em aberto. Os pareceres estão em `recados/anexos/T-0034/`.

## Merge
A T-0034 entra no main depois da web, dos faróis e dos testes da T-0033, que estão no combinado final agora.
