# T-0023 v2 e T-0025 v2 · Parecer de redundância e excesso no desenho (corretor-redundancias)

- **Escopo:** `git diff origin/main...origin/engenheiro-software/T-0023-T-0025-contrato` (6 arquivos, +725 −1): `.coord/contratos/relatorio.md` §10.9 e §10.10, `docs/decisoes/0005-config-editada-pela-web.md`, `docs/desenho/T-0023.md`, `docs/desenho/T-0025.md`, `docs/decisoes/README.md` e o diário. Comparado com o `main` (`a32b610`): o contrato §10.1, §10.7 e §10.8, `web/app/edicoes.py`, `web/app/tabelas.py`, `web/app/main.py`, `bap_automation.py` (`EDICOES_WEB`, `CAMPOS_EDICAO_WEB`, `edicao_web`, `validar_edicao_web`, `aplicar_edicao_web`, `gravar_edicoes_pc`, `opcoes_edicao_web`, `_CORTES_FAROL_WEB`, `_AVISO_SO_PC_WEB`) e `bap_relatorios.py` (`EDICAO_SO_WEB`, `MSG_EDICAO_SO_WEB`).
- **Head SHA revisado:** `75d66f577499f2af8b7bd36e4cbfb3996e7eff78`.
- **Numeração:** os RD-0082 a RD-0084 já são do PR #137 (T-0045). Este parecer usa do **RD-0085 ao RD-0097**.
- **Resultado:** **não libera.** São 13 achados (1 alto, 11 médios, 1 baixo), todos em docs do desenho. Nenhum está só em comentário ou título de teste.
- **Dono de todos os achados:** engenheiro-software (`node scripts/coord.mjs dono` nos 4 arquivos).
- **Linhas:** as do contrato são as do arquivo na branch (o §10.9 começa na 1026). As da ADR e dos desenhos são as do arquivo.

## Achados

### RD-0085 · A ADR 0005 repete o §10.9.5, com outra contagem de passos
- **Onde:** ADR 0005 §3, itens 1 a 4 (36-48), e §4 (58-61) × contrato §10.9.5 (1163-1213).
  1. **Fila:** os 4 campos (`modulo`, `chave`, `valores`, `antes`) estão na ADR:37-41 e no contrato:1196-1202.
  2. **Passos do robô:** a ADR:42-47 tem 5 itens; o contrato:1204-1211 tem 7. A ADR:61 manda "um teste por passo do §3.3" (5), e o `T-0025.md`:66 manda "os 7 passos do §10.9.5". O `testes` recebe duas listas.
  3. **Cópia antes:** ADR:46 × contrato:1115-1120. A ADR diz "nunca apagada"; o contrato diz "nunca é apagada pelo robô".
  4. **Dado pessoal e concorrência:** ADR:58-59 × contrato:1190-1192 e 1206.
- **Tipo:** doc. **Impacto:** manutenção (duas fontes para o mesmo formato) e decisão (quantos testes o `testes` escreve).
- **Severidade:** média.
- **Proposta** (o formato fica no contrato; a ADR diz o porquê e aponta para ele):
  - ADR:36-47, **depois:**
    "1. **No pacote:** o bloco `parametros_edicao`, só no farol dono da config, lido pela web só para o admin.
    2. **Na web:** uma página por config, uma aba por seção e um "Salvar" por seção, na fila da T-0021.
    3. **No robô:** troca só a seção, e só se o hash dela ainda bate. Valida e grava com as funções do PC, depois da cópia antes.
    Formato, fila e passos: contrato §10.9.5 (cópia antes: §10.9.3)."
  - ADR:58, **depois:** "- **Dado pessoal:** contrato §10.9.5 (tetos) e §10.10.3."
  - ADR:59, **depois:** "- **Concorrência:** pelo hash da seção (contrato §10.9.5, passo 2). A pessoa abre de novo e refaz."
  - ADR:61, **depois:** "- **Teste:** um teste por passo do contrato §10.9.5, com config fictícia em pasta temporária, nunca na base real."

