---
id: R-20261124-183310-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:33:10-04:00
---
# Parecer do corretor-redundancias: #47 e #48 sem achado; #49 RD-0015; #50/#51 RD-0016

> Parecer do corretor-redundancias (subagente do gerente-projetos; gravado pelo gerente sem alteração, pela limitação do --de no coord.mjs).

# Re-auditoria do corretor-redundancias: T-0017, PRs #47 a #51

Data: 24/11/2026. Fiz só leitura: `git diff <head antigo> <head novo>` e, para o #51, `git diff origin/main...<head>`. Não vi o print real das telas: o parecer de tela se apoia no template e no teste.
Base: o parecer anterior (`rd-47-50.md`, RD-0001 a RD-0014). Os achados novos continuam a numeração (RD-0015 e RD-0016).
O RD-0014 (a constante "000040" espalhada) é anterior à T-0017. Vira tarefa própria e não bloqueia este lote. Com a saída do `CONTA_TESTE` no #50, as constantes voltam a ser 3.

---

## PR #47 · engenheiro-software/T-0017-contrato-farol · head 1cde84dfb4a2febae533e708d01260a9975eb5d1

**Veredito: sem achado em aberto.**

| ID | Situação | Evidência |
|---|---|---|
| RD-0001 | fechado | No ADR 0001, Adendo 2, o item dos mini-gráficos agora diz "em `kpis[i]["estados"]`, só nos cartões que o PC desenha assim (formato no contrato, §10.1)". O formato fica só no contrato. |
| RD-0002 | fechado | No contrato §10.1, o "Filtro por estado" agora diz "o texto é da web: `web/app/render.py`, `AVISO_UF`". Saiu o texto de tela fixado no contrato. |

Observação, sem bloqueio e fora do catálogo: a linha `avisos` do contrato ainda diz "o robô pode acrescentar (ex.: bloco tirado)". O #49 deixou de acrescentar aviso (RD-0010). O texto é permissivo e não está errado. Se o dono quiser, troca por "os do PC" no próximo lote.

---

## PR #48 · modulo-web/T-0017-farois-web · head 18d65d977ae1e1b642ed2209220775a5510f5247

**Veredito: sem achado em aberto.**

| ID | Situação | Evidência |
|---|---|---|
| RD-0003 | fechado | Agora `AVISO_UF = "Resumo e gráficos: BAP inteira."`, sem o "Cartões: {uf}". O `<h2>Resumo gerencial</h2>` ficou sem o "· BAP inteira". O teste `test_farol_filtro_por_estado_troca_so_os_cartoes` confere `"· BAP inteira" not in h`. |
| RD-0004 | fechado | No ramo do estado sem recorte, os cartões saem sem `detalhe`, e há um aviso só: `SEM_DADO_UF = "Sem números de {uf} neste pacote."` somado ao `AVISO_UF`. A dica `SEM_RECORTE` ficou só no ramo parcial (render.py:318). |
| RD-0005 | fechado | O `INDISPONIVEL` vai ao contexto (`main.py:124`, `indisponivel=render.INDISPONIVEL`) e é usado em `farol.html:7` e `:59` e em `home.html:5`. Não sobrou literal no template, e a frase que explicava o funcionamento saiu. |
| RD-0006 | fechado | A macro única `templates/_estados.html` (`barras_estados`) é usada em `painel.html` e `farol.html`. As 6 regras `.mini*` saíram e ficou uma modificadora `.kpi-est .rc-barras`. O farol voltou a ter `rot` e `legenda`. |
| RD-0007 | fechado | O cabeçalho agora diz "Baixado do ERP em …", sem o "(Manaus)". Coberto por teste. |
| RD-0008 | fechado | Ficou uma regra `.gb-txt` só (estilo.css:88). A segunda declaração saiu. |

---

## PR #49 · modulo-robo/T-0017-farol-inadimplencia · head e8bd178c6687ca51aba4a3bce9aab035883f0fae

