---
id: R-20261127-011018-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: aviso
prioridade: normal
tarefa: T-0045
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T01:10:18-04:00
---
# T-0045: desenho pronto (PR #137), passos 1 e 2 da Máxima já liberados e um furo no guardião

## T-0045: desenho pronto
O PR #137 (ADR 0004 e contrato) está em revisão. Não é governança. As decisões 2 A, 3 A, 4 A, 5 A e 6 B estão registradas.
- **Como as visitas chegam ao site:** um lote por dia, por rota própria e com um token que o Render gera sozinho.
- **Senha da Máxima:** fica só no serviço agendado, nunca no site.
- **Botão "Atualizar visitas":** cai numa fila que o serviço lê a cada 10 minutos.
- **Erros:** confirmação, captcha ou bloqueio pausam as rodadas, sem nova tentativa, e aparecem só como código do erro.
- **Agenda:** nasce desligada. O diagnóstico roda primeiro, e só o admin liga a agenda.

## Passo a passo do Alexandre (fila das 06h)
Anexo: recados/anexos/T-0045/passo-a-passo-alexandre.md (9 passos).
- Os passos 1 e 2 já podem ser feitos: criar na Máxima um usuário só para o robô, com o mínimo de acesso (leitura do Espelho de Rotas). O usuário e a senha ficam só com ele.
- Os passos 3 a 9 vêm depois do código, quando eu avisar.

## Governança (fila das 06h, nada a autorizar agora)
- **donos.json:** os caminhos novos  (modulo-robo) e  (engenheiro-software) precisam de um PR de governança. Mando o número e o SHA quando o código começar.
- **render.yaml:** é o último passo, depois do código no main e antes do diagnóstico. Também mando o número e o SHA.

## Furo no guardião (para o Alexandre saber)
- **O que aconteceu:** num subagente rodando em worktree (), o guardião de donos não disparou. Uma edição no render.yaml passou sem bloqueio.
- **Quem pegou:** o próprio engenheiro percebeu e desfez, sem commit. Nada foi para o GitHub, e o verificar do CI continua barrando por commit.
- **Correção:** o conserto é no .claude/hooks e, portanto, é governança. Proponho uma tarefa para o Alexandre autorizar.
- **Enquanto isso:** confiro o verificar --por-commit de toda branch antes de cada merge, como já faço.

## Previsões (Manaus)
- Código da T-0045: robô, rota e web em paralelo, de 28/11 a 29/11.
- Simulação da tela "Atualizar visitas": 28/11 12h. É tela nova, então vem para aprovação.