### RD-0086 · O teto do texto fica em 3 lugares, e os documentos discordam sobre qual é a fonte
- **Onde:**
  - contrato:1079: "O teto do robô é a fonte […] O núcleo manda o mesmo número, e um teste do `testes` confere os dois";
  - `T-0023.md`:47, PR #103, muda 1 e 2: "regra no núcleo, o robô só traduz" e "Os tetos de texto ficam numa tabela só por (módulo, campo), conferida contra o `max` do pacote";
  - `T-0025.md`:53 aproveita `LIMITES_TEXTO_EDICAO_WEB` (tabela do robô);
  - a tabela do §10.9.3 traz os números uma terceira vez: "até 600" (1103), "até 80" e "até 200" (1105).
- **No código:** o número fica no `max` da `edicao` do núcleo e no `LIMITES_TEXTO_EDICAO_WEB` do robô, com um teste para manter os dois iguais. Hoje o robô já tem o `relatorios_nucleo` no mesmo PC (`edicao_web` importa `_edicao_autorizacao`). Não precisa de uma segunda tabela.
- **Tipo:** código e doc. **Impacto:** manutenção (uma regra com 2 cópias e um teste de sincronia) e leitura (um desenho diz "a regra fica no núcleo", o contrato diz "a fonte é o robô").
- **Severidade:** alta (confunde quem implementa).
- **Proposta:**
  - contrato:1079, **depois:** "**O robô confere de novo** (`validar_edicao_web`) por (módulo, campo): o tipo, a lista fechada do PC, a data, o valor e o teto do texto. O teto vem de **um lugar só**: `relatorios_nucleo.MAX_TEXTO_EDICAO[(módulo, campo)]`. O núcleo usa esse número no `max` da `edicao`, e o robô o usa ao conferir. Um `max` do pacote diferente do número do núcleo = `MOTIVO_TEXTO_WEB`."
  - `T-0023.md`:47, muda 2, **depois:** "2. O teto do texto vem do `relatorios_nucleo.MAX_TEXTO_EDICAO` (§10.9.1), sem tabela no robô."
  - `T-0025.md`:53: tirar `LIMITES_TEXTO_EDICAO_WEB` do "Aproveita".
  - §10.9.3, coluna "Campos": tirar os números ("até 80", "até 200", "até 600") e deixar só "(livre)" ou "(longo, `multilinha`)".

### RD-0087 · A marca do cartão restrito fica em 3 lugares: núcleo, robô e web
- **Onde:** o par `("vc_champions", "Vendedores"/"Supervisores")` e o `"TOTAL A PAGAR"` estão em `tabelas.RESTRITAS` (contrato:1135-1138) e de novo em `bap_automation._KPIS_DA_COLUNA_WEB` (contrato:1154). O rótulo "Total a pagar" fica no núcleo (`cartoes_de`), e um teste confere que os dois rótulos são iguais (contrato:1155). O `T-0025.md`:53 (muda 3) e o :66 repetem isso.
- **Tipo:** código. **Impacto:** manutenção. Se o núcleo trocar o rótulo, o teste só avisa, e a correção é em 2 arquivos.
- **Severidade:** média.
- **Proposta:** o núcleo já calcula o cartão a partir da coluna, então ele põe a marca no próprio `Kpi`. O modulo-farois já mexe no `relatorios_nucleo` na P1 A.
  - contrato:1154-1155, **depois:** "- Quem põe é o núcleo, no próprio cartão (`relatorios_nucleo.bap_champions`, `cartoes_de`: `"coluna": "TOTAL A PAGAR"`). O robô passa a chave sem mudança."
  - `T-0025.md`:53 (muda 3) e :66: tirar `_KPIS_DA_COLUNA_WEB`. A linha do modulo-farois no :64 ganha "`Kpi.coluna` no cartão Total a pagar".

