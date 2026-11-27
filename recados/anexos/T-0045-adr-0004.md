# ADR 0004 — "Atualizar visitas" da Máxima no Render: o navegador roda num serviço do Render, e a senha fica só lá

- **Status:** proposta (T-0045), **sem código**. Ela vai ao Alexandre pelo po com as decisões D1 a D5 (§10). O `render.yaml` só muda depois, num PR de governança com o "autorizo" do Alexandre.
- **Data:** 2026-11-27
- **Tarefa:** T-0045 · **Autor:** engenheiro-software
- **Depende de:**
  - ADR 0001: web no Render, modelo M2, perfis (§4.5), adendos 2 e 5 (dado de cliente no Render);
  - ADR 0002: rotina diária (regra 11) e o limite 3 (`/saude`);
  - ADR 0003 (T-0035, PR em aberto): pacote por farol. Ela não muda nada aqui, só o caminho do `vc_visitas` até o site.
- **Consumidores:**
  - modulo-robo: `visitas_maxima.py` (o `Robo`), `bap_automation.py` (a importação na volta de 30 min), `atualizar_visitas.bat` (sem mudança) e a pasta nova `nuvem/visitas/`;
  - modulo-rota: `visitas_nucleo.py` (2 funções puras);
  - modulo-web: `web/app/` (API, tela "Atualizar visitas", `/saude`);
  - testes; designer-ux (simulação da tela, regra 10).
- **Recados:**
  - R-20261126-182728-alexandre: a opção C, contra a recomendação do po (texto literal no recado);
  - R-20261126-175814-gerente-projetos: o plano da migração (T-0043 "Pedir rodada", a volta de 30 min);
  - `recados/anexos/T-0033/inventario-pc-site.md`, item 24 e §2.3.

## 1. Contexto

**Hoje, no PC** (`visitas_maxima.py`, chamado pelo `atualizar_visitas.bat` ou pelo botão do Farol de Visita):
1. pede usuário e senha da Máxima na hora (a senha nunca é gravada) e abre o Edge/Chrome pelo Playwright;
2. entra no maxGestão > Painel Auditoria e marca todas as filiais, supervisores e representantes;
3. **baixa**, dia a dia e vendedor a vendedor, o Espelho de Rotas em Excel: `RELATORIOS/Visitas/ANALITICO/<VENDEDOR>/VISITA-<VENDEDOR>-DD-MM-AAAA-HH-MM.xlsx`;
4. **monta**, com esses Excel, `diario/AAAAMMDD.csv` (`visitas_nucleo.montar_dia`), `AAAAMM.csv` (`montar_mes`), `ACOMPANHAMENTO_VISITAS_BAP.xlsx` (`atualizar_acompanhamento`, só acrescenta linha) e `VISITAS_POR_CLIENTE.xlsx` (`atualizar_por_cliente`, retrato refeito);
5. junta a Prospecção do Forms (`prospeccao_forms.atualizar`), que lê o Excel de respostas **sincronizado pelo OneDrive no PC**.

**No site,** o Farol de Visita (`vc_visitas`) mostra o que o robô mandou no pacote, montado no PC a partir desses arquivos (`bap_automation._FONTE_BAIXADO_WEB`).

**O que muda com a opção C:** só o passo 3 (o navegador e a senha) vai para o Render. Os passos 4 e 5 **continuam no PC**, com o mesmo código, por três motivos:
- a Prospecção depende do OneDrive do PC; lê-la do Render exigiria o Graph (regra 9);
- a aderência ao Planner lê as rotas exportadas que estão no PC (`visitas_nucleo._RX_ROTA_PLANNER`);
- o `ACOMPANHAMENTO_VISITAS_BAP.xlsx` é a planilha de acompanhamento da regra 7 (só acrescentar). Ela fica com um dono só, o PC.

**Números de hoje** (da pasta `RELATORIOS/Visitas`, sem nome):
- 15 representantes por dia (17 pastas no ANALITICO);
- 1.622 Excel em 111 dias, com 22 a 51 KB cada (mediana de 26 KB): cerca de 0,4 MB por dia;
- tempo por dia no PC, pelo `_baixados.json` (out–nov/2026): de 77 a 310 s, em geral de 107 a 152 s;
- o robô do PC roda na volta de 30 min, das 07h às 21h (ATIVAR_ROBO_30MIN), e o web do Render é o Starter de 512 MB (`render.yaml`).

## 2. Onde roda o Playwright no Render

### 2.1 Memória e CPU estimadas

Tudo [SUPOSIÇÃO]: não há Playwright neste ambiente e não se mede sem a Máxima. A conta vem do Chromium sem tela com uma SPA pesada (o maxGestão é React com MUI DataGrid, e o visualizador do Espelho é um gerador de relatório em JavaScript). A medida real sai da rodada de diagnóstico (§9, passo 6).

