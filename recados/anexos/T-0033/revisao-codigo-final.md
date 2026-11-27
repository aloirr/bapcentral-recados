# T-0033 — revisão de código final (revisor-codigo)

- **Data:** 27/11/2026 (Manaus).
- **Repositório:** `aloirr/bapcentral` (conferido com `git remote -v`). Base: `origin/main` em `767a389`.
- **Vale para os heads abaixo.** Um commit novo em qualquer branch pede revisão nova daquele branch.

| Parte | Branch | Head revisado | Parecer |
|---|---|---|---|
| Contrato | `engenheiro-software/T-0033-contrato-bc3` | `9ff2851` | 🟡 2 |
| RN-VIS-001 | `gerente-projetos/T-0033-rn-vis-001` (PR #135) | `046a4db` | aprovado |
| Web | `modulo-web/T-0033-revisao-geral` | `3165af2` | 🟡 3 · 🟢 4 |
| Faróis | `modulo-farois/T-0033-aderencia-cor` | `7de029b` | 🟡 1 · 🟢 2 |
| Rota | `modulo-rota/T-0033-marca` | `f39e389` | aprovado · 🟢 1 |
| Robô | `modulo-robo/T-0033-marca` | `ff6e7f0` | aprovado |
| Pós-venda | `modulo-posvenda/T-0033-marca` (PR #127) | `aa3fc77` | aprovado · 🟢 1 |
| Testes | `testes/T-0033-marca-aderencia` | `f91c265` | aprovado · 🟢 1 |

**Resultado: nenhum 🔴. Há 6 🟡 a corrigir antes do merge: 3 na web, 2 no contrato e 1 nos faróis.** Os 🟡 da web e do contrato vêm da mesma divergência entre os dois contratos e o manual.

## Conferências comuns (os 8 heads)
- **Segredos e dados pessoais:** nenhuma chave, senha, token, CNPJ ou e-mail de pessoa no diff somado. Só aparece `@bapautoparts.com.br`, dentro do teste da grafia.
- **Dado digitado intocável:** nenhuma das bases de dado digitado está no diff (`_EDICOES_POS_VENDA`, `_NCC`, `_GARANTIAS`, `_AUTORIZACOES`, `champions_config.json`, `transportadoras_config.json` e `painel_diretor_config.json`). O `planner_config.json` também ficou fora.
- **Pastas congeladas:** `RELATORIOS/`, `SISTEMA BAP/` e `BAP Ajuda 2.0/` ficam fora do diff líquido. A exceção está só no histórico do #127, como explica o 🟢 do pós-venda.
- **`bap_dados.VERSAO`:** continua 27, e nenhuma regra de cache mudou.
- **Governança:** o diff não mexe em `.claude/`, `.github/`, `donos.json`, `coord*.mjs` nem nos `.json` da raiz.
- **Donos:** `node scripts/coord.mjs verificar <dono> --base origin/main` deu OK nos 8 branches. Arquivos alterados por branch:

  | Branch | Arquivos |
  |---|---|
  | Rota | 2 |
  | Robô | 1 |
  | Contrato | 4 |
  | RN-VIS-001 | 1 |
  | Web | 36 |
  | Faróis | 8 |
  | Testes | 6 |
  | Pós-venda | 2 |

  Os commits trazem o trailer `Agente:`. O `--por-commit` aponta só os dois commits do #127.
- **Número do Diretor:** nenhuma conta mudou. Mudaram só cores, nomes e títulos ("Painel Executivo"). O `tom_aderencia` repete o corte antigo da linha: `>= 80` ok e `>= 50` atenção. O `test_T0022_numero_bate` passa.

## RN-VIS-001: a mesma regra no PC, no pacote e no site
- **PC:**
  - `relatorios_nucleo.tom_aderencia` pinta a linha.
  - `faixa_aderencia()` dá o chip de cada dia e da % acumulada.
  - Os dois usam o mesmo corte: `ADERENCIA_AMARELO = 50` e `ADERENCIA_VERDE = 80`.
  - O teto de cada faixa é `math.nextafter(corte, 0)`, e vale a regra `valor <= ate`, a mesma do `bap_visual.Tabela._faixa_de`.
- **Robô:** o selo `faixa_opc` do `bap_automation._selo_web` repassa o chip do PC. Sem chip, a coluna vai sem cor e a aba fica. Chip torto tira só a aba.
- **Site:**
  - `tabelas._colunas_erro` aceita a faixa só nas colunas `pct` da "Aderência dia a dia".
  - `_faixa_de` usa o mesmo `<=`.
  - A web não tem 50/80 escrito em lugar nenhum: a cor sai pronta do PC.
- **Bordas testadas:**
  - `tests/test_T0033_aderencia_cor.py`: 0, 49,99, 49,99995, 50, 50,01, 79,99, 79,99995, 80, 80,01, 100 e 125; tom e chip juntos e contra o manual.
  - `tests/test_T0033_aderencia_pacote.py`: PC → robô → `tabelas.validar` e `pacotes.validar`, com chip, sem chip e com chip torto.
  - `web/tests/test_T0033_grade.py`: 100, 75, 50 e 0 desenhados.
  - **Resultado: a RN-VIS-001 é a mesma no PC, no robô e no site.**

## 🟡 Corrigir antes do merge

**W1. Web, `web/app/main.py:396`: com estado escolhido, a aba mostra o número da BAP inteira, e às vezes sem dizer de onde ele vem.**
- O cartão só ganha "BAP inteira" ou "sem o filtro" quando o PC não pôs `detalhe` (`k.get("detalhe") or ...`). Se o cartão já tem detalhe, o número da BAP inteira aparece com o estado "AM" marcado e sem marca nenhuma.
- Os contratos dizem outra coisa:
  - `tela-bc3.md` §4.2 (l. 83) e a tabela de estados (l. 262): estado sem recorte mostra "—", "nunca o número da BAP inteira".
  - `relatorio.md` §10.7.2 (l. 670 e 821) e §10.7.6 (l. 788): com filtro, recorte ou estado, os cartões da aba saem e entra o `AVISO_CARTOES`.
- **Correção:**
  - com estado sem recorte, "—" no `kpis_padrao`, como manda o tela-bc3;
  - com filtro ou recorte, a marca vai sempre, por exemplo "sem o filtro · {detalhe}";
  - um teste com um cartão que já traz `detalhe`.

**W2. Web, `web/app/templates/base.html:6`: o `<title>` passou a "{tela} · BAP Central".**
- O manual aprovado diz, no §7 (Site, PC): "Aba do navegador: '{tela} · BAP AUTOPARTS'".
- O manual é a fonte única da marca e só muda com um novo "aprovo" do Alexandre.
- **Correção:** voltar a "· BAP AUTOPARTS" ou levar a troca ao Alexandre pelo design-de-marca. Ver C2.

**W3. Web, `web/app/tabelas.py:187`: o `PALETA_TOM["ok"]` usa `--verde-claro` #E5F3DF com `--verde-escuro` #2F7D32.**
- O manual proíbe essa combinação no §4.4: dá 4,44:1 em texto pequeno.
- O §4.2 criou o `--ok-claro` #F0F7EC para esse caso, e o `CHIP_SLA` do Pedidos já usa esse tom.
- Hoje o SLA da Entregas e o do Pedidos saem com verdes diferentes.
- **Correção:** `("--ok-claro", "--verde-escuro")`. Ver F1, a mesma troca no PC.

**F1. Faróis, `bap_visual.py:1309`: a paleta do selo pela linha (`chip_tom`) ainda tem `"ok": ("#E5F3DF", "#2F7D32")`.**
- É o mesmo problema do W3 no PC.
- O branch trocou `atencao`, `alerta` e `cinza` nesse dicionário, mas deixou o `ok`.
- **Correção:** `"ok": ("#F0F7EC", "#2F7D32")`, igual ao `_VERD`.

**C1. Contrato, `.coord/contratos/relatorio.md:688`: a paleta fixa do `chip_tom` está velha.**
- O contrato ainda lista `#FFF1C7`, `#B3261E` e `#69736D`.
- O PC (F1) e a web (W3) já usam `#FFF4D6`, `#B42318` e `#5E6B63`.
- **Correção:** atualizar a linha, já com o `ok` #F0F7EC do F1/W3.

**C2. Contrato: o `tela-bc3.md` diverge do manual e do próprio `relatorio.md`.**
- (a) A l. 365 manda o `<title>` "<tela> · BAP Central", contra o manual §7. Ver W2.
- (b) O §4.2 (l. 83), "o número continua e ganha 'sem o filtro'", contradiz o `relatorio.md` §10.7.2 e §10.7.6, onde os cartões saem e entra o `AVISO_CARTOES`.
- **Correção:** escolher uma regra só e alinhar os dois contratos. A web segue a que ficar (W1).

## 🟢 Sugestões (não bloqueiam)
- **Faróis:** cores fora da paleta, que o branch não tocou.
  - `painel_cartoes.py:582`: `bom #2E7D32` e `ruim #C62828`, quase iguais ao `--ok` e ao `--alerta`.
  - `bap_visual.ATING_FUNDO` e `ATING_CORES`: o vermelho `#FDE0DE/#A3201A` e o verde `#DDF2DF/#1E6B2A`.
  - `relatorios_nucleo.AMARELO #C98A00`.
  - Hex soltos que o manual §4 manda trocar pela constante: `CHIP_SLA`, a última faixa; `CalendarioVisitas`, `#FDECEA`.
- **Faróis:** o `NOME_MARCA` existe só no `bap_visual`. O `email_parcial` e os outros `.py` ainda escrevem a grafia por extenso. Não é erro, porque o teste RN-GER-009 varre tudo.
- **Rota:**
  - `bap_planner.py:151-155`: `COR_ACENTO #4FA236`, `COR_ACENTO_ESC #3F8C2E` e `COR_OK #1E7A46` estão fora da paleta.
  - `email_rota.py`: `LIN #E3E7E2` é quase igual ao `--borda #E3E8E4`.
  - O `TButton` "pressed" foi para `#E3E8E4`, por troca mecânica do `#D5DAD4`. Vale conferir no print.
- **Web:**
  - Os 55 tokens `--c-*` do `:root` são hex soltos com outro nome; a consolidação é a MC-0006 do design-de-marca.
  - Restam 9 regras com `font-weight:800` (o manual §5 só aceita 400/600/700) e a Inter não está hospedada.
  - `_bc3_cab.html:29`: o seletor desligado não tem `aria-disabled="true"` e usa o `title` "Esta aba mostra a BAP inteira", que difere do tela-bc3 §4.2 ("Esta aba é só da BAP inteira").
  - `web/tests/farol_fixture.py:391`: os tetos 49,9999 e 79,9999 estão escritos à mão. O melhor é gerar a fixture do `faixa_aderencia()` do PC e testar 79,99 e 80 na tela.
- **Pós-venda (#127):**
  - Os commits `ea6a003` e `aa3fc77` gravam e depois desfazem o `RELATORIOS/painel_diretor_hist.json`. O diff líquido é zero e o squash resolve.
  - A causa é a suíte regravar o histórico. O `testes` corrige isso no `test_T0022_numero_bate`, com uma cópia temporária. Até esse PR entrar, quem rodar a suíte precisa de `git restore` antes do commit.
- **Testes:** as docstrings de `tests/test_T0033_aderencia_cor.py` (l. 3 e 9) e do `test_T0033_aderencia_pacote.py` dizem "50% a 79,99%". A RN-VIS-001 do `046a4db` diz "menos de 80%".

## O combinado: os 8 heads mesclados num branch local descartável
- **A mescla:** os heads entraram na ordem proposta, por cima do `origin/main` `767a389`, sem conflito.
- **Python:** 3.12, num venv com as dependências do `ci.yml`. O `python3` do ambiente (3.13) não tem `tkinter`.
- **Com os 8 heads:**
  - `python -m compileall -q .`: sem erro;
  - `pytest tests/`: **609 passed, 2 xpassed**;
  - `pytest web/tests`: **343 passed**;
  - o `painel_diretor_hist.json` ficou intacto;
  - os smokes não foram rodados.
- **Passos intermediários, para o CI de cada PR:**
  - Depois da web (`main + #127 + rota + robô + contrato + #135 + web`): `tests/` 552 passed e 2 xpassed; `web/tests` 343 passed.
  - Depois dos faróis (todos menos `testes`): `tests/` 552 passed e 2 xpassed; `web/tests` 343 passed.
  - Nos dois passos a suíte regravou o `RELATORIOS/painel_diretor_hist.json`, restaurado com `git restore`. É a falha que o branch `testes` corrige.
- O branch descartável foi apagado. Nada foi alterado nem enviado.

## Ordem de merge
**A proposta serve: #127 → rota → robô → contrato → #135 → web → faróis → testes.**
- **Robô antes da web não quebra o site.** O robô novo só manda o chip quando o PC o põe, e o PC do `main` não põe. Simulei o pacote do robô contra a web do `main`:
  - PC sem chip: a aba vai, sem chip, e `tabelas.validar` e `pacotes.validar` devolvem `[]`.
- **A dependência que obriga a ordem: os faróis só depois da web.** Com o PC já pintando o chip, a web do `main` recusa o pacote:
  - erro: `vc_visitas: tabela Aderência dia a dia: selo fora das colunas marcadas ou mal formado`;
  - ele aparece também no `pacotes.validar`, então o pacote inteiro do Visita cai.
  - A folga de 2 h do instale do PC ajuda, mas não vale contar com ela. **Faróis nunca antes da web.**
- **`testes` por último.** Os testes novos precisam do resto:
  - a grafia em toda a raiz e no site;
  - o `CORES_SINAL` do manual;
  - o chip no pacote, que pede robô, faróis e web.
- **#135 (só doc) e contrato (só `.coord/contratos`)** podem entrar em qualquer ponto antes da web. É melhor o contrato entrar já com o C1/C2 corrigido.
