---
id: R-20261124-182529-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:25:29-04:00
---
# Parecer do corretor-redundancias: PRs #47, #48, #49 bloqueados (RD-0001..0011); #50 sem achado

> Parecer do corretor-redundancias (subagente do gerente-projetos; gravado pelo gerente sem alteração, pela limitação do --de no coord.mjs).

# Pareceres do corretor-redundancias: T-0017, PRs #47 a #50

Data: 24/11/2026. Leitura do `git diff origin/main...origin/<branch>`, só leitura, sem print real das telas (o parecer de tela está baseado no template, na fixture e no código).
[SUPOSIÇÃO] Numeração começando em RD-0001: `docs/redundancias/catalogo.md` ainda não existe no `origin/main`.
Regra de liberação: o lote só sai sem achado em aberto. A exceção é achado baixo só em comentário ou título de teste: esse não bloqueia.

---

## PR #47 · engenheiro-software/T-0017-contrato-farol · head 45019f236cf319bfdcf7df0ada01661801fe2cb6

**Veredito: BLOQUEIA (2 achados de doc em aberto).**

| ID | Onde | Tipo | O que se repete | Impacto | Sev. | Proposta (antes → depois) | Dono | Bloqueia |
|---|---|---|---|---|---|---|---|---|
| RD-0001 | `docs/decisoes/0001-bap-central-web-render.md`, Adendo 2, "A mudança", 4º item (mini-gráficos) | doc | O formato `kpis[i]["estados"] = {"barras": [[UF, número, "texto", "% na barra", "tom"], ...], "legenda": ""}` aparece 2 vezes, no ADR e no contrato §10.1, com grafias diferentes ("número" × `numero`) | manutenção: na v2 alguém atualiza um documento e esquece o outro | média | antes: o item inteiro com o formato → depois: "**Mini-gráficos por estado dos cartões** vão no pacote, só nos cartões que o PC desenha assim (formato no contrato, §10.1)." A fonte da verdade do formato é o contrato. | engenheiro-software | sim |
| RD-0002 | `.coord/contratos/relatorio.md` §10.1, "Filtro por estado" | doc | Texto de tela fixado no contrato ("Cartões por estado; gráficos da BAP inteira.") diferente do que a web mostra (`web/app/render.py` `AVISO_UF` = "Cartões: {uf}. Resumo e gráficos: BAP inteira."). O mesmo aviso tem 2 textos. | manutenção: o contrato fica desatualizado a cada ajuste de texto | baixa | antes: `e a tela avisa: "Cartões por estado; gráficos da BAP inteira."` → depois: `e a tela avisa que os gráficos são da BAP inteira (texto em web/app/render.py, AVISO_UF).` | engenheiro-software | sim (é doc, não comentário) |

Sem achado no resto: a tabela de chaves, o filtro e a ordem de publicação estão num lugar só (contrato), e o ADR registra a decisão.

---

## PR #48 · modulo-web/T-0017-farois-web · head 9211d8b29a1f6465ba005349652daccac7c5762c

**Veredito: BLOQUEIA (5 achados em aberto, 4 médios e 1 baixo).**

