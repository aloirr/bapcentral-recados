---
id: R-20261127-195452-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0013
responde_a: R-20261127-194139-alexandre
encerra: true
contrato: null
criado_em: 2026-11-27T19:54:52-04:00
---
# Entrega T-0013 e T-0014: web no ar com o Painel e as visões por estado

Fechadas com o ok do po (19:55) à recomendação do R-20261127-194317-gerente-projetos.

## T-0013: web onda 0 e primeira entrega
O site está no ar desde 23/11 (https://bap-central.onrender.com), hoje na versão 0.16.0, com o Painel (resultado e produtividade) feito a partir do pacote do robô. Faltava o primeiro pacote do notebook e o número da web igual ao do farol. Isso está cumprido:
- o /saude mostra o lote 20261127T173703 com 18 faróis;
- a conferência do Farol de Pedidos (T-0053) deu farol = fonte nas bases congeladas.

## T-0014: visões prontas por estado
O filtro por estado está no site desde #35–#38. Com a T-0058 (#217 e #224), o número por estado na web passa a bater com o Painel também quando há devolução de vendedor sem venda no mês. Isso vale com o pacote do robô novo de 28/11.

## O que sobra
- O layout das telas da web vai para a T-0059 parte 2 (simulação 28/11, 10h).
- O filtro por supervisor continua como "depois", como estava no pedido.

## Como testar em 5 passos
1. Abra https://bap-central.onrender.com/saude: a versão aparece e o "lote" é de hoje.
2. Entre no site como admin e abra o Painel: os números são os do último pacote.
3. Abra o mesmo mês no Painel do Diretor do PC: faturamento e positivação batem.
4. No Farol de Pedidos do site, escolha um estado no filtro: o total muda para o do estado.
5. Depois do pacote de 28/11, confira AGO/26 PA: R$ 33.834, igual ao Painel (T-0058).
