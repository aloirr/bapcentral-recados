---
id: R-20261124-212741-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: alta
tarefa: T-0017
responde_a: R-20261124-192008-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T21:27:41-04:00
---
# T-0017 entrega 2: simulação do WhatsApp, Títulos e Por cliente pronta (dados fictícios) — aprovação

## Simulação ("Simule" = mostrar antes)
14 imagens em recados/anexos/T-0017/entrega2/ (computador -pc e celular -cel), TODAS com dados fictícios (Cliente NNN, Vendedor NN, telefones 5592900000xxx), conferidas pelo designer-ux e por varredura automática:
- sim4-titulos / sim4-cliente: abas com CLIENTE, NOME e o valor primeiro, 1ª coluna fixa, rolagem lateral, selos de Situação/Faixa/Status como no PC; filtros recolhidos; sem exportar.
- sim4-cobranca: fila "Cobrar" de 10 em 10, do maior atraso ao menor; um botão principal "Abrir WhatsApp"; "Marquei como enviado" só depois de abrir o WhatsApp; "Pular" separado; avisos de telefone fixo ou sem número.
- sim4-cobranca-desfazer: "Desfazer" por 10 s depois de marcar.
- sim4-cobranca-tratados: quem já foi tratado hoje vai para "Já tratados hoje", recolhido.
- sim4-cobranca-erro: aviso quando o registro não chega ao servidor.
- sim4-gerente: o gerente vê as tabelas sem telefone e sem botão (RN-POS-004).
Faixa no topo: "Situação do PC até hh:mm" — o que é marcado no site volta ao PC nas rodadas das 08h e 14h, sem apagar nada do diário do PC.

## Também nesta entrega
- A saudação da mensagem deixa de levar o CPF do MEI (vale também para o PC): "Olá, <fantasia ou nome>!".

## Decisão para o Alexandre (resposta pronta "N X")
1. Simulação da entrega 2: (A) aprovada, abrir os PRs (pós-venda, site, robô, testes); (B) ajustar antes (diga o quê). Recomendo A. Resposta: "1 A".

## Depois do 1 A
PRs na ordem pós-venda → site → robô → testes, com revisão; o site publica sozinho no merge (deploy automático) e o robô novo só entra no PC na atualização da pasta (roteiro do R-20261124-211913). Previsão: PRs no main amanhã, 25/11, até 12h (antes do prazo de 02/12).
