---
id: R-20261127-194317-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: null
responde_a: R-20261127-194139-alexandre
encerra: false
contrato: null
criado_em: 2026-11-27T19:43:17-04:00
---
# Demandas paradas: dono, sessão e previsão de cada uma

Pedido: "veja se nenhuma demanda passou batida e ficou para tras ou parada".

Limite de uso em alerta. O plano roda em **2 frentes ao mesmo tempo**, cada uma com uma sessão por dono, e abre sessão nova só quando a anterior fecha. Horários em Manaus.

## 1. Migração "TUDO" para o site (plano R-20261126-175814)
A T-0033 a T-0037 já estão entregues. A T-0025 e da T-0038 à T-0044 não começaram, e eu deixei passar sem dono e sem data no quadro. Datas novas:

| Tarefa | Donos | Sessão | Simulação | Era |
|---|---|---|---|---|
| T-0025 DDR, Campanhas, Expositores na web | modulo-web, modulo-robo, modulo-farois, testes | abre 28/11 14h | 29/11 12h | 28/11 20h |
| T-0038 Parcial BAP, Exportar RH, PDF por pessoa | modulo-robo, modulo-farois, modulo-rota, modulo-web, testes | abre 29/11 08h | 30/11 12h | igual |
| T-0039 Painel Executivo completo (Excel, supervisor, mês anterior) | modulo-robo, modulo-web, testes | abre 30/11 08h | 01/12 12h | 30/11 18h |
| T-0040 Trocar loja de coleta pela web | modulo-web, modulo-robo, testes | depois da T-0025 | 01/12 18h | 01/12 10h |
| T-0041 Cadastros do Analista em leitura | modulo-rota, modulo-metas, modulo-posvenda, modulo-robo, modulo-web, testes | depois da T-0038 | 02/12 18h | 02/12 12h |
| T-0042 Os mesmos cadastros com edição | idem | depois da T-0041 | 04/12 12h | 03/12 18h |
| T-0043 Página "Dados e robô" | engenheiro-software, modulo-robo, modulo-web, testes | depois da T-0039 | 04/12 18h | 04/12 12h |
| T-0044 Desligar no PC o que ficou 2 semanas igual | modulo-farois, engenheiro-software, testes | — | a partir de 19/12, farol a farol, com o seu "ok" | 18/12 |

Motivo do atraso de até 1 dia: o limite de uso não deixa abrir 3 a 4 frentes, como o plano previa. Se ele subir, volto às datas de antes.

## 2. T-0013 e T-0014 (em_teste desde 23/11)
Faltava o primeiro pacote do robô e conferir o número da web contra o farol. Hoje isso está cumprido: chegam pacotes com 18 faróis, e o filtro por estado foi conferido pela T-0058. **Recomendo fechar as duas hoje**, com um recado de entrega às 20h30. O que sobrar de tela vai para a T-0059 parte 2.

## 3. T-0046, T-0047, T-0048 e T-0049
- **T-0046** (limpeza interna da web) e **T-0047** (faixas de cor, já decididas, R-20261127-010314): entram na **T-0059 parte 2**, na mesma sessão de web, marca e design. São as mesmas telas e a mesma paleta. A simulação da T-0059 é amanhã às 10h; a da T-0046 e da T-0047 às 14h; merge às 17h.
- **T-0048** (desconto do Diretor 15,0 × 15,1): entra no **lote 2 da T-0060**, na sessão do modulo-farois, porque é número do Diretor. Simulação 28/11 às 11h e merge às 14h.
- **T-0049** (uma fonte só para o dado pessoal): engenheiro-software, depois da T-0043. Simulação não se aplica (não tem tela); PR em 05/12.
- **T-0050** (acesso aos faróis por usuário): o desenho está pronto e as perguntas P2 a P4 foram ao Alexandre às 06h15 (R-20261127-061520). Confiro hoje se há resposta e, se houver, a sessão abre em 29/11.

## 4. Quadro e pedido literal
Confirmado: o quadro está parado desde 06h25 e o .coord/tarefas só vai até a T-0018. Hoje às 21h30 faço um PR meu com:
- o quadro atualizado da T-0019 à T-0060;
- um arquivo por tarefa aberta, com o pedido literal e o id do recado;
- nas tarefas entregues, o id do recado de entrega.
Daqui em diante, atualizo o quadro a cada entrega.

## 5. Render da T-0045
Não há caminho sem ele: o usuário e a senha da Máxima são segredo (regra 5), e só o Alexandre tem acesso ao painel do Render. O mínimo é **um passo só**:
- no serviço bap-visitas-maxima do Render, preencher BAP_MAXIMA_USUARIO e BAP_MAXIMA_SENHA;
- o serviço já está no render.yaml com deploy automático. Se ele não aparecer no painel, é 1 clique em "Sync" no Blueprint.

Enquanto isso não acontece, as visitas seguem pelo robô do PC, como hoje, sem perda.

## 6. T-0054
Confirmado: o admin (e o pós-venda) já editam o Farol de Entregas no site, **sem passo dele**. O pré-requisito era o robô novo no notebook, e esse robô já chega com os 18 faróis.

## Sai da lista "aguarda você"
O BAP_WEB_LEITURA_TOKEN já está no Render e a porta responde 200 desde as 17h.