### RD-0088 · Uma segunda tabela "fonte única" de textos de aviso
- **Onde:** contrato:1339, `AVISO_PARAMETROS_FORA` = "Os parâmetros das campanhas ficaram fora desta atualização. Veja no PC.", e contrato:1344: "tem o texto fonte única nesta tabela, como os do §10.7.6". A fonte única dos avisos é a tabela do §10.7.6 (RD-0024 e RD-0027). O robô e os testes passam a ler os avisos em dois lugares.
- **Tipo:** doc. **Impacto:** manutenção.
- **Severidade:** média.
- **Proposta:**
  - no §10.7.6, uma linha nova na tabela: "| `AVISO_PARAMETROS_FORA` | o robô, em `avisos` do `vc_champions` (§10.10.4) | `Os parâmetros das campanhas ficaram fora desta atualização. Veja no PC.` |";
  - contrato:1339, coluna "Aviso", **depois:** "`AVISO_PARAMETROS_FORA` · `AVISO_ABAS_FORA`";
  - contrato:1344 sai.

### RD-0089 · A tabela de tamanho e cortes repete a regra "os outros" do §10.8.7
- **Onde:** contrato:1333-1343.
  - A coluna "Teto do farol" repete "8 MB (robô) / 10 MB (web)" e depois "idem" 5 vezes. O número já está no §10.8.7 e no §10.8.3.
  - 5 das 7 linhas (`pl_devolucoes`, `pl_ncc`, os 3 DDR e `tm_expositores`) dizem "todas as `tabelas` saem · `AVISO_ABAS_FORA`", que é a linha "os outros" do §10.8.7.
  - A frase "A memória da web segue a ADR 0003 […]" (1343) repete o §10.8 e a ADR 0003.
- **Tipo:** doc. **Impacto:** leitura (7 linhas para 2 regras novas) e manutenção.
- **Severidade:** média.
- **Proposta:** só os 2 faróis com corte próprio ficam na tabela.
  - **Depois:** "Teto e corte: §10.8.7. Os 6 faróis abaixo de 60 KB (`pl_devolucoes`, `pl_ncc`, os 3 DDR e `tm_expositores`) seguem a linha "os outros". Dois têm corte próprio:" + a tabela só com as linhas `pl_garantias` e `vc_champions`, sem a coluna "Teto do farol".
  - 1342, **depois:** "Os 8 faróis somam cerca de 1,5 MB no disco do Render."
  - 1343 sai.

### RD-0090 · As chaves que nunca vão e o `CONTATO CLIENTE`, cada um dito 2 ou 3 vezes
- **Onde:**
  1. **Chaves de topo:** contrato:1040 ("`editar`, `abrir`, `garantia`, `campanha_export`, `_champions` e qualquer callable continuam fora, sempre") × contrato:1323-1328 ("Nunca vão": `garantia`, `campanha_export`, `_champions`, `editar` e `detalhe_pedido`). O §10.1 do `main` já tira o `_champions` (chave com `_`) e o `editar`/`abrir` (nunca, em qualquer nível), e a lista branca do §10.1 já deixa o resto fora.
  2. **`CONTATO CLIENTE`:** contrato:1270 ("nunca vai […] o robô corta, e a web recusa") × contrato:1317 (a mesma regra, com os nomes das constantes).
- **Tipo:** doc. **Impacto:** leitura e manutenção (3 listas de chaves proibidas).
- **Severidade:** média.
- **Proposta:**
  - contrato:1040, **depois:** "**Exceção às listas "Fora, sempre" do §10.1 e do §10.7.2:** a chave `edicao` vai no pacote **só** na forma desta seção e **só** nos lugares da §10.9.3. Em qualquer outro lugar, ela continua proibida, e a web recusa o pacote. As outras chaves proibidas não mudam (§10.10.3)."
  - contrato:1323-1328, **depois:** "- **Nunca vão** (fora da lista branca do §10.1): `garantia`, `campanha_export` e `detalhe_pedido`. O `_champions` e o `editar` já saem pelo §10.1. O `testes` procura essas chaves e os padrões de CPF, CNPJ, telefone e e-mail no JSON de cada farol."
  - contrato:1270, **depois:** "- **`CONTATO CLIENTE` nunca vai** (§10.10.3);".

