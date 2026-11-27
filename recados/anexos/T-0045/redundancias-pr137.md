# T-0045 · PR #137 · Parecer de redundância e excesso (corretor-redundancias)

- **Escopo:** `git diff origin/main...origin/engenheiro-software/T-0045-visitas-render` (7 arquivos, +833 −1): ADR 0004, contrato `.coord/contratos/visitas-nuvem.md` v1, `docs/desenho/T-0045-render-yaml.md` e `.diff`, `requirements-visitas.txt`, `docs/decisoes/README.md` e o diário. Comparado com o `main`: `visitas_maxima.py`, `visitas_nucleo.py`, `bap_automation.py` (`sincronizar_edicoes_web`, `preparar_cobranca_web`, `passo_pacote_web`), `web/app/edicoes.py`, `web/app/cobranca.py` e `web/app/main.py` (`/saude`).
- **Head SHA revisado:** `a6c719c4e226d1b3894fc4dabed8ae8728f3ef76`.
- **Numeração:** o último RD usado é o RD-0071. Este parecer usa do RD-0072 ao RD-0081.
- **Resultado:** **não libera**. São 10 achados (9 médios, 1 baixo), todos em docs do desenho, nenhum em comentário ou título de teste.
- **Dono de todos os achados:** engenheiro-software (`node scripts/coord.mjs dono` nos 5 arquivos).
- **Rotina nova × robô do PC:** no geral, o desenho reaproveita: `depois_de_baixar` sai do `executar` para uma função só; `dias_a_baixar` sai do `plano` e do `dia_fechado`; a importação usa `arquivo_analitico`, `montar_dia`, `montar_mes` e `gravar_equipe_maxima`. Hoje o PC **não** baixa visitas sozinho (`bap_automation._FONTE_BAIXADO_WEB`: "o Atualizar visitas e manual no PC"), então a agenda das 06h00 não repete uma tarefa agendada que já existe. Ficam duas duplicações: o índice de dias baixados (RD-0076) e o laço `desde`/`epoca`/confirmar (RD-0077).

## Achados

### RD-0072 · A mesma regra escrita na ADR e no contrato, com textos diferentes
- **Onde:** ADR 0004 × `visitas-nuvem.md`. A ADR diz (linha 6): "Esta ADR diz o porquê; o contrato diz o formato". Na prática, os dois descrevem o mesmo formato:
  1. **Importação no PC:** ADR §5.1, item 3 (linhas 183-193) × contrato §4.5 (205-208). O contrato manda ler os passos na ADR ("Passos e regras: ADR 0004, §5.1") e logo depois repete `.tmp` + `os.replace`, o pulo pelo sha256, o sufixo `-2`, "Nunca sobrescreve nem apaga" e o `.jsonl`.
  2. **Segredos:** ADR §7 (242-246: `os.environ.pop`, a senha que vira `None`, `DEBUG=pw:*`, `CONFIG_INSEGURA`) × contrato §1 (24-25).
  3. **Falhas:** a tabela da ADR §6 (221-232) repete 10 dos 17 códigos do contrato §5 (229-247), com a coluna "Depois" em outras palavras. **Os dois já divergem:** no `SITE_FORA`, a ADR diz "o dia volta a ser baixado depois (sem disco, a nuvem não guarda)" (231) e o contrato diz "só no log do Render; o site vê `RODADA_INTERROMPIDA`" (243). O texto "Baixado às 06h08 · esperando o PC importar" (232) só existe na ADR, fora do contrato que guarda os textos.
  4. **Confirmação ou captcha no diagnóstico:** ADR §6 (234) × contrato §5.1 (262), quase literal (o "liberar na Máxima os IPs de saída do Render, ou voltar à opção A do po" aparece 2 vezes).
  5. **Sem print:** ADR §6 (235) × contrato §5 (227), além da D5 no §0 da ADR (31).
  6. **Aviso do PC:** o texto "O site está baixando agora; baixar aqui também pode derrubar a sessão da Máxima. Continuar?" está literal na ADR §3.4 (155) e no contrato §4.4 (201).
  7. **Plano pelo pico de memória:** ADR §2.3 (99) × contrato §6 (280). Só o contrato diz para qual plano sobe (`pro`).
  8. **Retenção dos lotes:** ADR §6 (232: "até 30 dias") e §7 (256: "sai 7 dias depois de importado") × contrato §2 (`LOTE_GUARDA_DIAS`, 46) e §7 (289). São 4 lugares para 2 números.
