---
id: R-20261124-192615-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: alta
tarefa: T-0017
responde_a: R-20261124-192427-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T19:26:15-04:00
---
# Deploy v0.2.0: falta um clique do Alexandre no Render (o time não tem acesso ao painel)

O código da v0.2.0 está no main (web/ igual desde 73a8b4a; o main atual 3ebc793 só acrescenta testes e docs). O Render está com deploy automático desligado e o time não tem login nem deploy hook (segredo só do Alexandre), então o deploy é um clique dele:

1. Entrar em https://dashboard.render.com e abrir o serviço bap-central.
2. Botão "Manual Deploy" > "Deploy latest commit" (branch main).
3. Esperar o status "Live" (2 a 4 minutos).
4. Avisar o po "deploy feito".

Eu confiro na hora: hoje /saude responde versao 0.1.0 (19:26, último pacote 18:07); depois do deploy tem de responder versao 0.2.0, e o menu do site passa a mostrar os 4 faróis (Inadimplência com dados só depois do "instale" do robô; os outros 3 como "ainda não disponível").

Obs.: a tag v0.2.0 não subiu daqui (o proxy desta sessão recusa push de tag); se o Alexandre quiser a tag, pode criá-la no GitHub em Releases sobre o commit 73a8b4a. Não muda o deploy.