| Parte | Memória (pico) |
|---|---|
| Python e o `Robo` | 40–60 MB |
| Driver do Playwright (Node) | 50–80 MB |
| Chromium: processo principal, GPU e utilitários | 100–150 MB |
| Aba do maxGestão (grade com 15 linhas) | 150–250 MB |
| Visualizador do Espelho (aba ou iframe) e o download | 80–200 MB |
| **Total do navegador** | **cerca de 420 a 740 MB** |
| O site de hoje (`uvicorn`, 1 processo, com o pacote; ADR 0003, §1) | 70–140 MB, com pico perto de 512 MB no recebimento |

- **CPU:** o navegador fica quase todo o tempo esperando a Máxima. Com 0,5 CPU (Starter), a pintura da grade e do visualizador deve levar de 1,5 a 2 vezes o tempo do PC [SUPOSIÇÃO]. Com 1 CPU (Standard), fica perto do PC.
- **Não cabe no Starter de 512 MB junto com o site.** Quando falta memória, o Render derruba o processo inteiro, e o site cai junto com a rodada.
- Sozinho num serviço de 512 MB, fica no limite: o visualizador do Espelho pode estourar. Mesmo assim, é o ponto de partida da medição.

### 2.2 Opções

Preços [SUPOSIÇÃO: a tabela do Render como a conheço, não conferida em render.com/pricing; o Alexandre ou o po confirma no painel]. Web e worker: Starter US$ 7 (512 MB, 0,5 CPU), Standard US$ 25 (2 GB, 1 CPU). Cron job: cobrado por minuto de rodada, Starter cerca de US$ 0,00016/min e Standard cerca de US$ 0,00058/min, com mínimo de US$ 1 por mês.

| | Opção | Custo/mês a mais | A favor | Contra |
|---|---|---|---|---|
| W1 | **No próprio serviço web** (`bap-central`), numa thread ou num processo filho | **+US$ 18**: o site sobe do Starter para o Standard | um serviço só; o disco já está lá | o navegador disputa memória e CPU com o site, e uma falta de memória derruba os dois; a senha da Máxima fica no serviço que atende a internet; o site precisa trocar o runtime Python pelo Docker (o Chromium pede bibliotecas do sistema), o que muda o deploy do site inteiro; todo deploy (a cada commit no `main`, ADR 0001, adendo 4) mata a rodada no meio |
| W2 | **Worker separado** (`type: worker`), sempre ligado | +US$ 7 (Starter, no limite da memória) ou +US$ 25 (Standard) | isolado do site; sem tempo-limite | paga 24 h para usar cerca de 15 min por dia; não divide o disco do site (no Render, o disco é de um serviço só), então precisa da mesma API da W3 |
| **W3** | **Cron job separado** (`type: cron`, Docker), que acorda a cada 10 min, olha se há trabalho e sai | **cerca de US$ 1 a 3** no Standard (conta na §4.3) | isolado do site; paga só o minuto rodado; a senha fica **só** nele, fora do serviço que atende a internet; o Render roda uma execução por vez; o deploy do site não interrompe a rodada | sem disco: manda os Excel ao site pela API, como o robô do PC; acorda de 10 em 10 min (o botão leva até 10 min para começar); a imagem Docker do Playwright (cerca de 2 GB) é refeita quando o código dele muda |

Características do Render que a W3 usa, todas [SUPOSIÇÃO, a conferir no diagnóstico]:
- o cron job aceita Docker e o Standard, mas não aceita disco;
- ele fala com o web pela rede privada da mesma região (`fromService ... property: hostport`);
- o horário do `schedule` é em UTC;
- a execução dura no máximo 12 h, e a próxima não começa enquanto a anterior roda.

### 2.3 Recomendação (D1): W3 no Standard

- **W3, cron job `bap-visitas-maxima`, Docker, Standard (2 GB, 1 CPU).** Por minuto, a diferença entre Starter e Standard é de centavos no mês, e o Standard tira o risco de faltar memória.
- Se o diagnóstico medir **pico abaixo de 350 MB**, ele desce para o Starter (outro PR de governança).
- Ela atende a decisão C: **roda no Render, não no PC, e a senha fica no Render.** É um serviço a mais da mesma conta, ligado ao site pelo botão. A tela continua sendo o site.
- **O site (`bap-central`) continua no Starter de US$ 7**, sem mudança de runtime.
- W1 é a leitura literal de "o próprio site roda o navegador". Ela custa US$ 18 a mais por mês, põe a senha no serviço exposto e faz o site cair junto se faltar memória. Por isso não é a recomendação.

### 2.4 Texto proposto para o `render.yaml` (governança; o PR é à parte e só com "autorizo")

