# T-0023 v2 e T-0025 v2 · Reteste de redundância do desenho (corretor-redundancias)

- **Escopo:**
  - `git diff 75d66f5 origin/engenheiro-software/T-0023-T-0025-contrato`, com 7 arquivos: o contrato §10.7.6, §10.9 e §10.10; a ADR 0005; a ADR 0001, adendo 6 (novo); os dois `docs/desenho`; o README das decisões; o diário.
  - `git diff origin/main...origin/gerente-projetos/T-0023-regras`, só o `docs/produto/03-regras.md`.
- **Head SHA revisado:** `97ccba78a75a8d90aba932a832b9610ad10fdbe9` (contrato). O `T-0023-regras` foi revisado em `58760c0513d74cf7b5fa5e7585a75a4f7899eda6`.
- **Resultado:** **não libera.**
  - Dos 13 achados, 11 estão fechados. O RD-0093 e o RD-0095 têm resto em aberto.
  - A correção e as decisões P1 a P4 criaram 6 repetições novas, do RD-0104 ao RD-0109: 1 alta, 4 médias e 1 baixa.
  - Nenhum achado está só em comentário ou título de teste.
- **Numeração:** os RD-0098 a RD-0103 já são da T-0045. Os achados novos deste reteste são os **RD-0104 a RD-0109**, na ordem em que aparecem.
- **`03-regras.md`:** o gerente-projetos informou que já o corrigiu em `c8f445a`. Aquele commit não foi retestado aqui: o texto abaixo vale para o `58760c0`.
- **Donos:** engenheiro-software (contrato, ADRs e desenhos) e gerente-projetos (`03-regras.md`, no RD-0095 e no RD-0104).
- As linhas do contrato são as do arquivo no head (o §10.9 começa na 1027).

## Os 13 achados do parecer anterior

| ID | Situação | Evidência no head |
|---|---|---|
| RD-0085 | fechado | ADR 0005 §3 (36-41) e §4 (55-58) apontam para o §10.9.5 e o §10.9.3; a contagem de passos só está no contrato:1258. Sobrou uma frase repetida: ver RD-0109 |
| RD-0086 | fechado | contrato:1075-1080, `relatorios_nucleo.MAX_TEXTO_EDICAO` (um lugar só, o robô importa o núcleo); os números saíram da tabela do §10.9.3 (1131, 1133); `LIMITES_TEXTO_EDICAO_WEB` não aparece mais em nenhum dos 4 arquivos |
| RD-0087 | fechado | contrato:1180-1181, o núcleo põe o `Kpi.coluna`; `_KPIS_DA_COLUNA_WEB` sumiu |
| RD-0088 | fechado | linha nova no §10.7.6 (794); o §10.10.4 (1399) só cita a constante |
| RD-0089 | fechado | contrato:1394-1401: 2 linhas mais "os outros" do §10.8.7; a frase da memória saiu |
| RD-0090 | fechado | contrato:1041, 1332 e 1389, como proposto |
| RD-0091 | fechado | contrato:1287 (o "Mudou no PC?" entra na lista do que vale) e 1304; o "Antes de cada PR" saiu |
| RD-0092 | fechado | as Fontes (1031-1035) só citam; o Status da ADR 0005 foi limpo; a P1 virou decisão (1196) |
| RD-0093 | **resto em aberto** | abaixo |
| RD-0094 | fechado | o risco de concorrência saiu da T-0025, e os riscos de dado pessoal apontam para o contrato (T-0023:126, T-0025:144) |
| RD-0095 | **resto em aberto** | abaixo |
| RD-0096 | fechado | ADR:41 e T-0023:105 citam `MSG_EDICAO_SO_WEB` |
| RD-0097 | fechado | contrato:1375-1382, bloco `colunas-fora-por-tabela`, com o teste das duas cópias |

### RD-0093 (resto) · O resumo da ordem nos desenhos já diverge do §10.9.6, e o "Antes" está 3 vezes
- **Onde:**
  1. T-0023:68 e T-0025:75 resumem a ordem como "web → núcleo → robô → PC só leitura → testes". Falta o passo 1 do §10.9.6 (1275), "testes que destravam o CI". O §3 dos dois desenhos tem esse PR ("testes (PR 1, destrava)").
  2. O "Antes" do §10.9.6, item 0 (1271-1274), aparece de novo no T-0023:69 (T-0033) e no T-0025:76-77 (T-0023 v2 e lote B).
  3. "O lote B só começa com o lote A no `main`" está em 3 lugares: contrato:1274, T-0025:41 e T-0025:77.
