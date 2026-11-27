# T-0023 v2 · Parecer final de redundância antes dos PRs (corretor-redundancias, 27/11/2026)

## Escopo

| Parte | Branch | Head revisado |
|---|---|---|
| Web | `modulo-web/T-0023-web` (PR #154) | `db0974abca9bfdf25e7e3242b29abc3fbef314d3` |
| Núcleo | `modulo-farois/T-0023-nucleo` (PR #155) | `f0af1127975ba74276065eaac6ce1410e6f6b16d` |
| Robô | `modulo-robo/T-0023-robo` | `5176c2d619ebfa4b74232518e4041958209bbdb4` |
| Testes | `testes/T-0023-testes` | `25b2633812181961270ee64da997554676ca53fc` |
| Contrato | `engenheiro-software/T-0023-contrato-dado-pessoal` | `36ecf9d9d05aa91b835198fa70e18dcc3650612f` |
| Contrato | `engenheiro-software/T-0023-contrato-motivo` | `077ef2614ecdcdda6ce627dccd60c44ee615cf7a` |

- **Main comparado:** `origin/main` em `472888058e870ef3e1864358045ac59e53a94a47`. Ele já tem a T-0033, a T-0034, a rota da T-0045 (#149, #150) e a web das visitas da T-0045 (#151, web 0.6.0). O #151 entrou durante esta revisão: o main estava em `98f87db` no começo.
- **Como conferi:**
  - `git diff origin/main...<head>` em cada parte;
  - o arquivo inteiro de cada head;
  - `git merge-tree` da web com o main;
  - a lista de PRs abertos (`gh api .../pulls`).
- **Fora desta revisão:** commit e recados.
- **Numeração:** o maior RD usado nos anexos era o RD-0155 (T-0045). Os novos vão do **RD-0156 ao RD-0167**.
- **Limites:**
  - `vulture` e `pylint` não estão instalados, então o código morto foi procurado à mão;
  - não houve print real das telas. Os achados de tela vêm do template e do CSS.
- **RDs da T-0023:** do RD-0131 ao RD-0146 e do RD-0151 ao RD-0153, conferidos nos 4 arquivos `redundancias-*.md` e `reteste*-redundancias*.md`. O RD-0130 é da T-0045 (`T-0045/reteste-redundancias-codigo.md`), não desta tarefa.

## Resultado: **não libera**
- Dos 19 RDs anteriores, **18 fecharam**. O RD-0139 fica **fora deste lote**: ele vai no PR 2 de faróis, "PC só leitura".
- Há **12 achados novos**, do RD-0156 ao RD-0167: 6 médios e 6 baixos.
  - **11 seguram o lote.**
  - O **RD-0162** (baixo, só comentário e título de teste) **não segura** e entra no lote seguinte.
- O RD-0167 (dado pessoal em 4 redes) nasce do encontro da T-0023 com a T-0045. Recomendo uma tarefa própria, como o RD-0139. Quem decide é o gerente-projetos. Sem essa decisão, ele segura o lote.

## Os RDs anteriores

| ID | Situação | Evidência no head |
|---|---|---|
| RD-0131 | fechado | `git diff origin/modulo-farois/T-0023-nucleo origin/modulo-robo/T-0023-robo -- relatorios_nucleo.py painel_farol.py` = vazio |
| RD-0132 | fechado | `_eventos_faturamento` chama o `_liquido` (núcleo) |
| RD-0133 | fechado | `pd_ = pct_do_liquido(...)` uma vez em `devolucoes` e em `_abas_do_painel` |
| RD-0134 | fechado | `_campos_garantia_web()` traduz o `CAMPOS_EDICAO_GARANTIA` do núcleo; o `"garantias"` não está no `CAMPOS_EDICAO_WEB` |
| RD-0135 | fechado | O robô não tem mais `__getattr__`, `MOTIVO_TEXTO_WEB` nem `MAX_TEXTO_WEB`; só tem o `motivo_texto_web(maximo=None)`, com o padrão `_rn.MAX_TEXTO_PADRAO`. Os testes usam `ba.motivo_texto_web(...)`, e o `test_T0023_robo.py:327` confere `not hasattr(ba, "MOTIVO_TEXTO_WEB")`. O contrato:1082 cita `bap_automation.motivo_texto_web(maximo)`. A linha 1083, nova, traz outra repetição (RD-0156) |
| RD-0136 | fechado | `_RE_TICKET_WEB = re.compile(r"^[\w.\-/ ]+$")` (`bap_automation.py:9653`); o 40 está só no `MAX_TEXTO_EDICAO[("garantias", "ticket")]` do núcleo |
| RD-0137 | fechado | sem `REMOVIDO_WEB`; `if _rn.REMOVIDO in v` |
| RD-0138 | fechado | sem `_RE_PESSOAL_EDICAO_WEB`; só `_rn.texto_sem_contato(v) != v` |
| RD-0139 | **fora deste lote** | `bap_relatorios.py` do head do núcleo é igual ao do main: `:4330` (padrões da nova), `:4418` (`_prazo_padrao`) e `:4476` (`"FAROL DE GARANTIAS"`). O núcleo e o robô já usam `PADRAO_NOVA_GARANTIA`, `prazo_padrao_txt` e `campos_garantia_a_gravar`. A janela do PC passa a usar essas funções no PR 2 de faróis ("PC só leitura") |
| RD-0140 | fechado | `edicoes.campo_tela` nos 2 formulários (`main.py:676` e `:690`) |
| RD-0141 | fechado | `TITULO_SEM_NOVO`, `MSG_SEM_NOVO` e `MSG_FALHA_FILA` (`edicoes.py:280-282`); `volta_ed(volta)` nos 2 POST |
| RD-0142 | fechado | `_CTRL.search(_norm_texto(bruto).replace("\n", ""))`; `edicoes.mostrado(form, c)` |
| RD-0143 | fechado | `editar.html:9` = `<p class="sub">{{ tab }}</p>` |
| RD-0144 | fechado | `editar.html:43`: a "Sugestão do PC" aparece só com `c.atual != c.padrao` |
| RD-0145 | fechado | `tabelas._agrupa_ncc(nome)` (`tabelas.py:210`, `:269`) |
| RD-0146 | fechado | `_corte_aba_web(titulo)` (`bap_automation.py:8643`), usado pelo Cliente a cliente e pelo Histórico de compra |
| RD-0151 | fechado | um `import relatorios_nucleo as _rn` por função, sem `_rn2`. O `recortes_farol_por_uf`, que importa 2 vezes em ramos diferentes, é do main e não é desta tarefa |
| RD-0152 | fechado | `tabelas.cod_e_nome(v)`, usado pelo `cliente_so_nome` e pelo `resumo_da_linha` |
| RD-0153 | fechado | uma regra `.ed-botoes` só (`estilo.css:357`); a `:667` é outro seletor (`.ed-botoes a.ed-cancelar`) |

## Resumo por dono (achados novos)

| Dono | Achados |
|---|---|
| engenheiro-software | RD-0156, RD-0158, RD-0167 (a fonte única) |
| gerente-projetos | RD-0157 |
| testes | RD-0159, RD-0160, RD-0161, RD-0162 (não segura) |
| modulo-robo | RD-0163 |
| modulo-web | RD-0164, RD-0165, RD-0166, RD-0167 (o lado da web) |
| modulo-rota | RD-0167 (o `visitas_nucleo`) |

## Achados novos

### RD-0156 · O contrato repete o teto padrão de 60 e diz que a fonte do robô é a constante da web
| Campo | Conteúdo |
|---|---|
| Onde | `.coord/contratos/relatorio.md:1083` @ 077ef26 × `:1075` (o mesmo arquivo) × `:1079` |
| Tipo | doc |
| O que se repete | Aparece 2 vezes "sem ela, 60 (`edicoes.MAX_TEXTO`)": na `:1075`, que é o pacote da web, e de novo na `:1083`, para o `motivo_texto_web` do robô. Só que o robô lê o `relatorios_nucleo.MAX_TEXTO_PADRAO`, e a `:1079` diz "Teto do texto, um lugar só: `relatorios_nucleo.MAX_TEXTO_EDICAO`" |
| Impacto | leitura e manutenção: o leitor vê 2 fontes para o 60 do robô |
| Severidade | média |
| Proposta | **Antes:** "…com o `max` do campo; sem `maximo` (`None`), o teto é 60 (`edicoes.MAX_TEXTO`)." **Depois:** "…com o `max` do campo; sem `maximo`, o padrão do núcleo (`relatorios_nucleo.MAX_TEXTO_PADRAO`)." |
| Dono | engenheiro-software |

### RD-0157 · Os PRs da T-0023 v1 seguem abertos junto com os da v2, para os mesmos donos
| Campo | Conteúdo |
|---|---|
| Onde | PRs abertos #102 (`modulo-web/T-0023-posvenda-farois`), #103 (`modulo-robo/…`), #105 (`modulo-farois/…`) e #106 (`testes/…`), todos de 26/11, ao lado do #154 (web v2), do #155 (núcleo v2), do #153 (ponte do testes) e dos PRs do robô e do testes que vão abrir |
| Tipo | tarefa |
| O que se repete | 2 PRs abertos da mesma tarefa para o mesmo dono: web #102 e #154; núcleo #105 e #155; robô #103 e o PR v2; testes #106, o #153 e o PR v2. A regra é "um PR por dono e por lote" |
| Impacto | decisão: o quadro mostra 2 entregas da mesma coisa, e o PR velho pode ser revisado ou entrar no main por engano |
| Severidade | média |
| Proposta | **Depois:** fechar o #102, o #103 e o #106, cada um com o comentário "Substituído pela T-0023 v2: #154 / PR do robô / PR do testes". O #105 fica aberto só até nascer o PR 2 de faróis v2 ("PC só leitura", RD-0139) e então fecha da mesma forma. [SUPOSIÇÃO] O #105 é a versão v1 desse PR 2 |
| Dono | gerente-projetos |

### RD-0158 · O contrato está em 2 branches, uma dentro da outra
| Campo | Conteúdo |
|---|---|
| Onde | `engenheiro-software/T-0023-contrato-dado-pessoal` (36ecf9d) × `engenheiro-software/T-0023-contrato-motivo` (077ef26 = 36ecf9d + 1 commit) |
| Tipo | tarefa |
| O que se repete | O commit 36ecf9d (§10.10.3) está nas 2 branches. Dois PRs levariam o mesmo §10.10.3 duas vezes, e o squash do primeiro deixaria o segundo com o mesmo trecho repetido no diff |
| Impacto | manutenção (revisão e merge em dobro) |
| Severidade | baixa |
| Proposta | **Depois:** um PR só, da `T-0023-contrato-motivo` (077ef26), com o §10.10.3 e o §10.9.1. A `T-0023-contrato-dado-pessoal` não vira PR |
| Dono | engenheiro-software (cc gerente-projetos) |

### RD-0159 · O doc do testes reescreve o §10.10.3 com outro texto, e o pedido ao contrato já foi atendido
| Campo | Conteúdo |
|---|---|
| Onde | `docs/testes/T-0023.md:101-107` @ 25b2633 × contrato §10.10.3 "Onde o `testes` procura" (`relatorio.md:1392-1396` @ 077ef26) |
| Tipo | doc |
| O que se repete | As 4 regras da busca de dado pessoal no JSON aparecem nos 2 docs, com textos diferentes. O doc diz "inteiro de 11 ou 14 dígitos reprova"; o contrato diz "só reprova o inteiro de 11 ou 14 dígitos **fora das colunas de código**". O doc tem uma regra que o contrato não tem ("nenhum CPF/CNPJ formatado e nenhum e-mail no texto inteiro"). A `:102` ainda diz "O que precisa mudar é a frase do §10.10.3… Recado `pedido` ao engenheiro-software", e isso já foi feito em 36ecf9d |
| Impacto | manutenção e decisão: são 2 versões da mesma regra de teste |
| Severidade | média |
| Proposta | **Depois** (`:102-107`): "- Nem o robô nem o núcleo têm defeito aqui: o `texto_sem_contato` roda onde o §10.10.3 manda. O teste segue o §10.10.3, "Onde o `testes` procura" (fonte da verdade), sem afrouxar: saiu a isenção larga do teste do robô, que pulava a coluna toda." |
| Dono | testes |

### RD-0160 · O "06/10 sem % negativo" é testado 2 vezes, em 2 arquivos, com o mesmo `montar` real
| Campo | Conteúdo |
|---|---|
| Onde | `tests/test_T0023_nucleo_pct_du.py:30` (`test_RN_GER_002_resumo_06_10_sem_percentual_negativo`) × `tests/test_T0023_valor_regra.py:494` (`test_RN_GER_002_faturado_liquido_zero_ou_negativo_mostra_traco`) |
| Tipo | teste |
| O que se repete | Os 2 testes rodam `rn.montar("pl_devolucoes", RAIZ, …, {"ANO": "2026", "MÊS": "10"})` na base real e conferem que nenhum valor do "% devolvido do faturado" é negativo. A docstring do `nucleo_pct_du` já diz que o valor × regra de 06/10 "mora em tests/test_T0023_valor_regra.py" |
| Impacto | desempenho (2 `montar` reais) e manutenção |
| Severidade | baixa |
| Proposta | **Depois:** sai o `test_RN_GER_002_resumo_06_10_sem_percentual_negativo` do `nucleo_pct_du`. No `valor_regra:494`, depois do `r = rn.montar(...)`, a conferência passa a valer para todas as séries: `assert all(v is None or v == "—" or v >= 0 for b in r["painel"]["blocos"] for g in [b.get("grafico") or {}] if str(g.get("titulo", "")).startswith("% devolvido do faturado") for s in g.get("series", []) for v in s["valores"])` |
| Dono | testes |

### RD-0161 · Os 2 arquivos de teste do núcleo conferem os mesmos tetos da `edicao_garantia`
| Campo | Conteúdo |
|---|---|
| Onde | `tests/test_T0023_nucleo_rd.py:55-56` (`assert "max" not in por["descricao"]` e `assert por["observacao"]["max"] == 600`) × `tests/test_T0023_nucleo_garantia.py:43` e `:45` (as mesmas 2 conferências) |
| Tipo | teste |
| O que se repete | 2 asserts iguais sobre a mesma saída de `rn.edicao_garantia`, em 2 arquivos |
| Impacto | manutenção |
| Severidade | baixa |
| Proposta | **Depois:** no `nucleo_rd`, o `test_RN_GER_012_ticket_max_40_vem_do_nucleo` fica só com `assert por["ticket"]["max"] == 40`, e saem as linhas 55 e 56 |
| Dono | testes |

### RD-0162 · Comentário com o RD errado e título de teste repetido (não segura o lote)
| Campo | Conteúdo |
|---|---|
| Onde | `tests/test_T0023_robo.py:507` (`# RD-0151: o teto padrão é só o do núcleo`); `tests/test_T0023_robo.py:405` × `tests/test_T0023_nucleo_rd.py:32`, os 2 chamados `test_RN_POS_005_prazo_igual_ao_padrao_fica_em_branco` |
| Tipo | teste (comentário e título) |
| O que se repete | O `MAX_TEXTO_WEB` saiu pelo RD-0135, e o RD-0151 é o import duplicado. O mesmo nome de teste aparece em 2 arquivos: um testa a função do núcleo, o outro testa o plano do robô |
| Impacto | leitura |
| Severidade | baixa (só comentário e título) |
| Proposta | **Depois:** `:507` `# RD-0135: o teto padrão é só o do núcleo`; `:405` `def test_RN_POS_005_plano_da_garantia_usa_a_regra_do_prazo_do_nucleo():` |
| Dono | testes |

### RD-0163 · A fonte "Movimentos do Protheus" está escrita 6 vezes no `_FONTE_BAIXADO_WEB`
| Campo | Conteúdo |
|---|---|
| Onde | `bap_automation.py:6746-6769` @ 5176c2d. As entradas `"pl_devolucoes"` e `"pl_garantias"` (novas) se somam a `pv_pedidos`, `pl_entregas`, a compreensão do lote 2 e `vc_meta` |
| Tipo | código |
| O que se repete | `(Path(BKP_BAPTOOLS), "Relatorio_Movimentos_BAP_Protheus_*.xlsx")`, 6 vezes, 2 delas novas |
| Impacto | manutenção: se o nome do arquivo mudar, é preciso trocar em 6 lugares |
| Severidade | baixa |
| Proposta | **Depois:** ```_MOVIMENTOS_WEB = (Path(BKP_BAPTOOLS), "Relatorio_Movimentos_BAP_Protheus_*.xlsx")``` e, no dicionário, ```# Movimentos do Protheus (ftPedidos): Pedidos, Entregas, lote 2 (T-0024), Metas (T-0022), Devoluções e Garantias (T-0023 v2)``` ```**{r_: _MOVIMENTOS_WEB for r_ in ("pv_pedidos", "pl_entregas", *RIDS_LIVRES_WEB, "vc_meta", "pl_devolucoes", "pl_garantias")},``` com o `pl_inadimplencia`, o `vc_visitas` e o `pl_ncc` como estão |
| Dono | modulo-robo |

### RD-0164 · O CSS novo abre 2 blocos `@media(max-width:700px)` e repete o 44 px do `--alvo`
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/static/estilo.css:663` (`@media(max-width:700px){.bc3-k small{…}}`) × `:677-679` (outro `@media(max-width:700px)`, com `min-height:44px`) @ db0974a; o token `--alvo:44px` está na `:96` |
| Tipo | código |
| O que se repete | A mesma media query 2 vezes no trecho novo da T-0023, a 14 linhas uma da outra, e o 44 px literal no lugar de `var(--alvo)`. O main já usa `var(--alvo)` nos alvos novos: `.bt-principal` e as regras `.vz-*` da T-0045 |
| Impacto | manutenção |
| Severidade | baixa |
| Proposta | **Depois:** sai a `:663`, e o bloco final fica ```@media(max-width:700px){ .bc3-k small{hyphens:auto;overflow-wrap:anywhere} .ed-botoes button,.ed-botoes .ed-cancelar,.bc3-ed a.bt-ed,.ed-campo input,.ed-campo select{min-height:var(--alvo)} }```, com os comentários "UX R2" e "UX A4" no topo |
| Dono | modulo-web |

### RD-0165 · O `edicoes.py` refaz 2 contas que ele já tem
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/edicoes.py:331` (`teto = _mais_um_ano(hoje)` no `_checa`) × `:275` (`data_max(hoje)`, "Teto da data livre"); `:436-437` (`_norm_texto(...)` e `v if c.get("caixa") else v.upper()` no `valores_do_novo`) × `:351-353` (a mesma conta no `_checa`) |
| Tipo | código |
| O que se repete | O teto da data livre, 2 vezes: uma pela função pública e outra pelo `_mais_um_ano` direto. A normalização do texto livre com a caixa, 2 vezes |
| Impacto | manutenção: uma regra da data livre ou da caixa pode mudar num caminho e não no outro |
| Severidade | baixa |
| Proposta | **Depois:** `:331` `teto = data_max(hoje)`. No `edicoes.py`, ```def _texto_form(c: dict, s: str) -> str: """Texto livre como o PC compara: quebras e pontas normalizadas; em maiúsculas se o campo não mantém a caixa.""" v = _norm_texto(s) return v if c.get("caixa") else v.upper()```, usado no `_checa` (`v, ref = _texto_form(c, bruto), _texto_form(c, atual)`) e no `valores_do_novo` (`v = _texto_form(c, str(form.get("c_" + nome, c["padrao_txt"])))`) |
| Dono | modulo-web |

### RD-0166 · O PR da web leva a fila antiga, que o main trocou na T-0045
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/edicoes.py` @ db0974a: `Fila.registrar` (o `quando = (agora_ or agora()).astimezone(MANAUS).strftime(...)` e o `reg = {...}` em linha, com o `novo`) e `Fila._acrescentar` (`open`/`fsync` em linha) × main 4728880 (#151): `_quando(agora_)`, `Fila.registrar_item(campos)` e `arquivos.acrescentar_linha` |
| Tipo | código |
| O que se repete | A hora da fila, a montagem do registro e a gravação com `fsync` ficam em 2 versões. O `git merge-tree origin/main origin/modulo-web/T-0023-web` dá conflito no `edicoes.py`, no `estilo.css`, no `__init__.py` e no `test_T0035_pacote_por_farol.py`. Se o conflito for resolvido mantendo o lado da T-0023, a fila volta a ter a cópia que o #151 tirou (o mesmo caso do RD-0131) |
| Impacto | manutenção: as edições e os lotes de visitas deixam de usar a mesma fila |
| Severidade | média |
| Proposta | **Depois** (com o merge do `origin/main`): ```def registrar(self, *, usuario, rid, tabela, modulo, chave, valores, antes, agora_=None, novo: bool = False) -> dict: campos = {"id": str(uuid.uuid4()), "usuario": usuario, "rid": rid, "tabela": tabela, "modulo": modulo, "chave": chave, "valores": valores, "antes": antes} if novo: campos["novo"] = True                       # §10.9.2: linha nova, chave NOVO-xxxxxxxx return self.registrar_item(campos, agora_=agora_)```. O `_acrescentar` e o `_quando` ficam como estão no main. Pronto quando `git diff origin/main origin/modulo-web/T-0023-web -- web/app/edicoes.py` não mexer mais no `registrar_item`, no `_quando` nem no `_acrescentar` |
| Dono | modulo-web |

### RD-0167 · Dado pessoal (RN-GER-011) com 4 redes diferentes: 2 no PC e 2 na web
| Campo | Conteúdo |
|---|---|
| Onde | **PC:** `relatorios_nucleo.py:814-831` (`_DOC_MEIO`, `_DOC_SOLTO`, `_EMAIL`, `_FONE`, bloco `padroes-pessoais` do contrato relatorio §10.9.1) × `visitas_nucleo.py:1541-1544` (`_RX_EMAIL`, `_RX_CNPJ`, `_RX_CPF`, `_RX_FONE`, contrato visitas-nuvem §3.6). **Web:** `web/app/edicoes.py` @ db0974a (`RE_EMAIL`, `RE_DOC_MEIO`, `RE_DOC_SOLTO`, `RE_FONE`, novos nesta tarefa) × `web/app/visitas.py:112-116` no main (`RE_PESSOAL`) |
| Tipo | código · doc |
| O que se repete | A mesma regra ("o texto não leva CPF, CNPJ, telefone nem e-mail") aparece em 2 pares de espelhos, com padrões diferentes. O e-mail tem 2 textos (`(?:\.[\w\-]+)+` × `(\.[\w-]+)+`). No CPF e no CNPJ, o `DOC_MEIO` aceita os separadores como opcionais, e o `_RX_CPF`/`_RX_CNPJ` exige a máscara ou os dígitos soltos. O telefone é outra regra (`_FONE` com +55 e separadores × `_RX_FONE` com hífen). Quando a T-0023 entrar, o mesmo site terá 2 redes. É uma redundância nova, do encontro desta tarefa com a T-0045 |
| Impacto | decisão e manutenção: o mesmo texto pode ser barrado nas edições e aceito nas visitas, ou o contrário; e uma mudança na regra precisa ser feita em 4 lugares e 2 contratos |
| Severidade | média |
| Proposta | **Depois:** a regra fica num padrão só, o bloco `padroes-pessoais` do contrato relatorio §10.9.1 (fonte da verdade). (1) O contrato visitas-nuvem §3.6 passa a apontar para o bloco, sem padrões próprios (engenheiro-software). (2) O `visitas_nucleo` usa os padrões do `relatorios_nucleo`, que já vai no COPY do serviço da T-0045, e mantém só o `formato` dele (modulo-rota). (3) O `web/app/visitas.py` usa os `edicoes.RE_*` em vez do próprio `RE_PESSOAL`, ou os 2 passam a ler um `web/app/pessoal.py` (modulo-web). (4) O teste de paridade confere as 2 pontas contra o bloco (testes). **Recomendação:** é uma mudança de regra que vai além da T-0023, então sugiro uma tarefa própria, como o RD-0139, marcada "fora deste lote". Quem decide é o gerente-projetos. Sem essa decisão, o achado segura o lote |
| Dono | engenheiro-software (a fonte única), modulo-rota, modulo-web (e testes, a paridade) |

## Redundância útil (não remover)
- **As 2 pontas do contrato entre o PC e o Render**, porque o Render não importa o PC. Ficam:
  - robô `_RE_CHAVE_NOVA_WEB` × web `RE_CHAVE_NOVA`;
  - `_MAX_CAMPOS_EDICAO_WEB` × `MAX_CAMPOS` (16);
  - `_DATA_LIVRE_MIN_WEB` e `_mais_um_ano_web` × `DATA_MIN` e `_mais_um_ano`;
  - `_texto_normalizado_web` × `_norm_texto`;
  - as listas de abas e colunas dos 3 faróis (`_ABAS_TABELAS_WEB` e `_COLUNAS_TABELAS_WEB` × `ABAS` e `COLUNAS_RID`);
  - o contato fora em 2 fronteiras (`_COLUNAS_FORA_TABELA_WEB` × `FORA_POR_TABELA`, mais a checagem do nome do campo e do rótulo no `erro_spec`).
- `manter?` · **A ponte do `test_T0021` (PR #153, igual em `testes/T-0023-testes`).**
  - O que é: `_MOTIVO_TEXTO_60 = (ba.motivo_texto_web(60) if hasattr(ba, "motivo_texto_web") else ba.MOTIVO_TEXTO_WEB)`.
  - Por que fica: ela deixa o CI do PR do robô verde enquanto o main ainda tem a constante velha.
  - Quando sai: depois do merge do robô, o ramo `else` e o comentário "no main de hoje" viram código morto (o mesmo caso do RD-0155). Saem no lote seguinte, com `ba.motivo_texto_web()`.
  - O mesmo vale para os `skipif` "núcleo sem … (f0af112)" dos arquivos de teste da T-0023.
- `manter?` · **`teto` no `validar_edicao_web` (`:9807`).**
  - Para um campo que não é texto, o `else _rn.MAX_TEXTO_PADRAO` dá o mesmo que `_rn.max_texto_edicao(...)`, porque sem entrada o núcleo já devolve 60.
  - Fica como leitura explícita ("data e lista não têm teto próprio"), sem um segundo número.

## Fora do escopo: encaminhar ao `testes`
1. `docs/testes/T-0023.md:14`: o cabeçalho da coluna diz "Combinado, rodada 2", e o texto do topo diz que "vale" a rodada 5. O rótulo contradiz o valor.
2. O contrato:1082 diz "`max` do pacote diferente do número do núcleo = edição **recusada**, com o motivo de `motivo_texto_web`". O `edicao_web` levanta `ValueError` (`bap_automation.py`, "max da edicao diferente do nucleo"), e aí a edição nem vai à web, sem motivo nenhum. A divergência segue desde o primeiro parecer.
3. `_FONTE_BAIXADO_WEB["pl_garantias"]` aponta para os Movimentos do Protheus. As garantias são digitadas no `_GARANTIAS`, e só o Histórico de compra vem dos Movimentos. Falta conferir se o "baixado em" da faixa é o que a pessoa espera.

## Para liberar
- Fechar os RD-0156 a RD-0161 e os RD-0163 a RD-0166, com reteste nos novos heads (diff antes → depois).
- No RD-0166, o merge do `origin/main` na web antes do PR.
- No RD-0167, uma de 2 saídas: a decisão do gerente-projetos de abrir a tarefa própria ("fora deste lote") ou a correção nos 4 donos.
- O RD-0162 entra no lote seguinte. O RD-0139 vai no PR 2 de faróis.
- Este parecer vale para os heads da tabela do Escopo. Um head novo pede reteste.

---

# Reteste 1 · heads novos (corretor-redundancias, 27/11/2026)

## Escopo
| Parte | Branch | Head revisado |
|---|---|---|
| Contrato | `engenheiro-software/T-0023-contrato-motivo` | `a81a1b0306c96942609811aaa10d6221453ef87b` (com o merge do main 4728880) |
| Robô | `modulo-robo/T-0023-robo` | `03e9c9debe5e14f9b0a1ea7427c8043e6841f309` |
| Web | `modulo-web/T-0023-web` | `5c467217a197429e49c95232eb535e443a4d287a` (com o merge do main 4728880 em `1772234`) |
| Testes | `testes/T-0023-testes` | `25b2633` (sem head novo) |

- **Main:** `472888058e870ef3e1864358045ac59e53a94a47`.
- **Como conferi:** `git diff <head antigo> <head novo>`, `git diff origin/main...<head>`, o arquivo inteiro e o estado dos PRs pela API (`gh api .../pulls/<n>`).
- **Numeração:** o maior RD usado era o RD-0169 (o RD-0168 e o RD-0169 são da T-0045, `T-0045/redundancias-reteste-testes.md`), então o novo é o RD-0170. O próximo livre é o RD-0171.

## Resultado: **não libera ainda**
- Fecharam 8 achados: do RD-0156 ao RD-0158 e do RD-0163 ao RD-0166.
- O RD-0167 ficou **fora do lote**: virou a T-0049, por decisão do gerente-projetos.
- Os 4 do `testes` (RD-0159 a RD-0162) seguem **abertos** até o head novo. Desses, 3 seguram o lote; o RD-0162 não segura.
- A correção da web trouxe 1 comentário desatualizado: o RD-0170, baixo, só comentário. Ele não segura o lote.

| ID | Situação | Evidência |
|---|---|---|
| RD-0156 | **fechado** | `relatorio.md:1083` @ a81a1b0: "sem `maximo` (`None`), o teto é o padrão do núcleo (`relatorios_nucleo.MAX_TEXTO_PADRAO`)". A `:1075` fica com o `edicoes.MAX_TEXTO`, que é o lado do pacote da web. O PR, contra o main, mexe só no `relatorio.md` e no diário |
| RD-0157 | **fechado** (o #105 vai junto com o RD-0139) | #102, #103 e #106 = `closed`. O #105 segue `open` até nascer o PR 2 de faróis, como combinado |
| RD-0158 | **fechado** | Decisão: um PR só, da `T-0023-contrato-motivo` (a81a1b0). A `T-0023-contrato-dado-pessoal` (36ecf9d) não tem PR aberto. Confiro de novo quando o PR nascer |
| RD-0159 | **aberto** | `testes` sem head novo (25b2633) |
| RD-0160 | **aberto** | idem |
| RD-0161 | **aberto** | idem |
| RD-0162 | **aberto** (não segura) | idem; é baixo, só comentário e título |
| RD-0163 | **fechado** | `_MOVIMENTOS_WEB` (`bap_automation.py:6746-6747`) é usado pelas 6 entradas. A string do arquivo aparece 1 vez no robô. O núcleo dentro do robô segue igual ao `f0af112` |
| RD-0164 | **fechado** | O trecho da T-0023 tem 1 bloco `@media(max-width:700px)` só, com o `.bc3-k small` e os alvos em `min-height:var(--alvo)`. Não há mais 44 px literal no trecho novo |
| RD-0165 | **fechado** | `edicoes.py:348` `teto = data_max(hoje)`; `_texto_form(c, s)` (`:275`) usado no `_checa` (`:368`) e no `valores_do_novo` (`:451`); o `_mais_um_ano` só é chamado pelo `data_max` (`:294`) |
| RD-0166 | **fechado** | A web tem o main 4728880. O `Fila.registrar(..., novo=False)` monta os `campos` e chama o `registrar_item`. O `git diff origin/main origin/modulo-web/T-0023-web -- web/app/edicoes.py` não mexe no `registrar_item`, no `_quando` nem no `_acrescentar` (`acrescentar_linha`) |
| RD-0167 | **fora do lote** | T-0049, "uma fonte só para a regra do dado pessoal", por decisão do gerente-projetos (como o RD-0139) |
| RD-0139 | **fora do lote** | sem mudança: vai no PR 2 de faróis |

## Repetição nova

### RD-0170 · O comentário do CSS ainda promete os alvos de 44 px no bloco errado (não segura o lote)
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/static/estilo.css` @ 5c46721, os 2 comentários do trecho da T-0023: "/* T-0023 v2 (UX R2): rótulo longo do cartão da faixa se divide em vez de vazar */" (acima do `@media(max-width:700px)` que agora tem também os alvos) e "/* T-0023 v2 (UX A1/A2/A4): formulário largo (Garantia) em 4 colunas no PC, sem rolar; alvos de 44 px no celular */" (acima do bloco do PC, que não tem alvo) |
| Tipo | código (comentário) |
| O que se repete | "alvos de 44 px no celular" está no comentário do bloco do PC, e os alvos foram para o bloco do celular, que só cita a R2 |
| Impacto | leitura |
| Severidade | baixa (só comentário) |
| Proposta | **Depois:** "/* T-0023 v2 (UX R2 e A4): no celular, o rótulo longo do cartão se divide e os alvos têm `--alvo` */" acima do `@media(max-width:700px)`, e "/* T-0023 v2 (UX A1/A2): formulário largo (Garantia) em 4 colunas no PC, sem rolar */" acima do resto |
| Dono | modulo-web |

## Para liberar
- Os RD-0159, RD-0160 e RD-0161 fechados no head novo do `testes`. O RD-0162 pode ir junto ou no lote seguinte.
- Os RD-0162 e RD-0170 não seguram o lote.
- Este reteste vale para a81a1b0 (contrato), 03e9c9d (robô) e 5c46721 (web). Um head novo pede reteste.