**Veredito: BLOQUEIA por 1 achado novo (RD-0015, código). RD-0009 a RD-0011 estão fechados. O RD-0012 continua aberto, mas não bloqueia porque é só comentário.**

| ID | Situação | Evidência |
|---|---|---|
| RD-0009 | fechado | Agora `_CHAVES_FORA_FAROL_WEB = _PACOTE_WEB_CHAVES_ACAO \| {"tabelas", "juntas", "editar", "abrir"}`. `_para_json(..., fora=...)` repassa o parâmetro na recursão. `_sem_chaves_de_acao` foi apagada. Resta uma lista e uma varredura. |
| RD-0010 | fechado | `"avisos"` leva só os do PC. O aviso "gráfico(s) com nome de pessoa…" saiu. |
| RD-0011 | fechado | A função `_com_fuso_manaus(quando=None)` é usada em `montar_pacote_web` e em `selecionar_farol_web`. As 4 linhas copiadas saíram. |
| RD-0012 | aberto, não bloqueia | O comentário "D1 do Alexandre pendente … fica FORA do pacote enquanto for False" continua igual, com a constante em `True`. A docstring de `selecionar_farol_web` ainda cita `tests/test_T0017_farol_web_robo.py`, que não existe no branch. Entra no lote seguinte. |

**Achado novo**

| ID | Onde | Tipo | O que se repete | Impacto | Sev. | Proposta (antes → depois) | Dono | Bloqueia |
|---|---|---|---|---|---|---|---|---|
| RD-0015 | `bap_automation.py`, `_FONTE_BAIXADO_WEB` (≈ linha 6693) | código | O caminho `Path("SISTEMA BAP") / "BACKUP_RELATORIOS" / "BKP_RELATORIOS_BAPTOOLS"` foi escrito à mão. O mesmo módulo já tem a constante `BKP_BAPTOOLS = f"{SUBPASTA_BACKUP}/BKP_RELATORIOS_BAPTOOLS"` (linha 269), que existe para isso. São 2 definições do mesmo caminho no mesmo arquivo. | manutenção: se a pasta mudar, alguém corrige a constante e o "baixado em" da web passa a dar `None` sem aviso (o `except` engole o erro) | média | antes: `"pl_inadimplencia": (Path("SISTEMA BAP") / "BACKUP_RELATORIOS"`<br>`/ "BKP_RELATORIOS_BAPTOOLS",`<br>`"Relatorio_Titulos_em_Abertos_*.xlsx")}` → depois: `"pl_inadimplencia": (Path(BKP_BAPTOOLS), "Relatorio_Titulos_em_Abertos_*.xlsx")}` | modulo-robo | sim (código) |

Encaminhamento ao `testes` (é valor, não entra no catálogo): o `baixado_em` agora usa o `st_mtime` do arquivo de nome mais novo. Conferir se a data de gravação do arquivo é mesmo a hora do download, e não a de uma cópia ou do backup. O branch continua sem teste T-0017 do robô.

---

## PR #50 · modulo-farois/T-0017-inadimplencia-internos · head 5ef155b78db85bdaa0b34eef7409517eb1ab3878