### RD-0091 · O §10.10 repete regras do §10.7, que ele mesmo diz seguir
- **Onde:** o contrato:1226 diz que cada farol "segue o §10.1 e o §10.7, com as diferenças abaixo". Mesmo assim:
  1. contrato:1242: "O diretor vê só o Resumo […] Aba de tabela pedida por ele = 403". É o §10.7.5, e a coluna "Veem as abas de tabela" da tabela logo acima já tira o diretor;
  2. contrato:1309, "Antes de cada PR: […] Lista diferente do `montar` = a seção muda antes do código", repete o "Mudou no PC?" do §10.7.3 com outro texto.
- **Tipo:** doc. **Impacto:** leitura e manutenção (duas redações da mesma regra).
- **Severidade:** média.
- **Proposta:**
  - contrato:1242, **depois:** "- O diretor fica fora das abas de tabela nos 8 faróis (decisão de 26/11, RN-GER-014); a regra é a do §10.7.5."
  - contrato:1309 sai.

### RD-0092 · As decisões de 26/11 e a 6 A, contadas de novo em cada documento
- **Onde:**
  1. **Pergunta P1 dentro do contrato:** contrato:1157 traz o raciocínio da P1 (o `cartoes_de(...)[:1]`, por que o diretor não vê). Isso também está no `T-0025.md`:160-164 e no :31.
  2. **"Um autorizo por arquivo" (6 A):** contrato:1033 (Fontes) e contrato:1161; ADR:3 (Status) e ADR:50; `T-0025.md`:4 e :138.
  3. **Fontes com o conteúdo das decisões:** o contrato:1031-1032 resume as decisões de 26/11, e os §10.9.4, §10.9.5 e §10.10.1 dizem o mesmo de novo.
- **Tipo:** doc. **Impacto:** leitura e manutenção (se a P1 ou a 6 A mudarem, são 6 lugares).
- **Severidade:** média.
- **Proposta:**
  - contrato:1157, **depois:** "**O diretor:** depende da P1 (`docs/desenho/T-0025.md`, §7). Até a resposta, ele não vê o TOTAL A PAGAR."
  - contrato:1030-1034, **depois:** "Fontes: RN-GER-012; R-20261126-171559-alexandre e a decisão 6 A do R-20261126-180314-alexandre (o que dizem está no §10.9.4, no §10.9.5 e no §10.10.1); ADR 0005."
  - ADR:3, **depois:** "- **Status:** proposta (T-0025 v2)." A 6 A fica só no ADR:50.

### RD-0093 · A ordem de publicação está escrita 3 vezes, e cada texto traz uma regra que os outros não trazem
- **Onde:** contrato §10.9.6 (1215-1221, "vale para cada lote da T-0023 e da T-0025") × `T-0023.md` §4 (64-72) × `T-0025.md` §4 (70-87).
  - "Antes das 04h30" só está nos desenhos (T-0023:70 e T-0025:77).
  - "Nenhum dos dois entra no `main` sem a web nova no `/saude`" só está no contrato:1220.
  - A frase "Assim, o PC não fica só leitura sem a web gravar" aparece no contrato:1220 e no T-0023:70.
  - O T-0025:87 repete a ADR:52 (a rotina diária não leva a config).
- **Tipo:** doc. **Impacto:** decisão (quem lê só o contrato perde o limite das 04h30) e manutenção.
- **Severidade:** média.
- **Proposta:**
  - contrato:1220, item 4: acrescentar "antes das 04h30 (2 h no `main` antes da rotina das 06h30, regra 11)".
  - `T-0023.md`:64-72, **depois:** "## 4. Ordem de merge — Ordem: contrato §10.9.6. **Antes:** os PRs da T-0033 com a `GRADE` e a casca BC3 no `main` (sem eles, o PR da web conflita em `tabelas.py` e nos templates). O PR 2 do `testes` pode ir junto do passo 4 se o CI pedir."
  - `T-0025.md`:70-87, **depois:** "## 4. Ordem de merge — Ordem: contrato §10.9.6, uma vez por lote. **Antes:** a T-0023 v2 no `main` (mesmos arquivos, e o `novo` nasce nela). O lote B só começa com o lote A no `main`. Testes: critérios 1 a 7 no lote A, 8 e 9 no lote B. Fora a regra 11, nada pede o "instale" (a config fica fora da rotina diária: ADR 0005, §3.5)."