- **Severidade:** média (o resumo já perdeu um passo).
- **Proposta:**
  - T-0023:68-69, **depois:** "A ordem é a do contrato §10.9.6 (fonte única)." A linha 70 fica.
  - T-0025:75-77, **depois:** "A ordem é a do contrato §10.9.6 (fonte única), uma vez por lote." As linhas 78 a 80 ficam.
  - T-0025:41 sai.

### RD-0095 (resto) · As RNs ficaram escritas no `03-regras.md` e de novo nos desenhos, com textos diferentes
- **Onde:** o `03-regras.md` (branch `gerente-projetos/T-0023-regras`) já tem a RN-GER-014, a 015, a 016, a RN-POS-005 e a 006. Os desenhos ainda têm o bloco "RNs a numerar" (T-0023:114-117 e T-0025:133-136), com outro texto:
  - **RN-GER-015:** no desenho, "PTS VÁLIDOS + PTS RELÂMPAGO, em pontos […] os pontos seguem visíveis para `vendas` (P4, provisória)"; no `03-regras.md`, nada da conta nem da P4;
  - **RN-GER-016:** no desenho, a cópia antes e o `antes` valem para "config, DDR, Expositores"; no `03-regras.md`, só para a config (ver RD-0104).
- **Tipo:** doc. **Impacto:** decisão (o `testes` cita a RN, e cada texto diz uma coisa).
- **Severidade:** média.
- **Proposta:**
  - T-0023:114-117, **depois:** "**RNs:** RN-GER-014, RN-POS-005 e RN-POS-006 (`docs/produto/03-regras.md`, fonte da verdade)."
  - T-0025:133-136, **depois:** "**RNs:** RN-GER-014, RN-GER-015 e RN-GER-016 (`docs/produto/03-regras.md`, fonte da verdade)."
  - A P4, se o Alexandre a confirmar, entra só no `03-regras.md` (gerente-projetos).

## Repetições novas

### RD-0104 · A exceção "edição no lugar" está em 6 lugares, e a RN cobre só parte dela
- **Onde:**
  1. contrato §10.9.3 (1145-1150): DDR, Expositores e config, com **as 2 garantias** (`antes` e cópia antes) para os três;
  2. ADR 0005 §3.5 (42-45): repete as 2 garantias;
  3. T-0025:141 (risco 1): repete;
  4. T-0025:136 (RN-GER-016 do desenho): repete;
  5. `03-regras.md`, RN-GER-012: "quando a tela do PC troca uma célula (DDR e Expositores), o robô […] guarda o valor anterior (`antes`)". Ali, **sem a cópia antes**;
  6. `03-regras.md`, RN-GER-016: na config, "guarda uma cópia do arquivo antes de gravar". Ali, **sem o `antes`**.
  O mesmo fato fica partido em 2 RNs, e cada uma traz uma das 2 garantias. Pela fonte da verdade, o DDR fica sem cópia e a config fica sem o `antes`, ao contrário do contrato. O `03-regras.md` também repete o mecanismo do contrato (o `antes`, o "registro das edições aplicadas").
- **Tipo:** doc. **Impacto:** decisão (o `testes` testa pela RN e não cobre a cópia do DDR) e manutenção.
- **Severidade:** alta (confunde).
- **Proposta:** a regra fica numa RN só, em linguagem de regra, e o resto aponta para ela.
  - **`03-regras.md`, RN-GER-012**, a 1ª "Exceção", **depois:** "Exceção: onde a tela do PC já editava no lugar (DDR, Expositores e a config editada pelo site), o robô usa a mesma função, guarda o valor anterior de cada troca e faz uma cópia do arquivo no dia, antes da 1ª gravação (27/11, T-0025 v2)."
  - **`03-regras.md`, RN-GER-016**, **depois:** "RN-GER-016 · Um arquivo de configuração só passa a ser editável pelo site com um "autorizo" do Alexandre para aquele arquivo (6 A do R-20261126-180314-alexandre; ADR 0005). O primeiro é o `champions_config.json` (T-0025 v2)."
  - Contrato:1145, **depois:** "- **Exceção da RN-GER-012, a edição no lugar:** DDR, Expositores e a config gravam com a mesma função da tela do PC. As 2 garantias:" (seguem os itens 1 e 2, sem a frase sobre quem escreve a RN).
  - ADR:42-45, **depois:** "5. **A edição no lugar é a exceção da RN-GER-012** (a config, o DDR e os Expositores não têm diário). As garantias estão no contrato §10.9.3."
  - T-0025:141, **depois:** "- As funções do PC editam no lugar (a exceção da RN-GER-012; garantias no §10.9.3)."