**Veredito: BLOQUEIA por 1 achado novo (RD-0016, regra de negócio repetida com o #51). O RD-0013 caiu.**

| ID | Situação | Evidência |
|---|---|---|
| RD-0013 | fechado (caiu) | Saiu `CONTA_TESTE = "000040"` e, com ele, o comentário. A docstring de `titulos_sem_internos` agora cita só a RN-GER-004. |

**Achado novo (compartilhado com o #51)**

| ID | Onde | Tipo | O que se repete | Impacto | Sev. | Proposta (antes → depois) | Dono | Bloqueia |
|---|---|---|---|---|---|---|---|---|
| RD-0016 | `relatorios_nucleo.titulos_sem_internos` (#50, linha 727) × `bap_dados.fotos_sem_internos` (#51, linha 1427) | código (regra de negócio repetida) | As 2 funções puras têm o mesmo corpo: `return [t for t in titulos or [] if not _interno(t.get("nome"), t.get("fantasia"))]`. A mesma regra (RN-GER-004 sobre títulos em aberto) fica em 2 módulos. A docstring do #51 diz que é "a mesma regra … do filtro dos titulos no farol". | manutenção: se a regra dos internos sobre títulos mudar (ex.: filtrar pelo `A1_CGC`), um lado fica para trás, e o cartão do farol deixa de bater com o atraso, o recebido e o recuperado das fotos | média | **Fonte única em `bap_dados`**, a camada de baixo (o `relatorios_nucleo` já importa `bap_dados as bd`, e o `bap_dados` não importa o núcleo).<br>1) #51 (engenheiro-dados): `def fotos_sem_internos(titulos) -> list:` → `def titulos_sem_internos(titulos) -> list:`, com docstring `"""RN-GER-004 (funcao pura): tira dos titulos em aberto (fotos e ftTitulos) os de CNPJ interno (BAP AUTOPARTS / FRW / PMZ DISTRIBUIDORA)."""`. A chamada fica `lidos = titulos_sem_internos(_ler_titulos(wb.worksheets[0]))`.<br>2) #50 (modulo-farois): apagar a `def titulos_sem_internos` do `relatorios_nucleo.py`. No `_sem_internos`, `bloco = dict(bloco, titulos=titulos_sem_internos(bloco.get("titulos")))` → `bloco = dict(bloco, titulos=bd.titulos_sem_internos(bloco.get("titulos")))`.<br>3) Ordem: o merge do #51 vem antes. Depois o #50 se atualiza com o `main`. | modulo-farois (#50, tirar a cópia) · engenheiro-dados (#51, nome público) | sim, nos dois PRs |

Opcional, sem bloqueio: o `_bloco_inadimplencia` poderia filtrar também os `titulos` do `ftTitulos` na montagem (a marca "fi1" já refaz o bloco). Aí o ramo `elif nome == "inadimplencia"` do `_sem_internos` só se justificaria para cache antigo. Fica a critério dos donos.

Encaminhamento ao `testes` (repete o item 3 do parecer anterior): nem o #50 nem o #51 têm `test_RN_GER_004_...` para o filtro (regra 2 do CLAUDE.md).

---

## PR #51 · engenheiro-dados/T-0017-fotos-sem-internos · head 464711ae378c4abf13e2d2bbb8b79e1e925825f4

**Veredito: BLOQUEIA pelo RD-0016 (ver o bloco do #50). Do lado do #51, a parte é renomear `fotos_sem_internos` para `titulos_sem_internos` e publicar como a fonte única. Fora isso, sem achado.**

- O cache usa a marca nova "fi1" na assinatura do bloco `inadimplencia`, sem mexer no `VERSAO`. Isso segue a regra 3 e não repete nada.
- A função reaproveita o `_interno` e não recopia a lista de CNPJs internos. O problema é só a função existir 2 vezes (RD-0016).

---

## Resumo do lote

| PR | Head | Veredito | Em aberto que bloqueia |
|---|---|---|---|
| #47 | 1cde84d | sem achado em aberto | — |
| #48 | 18d65d9 | sem achado em aberto | — |
| #49 | e8bd178 | bloqueia | RD-0015 (modulo-robo); RD-0012 segue aberto sem bloquear |
| #50 | 5ef155b | bloqueia | RD-0016 (modulo-farois) |
| #51 | 464711a | bloqueia | RD-0016 (engenheiro-dados: renomear para a fonte única) |
| — | — | fora do lote | RD-0014 (tarefa própria) |

Não gravei recado: o coord desta sessão só aceita `--de gerente-projetos`. Cabe ao gerente-projetos mandar um recado por dono: modulo-robo (RD-0015 e RD-0012), modulo-farois e engenheiro-dados (RD-0016).