- **Tipo:** doc. **Impacto:** manutenção (a v2 do contrato vai ter de mudar 2 arquivos, e o item 3 já diverge) e decisão (no `SITE_FORA`, o modulo-web e o modulo-robo podem seguir textos diferentes).
- **Severidade:** média.
- **Proposta** (o formato fica no contrato; a ADR aponta para ele):
  1. Contrato:206, **antes:** "Passos e regras: ADR 0004, §5.1 (RN-VIS-001 e RN-VIS-002). Grava o Excel no `ANALITICO` por …" → **depois:** "Passos: (1) `GET /api/visitas/lotes?desde=<seq>` e cada lote, conferindo o sha256 de cada arquivo (se não conferir, `recusado:sha256`); (2) grava no `ANALITICO` (RN-VIS-002): `.tmp` + `os.replace`; nome que casa com `visitas_nucleo._RX_ARQ_ANALITICO`, sem `/`, `\` nem `..`; pasta = `nome_limpo`; mesmo sha256 = pula; outro conteúdo = sufixo `-2`, `-3`… (`visitas_maxima.arquivo_analitico`); nunca sobrescreve nem apaga; (3) `gravar_equipe_maxima`, `anotar_baixado` com o `baixado_em` da nuvem (RN-VIS-001), `montar_dia` e `montar_mes`; (4) `depois_de_baixar(raiz, log)`, uma vez por importação; (5) registro e `POST /api/visitas/lotes/confirmar`." ADR §5.1, item 3 (183-193), **depois:** "**No PC,** o robô traz os lotes na volta de 30 min, antes de montar o pacote (`bap_automation.sincronizar_visitas_web`; passos no contrato, §4.5), e monta com as mesmas funções do botão do PC (`depois_de_baixar`): uma regra num lugar só."
  2. ADR:242-246, **depois:** uma linha só: "O cron lê os 2 segredos antes de abrir o Playwright e não parte com depuração ligada (contrato, §1)."
  3. ADR §6: a tabela (219-232) sai. **Depois:** "Os códigos, o texto no site e o que acontece em seguida: contrato, §5." Ficam as linhas 234 e 236. No contrato §4.6 (215), a linha do `GET /visitas/atualizar` ganha o texto do robô parado: "lotes à espera do PC ("Baixado às HHhMM · esperando o PC importar")". O `SITE_FORA` fica com a versão do contrato.
  4. Contrato:262, **depois:** "Se o diagnóstico (§6) der `MAXIMA_CONFIRMACAO`, `MAXIMA_CAPTCHA` ou `MAXIMA_BLOQUEIO`, a agenda não é ligada (as saídas estão na ADR 0004, §6)."
  5. ADR:235 sai, porque a D5 do §0 e o contrato §5 já dizem.
  6. ADR:155, **antes:** "o PC consulta `GET /api/visitas/estado` e avisa: "O site está baixando agora; …Continuar?" Se a pessoa seguir, …" → **depois:** "o PC consulta o estado do site e pede confirmação (texto no contrato, §4.4). Se a pessoa seguir, …" (o resto continua).
  7. Contrato:280 sai (plano não é formato). ADR:99, **depois:** "Com **pico abaixo de 350 MB** no diagnóstico, ele desce para o Starter; acima de 1.600 MB, sobe para o Pro (os dois por PR de governança)."
  8. ADR:232, **depois:** "os lotes esperam no site (`LOTE_GUARDA_DIAS`, contrato §2); nada se perde". ADR:256, **depois:** "o lote é **só trânsito**: nenhuma rota o mostra, e ele sai pela retenção (`LOTE_GUARDA_DIAS`)". Contrato:289, **depois:** "o corpo do §3.4; sai pela `LOTE_GUARDA_DIAS`; o não confirmado sai com aviso no `/saude`".

