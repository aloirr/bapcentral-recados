# Revisão de código — T-0045, itens 6 e 8 (parte do robô do PC)

- **Revisor:** revisor-codigo · **Data:** 27/11/2026 (Manaus)
- **Branch:** `modulo-robo/T-0045-nuvem-robo` · **head SHA:** `11b24fcb8b0fdfd6f95b3984fc5879507a277527` (2 commits sobre `0f3106a`). Sem PR aberto.
- **Referências:** ADR 0004 §9 (itens 6 e 8) · contrato `.coord/contratos/visitas-nuvem.md` v1.1 (`42c81a1`) · o site do item 5 já no `main` (`web/app/visitas.py`).
- **Este parecer vale só para o head acima.** Commit novo = revisão nova.

## Veredito

**Não aprovado: 0 🔴, 5 🟡, 10 🟢.** O laço das edições ficou igual, o botão do PC continua igual no caminho feliz e a importação é só por acréscimo. Os 🟡 são três desvios de RN ou de contrato que o site já no `main` faz valer, uma detecção que pode barrar o login do botão do PC e a falta de teste no CI.

## O que rodei (numa cópia fora do repositório, venv 3.12 com tkinter)

| Conferência | Resultado |
|---|---|
| `python -m compileall -q visitas_maxima.py bap_automation.py visitas_nucleo.py` | ok |
| `pytest tests/` inteiro (a branch mais os 3 `test_T0045_*` do `main` `d9dd721`) | saiu 0, sem falha |
| `test_T0021_edicao_web_robo` + `test_T0045_*` | 63 passaram |
| Provas do autor, apontadas para a minha cópia: `cmp_edicoes.py` / `cmp_botao.py` / `visitas_web.py` | TUDO IGUAL (7 cenários) / TUDO IGUAL/OK / TUDO OK (14). O `ba_orig.py` e o `vm_orig.py` são byte a byte os do `0f3106a` |
| `coord.mjs verificar --por-commit 0f3106a..11b24fc` | OK, 2 commits do modulo-robo, nenhuma violação |
| `git merge-tree origin/main(e1d80a8) 11b24fc` | sem conflito |
| Arquivos da branch | só `visitas_maxima.py` e `bap_automation.py`. Nada em `RELATORIOS/`, `SISTEMA BAP/`, `BAP Ajuda 2.0/`, nas configs ou nos dados digitados |
| `bap_dados.VERSAO` | 27 (o arquivo não muda) |
| Sondas minhas (`rev45/sondas/s1.py`, `s2.py`) | as que sustentam os 🟡 1 e 4 |

## 🟡 Corrigir antes do merge

1. **`bap_automation.py:9955-9957` (`_aplicar_lote_visitas_web`): a importação rebaixa o índice do PC.** O `vn.anotar_baixado(raiz, dia, quando)` sobrescreve a hora com o `baixado_em` da nuvem, mesmo quando o PC baixou depois. A RN-VIS-002 (ADR 0004) diz: "entre a hora do PC e a da nuvem, vale a maior (`juntar_baixado`)".
   - Sonda `s1.py`: o PC tinha o dia 25/11 baixado às 26/11 10h00. Veio o lote da nuvem das 06h07 e o índice passou a dizer 06h07. Em seguida, o `fechados_pc` mandou 06h07 ao site.
   - Efeito: um lote atrasado da nuvem (botão no próprio dia, ou a fila puxada de novo depois de época nova) pode **reabrir** um dia que o PC já tinha fechado.
   - Correção: gravar a maior das duas horas, com `vn._quando_manaus`/`juntar_baixado`, sem reescrever a regra. Vale também para a chave do mês (9956-9957). Teste citando a RN-VIS-002.

2. **`visitas_maxima.py:1318` e `:429` (`rodar` / `codigo_da_excecao`): a fase `"navegador"` está fora da lista do §3.3.**
   - O `_fase("navegador")` chama o `ao_fase("navegador", None, None, None)`. Para falha ao abrir o navegador, o `codigo_da_excecao` devolve `("NAVEGADOR_FALHOU", "navegador")`.
   - O site no `main` recusa as duas coisas: `web/app/visitas.py` linha 560 (`progresso`: fase ∉ `FASES` → 400) e linha 691 (`fim`: "fase fora da lista" → 400). O primeiro progresso da rodada da nuvem e o `fim` do `NAVEGADOR_FALHOU` voltariam 400. Pior: o `fim` recusado vira `RODADA_INTERROMPIDA`.
   - Correção: guardar "navegador" só como marca interna. Não chamar o `ao_fase` com ela e devolver `fase=None` no `NAVEGADOR_FALHOU` (que não está em `PEDE_FASE`). Ou então acrescentar a fase ao contrato, com aviso aos consumidores. O `FASES` (linha 359) pode validar o `_fase`.

3. **`visitas_maxima.py:116` e `:753-760` (`CAPTCHA_JS` e o `pronto()` do `entrar`): falso positivo pode barrar o login do botão do PC.** O `entrar` é o mesmo no PC e na nuvem, e a detecção nova roda a cada 0,4 s logo depois do "Entrar", ainda no `/login`. Há dois riscos:
   - O seletor `[class*="captcha" i]` / `iframe[src*="captcha" i]` também casa com elemento **invisível**: o selo do reCAPTCHA v3 (`.grecaptcha-badge`) e o iframe do reCAPTCHA invisível, comuns em páginas de login. Se a página de login da Máxima tiver um deles, o botão do PC passa a falhar sempre com "A Máxima pediu captcha.", e a nuvem pausa no diagnóstico.
   - O `_RX_URL_VERIFICACAO` olha a URL **inteira**, com a query. Um token na query com "otp", "mfa" ou "2fa" faz o `pronto()` ler o texto da página. Uma página inicial com "Termos de uso" no rodapé vira então `MAXIMA_CONFIRMACAO`. A sonda `s1.py` mostra o caso `…/home?t=abOTPx9` + "Termos de uso" → `MAXIMA_CONFIRMACAO`.
   - Nenhuma prova do autor passa pelo `entrar`/`pronto()`: o `cmp_botao.py` só testa o `classificar_login` puro.
   - Correção: contar só captcha **visível** (tamanho > 0, fora do `.grecaptcha-badge`) e aplicar o regex só ao `urlparse(url).path`. Prova: uma rodada real do botão do PC com "Mostrar o navegador" (login ok), ou o DOM da página de login conferido pelo modulo-robo, registrada na entrega.