### RD-0105 · A conta do TOTAL A PAGAR e a P4 contadas 3 vezes, e 2 vezes dentro do próprio contrato
- **Onde:**
  1. **"vendas refaz o número":** contrato:1187, T-0025:147 (risco 3) e T-0025:157 (P4, "O fato");
  2. **"nenhuma coluna em R$ é pagamento":** contrato:1186 e contrato:1192 (a mesma ideia, 6 linhas abaixo), mais T-0025:158;
  3. **a alternativa "cortar também PTS VÁLIDOS e PTS RELÂMPAGO":** contrato:1194 e T-0025:159.
- **Tipo:** doc. **Impacto:** leitura e manutenção. A P4 é provisória, e quando o Alexandre responder serão 3 lugares para mudar.
- **Severidade:** média.
- **Proposta:** o fato fica no contrato, e a decisão fica no desenho.
  - Contrato:1192 sai (o 1186 já diz).
  - Contrato:1194, **depois:** "A alternativa, se o Alexandre pedir: `docs/desenho/T-0025.md`, §7, P4."
  - T-0025:157-158, **depois:** "- **O fato:** contrato §10.9.4 ("A conta"). **Como fica:** só a coluna TOTAL A PAGAR e o cartão saem para `vendas`."
  - T-0025:147, **depois:** "- Os pontos continuam visíveis para `vendas` (P4, §10.9.4)."

### RD-0106 · O adendo 6 da ADR 0001 repete a RN-GER-012 e a ADR 0005
- **Onde:** a ADR 0001:450 diz "As regras e os formatos ficam **só** no contrato […] e na ADR 0005. Este adendo registra a decisão." Mesmo assim:
  - os itens da ADR 0001:455-457 ("Só o admin edita", "chega ao PC pelo robô, gravada pela função da tela do PC", "A tela do PC fica só leitura") são a RN-GER-012;
  - a ADR 0001:459 ("só com um "autorizo" do Alexandre por arquivo (6 A) […] O primeiro é o `champions_config.json`") é a ADR 0005 §3.6, que também está na RN-GER-016.
- **Tipo:** doc. **Impacto:** manutenção (a 6 A fica em 4 lugares: ADR 0001, ADR 0005, RN-GER-016 e o cabeçalho da T-0025).
- **Severidade:** média.
- **Proposta:**
  - ADR 0001:454-458, **depois:** "2. **O item 4 do adendo 5 é substituído:** o site edita onde o contrato §10.9.3 lista um lugar, pela RN-GER-012 (inclusive Pedidos e Entregas, no `main` desde a T-0021 v4). Troca de loja de coleta, "Atualizar visitas", parciais e "Exportar campanha" continuam no PC."
  - ADR 0001:459, **depois:** "3. **Config editada pela web:** ADR 0005 e RN-GER-016."

### RD-0107 · A P2 A está escrita 4 vezes no T-0023 e de novo na RN-GER-012
- **Onde:** T-0023:36 (Não entra), :60 (modulo-farois, PR 2), :105 (critério 6), :132 (risco 6, com os campos `contato_nome` e `contato_fone` e "a única exceção ao PC só leitura […] na RN-GER-012") e :136 (§7, "exceção à RN-GER-012, risco 6"). A exceção também já está na RN-GER-012 do `03-regras.md`. O critério (:105) e o dono (:60) se justificam; o Não entra, o risco e o §7 dizem a mesma coisa.
- **Tipo:** doc. **Impacto:** leitura e manutenção.
- **Severidade:** média.
- **Proposta:** a decisão fica uma vez no §7, e o resto aponta para ela.
  - T-0023:36, **depois:** "- o contato do cliente na garantia (P2 A, §7);"
  - T-0023:132, **depois:** "6. **Garantia nova sem contato** (P2 A, §7): a assistente completa o contato no PC até ele voltar a ser visto."
  - T-0023:136, **depois:** "- **P2 A — Contato do cliente na garantia:** fica editável só no PC (exceção da RN-GER-012). No `DialogoGarantia`, só `contato_nome` e `contato_fone` gravam. A garantia nova nasce no site sem contato, e o telefone nunca passa pelo site."
  - [SUPOSIÇÃO] Pela redação, o risco 6 só se resolve quando o contato for visto no site. Se o risco não existe, o item 6 sai.