```yaml
  - type: cron
    name: bap-visitas-maxima
    runtime: docker
    plan: standard             # [SUPOSIÇÃO] por minuto de rodada; desce a starter se o pico < 350 MB
    region: oregon             # a mesma do bap-central (rede privada)
    schedule: "*/10 10-23,0-1 * * *"   # UTC = a cada 10 min, das 06h00 às 21h50 de Manaus
    dockerfilePath: ./nuvem/visitas/Dockerfile
    dockerContext: .
    buildFilter:               # só refaz a imagem quando o código dela muda
      paths:
        - nuvem/visitas/**
        - visitas_maxima.py
        - visitas_nucleo.py
        - requirements-visitas.txt
    envVars:
      - key: TZ
        value: America/Manaus  # o HH-MM do nome do Excel e o "hoje" em Manaus
      - key: BAP_WEB_HOSTPORT
        fromService: {type: web, name: bap-central, property: hostport}
      - key: BAP_VISITAS_TOKEN
        sync: false            # o Alexandre cria; o mesmo valor no bap-central
      - key: BAP_MAXIMA_USUARIO
        sync: false            # o Alexandre cria no painel
      - key: BAP_MAXIMA_SENHA
        sync: false            # o Alexandre cria no painel; só neste serviço
```

- No `bap-central` entra só `BAP_VISITAS_TOKEN` (`sync: false`).
- A imagem parte da oficial do Playwright para Python (`mcr.microsoft.com/playwright/python:v<versão>-noble`, Python 3.12). A versão do pip e a da imagem ficam fixadas juntas no `requirements-visitas.txt` (engenheiro-software). [SUPOSIÇÃO: a versão sai do diagnóstico.]
- **Sem dependência nova no PC:** o robô DT-AMADMBAP-03 importa com `requests` e a biblioteca padrão. O Playwright e o `openpyxl` já estão no `requirements.txt` do PC.

## 3. Quando roda e quem aperta

### 3.1 Agenda e botão (D2 e D3)

- **Um cron só,** de 10 em 10 min das 06h00 às 21h50 de Manaus. A cada volta, ele pergunta ao site se há trabalho (`GET /api/visitas/trabalho`, §5.2) e decide com a função pura `deve_rodar(agora, estado) -> motivo | None`, em `nuvem/visitas/`. A volta sem trabalho sai em segundos.
- **Agenda (recomendação D2 = A):** às **06h00**, todo dia (sábado e domingo também, como o PC), baixa **ontem**, que fecha o dia. Com falha da Máxima, tenta de novo às 06h30, 07h00 e 07h30.
- **Botão "Atualizar visitas"** no Farol de Visita do site:
  - pede um período, com padrão "dias ainda abertos até hoje" e **no máximo 7 dias**. Período maior continua no PC (até 93 dias);
  - a próxima volta, em até 10 min, atende o pedido.
- **Quem aperta (recomendação D3 = A):** `admin` e `gerente`. O "Baixar de novo" (refazer dia fechado) e o "Retomar" (§6) ficam só com o `admin`. Os outros perfis veem o estado e não veem o botão. O corte é feito no servidor, com teste de 403 por perfil (ADR 0001, §4.5).
- **O botão do PC continua** (decisão do R-20261126-182728 até a entrega, e depois como reserva). O desligamento dele segue a T-0044: 2 semanas iguais e o "ok" do Alexandre.

### 3.2 Duas rodadas que se cruzam

O site guarda uma **concessão** (lease): só uma rodada ativa por vez, gravada em disco (`/var/data/visitas/estado.json`) para sobreviver ao deploy. A concessão vale 10 min e é renovada a cada vendedor.

| Caso | O que acontece |
|---|---|
| Botão apertado durante uma rodada | o pedido entra na fila (no máximo 1 pendente). Apertar de novo mostra "Já pedido às HHhMM". Ele é atendido na volta seguinte ao fim da rodada |
| Agenda das 06h00 e um pedido juntos | uma rodada só, com os dias dos dois |
| Duas execuções do cron ao mesmo tempo (atraso do Render) | a segunda recebe 409 ao pedir a concessão e sai |
| Rodada morta (memória, tempo) | a concessão vence em 10 min. Os dias já enviados ficam, e a volta seguinte baixa só o que falta |
| Pedido maior que uma rodada (45 min, §4) | a rodada para no fim de um dia, e o pedido continua na volta seguinte, até 3 rodadas |
| "Atualizar visitas" do PC durante a rodada do site | o PC consulta `GET /api/visitas/estado` e avisa: "O site está baixando agora; baixar aqui também pode derrubar a sessão da Máxima. Continuar?" Se a pessoa seguir, os dois gravam com nomes diferentes, e vale o Excel mais novo por vendedor e dia (`espelhos_do_periodo`, regra de hoje). [SUPOSIÇÃO: a Máxima pode aceitar uma sessão só por usuário] |