4. **`bap_automation.py:9963` (`_aplicar_lote_visitas_web`): exceção inesperada segura a fila para sempre.** Avaliação da suposição do autor:
   - Para `PermissionError`/`OSError` (Excel ou CSV aberto, disco), `pendente` está certo: é passageiro.
   - Para qualquer outra exceção (`ValueError`, `AttributeError`…), o mesmo lote volta como `pendente` a cada 30 min. **Nenhum lote seguinte entra**, e o único sinal é uma linha de log. A sonda `s2.py`, com `equipe.filiais` torto, deu o mesmo `pendente` em 3 voltas seguidas, e o seq 2 nunca foi importado.
   - O site já valida `equipe`/`extras` (`validar_lote`), então hoje isso só acontece com defeito no `montar_dia`/`montar_mes`. Mas é exatamente o caso que ninguém vê.
   - Correção: validar `equipe` (3 dicionários) e `extras` (dicionário) no `_validar_lote_visitas_web`, como no site, com `erro`/`dia`. Para exceção não prevista, um teto de voltas por seq (ex.: 3) e depois `erro`/`dia`, com linha própria no log. Tirar a parte da nuvem do índice faz a nuvem baixar de novo, dentro do teto do dia.

5. **Sem teste no CI.** A branch não acrescenta teste. O contrato §4.4 pede que "os testes do laço são os das edições, rodados nos dois", e a regra 2 do CLAUDE.md pede teste citando a RN para cada função pura nova: `classificar_login`, `codigo_da_excecao`, `fechados_pc`, `aviso_site_baixando` e `gravar_excel_importado`. As provas `cmp_edicoes.py`, `cmp_botao.py` e `visitas_web.py` estão só no scratchpad. Pela ADR §9, o item 9 é do `testes`; antes do merge, o gerente pede a ele os testes, ou a decisão explícita de que o merge fica para depois do item 9. Mínimo: o laço `puxar_fila_web` rodado com as 2 rotas, o caso do 🟡 1, o 404 da web antiga e a validação do lote (sha256, `..`, dia futuro, nome × dia).

## 🟢 Sugestões

1. `visitas_maxima.py:773`: "O login não respondeu em 45 s." sai sem código e vira `TELA_MUDOU`. Duas seguidas na fase `login` pausam a agenda. Para Máxima lenta, `MAXIMA_FORA` (nova tentativa) descreve melhor o caso.
2. `visitas_maxima.py:777` (suposição "login não reconhecido = `MAXIMA_SENHA`"): **aceita**. É o lado seguro (nunca repete o login), e o texto do PC continua o de antes. A sonda mostra "Erro de comunicação com o servidor" e "Serviço indisponível" virando `MAXIMA_SENHA`, que pausa a nuvem. Sugiro um regex de indisponibilidade → `MAXIMA_FORA` e registrar a regra no §5.1 do contrato.
3. `bap_automation.py:9925` (suposição "lote 404 = `erro`/`sha256`"): **aceita**. Dos motivos do §4.3, é o único que leva o site a tirar a parte da nuvem do índice. Registrar no §4.2 do contrato ("404 = erro/sha256").
4. Tetos no PC: o contrato põe `LOTE_GZ_MAX`, `ARQUIVO_MAX` e `ARQUIVOS_MAX` no site, e o PC não confere. Conferir no PC custa pouco (`len(arquivos) <= 60`, `len(dados) <= 2 MB`, corpo gzip até 8 MB antes do `gzip.decompress`) e protege do gzip-bomba se o site falhar.
5. `visitas_maxima.py:471-481` (`consultar_saude`): no primeiro clique, o `import bap_automation` (pandas, openpyxl) roda na thread da tela. E `timeout=5` vale para a conexão **e** para a leitura (até ~10 s). Sugestão: `timeout=(3, 2)` e ler o `BAP_WEB_URL` sem importar o `bap_automation` inteiro.
6. `bap_automation.py:9952`: `replace(tzinfo=None)` supõe `-04:00`. `vn._quando_manaus` (ou `astimezone(Manaus)`) já trata outro fuso.
7. `bap_automation.py:9845`: o registro `IMPORTADOS_VISITAS_WEB.jsonl` traz `motivo`, além das chaves do §4.4, e o `em` não sai em ISO `-04:00`. São inofensivos e sem nome. Acertar o contrato (v1, chave opcional) ou o código.
8. `bap_automation.py:9635`: com `rotulo="Visitas web"`, a linha diz "falha ao puxar as **edicoes** do site". Trocar por "a fila do site".
9. `bap_automation.py:9727`: o 409 de época só zera o estado no caminho principal (9777). No caminho `not res` + `fechados_pc`, um 409 fica sem reação até a próxima volta com GET ok. Não chega a quebrar nada.
10. `bap_automation.py:10002`: o `depois_de_baixar` só roda quando entra lote novo. Se o acompanhamento falhou (Excel aberto), ele só se recupera na próxima importação ou no botão. Vale guardar a falha e repetir na volta seguinte. Redundância: o `FECHADOS_PC_DIAS = 40` está no `visitas_maxima` e também em `web/app/visitas.py`. Pode morar no `visitas_nucleo` (o núcleo que os dois usam), por pedido ao modulo-rota.

## Conferências pedidas: o que está certo

- **`sincronizar_edicoes_web` sem mudança de comportamento:** li linha a linha contra o `0f3106a`.
  - O estado vai no mesmo arquivo (`.tmp` + `os.replace`).
  - Mesmo GET paginado e mesma regra de época.
  - O confirmar só sai com `a_confirmar`, como antes: `extra_confirmar=None`, e o 409 não zera o estado.
  - `opcoes`/`aplicadas_web` são lidos depois do GET, como antes, e os textos de log são iguais.
  - Confirmado pelo `cmp_edicoes.py` (7 cenários: resultado, log, chamadas HTTP, estado e registro) e pelo `test_T0021`.
- **Botão do PC:**
  - `executar` igual. O `depois_de_baixar` é o mesmo bloco, com as mesmas chaves (`excel`, `por_cliente`, `prospeccao`).
  - `Robo(raiz, log, parar, visivel)` com `canal=None` segue o laço Edge → Chrome → Chromium de antes.
  - `foto=True`, e `eventos=False` mantém o log de antes.
  - Mudanças declaradas conferidas: HTTP 403 no `goto` → `MAXIMA_BLOQUEIO` na hora; captcha e confirmação → erro claro; `/saude` só com `precisa` e sem token (só `https`, por `_base_web`). Ressalva: o 🟡 3.