### RD-0073 · O `render.yaml`, as suposições do Render, as linhas do `donos.json` e a ordem do merge, cada um em 2 ou 3 lugares
- **Onde:**
  1. **YAML 2 vezes:** `T-0045-render-yaml.md` §2 (19-22 e 29-64) é uma cópia literal do `T-0045-render-yaml.diff` (18-19 e 29-62), com os mesmos comentários. Duas cópias do texto que o Alexandre aplica.
  2. **Características do Render:** a lista da ADR §2.2 (88-94) e a tabela do desenho §2.1 (72-84) trazem os mesmos 7 fatos [SUPOSIÇÃO] (docker no cron, sem disco, preço por minuto, `schedule` em UTC, teto de 12 h, rede privada e `generateValue`/`envVarKey`), com palavras diferentes.
  3. **Linhas do `donos.json`:** ADR §2.4 (113-116), ADR §9 item 2 (283) e desenho §3 (90-95).
  4. **Ordem de publicação ou de merge:** ADR §9 (291, 294-295), contrato §8 (293-298) e desenho §4 (129-137).
- **Tipo:** doc. **Impacto:** manutenção (quem corrige o diff tem de lembrar do `.md`, e quem muda a ordem tem de mexer em 3 arquivos).
- **Severidade:** média.
- **Proposta:**
  1. Desenho §2: os 2 blocos YAML saem. **Depois:** "Texto exato: `docs/desenho/T-0045-render-yaml.diff` (aplica com `git apply`). O que muda: …" Os tópicos de 24-25 e 66-70 continuam.
  2. ADR:88-94, **depois:** "As características do Render que a W3 usa, todas [SUPOSIÇÃO] e conferidas no diagnóstico e no painel, estão no `docs/desenho/T-0045-render-yaml.md`, §2.1." A fonte é a tabela do desenho, porque é ela que se confere no sync.
  3. ADR:113-116, **depois:** "**Donos:** as 2 linhas do `.coord/donos.json` estão no desenho, §3 (governança 1, §9). Até elas entrarem, o `Dockerfile` fica como texto." ADR:283 fica com "as duas linhas do `.coord/donos.json` (desenho, §3)".
  4. A fonte da ordem é a ADR §9. Contrato §8 (293-298), **depois:** "Ordem de publicação: ADR 0004, §9." Desenho §4 (129-137), **depois:** "Ordem do merge: ADR 0004, §9 (itens 2, 7, 8, 10 e 11). Se o `render.yaml` entrar antes do código, o build do cron fica vermelho no painel até o código chegar; o site não cai."

### RD-0074 · Dentro da ADR, as decisões aparecem 2 vezes, e há 2 numerações para elas
- **Onde:**
  1. **D1 a D5 em 2 tabelas:** §0 (25-32) e §10 (303-309), mais a linha 313, que repete o §9 (itens 2, 10 e 11). O preço "US$ 1 a 3" sai 4 vezes (27, 86, 169, 305).
  2. **2 numerações para as mesmas 5 decisões:** a ADR usa D1 a D5. O contrato e o desenho usam a numeração do po: "decisão 5 A" (contrato:20; desenho:61), "decisão 3 A" (contrato:32; desenho:67), "decisão 4 A" (contrato:216), "decisão 6 B" (contrato:225), "2 A" e "5 A" (desenho:5). Quem lê o contrato e vê "decisão 4 A" precisa da tabela de conversão do §0 para achar a D3.
  3. **"até cerca de 40 min" 3 vezes:** §4 (168), §5.3 (213) e §11 (321).
