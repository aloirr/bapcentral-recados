---
id: R-20261127-092946-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: resposta
prioridade: normal
tarefa: T-0045
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T09:29:46-04:00
---
# T-0045 sem nenhum passo do Alexandre: o que o time faz, o que só ele pode e o caminho pelo PC (recomendado)

Resposta ao R-20261127-092846-alexandre (T-0045: "não quero fazer nenhum passo, faça por mim").

## (a) O que o time faz sem ele
Já está pronto ou no main:
- web 0.6.0 com a tela "Atualizar visitas";
- botão do PC com a regra do núcleo;
- robô pronto para rodar na nuvem e trazer as visitas da nuvem para o PC (#165);
- testes (#166, entra hoje).

O time ainda faz, sem ele:
- o código do serviço agendado (`rodar.py` e `agenda.py`);
- o texto do Dockerfile;
- o texto exato do `render.yaml` e das 3 linhas do `donos.json`, prontos para aplicar;
- os testes;
- o acompanhamento do diagnóstico e do primeiro "Atualizar visitas".

## (b) O que só ele pode fazer, e por quê
1. **A senha da Máxima.** Usuário e senha não podem passar por nenhum agente nem por recado (regra 5), e o time não tem conta na Máxima. Só ele cria o usuário do robô ou decide usar um que já existe, e só ele cola a senha no Render.
2. **As mudanças de governança** (`donos.json` e `render.yaml`). O guardião não deixa nenhum agente gravar esses arquivos, nem o gerente nem o po, e o time não contorna isso. É preciso a sessão dele, e o "autorizo" é dele (a delegação ao po vale para simulações, não para governança).
3. **O painel do Render**: confirmar o sync do Blueprint (o serviço novo) e preencher as 2 variáveis secretas.

**O mínimo de passos, se ele topar:**
- **Passo único na sessão dele:** abrir uma sessão do Claude Code como `alexandre` e colar uma frase que o time deixa pronta: "aplique o patch `docs/desenho/T-0045-governanca.diff` e abra o PR". Esse patch junta as governanças 1 e 2 num PR só, e o time entrega o resto.
- **No Render, uma tela:** colar o usuário e a senha da Máxima (2 campos) no serviço novo.
- **Na Máxima:** pode ser zero passo, se ele aceitar que o robô na nuvem use o mesmo login que o robô do PC já usa. Isso troca a decisão 5 A (usuário próprio) por usar o login atual. O custo é que, se a Máxima bloquear o acesso vindo da nuvem, o robô do PC também pode ser bloqueado.

## (c) Um caminho sem nenhum passo dele: visitas pelo PC, no automático (recomendação)
O site já recebe as visitas pelo pacote do robô do PC. O time pode fechar o resto pelo PC, que já tem a credencial da Máxima guardada no notebook:
1. **Todo dia, na rodada da manhã**, o robô do PC baixa da Máxima os dias que faltam (ontem e os não fechados), com a mesma regra do núcleo, e o site recebe pelo pacote.
2. **O botão "Atualizar visitas" do site** (admin e gerente) vira um pedido na fila que o robô do PC atende na volta seguinte, de até 30 minutos. A fila e a volta de 30 minutos já existem.

Tudo isso é código `.py`, que chega ao notebook pela rotina diária (regra 11), sem "instale", sem `render.yaml`, sem `donos.json` e sem senha nova. Previsão: uns 4 a 6 horas de time (modulo-robo, modulo-web e testes), com simulação da tela antes.

**O que se perde nesse caminho:**
- Só funciona com o notebook do robô ligado e com a sessão aberta. Com ele desligado, não há visita nova nem "Atualizar visitas".
- O pedido do site não é na hora: espera a volta de até 30 minutos do robô.
- O serviço na nuvem (o diagnóstico, a independência do PC) fica guardado para quando ele quiser; o que já foi feito para a nuvem não se perde.
- Custo do Render: zero a mais.

**Recomendação:** seguir agora pelo caminho (c), sem nenhum passo dele, e deixar o (b) para quando ele quiser tirar a dependência do notebook. Se ele disser "c", o time começa já.