- **Segredo e dado pessoal:**
  - Nada de segredo no código.
  - Log do robô com o token trocado por `***`, só nomes de classe de exceção e sem nome de pessoa.
  - Com `eventos=True`: `self.log` mudo; `evento()` só com campos higienizados (`[A-Za-z0-9_.:-]`, 40 caracteres); a mensagem crua da Máxima não sai, nem no `✖` do vendedor (vira o nome da classe) nem no `MAXIMA_SENHA` (sem o texto). O texto da página no `classificar_login` só passa por regex.
  - O registro `.jsonl` não leva nome.
- **Validação antes de gravar:** em cada lote, tudo é conferido antes do primeiro Excel.
  - O sha256 do corpo é comparado com o do cabeçalho e o da linha.
  - `versao == 1`; `dia` igual ao da linha, `AAAAMMDD` e não futuro.
  - `pasta` sem `/`, `\`, `..` nem caractere de controle, e igual ao `nome_limpo`.
  - `nome` casa com `_RX_ARQ_ANALITICO`, começa com `VISITA-<pasta>-`, e a data do nome é o dia.
  - `b64` validado; sha256 e `bytes` de cada Excel conferidos.
  - Última trava em `gravar_excel_importado`. Tetos: ver 🟢 4.
- **Só acréscimo:** `gravar_excel_importado` pula se o sha256 for igual (com ou sem sufixo). Outro conteúdo ganha `-2`, `-3`… (`arquivo_analitico`). `.tmp` + `os.replace`, sem nunca sobrescrever nem apagar. O registro `.jsonl` é só de acréscimo, com `fsync`. O `.xlsx.tmp` que sobrar não casa com o `_RX_ARQ_ANALITICO` (o `montar_dia` ignora).
- **Contrato:**
  - §4.1: o 404 da web antiga não gera log e não dispara POST, porque ainda não há época.
  - §4.3: o `fechados_pc` sai em toda volta com época conhecida, mesmo sem lote; 409 → `desde=0`; os motivos ficam na lista do site.
  - §4.4: assinatura, `puxar_fila_web` único para as 2 filas, passos 1–3, `depois_de_baixar` uma vez, registro e retorno.
  - §4.5: o aviso com o texto literal.
  - §5: os códigos por fase.
  - §3.3: ver 🟡 2. Os §3.4 e §6 são do `rodar.py`, fora deste lote.
  - §4.3 × site no `main`: formato do `fechados_pc` aceito (`dia_valido` + `_dt`, até 400).
- **Número do Diretor:** não se aplica. **Tela:** só o `askyesno` com o texto do contrato §4.5; não houve print. Como o texto é o do contrato aprovado, não peço simulação.

## Para o re-teste

Commit novo com os 🟡 1 a 4 corrigidos e a prova do 🟡 3 registrada. Os testes do 🟡 5 entram no CI, ou o gerente registra a decisão de esperar o item 9. Depois, novo pedido de revisão com o head SHA.

---

# Reteste no head `ed640e12afe818a746cc57ebfbb5b1bb4db3a32b` (27/11/2026)

Delta `11b24fc..ed640e1`: 1 commit (`T-0045: correcoes da revisao…`, `Agente: modulo-robo`), só em `bap_automation.py` e `visitas_maxima.py`.

## Veredito no ed640e1

**Aprovado: 0 🔴 e nenhum 🟡 aberto no código.** Os 🟡 1 a 4 estão fechados. O 🟡 5 (testes no CI) foi passado ao `testes` no item 9 da ADR 0004 §9, por decisão do gerente-projetos: não é falha deste código, mas fica como condição (ver abaixo).

## O que rodei (cópia fora do repositório, venv 3.12)

| Conferência | Resultado |
|---|---|
| `compileall -q visitas_maxima.py bap_automation.py` | ok |
| `pytest tests/` inteiro (branch + os `test_T0045_*` do `main`) | **691 passaram, 2 xpassed**, saída 0 |
| `test_T0021_edicao_web_robo` + `test_T0045_*` | 63 passaram |
| `cmp_edicoes.py` | TUDO IGUAL (7 cenários): as edições continuam sem mudança |
| `visitas_web.py` | TUDO OK (18) |
| `sonda2.py` do autor | TUDO OK (16) |
| `cmp_botao.py` | 30 iguais e 1 "DIFERE": o caso `fase navegador`, que a correção do 🟡 2 tirou de propósito. O comportamento novo (`_abrindo` → `NAVEGADOR_FALHOU`/`inicio`) é provado no `sonda2.py` |
| Minhas sondas `s1.py`/`s2.py` | o índice do PC fica em 10h00 e o `fechados_pc` manda 10h00. `…/home?t=abOTPx9` + "Termos de uso" → `None`. Com `equipe` torta, o lote vira `erro` e a fila anda (2 recusadas na 1ª volta; as voltas seguintes não repetem) |
| `verificar --por-commit 0f3106a..ed640e1` | OK, 3 commits, nenhuma violação |
| `git merge-tree origin/main(e1d80a8) ed640e1` | sem conflito |
| `bap_dados.VERSAO` | 27 |
| Arquivos da branch | os 2 `.py`. Nada versionado em `RELATORIOS/`, nas bases, nas configs ou nos dados digitados |

## Os 🟡 do parecer anterior

1. **Fechado.** `_anotar_maior_visitas_web` (`bap_automation.py`) chama `vn.juntar_baixado` (a regra do núcleo, sem cópia): a hora do PC nunca recua e, no empate, vale a nuvem. Vale para o dia e para a chave do mês. A chave `AAAAMM` passa bem pelo `juntar_baixado`, que não filtra o formato.
2. **Fechado.** O `rodar()` começa em `inicio`. A falha ao abrir (`_abrindo`) vira `NAVEGADOR_FALHOU` com fase `inicio`, que está em `FASES` e que o site aceita no `progresso` e no `fim`. O `FASES` do robô é igual ao de `web/app/visitas.py` (`sonda2.py`).
3. **Fechado no código.** O regex de verificação olha só o `urlparse(url).path`. O captcha conta só se estiver visível (60×40 ou mais, `visibility`/`display`/`opacity`), fora do `.grecaptcha-badge`, e sem os seletores genéricos `[class*]`/`[id*]`. A prova numa rodada real ficou para o diagnóstico (decisão do gerente); ver 🟢 R1.
4. **Fechado.** Só `PermissionError`/`OSError` deixam o lote `pendente`. O resto vira `erro`/`dia` (motivo da lista do §4.3), a fila anda e o site tira a parte da nuvem do dia.
5. **Passado ao item 9 (`testes`) pelo gerente.** Condição: os testes do §4.4 (o laço nas 2 rotas, RN-VIS-002 no índice, 404 da web antiga, validação do lote, `classificar_login`, `codigo_da_excecao`) entram no `main` **antes do item 10** (`render.yaml`).

## 🟢 novos (não bloqueiam)

- **R1. A instalação no PC vem antes do diagnóstico.** Pela regra 11, o `entrar` novo chega ao botão do PC na rotina das 06h30 seguinte ao merge, antes do diagnóstico no Render. Vale o modulo-robo acompanhar o primeiro "Atualizar visitas" do PC depois do instale (login ok), ou pedir uma rodada com "Mostrar o navegador".
- **R2. Sem pista no log quando o lote dá `erro`/`dia`.** Na exceção não prevista, o log só diz "N recusada(s)". O comentário em `_aplicar_lote_visitas_web` fala em "o log só tem a classe", mas a classe não aparece. Uma linha `Visitas web: erro ao montar o dia (<Classe>)` ajuda a diagnosticar, sem dado pessoal.
- **R3. URL com fragmento.** O `pronto()` agora ignora o fragmento: um login com rota em hash (`#/login`) seria lido como "ok" na hora. A Máxima usa `/login` no caminho (`URL_LOGIN`), então hoje não há efeito. Fica a nota.
- Os 🟢 1 a 10 do parecer anterior continuam como sugestões.

