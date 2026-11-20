---
id: R-20261120-100628-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: normal
tarefa: T-0005
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-20T10:06:28-04:00
---
# T-0005: pendências herdadas do Cowork que dependem do Alexandre

## Contexto
- Fonte: seção 6 do `docs/legado/maestro_sistemas_bap.md` (estado até 13/11/2026).
- A T-0005 pede levar ao po o que depende do Alexandre. Nenhum destes itens trava o time na nuvem. Os nomes de clientes e de vendedores ficaram de fora (regra 6).

## O que depende dele
1. **Rota de um vendedor na Máxima** (recado antigo 20261109-1015). Decisão.
   - O que é: o gerador do JSON da rota repete compromissos. Um vendedor chegou a 27 compromissos para 12 clientes num dia, e o número dobra se o JSON antigo continuar ativo.
   - Em 09/11 ele disse "deixe como está por enquanto".
   - A proposta parada: data final = próxima visita + periodicidade − 1, sem exportar o sábado-depósito, sem inativo e sem CNPJ interno.
   - Se sim: entra como tarefa nova do modulo-rota, para a rota de dezembro. Se não: fica como está.
2. **Git no desktop DT-AMADMBAP-03.** Ação no PC, não é decisão.
   - O que é: sem o Git, o robô não sincroniza o BAP Ajuda (o estoque e a carteira do dia não sobem e as respostas não descem).
   - O que fazer: instalar o Git para Windows com as opções padrão.
3. **Robô de visitas da Máxima.** Ação no PC.
   - O que é: falhou duas vezes em 31/10, logo depois do login. O print saiu em branco.
   - Para diagnosticar falta rodar de novo com "Mostrar o navegador" e mandar a linha "Parou em: …".
   - [SUPOSIÇÃO] Pode já ter voltado a funcionar depois de 31/10.
4. **Novembro (NOV/26).** Decisão, e talvez já superada, porque o mês está acabando.
   - O que é: exportar e importar na Máxima o JSON da rota de novembro e travar as metas do mês.
   - Também decidir duas coisas: quem cobre as zonas de uma cadeira vaga no AM, e para onde vão os 405 clientes do Amapá da conta 000040.
   - Pergunta: ainda vale para novembro ou passa direto para dezembro?
5. **Coordenadas.** Ação dele ou de quem ele indicar.
   - O que é: conferir os 33 clientes que mudaram de lugar ao comparar com o ponto do Protheus.
6. **Segurança.**
   - O que é: o diário registra um token do GitHub colado num chat em 27/10, ainda marcado como "trocar".
   - Só ele pode trocar: ele gera o token novo e atualiza a configuração do app e do Render.
   - [SUPOSIÇÃO] Pode já ter sido trocado.

## Pronto quando
- O po responde, item a item: decidido, feito, superado ou adiado.