| ID | Onde | Tipo | O que se repete | Impacto | Sev. | Proposta (antes → depois) | Dono | Bloqueia |
|---|---|---|---|---|---|---|---|---|
| RD-0003 | tela do farol com estado escolhido: `farol.html` (aviso `aviso_uf` + `<h2>Resumo gerencial <small>· BAP inteira</small>`) e `render.AVISO_UF` | texto | "BAP inteira" aparece 2 vezes para o mesmo fato (aviso "Resumo e gráficos: BAP inteira." e o título do resumo), e "Cartões: AM" repete o filtro já marcado como ativo na barra de estados. Com o chip "BAP inteira", são 3 ocorrências. | leitura (regra 1: uma informação, um lugar) | média | `AVISO_UF = "Cartões: {uf}. Resumo e gráficos: BAP inteira."` → `AVISO_UF = "Resumo e gráficos: BAP inteira."` (o `.format(uf=uf)` sai); no `farol.html`, `<h2>Resumo gerencial{% if tela.uf %} <small>· BAP inteira</small>{% endif %}</h2>` → `<h2>Resumo gerencial</h2>` | modulo-web | sim |
| RD-0004 | `render.farol_para_tela`, ramo "estado sem recorte" (`SEM_RECORTE`) | texto | Quando o estado não tem recorte, **todos** os cartões mostram "—" e a mesma dica "só na BAP inteira" (6 vezes na fixture), além do aviso do estado | leitura (aviso repetido em vários cartões → um aviso só) | média | ramo `elif re.match(...)`: cartões com `"detalhe": ""` e um aviso só: `aviso_uf = SEM_DADO_UF.format(uf=uf)`, com `SEM_DADO_UF = "Sem números de {uf} neste pacote."`. A dica por cartão (`SEM_RECORTE`) fica só no ramo em que **alguns** cartões faltam. Ajustar `test_estado_sem_recorte_de_um_cartao_mostra_traco_e_dica` se ele cobrir o ramo total. | modulo-web | sim |
| RD-0005 | `render.py:141` `INDISPONIVEL`, `farol.html:6` e `:58`, `home.html:5` | código · texto | A constante `INDISPONIVEL` é definida e não usada (código morto). O literal "ainda não disponível na web" está escrito à mão no template. O mesmo estado tem 3 textos: "ainda não disponível" (menu), "ainda não disponível na web" (bloco) e "Ainda não disponível: este farol não veio no último pacote do PC." (página). A última frase explica o funcionamento do sistema, o que a regra 3 retira. | manutenção, leitura | média | `farol.html:58`: `<p class="indisp-bloco">ainda não disponível na web</p>` → `<p class="indisp-bloco">{{ indisponivel }}</p>` (passar `render.INDISPONIVEL` no contexto); `farol.html:6`: "Ainda não disponível: este farol não veio no último pacote do PC." → `{{ indisponivel|capitalize }}.` ("Ainda não disponível na web."); `home.html`: `<small>ainda não disponível</small>` → `<small>{{ indisponivel }}</small>` | modulo-web | sim |
| RD-0006 | `farol.html:24` (`.mini`, `.mini-c`, `.mini-a`, `.mini-t`, `.mini-uf`) × `painel.html:53-71` (`.rc-barras`, `.col`, `.area`, `.txt-b`, `.uf`); `estilo.css` | layout · código | Mesmo componente (as barrinhas por estado do cartão, que já saem do mesmo `render._barras`) reimplementado com HTML e CSS próprios: 6 regras CSS novas para uma coisa que já existe. A versão do farol também perde o `rot` ("% na barra") e a `legenda`, que o pacote leva. | manutenção, consistência visual entre painel e farol | média | criar `templates/_estados.html` com `{% macro barras_estados(est) %}` (o trecho atual do `painel.html:53-71`). `painel.html` e `farol.html` passam a usar `{{ barras_estados(c.estados) }}` / `{{ barras_estados(k.estados) }}`. Saem as regras `.mini*`; o tamanho do cartão do farol se ajusta com uma classe modificadora (`.kpi-est .rc-barras{height:110px}`). | modulo-web | sim |
| RD-0007 | `farol.html:8` × `base.html:21` | texto | O contexto "Manaus" aparece 2 vezes na mesma tela: "Dados de … (horário de Manaus)" (global) e "Baixado em … (Manaus)" (cabeçalho do farol) | leitura | baixa | `<span>Baixado em {{ tela.baixado_em\|manaus }} (Manaus)</span>` → `<span>Baixado do ERP em {{ tela.baixado_em\|manaus }}</span>` | modulo-web | sim (texto de tela) |
| RD-0008 | `estilo.css` (diff, linhas 33 e 48) | código | Regra `.gb-txt{...}` declarada 2 vezes; a segunda sobrescreve `overflow-wrap` da primeira | manutenção | baixa | juntar numa regra só: `.gb-txt{font-size:.62rem;font-weight:700;text-align:center;line-height:1.1;white-space:normal;overflow-wrap:normal}` e apagar a segunda | modulo-web | sim |