- **Tipo:** doc. **Impacto:** leitura (a numeração dupla confunde) e manutenção.
- **Severidade:** média.
- **Proposta:**
  1. O §10 sai inteiro. A tabela do §0 ganha a coluna "Recomendação do time" (A, A, A, A, B), e a frase da linha 311 ("Texto literal (R-20261127-005437-alexandre …): "2 A / 3 A / 4 A / 5 A / 6 B".") vai para baixo dela. A linha 313 sai: os passos pendentes já estão no §9. O status (linha 3) passa a apontar "§0".
  2. Contrato e desenho passam a usar D1 a D5: contrato:20 "(D4)"; :32 "D2: a rodada automática baixa **ontem**"; :216 "(D3)"; :225 "(D5: sem print de tela, só o código)"; desenho:5 "(D1: cron job à parte, plano de 2 GB por minuto; D4: usuário próprio da Máxima, só como variável secreta)"; :61 "(usuário próprio do robô, D4)"; :67 "(D2)". O "2 A … 6 B" fica só no §0 da ADR, para o rastro.
  3. ADR:321, **depois:** "**Atraso até a tela:** §4 e §5.3; o robô do PC precisa estar ligado."

### RD-0075 · A ADR e o desenho ainda mandam o leitor para a branch `T-0045-render-yaml`, que já está dentro deste PR
- **Onde:** ADR:101 "(proposta de governança, branch `engenheiro-software/T-0045-render-yaml`)"; ADR:103 "O texto exato está em `docs/desenho/T-0045-render-yaml.md` nessa branch"; ADR:282 "(branch `engenheiro-software/T-0045-render-yaml`)"; desenho:132 "O `requirements-visitas.txt` já está na branch da ADR". O commit a6c719c ("junta a proposta do render.yaml à branch da ADR 0004") trouxe os 2 arquivos para cá. A branch `origin/engenheiro-software/T-0045-render-yaml` continua no remoto, sem PR (pela API, o único PR da T-0045 é o #137), e é um subconjunto deste.
- **Tipo:** doc · tarefa. **Impacto:** leitura (2 lugares para o mesmo texto; quem segue a ADR abre a branch errada).
- **Severidade:** média.
- **Proposta:** ADR:101, **depois:** "### 2.4 O `render.yaml` (proposta de governança)". ADR:103, **depois:** "O texto exato está em `docs/desenho/T-0045-render-yaml.md` e no `.diff` ao lado. Resumo:". ADR:282, **depois:** "…proposta do `render.yaml` e o texto do `Dockerfile` (`docs/desenho/T-0045-render-yaml.md`)". Desenho:132, **depois:** "O `requirements-visitas.txt` já está neste PR." A branch antiga é do gerente-projetos decidir; nada nela se perde, porque os commits estão no #137.

### RD-0076 · Dois índices de "dia baixado", e só o do PC sabe dos dois lados: a nuvem pode baixar de novo o dia que o PC já fechou
- **Onde:** contrato §3.1 (80): o `indice` do site guarda "os dias que a **nuvem** já entregou"; `deve_rodar` (84-92) e `dias_a_baixar(indice, …)` (94) decidem só por ele. O PC tem o seu próprio índice (`visitas_nucleo.indice`, `diario/_baixados.json`, usado pelo `dia_fechado`). A importação leva o lado da nuvem para o PC (`anotar_baixado` + `juntar_baixado`, ADR §5.1 e §5.2), mas nada leva o lado do PC para o site.
- **O que se repete:** o mesmo fato ("o dia D foi baixado às H") em 2 índices que só se juntam numa direção. Casos concretos: retentativa das 06h30 depois de um `MAXIMA_FORA`, depois que a assistente já baixou ontem pelo PC; padrão do botão do site ("dias ainda abertos até hoje", ADR §3.2), que conta como abertos os dias fechados no PC; o primeiro uso, com o `indice` vazio e o PC com 111 dias. Nesses casos, o robô baixa a mesma coisa 2 vezes (checklist E). No `ANALITICO`, cada repetição deixa um Excel a mais por vendedor e dia, com outro `HH-MM`.
- **Tipo:** rotina. **Impacto:** minutos do cron, mais sessões na Máxima (o risco de sessão única da ADR §11) e Excel repetidos no `ANALITICO`.
- **Severidade:** média.
- **Proposta:** um índice só, juntado pela mesma função pura.
  - Contrato §4.3 (190), **depois:** `{"epoca": "e7c1…", "resultado": {"41": "importado", "40": "recusado:sha256"}, "fechados_pc": {"20261126": "2026-11-27T07:12:03-04:00"}}`, com a regra: "`fechados_pc` (opcional, v1) = os dias dos últimos 40 no `_baixados.json` do PC. O robô manda em toda volta, mesmo com `resultado` vazio. O site junta no `indice` com `visitas_nucleo.juntar_baixado`".
  - Contrato:80, **antes:** "os dias que a **nuvem** já entregou nos últimos 40 dias" → **depois:** "os dias baixados nos últimos 40 dias, pela nuvem (lote) ou pelo PC (`fechados_pc`, §4.3); `baixado_em` = o maior (`juntar_baixado`, RN-VIS-001)".
  - Na ADR §5.2, a RN-VIS-001 fica como está (ela já manda valer a maior hora).

### RD-0077 · A importação vai virar a 3ª cópia do laço `desde`/`epoca`/confirmar no PC, e o site, o 3º armazém de `seq`
- **Onde:** contrato §4.1-§4.5 e ADR §5.1, item 2 ("no mesmo desenho da fila de edições (`web/app/edicoes.py`)"). No `main`, o mesmo laço já existe 2 vezes em `bap_automation.py`: `sincronizar_edicoes_web` (9551-9628: `ler_estado`, `baixar_*_web`, "epoca nova → puxa tudo de novo", `confirmar_*_web`) e `preparar_cobranca_web` (9190-9210, com o mesmo bloco da época nova e `baixar_cobranca_web`/`confirmar_cobranca_web` em 9125-9185). No site, `edicoes.Fila` e `cobranca.Diario` já guardam `epoca` + `seq` com a mesma tranca.
- **O que se repete:** "mesmo desenho" quer dizer reimplementar pela 3ª vez a paginação por `seq`, a troca de `epoca`, a confirmação repetida na volta seguinte e o registro `.jsonl` do que já foi aplicado.
- **Tipo:** código (no desenho). **Impacto:** manutenção (uma correção no laço tem de ser feita em 3 lugares) e testes repetidos.
- **Severidade:** média.
- **Proposta:**
  - Contrato §4.5, novo item: "O laço `desde`/`epoca`/confirmar é o mesmo do `sincronizar_edicoes_web` e do `preparar_cobranca_web`. Ele sai para uma função só em `bap_automation` (por exemplo, `puxar_fila_web(rota, estado, base, token, sessao, log)`), usada pelos 3. O `sincronizar_visitas_web` só traz a parte própria: gravar o Excel e montar."
  - ADR §5.1, item 2, **antes:** "no mesmo desenho da fila de edições (`web/app/edicoes.py`)" → **depois:** "com o mesmo armazém de `epoca` e `seq` da fila de edições (`web/app/edicoes.py`), reaproveitado, não copiado".
  - A extração é do modulo-robo e do modulo-web no lote do código. O contrato só precisa dizer que é uma função e um armazém.

### RD-0078 · No `fim` e no diagnóstico, o mesmo fato vai em 2 ou 3 campos
- **Onde:**
  1. **`status` × `codigo`:** no `fim` (contrato:161 e 166) e no `/saude` (223). A tabela do §5 (229) dá um único `status` para cada código, então o `status` repete o `codigo` e pode contradizê-lo (`"status": "ok"` com `"codigo": "TELA_MUDOU"`). A saída do processo (250) também é derivada dele.
  2. **`pico_mb` 2 vezes:** no topo do `fim` (163) e dentro de `medidas` (272).
  3. **Confirmação e captcha 3 vezes no diagnóstico:** `codigo` (`MAXIMA_CONFIRMACAO`/`MAXIMA_CAPTCHA`), `medidas.pediu_confirmacao`/`medidas.captcha` (273) e `confirmacao=nao captcha=nao` na linha do log (279). Com confirmação ou captcha, a rodada para no login (§5.1, 261), então os campos só ficam verdadeiros quando o código já diz.
  4. **401 repetido:** o §3.4 lista "401 | token" (151), que é a regra comum do §3 (53). Só esta rota repete.
- **Tipo:** código (contrato) · indicador. **Impacto:** manutenção e risco de divergência entre campos.
- **Severidade:** média.
- **Proposta:**
  1. O `fim` leva só o `codigo`. O site deriva o `status` pela tabela do §5 (constante `STATUS_DO_CODIGO`, com teste). Contrato:161, **depois:** `{"codigo": "PARCIAL_VENDEDOR", "fase": null, "dias_ok": […], "dias_faltando": [], "erros_vendedor": 1, "duracao_s": 412, "pico_mb": 618.0, "medidas": null}`. Contrato:166, **depois:** "`codigo` da tabela do §5 (o `status` sai dela); `fase` quando o código pede." No `/saude` (223), o `"status"` sai do `visitas`.
  2. `pico_mb` fica só no topo do `fim`, que vale para toda rodada. Em `medidas` (272), sai `"pico_mb"` e fica `"fonte_pico"`. A regra de 277 passa a falar do `pico_mb` do `fim`.
  3. Em `medidas` (273), saem `pediu_confirmacao` e `captcha`. A linha do log (279), **depois:** `DIAGNOSTICO codigo=... pico_mb=... login_s=... vendedor_s=...`.
  4. A linha "401 | token" (151) sai.

### RD-0079 · Textos do site com garantia e explicação do que o sistema faz, e 3 nomes para o mesmo botão do PC
- **Onde:** contrato §5, coluna "Texto no site":
  - "O que veio está salvo." / "Os dias que já vieram estão salvos." aparece 3 vezes (240, 241, 244). É texto de garantia (regra 3);
  - "que o site não faz sozinho" (236) explica o funcionamento;
  - "As atualizações do site estão pausadas." (236) repete o estado de pausa que a tela já mostra (§4.6, "estado");
  - "o caso vai ao Alexandre" (238) é o que acontece por trás;
  - "(memória ou tempo do serviço)" (244) explica a causa;
  - o mesmo botão do PC tem 3 nomes: "o Atualizar visitas do PC" (236), "o botão do PC" (238 e 240).
- **Tipo:** texto. **Impacto:** leitura (o usuário só precisa do problema e da ação).
- **Severidade:** média.
- **Proposta (texto final):**
  - `MAXIMA_CONFIRMACAO` (236): "A Máxima pediu uma confirmação. Use o Atualizar visitas do PC; o admin retoma aqui depois."
  - `MAXIMA_BLOQUEIO` (238): "A Máxima bloqueou o acesso do site. Use o Atualizar visitas do PC."
  - `TELA_MUDOU` (240): "A tela da Máxima mudou (etapa: <fase>). Use o Atualizar visitas do PC até a correção."
  - `NAVEGADOR_FALHOU` (241): "O navegador do site parou. Tentamos de novo às HHhMM." (o mesmo molde do `MAXIMA_FORA`, que diz quando não precisa apertar de novo)
  - `RODADA_INTERROMPIDA` (244): "A rodada parou sem terminar. Tentamos de novo às HHhMM."
  - A ADR §6, linha 236 ("O que o usuário nunca vê"), continua.

### RD-0080 · Tela "Atualizar visitas": a última rodada aparece 2 vezes
- **Onde:** contrato §4.6 (215): "estado, última rodada (código e texto do §5), lotes à espera do PC, histórico de 10 rodadas". A última rodada é a 1ª linha do histórico.
- **Tipo:** layout. **Impacto:** espaço acima da dobra e leitura (regra 1, "uma informação, um lugar").
- **Severidade:** média.
- **Proposta:** contrato:215, **depois:** "estado (agenda, pausa, rodada em andamento), lotes à espera do PC ("Baixado às HHhMM · esperando o PC importar") e as 10 últimas rodadas (código e texto do §5; a mais recente em destaque, no topo)". A simulação do designer-ux (ADR §9, item 4) já parte dessa lista.

### RD-0081 · `GET /api/visitas/estado` repete o `/saude.visitas`
- **Onde:** contrato §4.4 (195-201) × §4.6 (223). As 2 rotas dão `agenda` e `pausado`. O `/saude` é público (`web/app/main.py:182`) e já é lido pelo PC (rotina diária, limite 3). Só faltam nele `rodada_ativa` e `fase`.
- **Tipo:** código (rota). **Impacto:** uma rota, um teste de token e um formato a menos para manter.
- **Severidade:** baixa.
- **Proposta:** o §4.4 sai. Contrato:223, **depois:** "`/saude` ganha `visitas: {"agenda", "diagnostico", "ultima_rodada", "codigo", "pausado", "rodada_ativa", "fase", "lotes_a_importar"}`, sem dado pessoal". O aviso do PC (o texto que está hoje no §4.4) passa para o §4.6, como "Aviso do botão do PC, quando `visitas.rodada_ativa`". ADR:155: "o PC consulta o `/saude`". ADR:270: o `GET /api/visitas/estado` sai da lista de tokens.

## Redundância útil ou `manter?` (não entra como achado)
- **`MAXIMA_CAPTCHA` × `MAXIMA_CONFIRMACAO`** `manter?`: os 2 têm o mesmo "Depois", o mesmo texto ("o mesmo texto do `MAXIMA_CONFIRMACAO`", 237) e as mesmas saídas na ADR §6. Ficam separados só se a ADR nova do §6 escolher saídas diferentes para captcha e para confirmação. Se não, os 2 se fundem em `MAXIMA_CONFIRMACAO`, e o `classificar_login` mantém o teste do captcha.
- **`NAVEGADOR_FALHOU` × `RODADA_INTERROMPIDA`:** manter. Quem grava é diferente (o cron manda o `fim` ou o site vê a concessão vencer), e só um deles aparece por rodada.
- **`pedidos.jsonl` × `estado.json.pedido`:** manter. Um é o histórico, só com acréscimo, e o outro é o pedido em vigor.
- **Aviso do PC durante a rodada do site** ("…Continuar?"): manter. É confirmação de ação que pode derrubar a sessão.
- **Comentários cruzados** do `requirements-visitas.txt` (3-4) e do `Dockerfile` (desenho:101) sobre a versão do Playwright: manter, porque quem abre qualquer um dos 2 precisa do aviso.
- **RN-VIS-001 a 005:** hoje só existem na ADR §5.2. Quando o po registrar no `docs/produto/03-regras.md`, a fonte da verdade passa a ser lá, e a ADR deve apontar para ela.

## Fora do meu escopo (vai ao `testes` e ao `revisor-codigo`, sem catálogo)
- Contrato:37: o vigia faz `os._exit(3)` aos 58 min, mas a regra de saída (250) só tem 0 e 1. Os 58 min também não têm constante.

## Pendências desta revisão
- **Catálogo:** o catálogo `docs/redundancias/catalogo.md` e os recados ao dono e ao gerente-projetos não foram feitos, por instrução de quem chamou (só o relatório, sem commit). [SUPOSIÇÃO] Quem chamou leva os RD-0072 a RD-0081 ao engenheiro-software.
- **Reteste:** no novo head SHA, depois da correção.