---

# Reteste no head `3511814057362fdb974d36eb393c82e2561da2dc` (PR #165, 27/11/2026)

Delta desde o `ed640e1` (aprovado):
- `9a886ae`: merge do `origin/main` `4fc6429`. Não mexe nos 2 `.py` do robô: o main não tocou neles desde `0f3106a`.
- `69b14cc`: D1 e D2 do `classificar_login`.
- `f6ae758`: RD-0172, 0173 e 0175 a 0179.
- `3511814`: RD-0181.

Contra o main, os arquivos alterados continuam só `bap_automation.py` e `visitas_maxima.py`.

## Veredito no 3511814

**Não aprovado: 0 🔴 e 2 🟡** (um no código, um de coordenação com o PR do `testes`). As RDs estão certas, e o `sincronizar_edicoes_web` continua igual.

## O que rodei (cópia fora do repositório, venv 3.12)

| Conferência | Resultado |
|---|---|
| `compileall` dos 2 `.py` | ok |
| `pytest tests/` inteiro no `f6ae758` (+ os testes do `origin/testes/T-0045-nuvem-testes` `5050cfe`) | 862 passaram e 2 falharam. Uma falha é do `main` (abaixo) e a outra é o 🟡 B |
| `test_T0021` + todos os `test_T0045_*` (do main e da branch do testes) no `3511814` | 235 passaram, 3 skipped e 1 falhou (o 🟡 B) |
| `cmp_edicoes.py` (`t0045b`) | **TUDO IGUAL** (7 cenários) no `f6ae758` e no `3511814` |
| `visitas_web.py` / `sonda2.py` | TUDO OK / TUDO OK |
| `cmp_botao.py` | só o "DIFERE" já esperado da fase `navegador` (ver o reteste do `ed640e1`) |
| Minhas sondas `s1.py` e `s3.py` | o índice do PC não recua. `fechados_pc` em `-04:00` pelo `_quando_manaus`, com a chave do mês e a data torta fora. O D1 está no 🟡 A |
| `verificar --por-commit 0f3106a..3511814` | OK (16 commits com o merge), nenhuma violação |
| `git merge-tree origin/main(4fc6429) 3511814` | sem conflito |
| `bap_dados.VERSAO` | 27 |

