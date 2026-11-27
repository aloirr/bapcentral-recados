# T-0037 — Releitura final do revisor-codigo (Farol de Fretes com edição)

- **Data:** 27/11/2026 (Manaus). **Base:** `origin/main` 30ae65d (#147, só o quadro).
- **Modo:** clone só leitura (`git fetch` e `git diff origin/main...<head>`), sem troca de branch. A suíte inteira não foi rodada. Rodei só testes escolhidos, numa cópia por `git archive` fora do repositório, para conferir o número e a ordem de merge.
- **Vale para estes heads.** Commit novo pede releitura.

| Branch | Head revisto | Parecer |
|---|---|---|
| `gerente-projetos/T-0037-regras` | 9611856 | 🟡 1 |
| `engenheiro-software/T-0037-desenho` | 0884880 | 🟡 2 |
| `modulo-farois/T-0037-fretes` | c53fc41 | aprovado |
| `modulo-robo/T-0037-fretes` | 9175831 | aprovado (🟢) |
| `testes/T-0037-fretes` | 43bb90a | 🔴 1 (ordem de merge com CI verde) |
| `modulo-web/T-0037-fretes` | **ee6b76b** | 🟡 1 |

Sobre a web: o c8a2e32 citado no pedido já foi trocado no remoto pelo ee6b76b ("PNGs fora do repositório; web 0.8.0", depois de um merge do main). Revisei o ee6b76b. Em relação ao c8a2e32, ele só muda três coisas: a `VERSAO`, o `test_T0035` (a versão escrita no teste) e os 10 PNGs, que saíram. A rodada combinada de 681 + 411 foi feita no c8a2e32. No ee6b76b, rodei o `web/tests/test_T0037_fretes.py`, o `test_T0021_edicao.py` e o `test_T0035_pacote_por_farol.py`: 58 passaram.

## 🔴 Bloqueia

**R1 — Não há ordem de merge em que cada PR tenha CI verde. Branch `testes/T-0037-fretes`.**
Três testes que já estão no `main` amarram o robô ao contrato, à web e à trava. Testei cada head sozinho sobre o `main` (`tests/test_T0024_trava_escopo_farois_web.py`, `tests/test_T0017_pacote_tres_farois.py`, `tests/test_T0017_tres_farois.py` e os `test_T0037_*`):

| Sobre o main | Resultado |
|---|---|
| só o `testes` | verde (72 passam, 2 pulados) |
| só o `modulo-farois` | verde |
| só o `engenheiro` (contrato) | ❌ `test_T0017_colunas_robo_igual_contrato_1073` (o contrato tem o `pl_fretes` e o robô não) |
| `engenheiro` + `web` (+ `testes`) | ❌ o 1073 e o `test_T0017_colunas_robo_igual_web` |
| `engenheiro` + `web` + `robo` + `farois`, sem `testes` | ❌ 4 testes: a trava (`pl_fretes: fora da lista PERMITIDA`), `trava_reprova_regra_de_uf_trocada`, `FAROIS_WEB_tem_os_quatro_farois...` e o robô × web |
| `robo` + `farois` + `testes`, sem `engenheiro` e sem `web` | ❌ o robô × web e o robô × contrato |
| os 5 juntos | ✅ 101 passam |

O contrato, a web e o robô só passam juntos. Como a regra é "um PR por dono" e "nunca merge com CI vermelho", a sequência não fecha.

**Correção (dono: testes):** deixar o `pl_fretes` "em transição", como já é feito na trava com o `FAROIS_T0037`:
- no `test_T0017_colunas_robo_igual_contrato_1073` e no `test_T0017_colunas_robo_igual_web`, as entradas do `pl_fretes` (`"Notas com frete"` e as `COLUNAS_RID` do `pl_fretes`) só entram na comparação quando o robô já tiver o `pl_fretes` em `ba.FAROIS_WEB`;
- com o robô no `main`, a comparação volta a ser estrita sozinha, porque o contrato e a web já terão entrado antes.
- Pronto quando: o novo head do `testes` passa sozinho sobre o `main`, e também sobre o `main` com o contrato, com o contrato e a web, e com todos.
- Depois, uma tarefa pequena do testes torna o `pl_fretes` obrigatório na trava.

## 🟡 Corrigir antes do merge

**Y1 — `gerente-projetos/T-0037-regras`: tirar o `docs/status/T-0037-sessao.md` do PR.**
O arquivo é o relato de uma sessão e vira ruído no `docs/status`:
- foge do padrão `docs/status/AAAA-MM-DD.md`;
- traz heads e "pontos para o PR" que ficam velhos no dia do merge;
- o que ele tem de útil já está no desenho §9 (P1 a P4), no `03-regras.md` e no `docs/testes/T-0037.md`.

Para onde levar:
- o relato inteiro vai para `recados/anexos/T-0037/` (a pasta já existe);
- no máximo, uma linha no `docs/status/2026-11-27.md`;
- o quadro do `main` (linha da T-0037: "status em docs/status/T-0037-sessao.md") passa a apontar para o anexo.

**Y2 — `engenheiro-software/T-0037-desenho`, contrato §10.11.3 ("Tela").** O contrato descreve outra grade, não a `web/app/tabelas.GRADE[("pl_fretes", "Notas com frete")]` do ee6b76b:

| | Contrato | Web |
|---|---|---|
| `grade` | 10 colunas, com o VLR NF | 9 colunas; o VLR NF vai ao popup ("9 + a coluna Editar") |
| `cel` | NF · CLIENTE · ETAPA · VLR FRETE | sem a ETAPA |
| `blocos` | Datas / Entrega / Outros | Nota / Entrega |

A mudança veio do revisor-ux (ffee80d). A correção é deixar o contrato só com a regra (até 10 colunas, chave NF, editáveis na grade e RESPONSÁVEL no popup) e apontar para a `tabelas.GRADE` como lista única. Assim a lista não fica escrita em dois lugares.

**Y3 — `docs/desenho/T-0037.md` §6, linha "`EDICOES_WEB` e `CAMPOS_EDICAO_WEB`".**
- A linha diz que o lugar do Fretes "não leva 'campos' (vale o padrão `pos_venda`)" e manda conferir "os 6 campos da ENTREGAS".
- Isso contradiz o §4.1, o §10, o contrato §10.11.4 e o código: `CAMPOS_LUGAR_WEB` com 5 campos, sem o `frete_real` (P2 A).
- É justamente a linha que quem fizer o merge da T-0023 vai ler.

**Y4 — `modulo-web/T-0037-fretes` (ee6b76b): o teste do diretor cita a RN errada.**
- `web/tests/test_T0037_fretes.py::test_RN_GER_012_diretor_so_o_resumo` testa a RN-GER-014.
- Renomear para `test_RN_GER_014_diretor_so_o_resumo` (regra 2: o teste cita a RN).

## Conferido

- **Regra 7 (dado digitado).**
  - Nenhum dos 6 diffs toca `RELATORIOS/`, `SISTEMA BAP/`, `BAP Ajuda 2.0/` ou um `.json` da raiz.
  - O `transportadoras_config.json` só é lido: `tr.carregar`, `tr.nomes` e `opcoes_para`, no núcleo e no `opcoes_edicao_web` do robô (RN-GER-016).
  - A ENTREGAS grava por `pos_venda.gravar_edicoes`: primeiro a linha no `_EDICOES_POS_VENDA` (só acrescenta), depois a célula "ass". O `APLICADAS_WEB` só acrescenta.
  - A troca no lugar, com o `antes` e a cópia `ANTES/` da RN-GER-012, não vale aqui: ela é do DDR, dos Expositores e da config. O Fretes grava igual ao `pl_entregas` e não muda o caminho da T-0021. Está coerente com o texto da RN-GER-012.
- **"% do faturado" líquido (RN-GER-002, P3 B): o número bate.**
  - Rodei o `montar("pl_fretes")` nas bases do repositório, com hoje = 27/11/2026, no `main` e na branch, com 2 casas decimais.
  - BAP inteira em NOV/26: **54,76% → 57,46%**. É 64.759,95 ÷ 112.701,43, igual ao `docs/testes/T-0037.md`.
  - MA: 45,57% → 90,52%. PA: 9,19% → 55,49%.
  - O denominador antigo do recorte era o da BAP inteira. O novo é o líquido dos clientes da UF, como diz o contrato §10.11.2.
  - O código reusa o `_liquido`, a mesma regra do `positivou` e do `_m3m_por`, e não a reescreve. O `_eventos_faturamento` não traz o cliente, por isso não serviria aqui.
  - O PC (Tkinter, pelo `chamar_kpis_de` com o filtro `{7: UF}`) e o recorte do robô chamam a mesma `kpis_fretes`. O teste `test_RN_POS_009_web_bate_com_o_pc_bap_e_uf` cobre esse ponto.
  - O Fretes não está no Painel do Diretor. O diretor vê o mesmo Resumo do PC.
- **§10.9 (edição pela web).** O lugar está em `EDICOES_WEB` e em `edicoes.LUGARES`. O `campos_do_lugar_web` é usado no `edicao_web` e no `validar_edicao_web`, e o `frete_real` é recusado com `MOTIVO_LUGAR_WEB`. A fila só acrescenta, os `IRMAOS` estão em lista explícita (a Devolução fica fora) e a linha sem chave mostra a mensagem do lugar.
- **Perfis.**
  - `FAROIS["pl_fretes"]` tem admin, diretor, gerente e pos_venda.
  - `VE_TABELAS` não tem o diretor: as abas dão 403 e ele vê só o Resumo (RN-GER-014).
  - O `pos_venda` vê as 4 abas (P4 A).
  - Só o admin edita: o botão some para os outros, e o GET e o POST do editar dão 403 (RN-GER-012).
- **Dado pessoal.**
  - As fixtures usam só "CLIENTE TESTE nn", "MOTORISTA FICTICIO n" e cidades e transportadoras inventadas.
  - O único texto em formato de CNPJ é o 12.345.678/0001-90, fictício, usado para provar a limpeza. O `main` já usa o mesmo em 4 arquivos.
  - No pacote, o CLIENTE sai com o `cliente_sem_documento` e a CHAVE é cortada da linha.
  - Nenhum segredo nos diffs, e nenhum arquivo proibido foi lido.
- **`VERSAO` e cache.** `bap_dados.VERSAO` = 27 nas 6 branches. Nenhuma regra de cache nova.
- **Donos.** `verificar --por-commit origin/main..<head>` está OK nas 6 branches, inclusive no ee6b76b. Na branch do engenheiro, os 2 commits do gerente (acrescentar e depois tirar o relato) se anulam no diff.
- **Numeração das RN.** As RN-POS-007 a 010 não colidem: o `main` vai até a RN-POS-006 e nenhuma outra branch remota usa da 007 à 010.

## 🟢 Sugestões

- **Regras.**
  - Reescrever a RN-POS-010: em vez de "só acrescentando no diário", dizer "primeiro a linha no `_EDICOES_POS_VENDA` (só acrescenta), depois a célula da assistente".
  - A linha solta "Frete: o mínimo vale quando o % da nota dá menos." repete a RN-POS-008.
  - A RN-POS-009 pode citar o R-20261127-013010-alexandre, como faz a RN-GER-015.
- **Desenho.**
  - O §2 cita o 04c13fd.
  - Os riscos 2 e 3 do §7 já estão resolvidos (P1 A e o par `(rid, título)`).
  - O §10 ("o que falta por dono") é um plano de trabalho e fica velho com o merge.
- **Testes.** O `docs/testes/T-0037.md` tem três pontos velhos:
  - a observação sobre o `MOTIVO_CAMPO_WEB`, que o contrato já corrigiu no 5d112f1;
  - a "rodada final" cita as regras no e1e1bdc (o head é o 9611856);
  - a mesma rodada cita a web no c8a2e32 (o head é o ee6b76b).
- **Web.**
  - A `0.8.0` pula a 0.6.0 da T-0036 e da T-0045 e a 0.7.0 da T-0023. Quem entrar depois precisa subir acima de 0.8.0.
  - O `test_T0035` escreve a versão à mão; comparar com `app.VERSAO` evita o conflito em todo PR.
  - Faltam 2 linhas em branco depois do `msg_sem_chave` (E305).
- **Robô.**
  - Falta a linha no diário do modulo-robo.
  - O RESPONSÁVEL, texto digitado no PC, vai ao site sem o `texto_sem_contato`. Isso já acontece no Entregas, e a base de hoje tem 0 de 134 valores com cara de contato. Proposta: incluir "RESPONSÁVEL" no `_COLUNAS_TEXTO_LIVRE_WEB` numa tarefa à parte, para os dois faróis.

## Ordem de merge

1. **`gerente-projetos/T-0037-regras`**, só com o `03-regras.md` (Y1). Os testes citam as RN-POS-007 a 010.
2. **`testes/T-0037-fretes`**, com o novo head da transição (R1). Ele passa sozinho, e os `test_T0037_*` ficam pulados até o código chegar.
3. **`engenheiro-software/T-0037-desenho`** (contrato), com o Y2 e o Y3.
4. **`modulo-web/T-0037-fretes`**, com o Y4. Publicar no Render e conferir `/saude` = 0.8.0 **antes** de o robô chegar à produção: sem a web nova, o pacote com o `pl_fretes` é recusado.
5. e 6. **`modulo-farois/T-0037-fretes`** e **`modulo-robo/T-0037-fretes`**, um logo depois do outro e na mesma janela da rotina diária. O `EDICAO_SO_WEB` do PC não pode chegar antes do robô que manda a edição ao site (contrato §10.11.4). Senão, por um dia, o Fretes não se edita em lugar nenhum.
7. Depois, uma tarefa pequena do testes torna o `pl_fretes` obrigatório na trava.

Cada head novo (testes, engenheiro, web e regras) precisa de releitura no SHA novo.

---

# Releitura 2 — heads novos (27/11/2026, Manaus)

- **Base:** `origin/main` 4728880 (#151). Os 5 heads fazem merge limpo com ele.
- **Modo:** clone de rascunho fora do repositório (`git clone --shared` e merges locais), sem troca de branch no repositório.
- **Ambiente:** Python 3.13 sem tkinter. Por isso o `tests/test_T0021_edicao_web_robo.py` não é coletado (importa o `bap_relatorios`). A falha é do ambiente: o CI tem tkinter.
- **Web fora desta rodada.** O c52d353 dá conflito com o `main` 4728880, como já era esperado.
- **Vale para estes heads.** Commit novo pede releitura.

| Branch | Head | Parecer |
|---|---|---|
| `gerente-projetos/T-0037-regras` | b28f09d | **aprovado** (Y1 fechado) |
| `testes/T-0037-fretes` | 2b822d2 | R1 fechado · **🟡 1** (T1) |
| `engenheiro-software/T-0037-desenho` | 27306a0 | Y2 e Y3 fechados · **🟡 1** (C1) |
| `modulo-farois/T-0037-fretes` | c53fc41 | **aprovado** (sem mudança) |
| `modulo-robo/T-0037-fretes` | f361173 | **aprovado** (🟢) |

## Os achados da releitura anterior

- **R1 fechado (testes).**
  - Os 2 testes de colunas ignoram o `pl_fretes` nos dois lados enquanto ele não estiver em `ba.FAROIS_WEB`. Isso está em `_RIDS_POR_PARTES_WEB` e `_rids_ignorados_web` (`tests/test_T0017_pacote_tres_farois.py`).
  - A trava aceita o `pl_fretes` como permitido, mas não como obrigatório (`FAROIS_T0037`).
  - Medido por mim:

| Combinação sobre o main 4728880 | Resultado |
|---|---|
| regras + testes, `pytest tests` inteiro | ✅ 628 passam, 3 pulados, 2 xpassed |
| regras + testes + contrato, inteiro | ✅ 628, 3 pulados |
| regras + testes + contrato + faróis, testes acoplados¹ | ✅ 131, 3 pulados |
| regras + testes + contrato + faróis + robô, **sem a web**, acoplados | ❌ só o `test_T0017_colunas_robo_igual_web` (o robô não pode vir antes da web) |
| só o robô, acoplados | ❌ 5 (a trava e as colunas; o robô não pode vir antes dos testes) |

¹ Os testes acoplados são `test_T0024_trava_escopo_farois_web`, `test_T0017_pacote_tres_farois`, `test_T0017_tres_farois`, `test_T0024_lote2_robo_web`, `test_T0024_robo_lote2`, `test_T0035_robo_web`, `test_T0017_farol_web_robo` e os `test_T0037_*`.

  - [SUPOSIÇÃO] As combinações com a web vêm do `docs/testes/T-0037.md`, que usou a web a350b75. Elas precisam ser refeitas com o head novo da web.

- **Y1 fechado (regras).** O PR só traz o `docs/produto/03-regras.md` (+4 linhas, RN-POS-007 a 010). O relato da sessão está em `recados/anexos/T-0037/relato-sessao-tarefa.md`.

- **Y2 fechado (contrato §10.12.3), por outro caminho.**
  - A lista da grade continua escrita no contrato, mas agora é igual à `tabelas.GRADE[("pl_fretes", "Notas com frete")]` da web c52d353: 9 colunas, `cel` sem a ETAPA, `blocos` Nota/Entrega e a justificativa do 1366.
  - O risco de duplicação ficou como 🟢 (abaixo).

- **Y3 fechado.** O desenho cita os 5 campos do `CAMPOS_LUGAR_WEB`, sem o `frete_real`:
  - §6, linha "`EDICOES_WEB`, `CAMPOS_EDICAO_WEB` e `CAMPOS_LUGAR_WEB`";
  - §4.1, item 3;
  - §7.1.

- **Renumeração §10.11 → §10.12: certa.**
  - A §10.11 é dos faróis do Analista (`engenheiro-software/T-0036-desenho` 533707a).
  - Nenhuma citação "§10.11" sobrou nos diffs da T-0037.
  - Os dois desenhos dão conflito entre si no `relatorio.md` e no diário do engenheiro, porque os dois acrescentam depois da §10.10. Quem entrar depois precisa de um merge do main, e isso gera um **head novo, que pede releitura**.

- **Y4 (web):** fora desta rodada. Releio no head novo da web.

## 🟡 Corrigir antes do merge

**C1 — `engenheiro-software/T-0037-desenho` 27306a0: o contrato não descreve o Resumo que o robô manda.**

O que o contrato e o desenho dizem hoje:
- `.coord/contratos/relatorio.md:1467-1468` (§10.12.2): o gráfico vai "pela lista `_GRAFICOS_NO_PAINEL_WEB` da T-0023" e, "enquanto o robô da T-0023 não estiver no `main`, o farol vai só com os cartões";
- `docs/desenho/T-0037.md:108`, `:149` e `:212` repetem: o gráfico só depois da T-0023.

O que o robô f361173 faz:
- monta o Resumo em `bap_automation.blocos_resumo_fretes_web` (`bap_automation.py:6951`), com `_TIPOS_BLOCO_EXTRA_WEB["pl_fretes"] = ("tabela",)`;
- 1 bloco `barras` (12 meses);
- 3 blocos `tabela` com o título e o mês ("Por UF (NOV/26)" e as outras duas). Cada um tem as colunas `<rótulo>`, NOTAS, VLR NF e VLR FRETE, a linha `total` ("TOTAL", soma sem arredondar) e os rótulos "Sem UF", "Sem cidade / UF" e "Sem transportadora";
- 1 bloco `insights` "Resumo gerencial" com as 2 frases, que vão também em `insights_painel`.

A web vai ser refeita em cima desse pacote, e o contrato é a ponte.

Correção (dono: engenheiro-software): descrever esse Resumo no §10.12.2 e tirar o "só com os cartões" (contrato e desenho). Pode citar a função como fonte, sem copiar as frases.

**T1 — `testes/T-0037-fretes` 2b822d2: o teste da frase da UF confere outro critério.**
- O `tests/test_T0037_fretes_resumo.py:109-125` (`test_T0037_resumo_frase_de_uf_bate_com_a_tabela`) diz e confere "a UF com **mais notas**": `lin[uf][1] == max(x[1] ...)`, na linha 124.
- O robô escolhe a UF de **maior VLR NF**: `topo = max(ufs_ok, key=lambda x: x[2])`, em `bap_automation.py:7011`. A transportadora segue o mesmo critério, na linha 7020.
- Nas bases congeladas, a UF com mais notas e a de maior valor são a mesma, por isso o teste passa. Mas ele não prova a regra.

Correção:
- conferir pelo VLR NF (`x[2]`);
- acrescentar um caso sintético em que a UF com mais notas não é a de maior valor;
- se o critério combinado com o designer-ux for "mais notas", o pedido vai ao modulo-robo, e não se muda o teste.

## 🟢 Sugestões

**Robô (f361173)**
- A docstring do `blocos_resumo_fretes_web` cita "contrato 10.8". O certo é a §10.12.2, depois do C1.
- As 2 frases vão duas vezes no pacote: no bloco `insights` e em `insights_painel`. A web usa o `insights_painel` primeiro (`web/app/render.py:671` do main, `_insights(insights_painel) or ins_blocos`), então o bloco nunca aparece. Basta mandar um dos dois.
- `nomes.index("NOTAS")`, `"VLR NF"` e `"VLR FRETE"` (linha 6983) não estão na guarda, que só confere o `MÊS` e o rótulo. Se o PC renomear uma coluna, sai `ValueError`, em vez de a tabela ficar de fora.
- A frase da UF exige mais de uma linha. A da transportadora sai mesmo com uma só ("leva 100% do valor").
- Depois da T-0023, o gráfico em `barras` pode reusar o `_GRAFICOS_NO_PAINEL_WEB` (contrato `:1325`) em vez de um 3º caminho (os outros dois são o Fretes e os `RIDS_LIVRES_WEB`). Fica para o corretor-redundancias.

**Contrato**
- A grade do Fretes está escrita no §10.12.3 e na `tabelas.GRADE`. Um teste que compare as duas, ou uma remissão à `GRADE` como fonte, evita que elas se separem.

**Testes**
- No `docs/testes/T-0037.md:85`, a observação sobre o `MOTIVO_CAMPO_WEB` está velha: o §10.12.4 já cita o `MOTIVO_LUGAR_WEB`.
- A tabela de combinações cita o contrato 0884880 e a web a350b75.

**Quadro (main, gerente)**
- A linha da T-0037 em `.coord/quadro.md:61` ainda aponta para `docs/status/T-0037-sessao.md`. O certo é `recados/anexos/T-0037/relato-sessao-tarefa.md`.

## Conferido no código novo do robô

- **Função pura.** O `blocos_resumo_fretes_web(r)` só lê o dicionário do `montar` (`graficos`, `tabelas`, `filtros`) e devolve `(blocos, frases)`. Ele não faz leitura nem escrita e não abre arquivo. Os números saem das tabelas do PC, sem refazer a regra. O formato do texto usa `relatorios_nucleo.br`, `p`, `pct_de` e `moeda`, que já existem.
- **Número × cartão (RN-POS-009).**
  - O TOTAL de cada uma das 3 tabelas é igual ao cartão "Notas com frete" (nº e VLR NF do detalhe) e ao "Frete estimado". Os 3 TOTAIS são iguais.
  - A soma das linhas, já arredondadas, difere do TOTAL em no máximo meio centavo por linha, como está documentado.
  - O Fretes não vai ao Diretor (RN-GER-014: ele vê só o Resumo, que é este mesmo).
- **Regra 6.** Os blocos só têm UF, cidade e transportadora. O CLIENTE e o RESPONSÁVEL não entram. O `test_RN_GER_011_resumo_sem_dado_pessoal` procura CNPJ, e-mail, telefone e os nomes de cliente da base no painel e nas frases. Os blocos `tabela` ainda passam pelo filtro `_COLUNAS_PESSOA_TABELA_WEB` do `selecionar_farol_web`.
- **Configs.** O diff do robô não lê nenhum `.json`. O `transportadoras_config.json` continua só lido pelo núcleo. Nenhum arquivo proibido (`tomtom_config*`, `google_maps_config*`, `visitas_config.json`, `auth/`, `.env`) foi lido, nem por mim. Não há segredo nos diffs.
- **`bap_dados.VERSAO` = 27** no main e nas 5 branches. Não há regra de cache nova.
- **Donos.** `verificar --por-commit origin/main..<head>` está OK nas 5 branches (4, 7, 5, 7 e 8 commits). `compileall` está OK na árvore combinada.
- **Tela.** O Resumo muda o que aparece no site, e a simulação (regra 10) depende da web nova. Antes do merge da web e do robô, falta a simulação do Resumo aprovada pelo po, por delegação.

## Ordem de merge (confirmada, com condições)

1. **`gerente-projetos/T-0037-regras`** b28f09d.
2. **`testes/T-0037-fretes`**, depois do T1. Passa sozinho no `main`, e os `test_T0037_*` ficam pulados.
3. **`engenheiro-software/T-0037-desenho`**, depois do C1 e do merge do main com o #160 (T-0036), se ele entrar antes. Pede releitura no head novo.
4. **`modulo-web/T-0037-fretes`**, com o merge do main, o Y4 e a fixture do Resumo f361173. Pede releitura e as combinações refeitas (contrato + web + testes; todos). Publicar e conferir o `/saude` antes de o robô chegar à produção.
5. e 6. **`modulo-farois/T-0037-fretes`** c53fc41 e **`modulo-robo/T-0037-fretes`** f361173, um logo depois do outro e na mesma janela da rotina diária (o `EDICAO_SO_WEB` do PC não chega antes do robô).
   - Os faróis podem entrar antes da web sem quebrar o CI (medido).
   - O robô **não**: sem a web, o `test_T0017_colunas_robo_igual_web` cai.
7. Depois, uma tarefa do testes torna o `pl_fretes` obrigatório na trava e tira o `_RIDS_POR_PARTES_WEB`.

Cada PR precisa de CI verde no próprio head.