## 4. Tempo de cada rodada e limites

| Etapa | No PC (medido) | No Standard [SUPOSIÇÃO] |
|---|---|---|
| Login, maxGestão, Painel Auditoria e filtros | cerca de 1 a 2 min | 1,5 a 3 min |
| Um dia (15 vendedores) | 77 a 310 s, em geral de 107 a 152 s | 2,5 a 5 min |
| **Agenda (1 dia)** | — | **cerca de 5 a 8 min** |
| **Botão com 7 dias** | — | **cerca de 20 a 40 min** |

- **Limite da rodada:** 45 min (`RODADA_MAX_MIN`), conferido no fim de cada dia. O que faltar continua na volta seguinte (§3.2). O teto do Render (12 h) nunca é o freio.
- **Do fim da rodada até a tela:** até 30 min para o robô do PC importar (§5), mais a rodada do robô (cerca de 9 min). Na tela, o "baixado em" do farol muda nessa volta.
- **Conta do custo (D1, Standard):** a agenda dá 30 × 8 min; 10 botões de 25 min por mês; e 96 voltas por dia sem trabalho, de 30 s cada (a partida do contêiner [SUPOSIÇÃO: se for cobrada]). São cerca de 1.900 min por mês, **cerca de US$ 1 a 3 por mês**.

## 5. Como os arquivos voltam ao PC sem perder dado

### 5.1 O caminho

```
cron (Render) --POST dia a dia--> site (/var/data/visitas/lotes) <--GET na volta de 30 min-- robô do PC
                                                                   --grava ANALITICO, monta, confirma-->
```