### RD-0108 · A web passa a calcular o número do ticket, que é regra do `garantias`
- **Onde:** contrato:1112: "A web soma a ele as garantias novas ainda pendentes na fila (ex.: o padrão G-0013 com 1 pendente vira G-0014)." Hoje, o número da garantia é regra do PC (`garantias.novo_ticket`; a conferência é do `garantias.renomear`). Com a soma, a web precisa conhecer o formato do ticket (prefixo e dígitos) e fazer a conta dela. É uma segunda cópia da regra de numeração, num módulo que não importa o código do PC. Os Expositores resolvem o mesmo problema sem cópia: o PC dá a chave `EXPnnnn` na gravação (contrato:1133).
- **Tipo:** código. **Impacto:** manutenção. Se o PC mudar o formato do ticket, a web sugere um número errado, e o robô recusa com "já existe".
- **Severidade:** média.
- **Proposta:**
  - contrato:1112, **depois:** "- **Ticket da garantia:** o `padrao` do `ticket` é o `garantias.novo_ticket` do pacote. Se o ticket que chega é o padrão e ele já foi usado nesta rodada, o robô grava com o `garantias.novo_ticket` da hora, como o `EXPnnnn` dos Expositores. O ticket digitado diferente do padrão segue a regra de hoje (repetido = `erro`). A web não calcula número."
  - No T-0023:58, sai "ticket sugerido com as pendentes" do `edicoes.py`.
  - `manter?`: se o admin precisar ver o número final antes de salvar, a soma na web fica. Aí o formato do ticket vai no pacote (ex.: `padrao` + `prefixo`), para a web não deduzir.

### RD-0109 · Duas frases repetidas pela correção
- **Onde:**
  1. "um teste por passo": contrato:1258 ("Os testes seguem estes passos, um teste por passo") e ADR 0005:58;
  2. "a web mostra só ao admin" (o `AVISO_PARAMETROS_FORA`): contrato:794 (§10.7.6) e contrato:1243.
- **Tipo:** doc. **Impacto:** manutenção.
- **Severidade:** baixa (em doc, então segura o lote).
- **Proposta:**
  - ADR:58, **depois:** "- **Teste:** com config fictícia em pasta temporária, nunca na base real."
  - Contrato:1243: sai "A web mostra esse aviso só ao admin."

## `03-regras.md` (branch `gerente-projetos/T-0023-regras`) × contrato
- Ele repete o contrato em 1 ponto: a RN-GER-012 descreve o mecanismo (o `antes` "no registro das edições aplicadas"). Isso está no RD-0104, com o texto de regra pronto.
- Ele diverge do contrato em 2 pontos:
  - a exceção da edição no lugar está partida entre a RN-GER-012 e a RN-GER-016 (RD-0104);
  - a RN-GER-015 não tem a P4 que o desenho traz (RD-0095).
- `manter?`: o "corte no servidor, também no Excel, no PDF e nos cartões" da RN-GER-015 se sobrepõe ao §10.9.4. Mas é a exigência de segurança da decisão de 26/11, não o mecanismo, e fica.
- A RN-GER-014, a RN-POS-005 e a RN-POS-006 batem com o contrato e não o repetem.

## Liberação
**Não libera.** Ficam em aberto os restos do RD-0093 e do RD-0095 e os RD-0104 a RD-0109. O reteste vale para os novos heads das duas branches.

[SUPOSIÇÃO] Por instrução de quem chamou, ficaram de fora o catálogo, os recados aos donos, o commit e qualquer alteração no clone de código.
