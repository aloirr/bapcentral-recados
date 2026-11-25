---
id: R-20261124-212021-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: alta
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T21:20:21-04:00
---
# Incidente: gravei por engano nomes de clientes no recado R-20261124-212002 (regra 6) — decisão de correção

## O que aconteceu
Às 21:20 gravei o parecer do designer-ux sobre a simulação da 2ª entrega (R-20261124-212002-gerente-projetos). Tirei o trecho do CPF, mas deixei passar uma linha que cita 4 nomes reais de clientes como exemplo (a simulação tinha a mensagem do WhatsApp sem anonimizar). Erro meu: o recado viola a regra 6 (sem nome de cliente em recado). O repositório de recados é privado; nenhum outro lugar recebeu o texto. As imagens e o pacote de simulação com dado real já foram apagados, e o robô está refazendo a simulação toda fictícia, com varredura automática de nomes e CPF/CNPJ antes de qualquer imagem.

## Por que não corrigi sozinho
Recado é imutável e o guardião trata alteração de recado existente como violação; apagar histórico é proibido. Não contorno.

## Decisão para o Alexandre (resposta pronta "N X")
1. (A) autoriza um commit no aloirr/bapcentral-recados que troca só a linha dos nomes por "[nomes de clientes ocultados — regra 6]" nesse recado (o nome continua no histórico do git, que não se apaga); (B) autoriza reescrever o histórico do repositório de recados para apagar de vez (exige force push, hoje proibido); (C) deixa como está. Recomendo A. Resposta: "1 A".

## Prevenção
Daqui em diante, todo parecer gravado pelo gerente passa por uma varredura automática (nomes do pacote real, CPF/CNPJ, telefone) antes do envio.
