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