### RD-0094 · Os riscos dos desenhos repetem o que o contrato e a ADR já resolvem
- **Onde:**
  - `T-0025.md`:154, risco 5 (concorrência), é o ADR:59 e o contrato:1206;
  - `T-0025.md`:146-149, risco 2 (dado pessoal), é o contrato §10.10.3 e o ADR:58;
  - `T-0023.md`:126-130, risco 2, é o contrato §10.10.3 e o §10.9.1 (texto livre).
  Em nenhum dos três o risco fica em aberto: a mitigação já é regra.
- **Tipo:** doc. **Impacto:** leitura (a lista de riscos mistura o que está resolvido com o que não está).
- **Severidade:** média.
- **Proposta:**
  - `T-0025.md`:154 sai, e os riscos 6 e 7 são renumerados;
  - `T-0025.md`:146-149, **depois:** "2. **Dado pessoal:** regras no §10.10.3 e na ADR 0005, §4. Fixtures 100% fictícias.";
  - `T-0023.md`:126-130, **depois:** "2. **Dado pessoal:** regras no §10.10.3 e no §10.9.1, com o texto de 600 também passando pelo `RE_PESSOAL`. Fixtures 100% fictícias, sem print com nome de cliente."

### RD-0095 · As RNs a numerar: a RN-GER-014 com 2 textos e a RN-GER-016 repetindo a RN-GER-012
- **Onde:**
  - **RN-GER-014:** o `T-0023.md`:115 diz "o diretor vê só o Resumo (cartões e gráficos) nos faróis novos do site (26/11, R-20261126-171559-alexandre)", e o `T-0025.md`:136 diz "o diretor vê só o Resumo nos faróis novos (26/11)". São 2 textos para o gerente-projetos gravar no `docs/produto/03-regras.md`.
  - **RN-GER-016** (`T-0025.md`:138): "config editada pela web só pelo admin, gravada pelo robô com a função do PC". Isso já é a RN-GER-012 do `03-regras.md`. A parte nova é só a cópia antes e o "autorizo" por arquivo.
- **Tipo:** doc. **Impacto:** manutenção (duas RNs para a mesma regra na fonte da verdade, `docs/produto/03-regras.md`).
- **Severidade:** média.
- **Proposta:**
  - `T-0025.md`:136, **depois:** "- RN-GER-014: a da T-0023 (§5), com o mesmo texto;"
  - `T-0025.md`:138, **depois:** "- RN-GER-016: arquivo que o PC edita no lugar (config, DDR, Expositores) ganha a cópia antes do dia, feita pelo robô (§10.9.3). Config editada pela web só com um "autorizo" do Alexandre por arquivo (6 A); o primeiro é o `champions_config.json`. O resto é a RN-GER-012."

### RD-0096 · A frase do PC só leitura copiada por extenso, em vez da constante
- **Onde:** ADR:48 ("com "A edição agora é só pela BAP Central web."") e `T-0023.md`:105 (o mesmo texto). A frase já é a constante `bap_relatorios.MSG_EDICAO_SO_WEB` (no `main` e no contrato:1126), e o contrato:1213 e o `T-0025.md`:127 já citam a constante.
- **Tipo:** doc. **Impacto:** manutenção.
- **Severidade:** baixa.
- **Proposta:**
  - ADR:48, **depois:** "4. **No PC:** a tela da config fica só leitura (RN-GER-012), com `MSG_EDICAO_SO_WEB` (§10.9.3)."
  - `T-0023.md`:105, **depois:** "[…] no `DialogoGarantia` mostram `MSG_EDICAO_SO_WEB`, e nenhum arquivo […]".