1. **Na nuvem,** a cada dia completo, o cron manda ao site um **lote do dia**: um JSON com gzip que leva `dia`, `baixado_em` (Manaus), `extras` (GPS e versão do app por vendedor, como lidos na janela), `equipe` (o `maxima_equipe.json` lido na tela), `erros` (quantos vendedores falharam) e `arquivos` (o nome de cada Excel, o sha256 e o conteúdo). São cerca de 0,5 MB por dia.
2. **No site,** o lote fica em disco com um `seq` crescente e uma `epoca`, no mesmo desenho da fila de edições (`web/app/edicoes.py`). A gravação é atômica. O site **nunca mostra nem serve** o Excel ao navegador.
3. **No PC,** o robô traz os lotes na volta de 30 min, **antes de montar o pacote**, no mesmo ponto do `sincronizar_edicoes_web` (`bap_automation.passo_pacote_web`). Assim, o pacote dessa rodada já sai com as visitas novas. A função nova é `sincronizar_visitas_web(raiz, base, token, ...)`, que nunca levanta e nunca derruba a rodada:
   1. `GET /api/visitas/lotes?desde=<seq>` e o lote, com a conferência do sha256 de cada arquivo. Um arquivo que não confere recusa o lote, com o motivo "arquivo corrompido", e a nuvem baixa o dia de novo;
   2. **grava os Excel no `ANALITICO`,** sempre por `.tmp` + `os.replace`:
      - o nome tem de casar com `visitas_nucleo._RX_ARQ_ANALITICO`, sem `/`, `\` ou `..`;
      - a pasta é o `nome_limpo` do vendedor;
      - já existe com o mesmo sha256: pula (idempotente);
      - já existe com outro conteúdo: grava com o sufixo `-2`, `-3`… (`arquivo_analitico`).
      - **Nunca sobrescreve nem apaga.**
   3. `gravar_equipe_maxima` (mescla); `anotar_baixado` do dia **com o `baixado_em` da nuvem**, não com a hora da importação (RN-VIS-001, abaixo); `montar_dia(raiz, d, extras)`; `montar_mes` dos meses tocados, anotado com o maior `baixado_em` do mês;
   4. uma vez por importação, o mesmo fim do botão do PC: `atualizar_acompanhamento` (só acrescenta dia fechado), `atualizar_por_cliente` e `prospeccao_forms.atualizar`. Esse fim sai do `visitas_maxima.executar` para uma função só, `depois_de_baixar(raiz, log)`, chamada pelo botão do PC e pela importação (uma regra num lugar só);
   5. registra em `RELATORIOS/_VISITAS_WEB/IMPORTADOS_VISITAS_WEB_<máquina>.jsonl` (só acréscimo: seq, dia, quantos arquivos, status) e confirma com `POST /api/visitas/lotes/confirmar`. Confirmação que falha é repetida na volta seguinte, e o `.jsonl` impede gravar duas vezes.
4. **Excel aberto** (`ACOMPANHAMENTO_VISITAS_BAP.xlsx` aberto por alguém): os arquivos do dia já ficaram gravados, e o acompanhamento devolve "aberto no Excel" (comportamento de hoje). Na volta seguinte, ele acrescenta o que faltou, porque a função é idempotente.
5. **O Farol de Visita e o Farol de Metas do PC** leem `RELATORIOS/Visitas` como hoje e não mudam. Os arquivos ficam iguais aos que o botão do PC grava.

**Regras novas** (o po registra no `docs/produto/03-regras.md`; os testes citam):
- **RN-VIS-001:** o dia está fechado quando foi baixado num dia depois dele, **pela hora da baixa** (nuvem ou PC), em Manaus. A importação não fecha o dia. Entre a hora do PC e a da nuvem, vale a maior (`juntar_baixado`, função pura).
- **RN-VIS-002:** a importação só acrescenta. Ela nunca sobrescreve nem apaga Excel do `ANALITICO`, e o acompanhamento só ganha linha de dia fechado (regra 7).
- **RN-VIS-003:** uma rodada da nuvem por vez (concessão de 10 min). O pedido do botão espera na fila.
- **RN-VIS-004:** senha recusada ou confirmação pedida pela Máxima **pausa** as rodadas da nuvem até o "Retomar" do admin. Não há segunda tentativa de login.
- **RN-VIS-005:** dia com vendedor que falhou é baixado de novo **uma vez** na agenda seguinte. Depois disso, ele fica como está ("Baixar de novo" pelo admin ou pelo PC).

### 5.2 A API (vira o contrato `.coord/contratos/visitas-nuvem.md` v1, do engenheiro-software, depois das decisões)

| Quem chama | Rota | Token | Para quê |
|---|---|---|---|
| cron | `GET /api/visitas/trabalho` | `BAP_VISITAS_TOKEN` | pausa, pedido pendente, índice `{AAAAMMDD: baixado_em, incompleto}` e rodada ativa |
| cron | `POST /api/visitas/rodada` | idem | pede a concessão (201 ou 409) |
| cron | `POST /api/visitas/rodada/<id>/progresso` | idem | fase, dia e contagem; renova a concessão |
| cron | `POST /api/visitas/rodada/<id>/dia/<AAAAMMDD>` | idem | o lote do dia (gzip, `X-BAP-SHA256`, teto de 8 MB, idempotente por rodada e dia) |
| cron | `POST /api/visitas/rodada/<id>/fim` | idem | `ok`, `parcial` ou `erro`, com **código fixo** e fase (§6) |
| robô do PC | `GET /api/visitas/lotes?desde=` · `GET /api/visitas/lote/<seq>` · `POST /api/visitas/lotes/confirmar` | `BAP_WEB_TOKEN` | a volta de 30 min |
| robô do PC | `GET /api/visitas/estado` | idem | o aviso do botão do PC (§3.2) |
| tela | `GET`/`POST /visitas/atualizar` · `POST /visitas/retomar` | sessão e perfil | botão, estado, histórico e retomar (só admin) |

- **Nome de vendedor nunca vai na URL** (o Render registra o caminho): ele vai só dentro do corpo.
- **No disco do site,** em `/var/data/visitas/`:
  - `estado.json`;
  - `pedidos.jsonl` e `rodadas.jsonl`, só acréscimo;
  - `lotes/<seq>.json.gz`, que sai 7 dias depois de confirmado. O não confirmado sai em 30 dias, com aviso no `/saude`.
  - São cerca de 15 MB por mês, dentro do disco de 1 GB.
- **`/saude`** ganha `visitas: {ultima_rodada, status, codigo, pausado, lotes_a_importar}`, sem dado pessoal.
- **Publicação:** a web antes, o robô depois (ADR 0001, adendo 2). O robô novo trata o 404 da web antiga como "sem visitas da nuvem" e segue.

## 6. Falhas: o que o usuário vê e o que fica no PC

| Caso | Como a nuvem percebe | O que o site mostra | O que fica no PC | Depois |
|---|---|---|---|---|
| **A Máxima pede confirmação, captcha, 2FA, termo ou "novo dispositivo"** | depois do "Entrar", a página continua no `/login` sem mensagem de erro, ou aparece um captcha (iframe ou elemento) ou um texto de verificação. A função pura `classificar_login(url, texto, tem_captcha) -> codigo` dá o código `MAXIMA_CONFIRMACAO` | "A Máxima pediu uma confirmação que o site não faz sozinho. As atualizações do site estão pausadas. Use o Atualizar visitas do PC; o admin retoma aqui depois." | nada muda; o botão do PC funciona | **pausa** (RN-VIS-004). Nunca tenta resolver captcha nem repete o login |
| **Senha errada ou vencida** | a mensagem de erro do login. Ela não é copiada, vira só o código `MAXIMA_SENHA` | "A Máxima recusou o usuário ou a senha. Só o Alexandre troca no painel do Render; depois, o admin clica em Retomar." | nada | **pausa** imediata, sem segunda tentativa, para não bloquear a conta |
| **A tela da Máxima mudou** | um `ErroRobo` na fase: `login`, `maxgestao`, `menu`, `filtros`, `grade`, `espelho` ou `salvar`. Código `TELA_MUDOU:<fase>` | "A tela da Máxima mudou (etapa: filtros). Os dias que já vieram estão salvos. Use o botão do PC até a correção." | os dias completos chegam normalmente; nada é apagado | 2 rodadas seguidas na mesma fase pausam a agenda, e o `/saude` mostra. A correção é do modulo-robo, testada no PC com "Mostrar o navegador" |
| **Um vendedor falhou** (o resto foi) | igual ao PC: o vendedor não para os outros | "1 Excel com erro (12/11)". O nome do vendedor aparece só na tela, para admin e gerente, e nunca no log | o dia chega com os outros | nova tentativa na agenda seguinte (RN-VIS-005) |
| **A Máxima está fora** (sem resposta, 5xx) | tempo esgotado no `goto`, ou erro HTTP. Código `MAXIMA_FORA` | agenda: "A Máxima não respondeu às 06h00; tentamos de novo às 06h30." Botão: "A Máxima não respondeu. Tente mais tarde." | nada | agenda: até 3 novas tentativas, de 30 em 30 min; botão: o pedido sai da fila |
| **Falta de memória ou de tempo no Render** | a concessão vence sem o `fim`. Código `RODADA_INTERROMPIDA` | "A rodada parou sem terminar (memória ou tempo do serviço). O que veio está salvo." | os dias já enviados chegam | a volta seguinte baixa o que falta. 2 seguidas aparecem no `/saude`, e o plano é revisto |
| **Site fora ou em deploy** | o POST do dia falha 3 vezes (com 30 s entre elas) | nada na hora. Depois, a rodada aparece como "parcial" | nada | o dia volta a ser baixado depois (sem disco, a nuvem não guarda) |
| **Robô do PC parado** (notebook desligado, fora das 07h–21h) | — | "Baixado às 06h08 · esperando o PC importar" | nada até o robô voltar | os lotes esperam no site até 30 dias; nada se perde |

- **O que o usuário nunca vê:** a senha, o usuário da Máxima, o texto cru do erro da Máxima, a URL com `PWE=` (o `url_limpa` já mascara).
- **Print da tela do erro** (D5): o print do PC (`Visitas/_erros`) pode mostrar nome de vendedor e de cliente. **Recomendação B:** a nuvem não tira print, e o código e a fase bastam; a investigação é feita no PC, que tem o print. A opção A guarda o print no disco do site, só para o admin, por 7 dias.

## 7. Segurança

- **A senha só no Render:** `BAP_MAXIMA_SENHA` e `BAP_MAXIMA_USUARIO` (`sync: false`) ficam **só no cron job**, nunca no `bap-central`, que atende a internet.
  - O Alexandre cria os valores no painel. O time nunca vê nem pede o valor. Nada disso vai em código, log, recado ou commit.
  - O cron lê com `os.environ.pop(...)` **antes** de abrir o Playwright, para que o driver (processo filho) não herde a senha.
  - A senha vai só no `fill` do login e em seguida vira `None` (como o `Robo.rodar` já faz).
- **Proibido no cron:**
  - `DEBUG=pw:*`, porque o `pw:api` imprime o texto do `fill`; o `rodar.py` recusa partir com ele;
  - trace, vídeo, HAR e `page.on("console")`;
  - print depois do `fill` (com a opção D5 = B, nenhum print).
  - Os testes conferem tudo isso.
- **Cookies e sessão:** contexto novo a cada rodada, sem `storage_state`. O contêiner do cron é descartado no fim, e o cron não tem disco. **Nada da sessão da Máxima é guardado**, nem no disco do site: o cookie é credencial e não deve ficar no serviço exposto.
- **Logs sem dado pessoal (regra 6):**
  - o `Robo` hoje escreve o nome do vendedor no log ("NOME ✔"). O modulo-robo troca o `log` por **eventos** (`evento`, `dia`, `n`, `codigo`) e uma função `texto_do_evento` de dois modos: no PC, com nome (a janela de hoje); na nuvem, sem nome;
  - um filtro final mascara o usuário e a senha, se aparecerem (como o `replace(_tk, "***")` das edições);
  - teste com nomes fictícios: nenhum nome entra no log da nuvem.
- **Tokens:** `BAP_VISITAS_TOKEN` é novo e só abre as rotas do cron (`/api/visitas/trabalho` e `/api/visitas/rodada*`). Ele não envia pacote nem lê edições. A comparação é em tempo constante. O robô do PC usa o `BAP_WEB_TOKEN` de hoje. O HTTPS pela URL pública é a reserva da rede privada.
- **Dado de cliente no disco do Render:** o Espelho traz código, nome e endereço de cliente. O adendo 5 da ADR 0001 já leva código e nome de cliente do `vc_visitas` ao Render, mas o endereço é novo. Por isso:
  - o lote é **só trânsito**: nenhuma rota o mostra, e ele sai 7 dias depois de importado;
  - [SUPOSIÇÃO: o Espelho não traz CNPJ nem telefone; conferir no diagnóstico. Se trouxer, o lote continua só em trânsito, e isso vai ao Alexandre.]
- **Conta da Máxima (D4):** hoje é o login do Alexandre (`docs/produto/06-integracoes.md`). Com um usuário próprio do robô, que só vê o Painel Auditoria, um vazamento do painel do Render expõe menos.
- **Regra 9:** nada de Microsoft 365 ou Graph. A Prospecção continua lida no PC.

## 8. Testes (agente testes; nomes com a RN)

- `test_RN_VIS_001_dia_fecha_pela_hora_da_baixa_nao_da_importacao`, `test_RN_VIS_001_juntar_baixado_vale_a_maior`;
- `test_RN_VIS_002_importacao_nunca_sobrescreve_grava_com_sufixo`, `test_RN_VIS_002_mesmo_sha_pula`, `test_RN_VIS_002_nome_com_barra_ou_ponto_ponto_recusado`, `test_RN_VIS_002_acompanhamento_so_acrescenta`;
- `test_RN_VIS_003_segunda_concessao_409`, `test_RN_VIS_003_concessao_vencida_libera`, `test_RN_VIS_003_concessao_sobrevive_ao_reinicio`;
- `test_RN_VIS_004_senha_recusada_pausa_sem_segunda_tentativa`, `test_RN_VIS_004_classificar_login_captcha_confirmacao`;
- `test_RN_VIS_005_vendedor_que_falhou_tenta_uma_vez`;
- `deve_rodar`: 06h00 com ontem aberto; pausado; pedido; fora da janela;
- perfis: 403 no botão para `diretor`, `pos_venda`, `pre_venda` e `vendas`, e 403 no refazer e no retomar para o `gerente`;
- segredo: log com usuário, senha e nomes fictícios; `DEBUG=pw:api` recusado; o `environ` sem a senha depois da leitura;
- ponta a ponta sem rede: Excel de exemplo **sem dado pessoal** (fixture gerada) → lote → importação → `diario/AAAAMMDD.csv` igual ao do PC com o mesmo Excel.
- **Diagnóstico no Render** (§9, passo 6): pico de memória pelo `memory.peak` do cgroup, tempo por fase, confirmação da Máxima a partir do IP do Render. O resultado vai ao Alexandre antes de ligar a agenda.
- **Conferência de 5 dias úteis:** o mesmo dia baixado pelo PC e pela nuvem dá o mesmo cabeçalho do Espelho por vendedor.

## 9. Plano por dono

| # | Dono | O quê | Tamanho | Depende de |
|---|---|---|---|---|
| 1 | engenheiro-software | contrato `.coord/contratos/visitas-nuvem.md` v1 (§5.2, com corpos e códigos); `requirements-visitas.txt`; propostas de governança: `render.yaml` (§2.4) e a linha `nuvem/**` → modulo-robo no `.coord/donos.json` | P (3 h) | decisões D1 a D5 |
| 2 | modulo-rota | `visitas_nucleo`: as funções puras `dias_a_baixar(indice, de, ate, hoje, refazer)` (sai do `visitas_maxima.plano` e do `dia_fechado`) e `juntar_baixado` | P (2 h) | 1 |
| 3 | modulo-robo | `visitas_maxima.Robo`: canal do navegador configurável (na nuvem, o Chromium da imagem), log por eventos sem nome, `ao_fechar_dia(d, resultado)`, `classificar_login` e códigos fixos por fase; `depois_de_baixar` fora do `executar`. O botão do PC continua igual, mais o aviso do §3.2 | M (5 h) | 1, 2 |
| 4 | modulo-web | API do §5.2, concessão e fila em disco, retenção, `/saude`, tela "Atualizar visitas" no Farol de Visita (botão, estado, histórico, Retomar), perfis | G (8 h) | 1 e a simulação do item 5 |
| 5 | designer-ux | simulação da tela (PNG, antes × depois), regra 10 | P (1 h) | 1 |
| 6 | modulo-robo | `nuvem/visitas/` (`rodar.py`, `deve_rodar`, `Dockerfile`) e `bap_automation.sincronizar_visitas_web` na volta de 30 min | M (6 h) | 3, 4 (web no ar antes) |
| 7 | testes | §8 e a fixture sem dado pessoal | M (5 h) | 2, 3, 4, 6 |
| 8 | Alexandre (pelo po) | "autorizo" do PR do `render.yaml` e do `donos.json`; cria no painel `BAP_MAXIMA_USUARIO`, `BAP_MAXIMA_SENHA` e `BAP_VISITAS_TOKEN` (este também no `bap-central`) | — | 1, 6 |
| 9 | modulo-robo + testes | **diagnóstico** (`rodar.py --diagnostico`: 1 dia e 2 vendedores, só as medidas, sem lote), resultado ao Alexandre; depois, a agenda ligada e a conferência de 5 dias úteis | P (2 h) + acompanhamento | 8 |

- **Ordem:** 1 → (2 ∥ 4 ∥ 5) → 3 → 6 → 7 → 8 → 9.
- **Web antes do robô:** o PR do item 4 vai ao ar antes do "instale" do item 6 no PC.
- **modulo-rota** entra só no item 2: a aderência ao Planner fica no PC e não muda.
- **Total:** cerca de 32 h de time, mais o diagnóstico.

## 10. Decisões ao Alexandre (com recomendação)

Do que se trata: como a atualização das visitas da Máxima vai rodar no Render, que é a opção C já escolhida. Nenhuma das decisões volta atrás na C.

| # | Pergunta | A | B | Recomendação |
|---|---|---|---|---|
| **D1** | Onde o navegador roda no Render | **Um serviço à parte (cron job) que só acorda para baixar**, cobrado por minuto: cerca de US$ 1 a 3 por mês a mais. O site continua no plano de US$ 7, e a senha fica só nesse serviço | **Dentro do próprio site:** o site sobe para o plano de US$ 25 (US$ 18 a mais por mês), a senha fica no serviço aberto à internet, e o site cai se faltar memória | **A** |
| **D2** | Quando roda sozinho | **Às 06h00, todo dia**, baixando ontem, mais o botão | às 06h00 e às 12h30, mais o botão | **A**: menos custo, e o meio-dia fica pelo botão |
| **D3** | Quem aperta "Atualizar visitas" no site | **admin e gerente**. "Baixar de novo" e "Retomar" só o admin | só o admin | **A** |
| **D4** | Que login da Máxima o site usa | **o Alexandre pede à Máxima um usuário só para o robô**, que só vê o Painel Auditoria; até ele sair, vale o login do Alexandre | o login do Alexandre, de vez | **A** |
| **D5** | Print da tela quando dá erro na nuvem | guardado no site, só para o admin, por 7 dias (pode mostrar nome de vendedor e de cliente) | **sem print**: o código e a etapa bastam, e o print sai do botão do PC | **B** |

Resposta pronta para copiar, se seguir as recomendações: **"1 A / 2 A / 3 A / 4 A / 5 B"**.

Depois das decisões, e não agora:
- o "autorizo" do PR do `render.yaml` e do `donos.json` (item 8 da §9);
- os 3 segredos, que o Alexandre cria no painel.

## 11. Consequências e riscos

- **A Máxima pode estranhar o IP do Render** (EUA, Oregon) e pedir confirmação a cada login, ou bloquear. É o maior risco [SUPOSIÇÃO]. O diagnóstico mostra isso antes de ligar a agenda. Se acontecer, a RN-VIS-004 pausa e o botão do PC segue. Saídas, numa ADR nova:
  - a liberação dos IPs de saída do Render, que o Render publica por região, junto à Máxima;
  - a volta à opção A do po (senha no cofre do notebook do robô).
- **Sessão única na Máxima** [SUPOSIÇÃO]: o PC e a nuvem ao mesmo tempo podem derrubar um ao outro. Por isso existe o aviso do §3.2.
- **Os termos de uso da Máxima** valem para a automação no Render como valem hoje no PC. Essa confirmação é do Alexandre.
- **Imagem Docker grande:** cada mudança no código das visitas refaz cerca de 2 GB de imagem. O `buildFilter` limita isso ao código da nuvem. Os minutos de build entram na franquia do Render [SUPOSIÇÃO].
- **Atraso até a tela:** da baixa ao farol do site, até cerca de 40 min (§4), e o robô do PC precisa estar ligado. Ir direto ao site exigiria montar o `vc_visitas` no Render, o que contraria o M2 (ADR 0001) e a Prospecção do PC.
- **Dois caminhos de baixa** (PC e nuvem) **com um só jeito de montar:** os arquivos e as funções são os mesmos (`depois_de_baixar`). A divergência fica limitada ao navegador e é vista na conferência de 5 dias.
- **Preços do Render não conferidos:** todos os valores em dólar são [SUPOSIÇÃO] e precisam ser confirmados no painel antes do "autorizo".
- **`bap_dados.VERSAO` fica em 27:** nada aqui toca o cache dos núcleos.