**Falha que já está no `main` (não é deste PR):** `tests/test_T0024_lote2_robo_web.py::test_T0024_pacote_real_do_lote2_pelo_formato2_abre_em_200_e_403_por_perfil`. Ela falha igual no `4fc6429` puro: o perfil `analista`, do T-0036 (#158), no `pv_indicadores`, e o teste do T-0024 não foi atualizado. Vai ao gerente para quem é dono do teste.

## 🟡

**A. `visitas_maxima.py`, `classificar_login` (D1): o login normal pode dar alarme falso.** Com o D1, o **caminho** da URL decide sozinho: casou o `_RX_URL_VERIFICACAO` fora do `/login`, o resultado é `MAXIMA_CONFIRMACAO` com qualquer texto, até vazio (página carregando).
- O regex procura **pedaços de palavra** (`otp`, `mfa`, `confirm`, `autentic`, `device`, `termo`…) em qualquer parte do caminho. A sonda `s3.py` dá `MAXIMA_CONFIRMACAO` para `/hotpage`, `/devices/home`, `/autenticacao/callback` com "Carregando…", `/auth/autenticar` e `/sso/confirm-redirect`.
- O `pronto()` olha a URL a cada 0,4 s logo depois do "Entrar". Um redirecionamento intermediário do login normal com um desses caminhos derruba o login do **botão do PC** sempre. Pela regra 11, o PC recebe isso na rotina seguinte ao merge, antes do diagnóstico.
- No `ed640e1`, esse caso exigia texto de confirmação. Agora o D1 é conservador para a conta da Máxima (nunca repete o login), mas **não** contra alarme falso, que era o ponto pedido.
- Correção sugerida, mantendo o D1:
  - (1) regex por **segmento inteiro** do caminho, numa lista fechada (`verificacao`, `verificar`, `confirmacao`, `confirmar`, `mfa`, `2fa`, `otp`, `dispositivo`, `novo-dispositivo`, `termos`, `aceite`, `redefinir-senha`, `trocar-senha`, `alterar-senha`, `nova-senha`), sem `autentic` e `device` soltos;
  - (2) no `pronto()`, o caso "só pelo caminho" (sem texto que case) só decide depois de ver o mesmo caminho em 2 leituras com 1 s ou mais entre elas.
  - Teste: os 5 caminhos acima → `None`; os `VERIFICACAO_TEXTO_NOVO` do testes → `MAXIMA_CONFIRMACAO`.

**B. Coordenação: o RD-0173 (3 funções das edições apagadas) conflita com o teste do item 9.** `tests/test_T0045_edicoes_web_igual_main.py::test_RN_GER_012_funcoes_publicas_das_edicoes_continuam` (branch `testes/T-0045-nuvem-testes` `5050cfe`) exige `gravar_estado_edicoes_web`, `baixar_edicoes_web` e `confirmar_edicoes_web` com as assinaturas do main. Com o `3511814`, falha com `AttributeError`.
- `git grep` no `3511814` (árvore inteira: PC, smokes, testes do main): **nenhum chamador** das 3 funções. A remoção está certa como código morto.
- Recomendo que o `testes` tire os 3 nomes do teste (os 2 que ficam, `ler_estado_edicoes_web` e `sincronizar_edicoes_web`, mais o efeito, continuam cobertos). Se for preferível manter a API, o robô devolve as 3 funções.
- Decide o gerente. Sem isso, o PR #165 e o do item 9 não ficam verdes juntos no main.

## As RDs e o D2 (conferidos, sem achado)

- RD fuso: `fechados_pc` e `_aplicar_lote_visitas_web` usam o `vn._quando_manaus`, sem regra própria. A saída continua `AAAA-MM-DDTHH:MM:SS-04:00`, a data torta e a chave `AAAAMM` ficam fora, e no lote sem `baixado_em` vale a hora de agora em Manaus.
- RD `conferir_importado`/`_base_analitico`: é a regra única para o `_validar_lote_visitas_web` e o `gravar_excel_importado`. É igual à anterior: o `startswith("VISITA-<pasta>-")` saiu, mas o `m.group("nome") == pasta` do `_RX_ARQ_ANALITICO` ancorado dá o mesmo resultado. Os motivos `pasta`/`nome` têm a mesma ordem. O `base64` continua importado no topo do módulo.
- RD `_fase` com `FASES`: todas as 12 chamadas usam fase da lista, e o PC não é afetado. O evento `vendedor` sai numa linha só, com `dia`. O `self.vendedores` continua certo, porque é atribuído no laço.
- RD `_no_login` e RD-0181: as 2 remoções são inalcançáveis. Depois do `if not no_login: return MAXIMA_CONFIRMACAO`, o `no_login` é sempre verdadeiro. No `pronto()`, todo caminho fora do `/login` que passa da primeira guarda já devolve código. O comportamento não muda.
- Logs: `Visitas web: N Excel de M dia(s).`, sem nome e sem token.
- D2 (troca de senha no `/login` → `MAXIMA_CONFIRMACAO`): ok. O texto avaliado no `/login` é só o do elemento de erro (snack-bar, `mat-error`…), então o "Esqueceu a senha? Crie uma nova senha" do rodapé não entra.

## Para o re-teste

Commit novo com o 🟡 A e a decisão do gerente sobre o 🟡 B. Novo pedido com o head SHA.

---

# Reteste no head `a020b5321d20d5c3655f5f108b55a4f2385348dc` (PR #165, 27/11/2026)

O delta desde o `3511814` é 1 commit (`a020b53`, `Agente: modulo-robo`), só em `visitas_maxima.py`:
- `_RX_URL_VERIFICACAO` passa a casar só **segmentos inteiros**, de uma lista fechada;
- `_texto_claro`;
- no `pronto()`, a 2ª leitura do mesmo caminho, 1 s ou mais depois, quando só o caminho decide;
- duas variantes de redação a mais no `_RX_CONFIRMACAO` ("o seu", "a sua").

## Veredito no a020b53

**Aprovado no código: 0 🔴 e o 🟡 A fechado.** O 🟡 B (as 3 funções das edições exigidas pelo teste do item 9) continua aberto, com o `testes` (RD-0180). Ele não é defeito deste código, mas o PR #165 e o do item 9 só ficam verdes juntos no `main` depois do RD-0180. Fazer o merge do #165 antes deixa o PR do `testes` vermelho até ele ajustar.

## O que rodei (cópia fora do repositório, venv 3.12)

| Conferência | Resultado |
|---|---|
| `compileall` dos 2 `.py` | ok |
| `test_T0021` + todos os `test_T0045_*` (os do main e os da branch do testes `5050cfe`) | 235 passaram, 3 skipped e 1 falhou: só o 🟡 B (`test_RN_GER_012_funcoes_publicas_das_edicoes_continuam`) |
| `cmp_edicoes.py` | **TUDO IGUAL** (7 cenários) |
| `visitas_web.py` / `sonda2.py` / `sonda4.py` / `sonda5.py` | TUDO OK nas 4 |
| `cmp_botao.py` | só o "DIFERE" já esperado da fase `navegador` |
| Minha `s3.py` | **os 5 caminhos dão `None`**: `/hotpage`, `/devices/home`, `/autenticacao/callback` ("Carregando…"), `/auth/autenticar`, `/sso/confirm-redirect`. `/home` e `/sistemas?next=/verificacao` também dão `None` (a query não conta) |
| Minha `s1.py` | igual ao reteste do `ed640e1`: senha, captcha, bloqueio e confirmação como antes. `…/home?t=abOTPx9` + "Termos de uso" → `None` |
| Minha `s6.py` (o `entrar` com URL que muda no tempo) | `/mfa` por 0,6 s e depois `/home` → **login ok**. `/termos` por 0,8 s e depois `/home` → **login ok**. `/aceite-termos` que fica → `MAXIMA_CONFIRMACAO` em ~1,2 s. Os caminhos do maxGestão que o robô usa (`/painel-auditoria`, `/geolocalizacao/…`) → login ok |
| `verificar --por-commit 0f3106a..a020b53` | OK (17 commits), nenhuma violação |
| `git merge-tree origin/main(4fc6429) a020b53` | sem conflito. Contra o main, os arquivos alterados continuam só os 2 `.py` |
| `bap_dados.VERSAO` | 27 |

O `pytest tests/` inteiro não foi repetido neste head. O delta é só o `entrar`/`classificar_login`. A suíte inteira do `f6ae758` teve só a falha do 🟡 B e a do `main` (`test_T0024_…_403_por_perfil`, já registrada no reteste do `3511814`).

## A lista fechada e os segmentos "termos" e "aceite-termos"

- **Não pega a página normal da Máxima.** Nenhum caminho que o robô conhece (`/login`, a raiz do maxGestão, `/painel-auditoria`, `/geolocalizacao/…`) é segmento da lista. O casamento exige o segmento **inteiro** entre `/` e `/` ou o fim: `/termos-de-uso`, `/verificacao-email` ou `/mfa-setup` não casam.
- **"termos" e "aceite-termos" fazem sentido.** O §5 do contrato põe o "aceite de termo" em `MAXIMA_CONFIRMACAO`. Ser levado, logo depois do "Entrar", a um `/termos` que **fica** 1 s ou mais é o caso do aceite. A página de termos que o usuário abre por link não aparece nesse ponto, porque o `pronto()` só olha até a primeira saída do `/login`. E a `s6.py` mostra que um `/termos` de passagem (menos de 1 s) não derruba o login.
- Risco que sobra, aceito: um salto intermediário do login normal que **pare 1 s ou mais** num desses segmentos, sem texto. Com segmentos tão específicos, é improvável. A rodada real do botão do PC depois do instale (🟢 R1) confirma.

## 🟢 (não bloqueiam)

- **R4.** Registrar no §5.1 do contrato a lista fechada dos segmentos e a regra "só pelo caminho = 2 leituras com 1 s ou mais entre elas" (v1, detalhe de implementação), para o site e o testes usarem a mesma lista.
- **R5.** Um caminho de verificação com acento codificado (`/verifica%C3%A7%C3%A3o`) não casa e segue como login ok, depois cai em `TELA_MUDOU`. É o lado seguro contra alarme falso; fica a nota.
- R1 (acompanhar o primeiro "Atualizar visitas" do PC depois do instale) continua valendo.

---

# Revisão no robô `479b8f6` (PR #165) e nos testes `cd794d1` (PR #166) — 27/11/2026

O `origin/main` andou para **`d2cd695`** durante a revisão:
- `bdbf2a7` (#168): conserta o `test_T0024` do perfil analista;
- `2e84ef7` (#167): testes do T-0023;
- **`d2cd695` (#171): o T-0023 no robô, que mexe no laço das edições.**

## Veredito

| PR | head | Veredito |
|---|---|---|
| #165 robô | `479b8f6` | **Não aprovado: 0 🔴 e 1 🟡 (R-A).** O RD-0200 está certo. O 🟡 é o conflito com o main `d2cd695` no laço das edições |
| #166 testes | `cd794d1` | **Conteúdo aprovado: 0 🔴; 1 🟡 (T-A) só de merge.** O 🟡 B do robô está fechado pelo RD-0180 |

## 🟡

**R-A (#165): conflito com o `main` `d2cd695` em `bap_automation.py`, com uma armadilha de semântica.** O #171 mudou o `sincronizar_edicoes_web` do main:
- `aplicar_edicao_web(raiz, reg, opcoes, gravar, _saida=extra)`;
- `_registrar_aplicada_web(..., res["epoca"], extra)`: o `chave_pc` (ticket da garantia) vai para o registro das aplicadas.

O #165 tirou esse laço para o `puxar_fila_web`. Resolver o conflito ficando com o lado do #165 **perde o `chave_pc`** sem erro aparente.

Correção: no merge do main, o `sincronizar_edicoes_web` do #165 passa o `extra` do `aplicar` ao `registrar` (closure por registro, ou o `aplicar` devolvendo o extra), sem mexer no laço comum.

Pronto quando: `tests/test_T0023_robo.py` (linha ~500, `linhas[0]["chave_pc"] == "G-0001"` pelo `sincronizar_edicoes_web`) e os `test_T0045_*` passam no head novo. Commit novo = revisão do delta.

**T-A (#166): conflito com o `main` `d2cd695` em `.coord/diario/testes.md`.** É só acréscimo dos dois lados: fica com as linhas de ambos. Commit novo = revisão do delta, que deve ser rápida.

## O que rodei (cópias fora do repositório, venv 3.12, `xvfb-run`)

| Conferência | Resultado |
|---|---|
| `compileall` dos 2 `.py` e dos testes novos | ok |
| `merge-tree origin/main(d2cd695)` × `479b8f6` / × `cd794d1` | **conflito** em `bap_automation.py` (R-A) / em `.coord/diario/testes.md` (T-A) |
| `verificar --por-commit` (#166: 3 commits; #165: `a020b53..479b8f6`) | OK nos dois, sem violação. Trailers `Agente: testes` e `Agente: modulo-robo` |
| **#166 com o main sozinho** (`4fc6429` + `cd794d1`, os 8 arquivos da T-0045) | 53 ✅ e 11 pulados (todos "robô ainda não está no main"). Bate com o relato |
| **#166 com o main `d2cd695`** (+ `test_T0023_robo`) | 136 ✅ e 11 pulados |
| **main + #165 `a020b53` + #166 `cd794d1`** (arquivos da T-0045) | **239 ✅ e 0 ❌** com `xvfb-run`; sem display, 236 ✅ e 3 pulados (a tela). Bate com o relato |
| main `4fc6429` + #165 `a020b53` + #166, `pytest tests/` inteiro com `xvfb-run` | 896 ✅, 2 xpassed e 1 ❌: o `test_T0024_…_403_por_perfil`, do main, já consertado no `bdbf2a7` (#168) |
| main + #165 `479b8f6` + #166 (T-0045 + `test_T0021`) | **269 ✅ e 0 ❌** |
| `sonda6.py` (726 casos, `479b8f6` × `a020b53`; o `vm_a020.py` do autor é byte a byte o do `a020b53`) | 0 diferenças |
| `cmp_edicoes.py` / `sonda5.py` no `479b8f6` | TUDO IGUAL / TUDO OK |
| Minhas `s3.py` e `s6.py` no `479b8f6` | os 5 caminhos genéricos → `None`. Passagem por `/mfa` (0,6 s) e `/termos` (0,8 s) → login ok. `/aceite-termos` que fica → `MAXIMA_CONFIRMACAO` |

## #166 — os testes pegam defeito de verdade

Rodei os testes do #166 contra as versões antigas do robô (troca só dos 2 `.py`):

| Robô | ❌ | O que os testes pegaram |
|---|---|---|
| `11b24fc` | **49** | o índice do PC que recua (`test_RN_VIS_002_hora_do_indice_do_pc_nunca_recua`); o erro inesperado que segura a fila; a fase `navegador`; o captcha invisível; a URL inteira em vez do caminho; o D1; o D2; o fuso; `conferir_importado`; o log dobrado |
| `ed640e1` | 30+ | D1, D2, fuso, `_fase` fora de `FASES`, `conferir_importado`, log |
| `3511814` | **8** | exatamente os 5 caminhos da minha `s3.py` (`test_RN_VIS_005_login_conservador_olha_so_o_caminho_da_url`), a passagem curta (`…_verificacao_de_passagem_nao_pausa`), as 2 leituras e o `/nova-senha` |

- **Os casos s3 e s6 estão lá:**
  - os 5 caminhos na `test_T0045_robo_nuvem.py:682-686`;
  - a passagem de menos de 1 s e a 2ª leitura com `time.monotonic() >= 1.0` (linha 115).
- **Guardas de skip:** com o robô no main, todas somem (0 pulados com `xvfb-run`). Sem o robô, pulam só as que dependem dele (11).
- **Régua das edições:** a `FONTE` do `ref_T0045_edicoes_web_main.py` é **idêntica**, por AST, às 5 funções do main `4fc6429`. O `test_RN_GER_012_*` compara resultado, chamadas, log e estado.
- **RD-0180:** o `test_RN_GER_012_funcoes_publicas_das_edicoes_continuam` agora confere só `ler_estado_edicoes_web` e `sincronizar_edicoes_web`. **Fecha o 🟡 B.**
- **§4.4:**
  - web antiga 404 mudo e sem POST;
  - lote importado byte a byte;
  - `fechados_pc` em toda volta (1ª e 2ª);
  - época nova sem duplicar e outro conteúdo com `-2`;
  - sha256 ruim (cabeçalho, linha, arquivo, `bytes`, base64);
  - `..`, barra, pasta ≠ nome, dia futuro ou diferente, e "um ruim = nenhum gravado";
  - hora que não recua;
  - erro inesperado → `erro`/`dia`, com disco e Excel aberto continuando pendentes;
  - `puxar_fila_web` como laço único das 2 filas, com páginas, 409 e confirmar que falha;
  - `depois_de_baixar` uma vez;
  - ponta a ponta `diario/AAAAMMDD.csv` = o do PC;
  - matriz web × robô novo/antigo com a `web/app/visitas.Visitas` de verdade.
- **Fixtures sem dado real:**
  - `visitas_nuvem_fixture.py` usa `VENDEDOR FICTICIO UM`/`DOIS`, `CLIENTE FICTICIO` e tokens fictícios;
  - nenhum dos 40 nomes de pasta reais de `RELATORIOS/Visitas/ANALITICO` aparece nos testes nem no `docs/testes/T-0045.md`;
  - nenhum padrão de CNPJ, CPF, telefone ou e-mail;
  - a tela troca o `ler_config` (nunca lê o `visitas_config.json`);
  - nada de `auth/`, `.env`, TomTom ou Google;
  - rodar os testes não grava nada versionado (só o cache do Python).

## #165 — o RD-0200 no 479b8f6

- `_classificar` → `(codigo, so_pelo_caminho)`, e `so_pelo_caminho` é `True` só no ramo "caminho de verificação sem texto". É **o mesmo** conjunto que o `cod == MAXIMA_CONFIRMACAO and not _texto_claro(texto)` do `a020b53`: chegar a esse ramo implica que `_RX_BLOQUEIO` e `_RX_CONFIRMACAO` não casaram, que é exatamente o `not _texto_claro`. O `classificar_login` público continua com a mesma assinatura e devolve `[0]`. A `sonda6.py` mostra 0 diferenças em 726 casos.
- **O debounce `vistos.setdefault(caminho, agora)`, julgado como o corretor pediu:** **não abre alarme falso no login normal.**
  - O `pronto()` termina com "ok" na primeira leitura de um caminho que não é `/login` nem da lista fechada. Uma "passagem rápida que volta ao mesmo caminho" só existe **dentro** da lista: o login normal não passa por `/mfa` nem por `/verificacao`.
  - Voltar ao `/login` no meio não mudava nada no `a020b53` (ele também só zerava a contagem num caminho da lista). A `s7.py` dá o mesmo resultado nos dois heads para `/mfa → /login → /home` e para `/mfa → /otp → /mfa → /home` (login ok).
  - A única diferença é `/mfa → /verificacao → /mfa` que **fica**: o `479b8f6` decide em ~1,2 s e o `a020b53` em ~2,4 s. Os dois devolvem `MAXIMA_CONFIRMACAO`, a mesma resposta certa, só mais cedo.
  - Por isso fica como 🟢 (R-B), não 🟡.

## 🟢 (não bloqueiam)

- **R-B (#165):** se o gerente quiser a semântica exata do `a020b53`, basta contar desde a última mudança de caminho (`if vistos.get("c") != c: vistos.update(c=c, em=agora)`). Fixar o comportamento escolhido num teste com `/mfa → /verificacao → /mfa`, que hoje nenhum teste distingue.
- **T-B (#166): guardas que podem mascarar defeito.** As guardas `hasattr(vm, "classificar_login")` / `hasattr(ba, "sincronizar_visitas_web")` são certas enquanto o robô não está no main. Depois do merge do #165, porém, um renome dessas funções faria **arquivos inteiros pularem em silêncio**. Se o #165 entrar antes do #166, tirar as guardas no próprio #166; se entrar depois, abrir a tarefa de tirá-las logo após.
- **T-C (#166): a tela não roda no CI.** O CI (`.github/workflows/ci.yml`) roda `pytest tests` sem `xvfb-run`, então os 3 testes da tela do aviso (`test_RN_VIS_004_*`) pulam no CI. É governança: recado ao Alexandre/po, para o `xvfb-run` no passo do `pytest`.
- **T-D (#166): régua defasada.** A régua `ref_T0045_edicoes_web_main.py` congela o laço do `e1d80a8`, e o #171 mudou o laço de propósito (`_saida`/`extra`). O teste continua passando (as fixtures não têm garantia), e o `chave_pc` é coberto pelo `test_T0023_robo`. Mesmo assim, pelo próprio docstring da régua, ela deve ser atualizada ao laço do `d2cd695` num PR do testes.
- **T-E:** o docstring do `test_RN_GER_012_funcoes_publicas…` cita "RD-0172". O RD das 3 funções apagadas foi informado como RD-0173: conferir a numeração.

---

# Reteste do R-A no robô `c1ad1be93e1ed85a5ffd333ef71d8cb2e561ef04` (PR #165, 27/11/2026)

`c1ad1be` = merge de `479b8f6` com o main `d2cd695` (#167, #168, #171). `Agente: modulo-robo`.

## Veredito no c1ad1be

**Robô aprovado: 0 🔴 e 0 🟡.** O R-A está fechado. Os 🟢 continuam como sugestões, inclusive o R-B (debounce). O #166 será relido no head novo que o gerente anunciou.

## O merge (pelo `git show --remerge-diff`)

A resolução mexe só em 4 pontos, todos certos:

1. **`puxar_fila_web`:** o laço cria `extra = {}` por registro, chama `aplicar(reg, extra)` e repassa o mesmo `extra` ao `registrar(reg, status, motivo, epoca, extra)`. O docstring foi atualizado.
2. **`sincronizar_edicoes_web`:** `aplicar_edicao_web(raiz, reg, opcoes, gravar, _saida=extra)` e `_registrar_aplicada_web(raiz, reg, status, motivo, epoca, extra)`, exatamente como no laço do main `d2cd695`.
3. **`sincronizar_visitas_web`:** recebe e ignora o `extra` (`_extra`) nos 2 lambdas. O registro das visitas não muda.
4. O resto do #171 entrou pelo merge automático. Não sobrou marcador de conflito, o `visitas_maxima.py` é igual ao do `479b8f6` e, contra o main, os arquivos alterados continuam só os 2 `.py`.

## O que rodei (cópia fora do repositório, venv 3.12, `xvfb-run`)

| Conferência | Resultado |
|---|---|
| `compileall` dos 2 `.py` | ok |
| `merge-tree origin/main(d2cd695) c1ad1be` | sem conflito |
| `verificar --por-commit 479b8f6..c1ad1be` | OK (3 commits), nenhuma violação |
| main `d2cd695` + `c1ad1be` + #166 `cd794d1`: T-0045 + `test_T0021` + `test_T0023_robo` | **352 ✅ e 0 ❌**, com o `chave_pc == "G-0001"` pelo `sincronizar_edicoes_web` |
| os testes do main que o #171 tocou (`test_T0023_*`, `test_T0013_pacote_web`, `test_T0017_pacote_tres_farois`, `test_T0024_*` do robô e da trava, `test_T0035_robo_web`) | **241 ✅ e 0 ❌**. O `test_T0024_…_403_por_perfil` já passa (#168) |
| `cmp_edicoes.py` com a régua trocada para o `bap_automation.py` do **`d2cd695`** | **TUDO IGUAL** (7 cenários) |
| `sonda6.py` (726 casos × `a020b53`) / `visitas_web.py` / `sonda2.py` / `sonda5.py` | 0 diferenças / TUDO OK / TUDO OK / TUDO OK |
| Minhas `s1.py` e `s3.py` | o índice do PC não recua; os 5 caminhos genéricos → `None` |
| **Mutação:** tirar o `extra` do `_registrar_aplicada_web` no `sincronizar_edicoes_web` | `test_T0023_robo.py::test_RN_GER_012_a_linha_nova_nunca_e_criada_duas_vezes_e_o_antes_fica_gravado` **falha**: a rede pega a perda do `chave_pc` |

Não repeti o `pytest tests/` inteiro neste head. Os arquivos do merge foram cobertos pelas 2 rodadas acima (T-0045 + T-0021 + T-0023 + T-0013/0017/0024/0035).

---

# Reteste dos testes `4a3089f` (PR #166, item 9) — 27/11/2026

O head `4a3089f` está sobre o main `eb7e267`, que já tem o robô #165. Os `visitas_maxima.py` e `bap_automation.py` do `eb7e267` são byte a byte os do `c1ad1be` aprovado. Desde o `cd794d1` entraram:
- 2 merges do main (`2e63019` com `d2cd695`, `e5954ee` com `eb7e267`);
- `b8aa385` (régua no `d2cd695`, guardas fora, RD-0201);
- `4a3089f`.

Todos com `Agente: testes`.

## Veredito no 4a3089f

**Aprovado: 0 🔴 e 0 🟡.** O T-A (conflito no diário), o T-B (guardas) e o T-D (régua) estão fechados. O T-E (numeração do RD) fica como o autor registrou (RD-0172). O T-C (a tela fora do CI, governança) continua 🟢.

## Conferido

- **Merges:** o `--remerge-diff` dos 2 merges só resolve `.coord/diario/testes.md`, ficando com as linhas dos dois lados (só acréscimo). Nenhum `.py` do PC entra pelo #166: contra o main, os arquivos alterados são só os de `tests/`, `docs/testes/T-0045.md` e o diário. `merge-tree origin/main(eb7e267) 4a3089f` sem conflito; `verificar --por-commit` OK nos 5 commits.
- **Régua no `d2cd695`:** a `FONTE` do `ref_T0045_edicoes_web_main.py` é **idêntica, por AST**, às 5 funções do `bap_automation.py` do `d2cd695`, inclusive o `_saida=extra` e o `extra` no `_registrar_aplicada_web`. O docstring explica a troca do `e1d80a8` para o `d2cd695`.
- **Teste novo `test_RN_GER_012_chave_pc_da_garantia_chega_ao_registro_igual_ao_main`:** compara laço extraído × régua com um `aplicar_edicao_web` falso que preenche o `chave_pc` (`TICKET-FICTICIO-0001`, fictício). **Mutação:** trocar o `extra` por `{}` no `registrar` do `puxar_fila_web` → esse teste **falha**. Ele pega exatamente o risco do R-A.
- **Guardas `hasattr` fora:** `robo_nuvem`, `visitas_web_robo`, `matriz`, a paridade robô × web e a do `test_T0045_plano`. O que sobra de `skip` é legítimo: sem tkinter ou sem display (a tela) e "sem índice de baixas nas bases congeladas" (o plano).
- **RD-0201:** o novo nome (`test_RN_VIS_003_gravar_excel_importado_levanta_o_motivo_do_conferir_importado`) descreve o que o teste confere.
- **Dados:** o teste novo e os ajustes continuam só com dados fictícios.

## O que rodei (cópia fora do repositório, venv 3.12)

| Conferência | Resultado |
|---|---|
| `compileall tests/` | ok |
| Arquivos da T-0045 (`ref_` + `test_T0045_*`), com `xvfb-run` | **240 ✅ e 0 ❌**, nenhum pulado. Bate com o relato |
| `pytest tests/` inteiro, sem display | **1029 ✅**, 3 pulados (a tela) e 2 xpassed, saída 0. Bate com o relato |
| Mutação no repasse do `extra` | `test_RN_GER_012_chave_pc_…` ❌ (1 de 19 no arquivo) |