### RD-0097 · A lista de colunas fora por tabela nasce em 2 cópias no código, sem fonte única
- **Onde:** contrato:1317 cria `bap_automation._COLUNAS_FORA_TABELA_WEB` e `web/app/tabelas.FORA_POR_TABELA`, com o `CONTATO CLIENTE` nas duas, e diz que a lista `colunas-fora` "não muda […] porque o teste dela compara as duas cópias". A lista nova não ganha bloco no contrato nem teste de cópia. É o caso que o RD-0021 fechou para a `colunas-fora`.
- **Tipo:** código. **Impacto:** manutenção. A próxima coluna por tabela pode entrar numa cópia só, e aí o robô manda o que a web recusa, ou ao contrário.
- **Severidade:** média.
- **Proposta:** contrato:1317, **depois:** "- o `CONTATO CLIENTE` das Garantias, uma coluna a mais só desta tabela. A lista fica no bloco abaixo (fonte única). O robô (`_COLUNAS_FORA_TABELA_WEB`) e a web (`tabelas.FORA_POR_TABELA`) têm uma cópia cada, e o teste da `colunas-fora` (§10.7.4) confere as duas contra o bloco:
  ```text colunas-fora-por-tabela
  pl_garantias|Garantias: CONTATO CLIENTE
  ```"

## Olhados e sem achado
- **A edição da T-0021 v4 (§10.9.1 a §10.9.3):** no `main`, ela só existia no código (`edicoes.py`, `bap_automation.py`), sem doc. Registrá-la no contrato não repete nada.
- **O §10.9 × o §10.8:** o §10.10 aponta para o formato 2 (contrato:1227) sem reescrevê-lo. O que repete está no RD-0089.
- **Código que o desenho manda escrever e que já existe:** nada é escrito do zero.
  - O `gravar_edicoes_pc` já tem `ncc`, `farol` e `expositores`, e o desenho pede só a garantia.
  - O `edicoes.MODULOS` já tem os 6 módulos.
  - O `edicoes.marca`, o `EDITA`, o `_CORTES_FAROL_WEB`, o `_AVISO_SO_PC_WEB`, o `opcoes_edicao_web`, o `EDICAO_SO_WEB` e o `FAROIS_LOTE2` (molde das travas) são estendidos, não refeitos.
- **§10.10.2 (colunas):** são `rid` novos, sem sobreposição com o §10.7.3.
- **`manter?` · `COLUNAS` × `COLUNAS_RID` na web:** são duas tabelas de colunas, uma por título e outra por `(rid, título)`, e o robô já usa só a segunda forma. A segunda se justifica porque títulos como "Por cliente" e "Hoje" se repetem (contrato:1255-1258). Migrar as antigas fica para quando uma delas mudar.
- **`manter?` · `RE_PESSOAL` na web e `_RE_PESSOAL_EDICAO_WEB` no robô:** a cópia já está no `main` (T-0021 v4). A web no Render não importa o código do PC, e a cópia segura a dupla conferência.

## Encaminhados (fora do escopo de redundância; não catalogados)
Ao `testes`, por serem texto ou regra que contradiz o valor:
1. Contrato:1091: a marca da linha nova é "N nova(s) aguardando o PC" e cita `edicoes.MSG_AGUARDA`. No `main`, `MSG_AGUARDA` = "Aguardando o PC".
2. `bap_automation.MOTIVO_TEXTO_WEB` diz "até 60 caracteres", e o `validar_edicao_web` corta em 60 fixo. Com o `max` até 600 (§10.9.1), a frase e o corte ficam errados.
3. A RN-GER-012 do `docs/produto/03-regras.md` diz "só acrescentando linha", mas o DDR, os Expositores e a config são editados no lugar (§10.9.3). A RN precisa da exceção, junto da RN-GER-016 (RD-0095).

## Liberação
**Não libera.** Os RD-0085 a RD-0097 estão em aberto. Nenhum é baixo só em comentário ou título de teste. O reteste é no novo head SHA, com o diff dos 4 arquivos.

[SUPOSIÇÃO] Por instrução de quem chamou, ficaram de fora o catálogo `docs/redundancias/catalogo.md`, o recado ao dono, o commit e qualquer alteração no clone de código. Quem chamou leva os achados ao engenheiro-software.