**Ponto de atenção: filtro de chaves proibidas no robô (#49) e na web (#48). Decisão: `manter`, é defesa em profundidade.**
- O robô **tira** as chaves antes do envio e a web **recusa** o pacote que as trouxer (`pacotes._chave_proibida` + `PROIBIDAS`).
- São lados diferentes de uma fronteira de confiança e de deploys diferentes. A web não pode importar `bap_automation`, e a recusa no servidor protege contra um PC desatualizado ou adulterado (regra 7, dado digitado intocável).
- A lista vem do contrato §10.1, que é a fonte da verdade. Sugestão sem bloqueio: o comentário de `PROIBIDAS` e o de `_CHAVES_FORA_FAROL_WEB` citarem "contrato §10.1".
- A duplicação a unificar fica **dentro do robô**: ver RD-0009.

`FAROIS`/`ACEITOS` (`pacotes.FAROIS = tuple(render.FAROIS)`) já têm fonte única. A fixture e os testes não repetem caso.

---

## PR #49 · modulo-robo/T-0017-farol-inadimplencia · head 84afe047606230ded5b558eac3ccc41de35fe7a9

**Veredito: BLOQUEIA (3 achados em aberto: RD-0009, RD-0010, RD-0011). O RD-0012 é comentário baixo e não bloqueia.**

| ID | Onde | Tipo | O que se repete | Impacto | Sev. | Proposta (antes → depois) | Dono | Bloqueia |
|---|---|---|---|---|---|---|---|---|
| RD-0009 | `bap_automation.py`: `_sem_chaves_de_acao` (nova) × `_para_json` (T-0013); `_CHAVES_FORA_FAROL_WEB` × `_PACOTE_WEB_CHAVES_ACAO` | código | Duas listas de chaves proibidas no mesmo módulo ("edicao" está nas duas) e duas varreduras recursivas: `selecionar_farol_web` chama `_para_json(_sem_chaves_de_acao(saida))`, e o `_para_json` já descarta chave proibida e chave com "_" em todo nível | manutenção: chave nova precisa entrar em 2 lugares; percorre a árvore 2 vezes | média | 1) `_CHAVES_FORA_FAROL_WEB = _PACOTE_WEB_CHAVES_ACAO \| {"tabelas", "juntas", "editar", "abrir"}`; 2) `def _para_json(obj, _nivel=0, fora=_PACOTE_WEB_CHAVES_ACAO)`, com `fora` repassado nas chamadas recursivas e o teste `ch in fora`; 3) em `selecionar_farol_web`: `val = _para_json(saida, fora=_CHAVES_FORA_FAROL_WEB)`; 4) apagar `_sem_chaves_de_acao`. | modulo-robo | sim |
| RD-0010 | `selecionar_farol_web`, chave `avisos` | texto | Aviso acrescentado "{n} gráfico(s) com nome de pessoa não aparece(m) na web." explica o que o sistema fez por trás. O gerente não decide nem age com ele (regra 3). | leitura, área de alertas poluída | média | `"avisos": [str(a) for a in (r.get("avisos") or [])] + ([f"{len(titulos_fora)} gráfico(s) ..."] if titulos_fora else [])` → `"avisos": [str(a) for a in (r.get("avisos") or [])]`. Se a falta precisar de registro, `log.info` no PC. Atualizar o contrato §10.1 ("o robô pode acrescentar (ex.: bloco tirado)"): recado ao engenheiro-software. | modulo-robo | sim |
| RD-0011 | `selecionar_farol_web` (4 linhas de fuso) × `montar_pacote_web` (as mesmas 4 linhas) | código | `agora = agora or _agora_manaus()` + `if getattr(agora, "tzinfo", None) is None: ... timezone(timedelta(hours=-4))` copiado; o `montar_pacote_web` já normaliza e repassa o `agora` | manutenção (regra de fuso em 2 lugares) | baixa | criar `def _com_fuso_manaus(agora=None) -> datetime:` com as 4 linhas e usar nas duas funções: `agora = _com_fuso_manaus(agora)` | modulo-robo | sim (código) |
| RD-0012 | bloco de constantes `# (T-0017)`: "D1 do Alexandre pendente: grafico com nome de pessoa ... fica FORA do pacote enquanto for False. Liga em 1 linha." | comentário | Comentário desatualizado: a D1 já foi decidida (R-20261124-175838-alexandre, "2 A") e a constante vale `True`. A docstring de `selecionar_farol_web` cita `tests/test_T0017_farol_web_robo.py`, que não está no branch. | manutenção | baixa | → `# D1 decidida (R-20261124-175838-alexandre, "2 A"): nome de vendedor e supervisor vai nos graficos; cliente e CNPJ nunca.` | modulo-robo | não (só comentário; entra no lote seguinte) |

