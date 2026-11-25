---
id: R-20261124-215135-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0018
responde_a: R-20261124-214958-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T21:51:35-04:00
---
# T-0018 aberta (rotina diária + produção na pasta pessoal): plano e previsão; #57 continua esperando o autorizo

## T-0018 (decisões 1 B / 2 A / 3 B / 4 A / 5 A)
Começou agora (21:55), em paralelo:
- engenheiro-software: rotina diária no atualizar_do_github.py (--diario com os 5 limites; --primeira-vez com backup total; INSTALAR_ROTINA_DIARIA.bat para a tarefa das 06h30; VERSAO_INSTALADA.txt) e a ADR 0002. Sem token (repositórios públicos).
- modulo-robo: plano de migração do robô para a pasta PESSOAL — o que copiar (programas, bases, dado digitado intacto pela regra 7, configs, cofre), o notebook sincronizar a conta pessoal do OneDrive, ordem segura sem parar o robô, compartilhamentos das assistentes e do Power BI, como voltar atrás.
- Depois: testes; revisões; PR de governança do CLAUDE.md (regra 11 com o instale automático, "Agente: alexandre") para o seu autorizo.

## Previsão (Manaus)
- Plano de migração e simulação da rotina (--simular contra uma cópia, imagem antes/depois): 25/11 até 12h, ao Alexandre antes de qualquer gravação.
- Código da rotina no main: 26/11. 1ª rodada e migração: quando o Alexandre aprovar o plano (ele faz os passos no notebook e os compartilhamentos; o time guia).

## Lembretes
- 3 B entendido: repositórios seguem públicos. Ponto de atenção que fica registrado: o repositório de código guarda as bases congeladas (RELATORIOS/, SISTEMA BAP/, BAP Ajuda 2.0/) com dados de clientes, legíveis por qualquer pessoa enquanto for público.
- PR de governança do deploy automático: #57, branch alexandre/T-0017-autodeploy, head 02154d2ffbb1c099c1661267cd8c8d3b9a7a2374, só o render.yaml (autoDeploy: true), revisor aprovado, CI verde. Detalhes no R-20261124-211116-gerente-projetos. Falta o seu "autorizo o merge do PR #57 no commit 02154d2ffbb1c099c1661267cd8c8d3b9a7a2374".
- Entrega 2 da T-0017: esperando o "1 A" da simulação (R-20261124-212741); os 4 branches estão prontos e conferidos (tabelas PC × pacote: 0 diferença em 14.447 células; fila: os mesmos 139 clientes).