**Ponto de atenção: `recortes_farol_por_uf` × `recortes_por_uf` (T-0014). Decisão: não é duplicação, `manter`.**
- `recortes_por_uf` **não calcula**: copia a barra do estado que o cartão do `vc_painel` já traz.
- `recortes_farol_por_uf` **recalcula** os cartões pelo `kpis_de` da tabela sobre as linhas da filial.
- As fontes e as saídas são diferentes, e a diferença de forma (`{"uf": {UF: {"cartoes"}}}` × `{UF: {"kpis"}}`) está documentada no contrato §10.1.
- Fica um risco de **valor**, que não é deste parecer: o mesmo número por estado sai por dois caminhos no farol (`kpis[i].estados.barras` e `recortes[UF].kpis`) e pode divergir. Vai para o `testes`.

---

## PR #50 · modulo-farois/T-0017-inadimplencia-internos · head f8257232e0b1dac7d385ca122a630acb3ff8bf36

**Veredito: SEM ACHADO EM ABERTO QUE BLOQUEIE. O RD-0013 é comentário baixo e não bloqueia. O RD-0014 é dívida antiga de outros donos e fica fora deste lote.**

| ID | Onde | Tipo | O que se repete | Impacto | Sev. | Proposta (antes → depois) | Dono | Bloqueia |
|---|---|---|---|---|---|---|---|---|
| RD-0013 | `relatorios_nucleo.py:727` `CONTA_TESTE = "000040"  # RN-GER-005: conta de testes, fora de tudo` | comentário | O comentário descreve a RN com texto diferente de `docs/produto/03-regras.md` (RN-GER-005: "fora de prospecção, indicação, pesquisa e e-mails"). A mesma regra tem 2 textos. | manutenção | baixa | → `CONTA_TESTE = "000040"      # RN-GER-005 (docs/produto/03-regras.md)` | modulo-farois | não (só comentário) |
| RD-0014 | constante "000040" espalhada: `planner_nucleo.CONTA_TESTE_MAXIMA`, `email_inadimplencia.COD_TESTE`, `respostas_bap_ajuda.COD_TESTE` e agora `relatorios_nucleo.CONTA_TESTE` | código (regra repetida) | A mesma regra (RN-GER-005) tem 4 constantes. Já havia 3 antes da T-0017. | manutenção | média | Fonte única: `relatorios_nucleo.CONTA_TESTE` (pública, ao lado de `titulos_sem_internos`); `email_inadimplencia` (já importa `rn`) passa a `COD_TESTE = {rn.CONTA_TESTE}`, e os outros importam a mesma. | modulo-posvenda, modulo-rota (e o dono de `respostas_bap_ajuda.py`) | não para a T-0017 (é anterior); tarefa própria no quadro |

**Ponto de atenção: `titulos_sem_internos` × `_interno`/`_sem_internos`.** Sem redundância: a função nova reaproveita `bd._interno` (não recopia a regra dos CNPJs internos) e é chamada de dentro do `_sem_internos` existente, no ramo novo `"inadimplencia"`. É o caminho certo.

---

## Encaminhamentos ao `testes` (valor e regra, fora do catálogo)
1. **#50:** `titulos_sem_internos` compara a conta 000040 com `t["cod"]`, que é o código do **cliente** (`E1_CLIENTE`, `bap_dados._ler_titulos`). Em `planner_nucleo` e `email_inadimplencia`, o 000040 é código de **vendedor** (`COD_VENDEDOR` / `cod_protheus`). Conferir se o filtro pega o campo certo.
2. **#50:** só os `titulos` passam pelo filtro. As `fotos` (atraso, recebido, recuperado e o gráfico "Em atraso (R$, última foto)") continuam com CNPJ interno e 000040.
3. **#50:** não há teste `test_RN_GER_004_...`/`test_RN_GER_005_...` para `titulos_sem_internos` (regra 2 do CLAUDE.md).
4. **#49:** `baixado_em` recebe o `agora` do pacote. Fica igual ao `gerado_em`, e não é a hora em que o farol foi baixado do ERP, como pede o contrato §10.1. Na tela aparecem 2 horários que dizem o mesmo.
5. **#49:** o mesmo número por estado sai em `kpis[i].estados.barras` e em `recortes[UF].kpis`. Conferir se os dois batem (filial da nota, RN-GER-006).
6. **#49:** a docstring cita `tests/test_T0017_farol_web_robo.py`, que não está no branch.
