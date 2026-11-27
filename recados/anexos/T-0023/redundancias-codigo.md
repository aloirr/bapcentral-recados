# T-0023 v2 · Auditoria de redundância do código (corretor-redundancias)

- **Escopo:** `git diff origin/main...<branch>` (main em `30ae65d`), nas 3 partes. O clone foi usado só para leitura, sem troca de branch.

| Parte | Branch | Head revisado |
|---|---|---|
| Núcleo | `modulo-farois/T-0023-nucleo` | `7580eb1496e722695e08cb3ca63bf4f4c87237bd` |
| Robô | `modulo-robo/T-0023-robo` | `f86adfa25d14fe5731d84bd6becfd233e347d51f` |
| Web | `modulo-web/T-0023-web` | `3cc4fe06cfeff7a9d494fdfa71a74acb83d6730b` |

- **Foco:** regra escrita 2 vezes entre núcleo, robô e web (tetos de texto, campos de edição, ticket, contato fora, "[removido]", "% do faturado"); cópia da edição da T-0021 em vez de reuso; texto repetido nas telas; código morto.
- **Resultado:** **não libera.** São 16 achados em aberto, do RD-0131 ao RD-0146: 1 alto, 10 médios e 5 baixos. Nenhum é só de comentário ou de título de teste, então todos seguram o lote.
- **Numeração:** o maior RD usado nos anexos era o RD-0128. A T-0045 ficou com o RD-0129 e o RD-0130, então esta auditoria começa no RD-0131.
- **Limites:**
  - `vulture` e `pylint` não estão instalados. A busca por código morto foi feita à mão, contando onde cada nome novo é usado.
  - Os achados de tela (RD-0143 e RD-0144) vêm do template, não de um print real. [SUPOSIÇÃO] A tela renderizada mostra o que o template monta.

## Resumo por dono

| Dono | Achados |
|---|---|
| modulo-farois | RD-0132, RD-0133, RD-0136 (com o robô), RD-0139 (com o robô e o modulo-posvenda) |
| modulo-robo | RD-0131, RD-0134, RD-0135, RD-0136, RD-0137, RD-0138, RD-0139, RD-0146 |
| modulo-posvenda | RD-0139 (as funções novas no `garantias.py`) |
| modulo-web | RD-0140, RD-0141, RD-0142, RD-0143, RD-0144, RD-0145 |
| gerente-projetos | RD-0131 (a ordem do merge) |

## Achados

### RD-0131 · O PR do robô leva uma cópia velha das regras do núcleo
| Campo | Conteúdo |
|---|---|
| Onde | robô `f86adfa`, `relatorios_nucleo.py`: `farol_ncc` (montar), `devolucoes`, `_abas_do_painel`, `_painel_devolucoes` |
| Tipo | código |
| O que se repete | O robô fez o merge do núcleo em `7ebfe4e`, e o núcleo seguiu até `b0e8ae2`/`7580eb1`. As mesmas 3 regras aparecem no PR do robô escritas de outro jeito, em 4 lugares: (1) RN-GER-007: `lambda a, b: ctx.uteis(a, min(b, hoje - timedelta(days=1)))` em linha, contra o `_uteis_ate_ontem(ctx)` do núcleo; (2) RN-GER-002: `v = it["valor"] if it["tipo"] == "VND" else -abs(it["valor"])` em linha, contra o `_liquido(it)`; (3) `pct_de(dev, atual['vnd'] - dev)` com `if atual["vnd"] - dev > 0`, contra o `pct_do_liquido(dev, atual['real'])`; (4) `(it["dt_nf"], abs(v), -abs(v))` no `_painel_devolucoes`, contra o `_eventos_faturamento(ctx, liquido=True)` |
| Impacto | manutenção: o PR do robô mostra uma regra que o núcleo já trocou. Com o merge squash, os 2 PRs se chocam nesses 4 pontos |
| Severidade | média |
| Proposta | **Antes:** `git diff origin/modulo-farois/T-0023-nucleo origin/modulo-robo/T-0023-robo -- relatorios_nucleo.py` mostra os 4 trechos. **Depois:** o robô faz o merge de `origin/modulo-farois/T-0023-nucleo` (`7580eb1`), ou do `origin/main` depois do merge do núcleo, e esse diff fica vazio. Ordem do merge: o núcleo primeiro, depois o robô, depois a web |
| Dono | modulo-robo (cc gerente-projetos, pela ordem do merge) |

### RD-0132 · O faturado líquido tem 2 funções, e o "% do faturado" do mesmo farol sai de cada uma
| Campo | Conteúdo |
|---|---|
| Onde | núcleo, `relatorios_nucleo.py:558` (`_eventos_faturamento`) e `:2622` (`_liquido`); quem usa: `devolucoes` (`:7841`, via `_liquido`) e `_painel_devolucoes` (`:19111`, via `_eventos_faturamento`) |
| Tipo | código |
| O que se repete | RN-GER-002 ("VND soma, DEV subtrai `-abs`") escrita 2 vezes: `_liquido` e o `liquido=True` do `_eventos_faturamento` (`ev += [(it["dt_nf"], -abs(it["valor"])) ... if it["tipo"] == "DEV"]`). O "% do faturado" da aba Devoluções e o "% devolvido do faturado" do painel do mesmo farol usam uma versão cada |
| Impacto | manutenção: uma mudança na regra (outro tipo de nota, por exemplo) muda uma tela e não a outra |
| Severidade | média |
| Proposta | **Depois** (`_eventos_faturamento` passa a usar o `_liquido`): ```def _eventos_faturamento(ctx, liquido=False): """[(data da NF, valor)] das vendas; liquido = VND - DEV (RN-GER-002, `_liquido`).""" ev = [] for it in ctx.tabela["itens"]: v = _liquido(it) if liquido else (it["valor"] if it["tipo"] == "VND" else None) if v is not None: ev.append((it["dt_nf"], v)) return ev``` |
| Dono | modulo-farois |

### RD-0133 · O mesmo percentual é calculado 2 vezes no mesmo cartão
| Campo | Conteúdo |
|---|---|
| Onde | núcleo, `relatorios_nucleo.py:7894-7895` (cartão "% do faturado" das Devoluções) e `:9580-9581` (cartão "Devoluções" do Painel) |
| Tipo | código |
| O que se repete | `pct_do_liquido(val, fat)` 2 vezes (valor e tom), e `pct_do_liquido(dev, atual["real"])` 2 vezes (texto e condição) |
| Impacto | manutenção: o valor e o tom (ou o texto e a condição) podem divergir numa edição futura |
| Severidade | baixa |
| Proposta | **Depois:** `pd = pct_do_liquido(val, fat)` e então `kpi("% do faturado", p(pd), "alerta" if (pd or 0) > 3 else "ok", "")`; no Painel, `pd = pct_do_liquido(dev, atual["real"])` e então `f"{br(pd, 1)}% do faturado" if pd is not None else ""` |
| Dono | modulo-farois |

### RD-0134 · Os 14 campos da Garantia e o tipo de cada um estão escritos 2 vezes
| Campo | Conteúdo |
|---|---|
| Onde | núcleo `relatorios_nucleo.py:1807` (`CAMPOS_EDICAO_GARANTIA`) × robô `bap_automation.py:8100` (`CAMPOS_EDICAO_WEB["garantias"]`) |
| Tipo | código |
| O que se repete | Os 14 nomes de campo e o tipo (`texto`→`livre`, `data`→`data_livre`, `lista`, `longo`, e o `ticket`), nas 2 listas. O contrato §10.9.3 diz "regra no núcleo, o robô só traduz" |
| Impacto | manutenção: um campo a mais no núcleo sem a mesma mudança no robô faz a `edicao_web` descartar o campo sem aviso |
| Severidade | média |
| Proposta | **Depois:** tirar o `"garantias"` do `CAMPOS_EDICAO_WEB` e, no `campos_do_lugar_web`, traduzir o do núcleo: ```_TIPO_CONFERE_WEB = {"texto": "livre", "data": "data_livre", "lista": "lista", "longo": "longo"} ... if lugar["modulo"] == "garantias": import relatorios_nucleo as _rn  # noqa: PLC0415 return {c: "ticket" if c == "ticket" else _TIPO_CONFERE_WEB[t] for c, _r, t, _col in _rn.CAMPOS_EDICAO_GARANTIA}``` |
| Dono | modulo-robo |

### RD-0135 · O teto padrão de 60 caracteres tem 2 fontes no PC
| Campo | Conteúdo |
|---|---|
| Onde | robô `bap_automation.py:9636` (`MAX_TEXTO_WEB = 60`), usado em `:8188`, `:8190` e `:9805` × núcleo `relatorios_nucleo.py:1799` (`MAX_TEXTO_PADRAO = 60`) |
| Tipo | código |
| O que se repete | O 60, 2 vezes. O RD-0086 do desenho fechou "o teto vem de **um lugar só**: `relatorios_nucleo.MAX_TEXTO_EDICAO`". A `edicao_web` compara `int(c.get("max") or MAX_TEXTO_WEB) != teto`: se o núcleo mudar o padrão, toda edição sem `max` deixa de ir |
| Impacto | manutenção |
| Severidade | média |
| Proposta | **Depois:** `:8188` `if int(c.get("max") or _rn2.MAX_TEXTO_PADRAO) != teto:` · `:8190` `if teto != _rn2.MAX_TEXTO_PADRAO:` · `:9805` `teto = _rn.max_texto_edicao(lugar["modulo"], campo)` para todo tipo (sem entrada, o núcleo já devolve 60). Sai o `MAX_TEXTO_WEB`. O `motivo_texto_web(maximo)` fica sem padrão. O `MOTIVO_TEXTO_WEB` só existe hoje para os testes da T-0021: eles passam a chamar `ba.motivo_texto_web(rn.MAX_TEXTO_PADRAO)`, e o contrato:1082 passa a citar o `motivo_texto_web(teto)` (recado ao engenheiro-software) |
| Dono | modulo-robo |

### RD-0136 · O teto de 40 do ticket está escrito 2 vezes no robô e fora da tabela do núcleo
| Campo | Conteúdo |
|---|---|
| Onde | robô `bap_automation.py:9650` (`_RE_TICKET_WEB = re.compile(r"^[\w.\-/ ]{1,40}$")`) e `:9813` (`len(v) > (40 if tipo == "ticket" else teto)`); núcleo `MAX_TEXTO_EDICAO` (sem o ticket) |
| Tipo | código |
| O que se repete | O 40, 2 vezes no robô. O `len` nunca recusa nada que o regex não recusasse. A web não recebe o número: o ticket vai sem `max` e o formulário aceita até 60 |
| Impacto | manutenção e cliques: a web aceita um ticket de 41 a 60 caracteres, e depois o PC recusa |
| Severidade | média |
| Proposta | **Depois:** no núcleo, `MAX_TEXTO_EDICAO[("garantias", "ticket")] = 40`, e o `edicao_garantia` põe `c["max"] = max_texto_edicao("garantias", campo)` quando o teto do campo for diferente do padrão (não só no `longo`). No robô: `_RE_TICKET_WEB = re.compile(r"^[\w.\-/ ]+$")` e `if len(v) > teto:` (sem o 40). O teto vem do núcleo, e a web passa a mostrar `maxlength="40"` |
| Dono | modulo-farois (o número) e modulo-robo (o uso) |

### RD-0137 · O "[removido]" tem 2 constantes no PC
| Campo | Conteúdo |
|---|---|
| Onde | robô `bap_automation.py:9648` (`REMOVIDO_WEB = "[removido]"`), usado em `:9816` × núcleo `relatorios_nucleo.py:833` (`REMOVIDO = "[removido]"`, que o `texto_sem_contato` usa) |
| Tipo | código |
| O que se repete | `"[removido]"`, 2 vezes no mesmo processo. A função que confere (`validar_edicao_web`) já importa o `relatorios_nucleo` como `_rn` |
| Impacto | manutenção: se a marca do núcleo mudar, o robô deixa de barrar o texto limpo que volta (regra 4 do §10.9.1) |
| Severidade | média |
| Proposta | **Depois:** `if _rn.REMOVIDO in v: return MOTIVO_REMOVIDO_WEB`, e sai o `REMOVIDO_WEB`. A cópia da web (`edicoes.REMOVIDO`) fica, porque o Render não importa o núcleo |
| Dono | modulo-robo |

### RD-0138 · O robô confere dado pessoal com 2 regras, e uma delas a web não tem
| Campo | Conteúdo |
|---|---|
| Onde | robô `bap_automation.py:9818-9819`: `_rn.texto_sem_contato(v) != v or _RE_PESSOAL_EDICAO_WEB.search(v)` (o regex vem da T-0021, `:8115`) |
| Tipo | código |
| O que se repete | 2 definições de "dado pessoal no texto". O contrato §10.9.1, item 3 (1089-1093): "o texto é recusado se `texto_sem_contato(v) != v` … O robô chama o próprio `texto_sem_contato`, sem cópia". A web trocou o regex velho pelo bloco `padroes-pessoais`, e o robô ficou com os 2. Eles divergem: o `@` solto do regex velho recusa no PC um texto que a web aceitou |
| Impacto | decisão e cliques: o admin vê "O PC recusou" num texto que a web deixou passar |
| Severidade | média |
| Proposta | **Depois:** `if _rn.texto_sem_contato(v) != v: return motivo_texto_web(teto)`. Sai o `_RE_PESSOAL_EDICAO_WEB` (era o último uso). O caso da T-0021 ("FULANO" + CPF) segue recusado, pelo `_DOC_MEIO` do núcleo |
| Dono | modulo-robo |

### RD-0139 · A regra da garantia nova e do prazo padrão foi copiada da janela do PC
| Campo | Conteúdo |
|---|---|
| Onde | `bap_relatorios.py` (`DialogoGarantia`): `:4330`, `:4418` (`_prazo_padrao`), `:4457` e `:4476`; núcleo `relatorios_nucleo.py:1837` (`edicao_garantia`); robô `bap_automation.py:9870-9873` (`plano_garantia_web`), `:9889-9890`, `:9916` (`_padrao`) e `:9692` (`_gravar_garantia_pc`) |
| Tipo | código |
| O que se repete | (1) Os padrões da garantia nova `{"status": "ABERTO", "resultado": "PENDENTE"}` e a data de hoje: **3 vezes** (janela do PC, núcleo e robô). (2) `"FAROL DE GARANTIAS"` como origem: 2 vezes (janela e robô). (3) A DT. FECHAMENTO padrão em texto (feriados com `try/except` + `gm.prazo_padrao` + `dd/mm/aaaa`): 2 vezes (`_prazo_padrao` e `_padrao`). (4) RN-POS-005, "o prazo igual ao padrão fica em branco": 2 vezes (`salvar` e `plano_garantia_web`). (5) A ordem `renomear` → `gravar`: 2 vezes (`salvar` e `_gravar_garantia_pc`, cuja docstring diz "A MESMA gravação da janela") |
| Impacto | manutenção e decisão: se a regra mudar no PC, a garantia criada pela web nasce diferente da criada no PC |
| Severidade | alta |
| Proposta | **Depois:** a regra fica numa função pura só, no `garantias.py`: ```PADRAO_NOVA = {"status": "ABERTO", "resultado": "PENDENTE"} ORIGEM_FAROL = "FAROL DE GARANTIAS" def prazo_padrao_txt(dt_sol_txt, fer) -> str: d = prazo_padrao(data(dt_sol_txt), fer); return f"{d:%d/%m/%Y}" if d else "" def campos_para_gravar(campos, dt_sol_txt, fer, novo) -> dict: """RN-POS-005: o prazo igual ao padrão fica em branco; a nova leva PADRAO_NOVA e ORIGEM_FAROL.""" ...``` A janela do PC (`salvar` e `_prazo_padrao`), o núcleo (`padroes = {**gm.PADRAO_NOVA, "ticket": ..., "dt_solicitacao": "@hoje"}`) e o robô (`plano_garantia_web` e `_padrao`) chamam essas funções. O teste cita a RN-POS-005 |
| Dono | modulo-posvenda (`garantias.py`), modulo-farois (`bap_relatorios.py` e núcleo) e modulo-robo |

### RD-0140 · O formulário da linha nova copia o campo do formulário da T-0021
| Campo | Conteúdo |
|---|---|
| Onde | web `web/app/main.py:647` (`form_ctx`) × `:674` (`novo_ctx`) |
| Tipo | código |
| O que se repete | O dicionário do campo (`campo`, `rotulo`, `tipo`, `atual`, `atual_iso`, `opcoes`, `min`, `max`, `teto`, `multilinha`) aparece inteiro nos 2, com o `isos = sorted(...)` e as 2 linhas da data livre, iguais caractere por caractere (`:664`/`:686` e as seguintes). O `edicoes._mais_um_ano` é privado, e o `main.py` o chama 2 vezes |
| Impacto | manutenção: a data livre ou o teto mudam num formulário e não no outro |
| Severidade | média |
| Proposta | **Depois:** no `edicoes.py`, `def campo_tela(c: dict, atual: str, ops: list, hoje=None, **extra) -> dict:` monta o dicionário (com `min`/`max` da data livre por `DATA_MIN` e `data_max(hoje)`, esta pública). O `form_ctx` chama `edicoes.campo_tela(c, atual, ops, sugestao=c.get("sugestao", ""), pendente=pend.get(c["campo"]))`, e o `novo_ctx` chama `edicoes.campo_tela(c, atual, ops, sugestao="", pendente=None, padrao=..., mostrado=..., obrigatorio=...)` |
| Dono | modulo-web |

### RD-0141 · O POST da linha nova repete o fim do POST da edição, e as frases de erro aparecem 2 vezes
| Campo | Conteúdo |
|---|---|
| Onde | web `web/app/main.py:705` e `:753` ("Não há linha nova aqui" + "Esta tabela não aceita linha nova. Volte ao farol."); `:745` e `:764` ("Não foi possível gravar agora. Tente de novo."); `:748` e `:767` (`RedirectResponse(volta + ("&" if "?" in volta else "?") + "ed=1", ...)`) |
| Tipo | código · texto |
| O que se repete | 2 frases, 2 vezes cada, e o redirecionamento 2 vezes |
| Impacto | manutenção: o texto da tela muda num lugar e não no outro |
| Severidade | baixa |
| Proposta | **Depois:** no `edicoes.py`, `TITULO_SEM_NOVO = "Não há linha nova aqui"`, `MSG_SEM_NOVO = "Esta tabela não aceita linha nova. Volte ao farol."` e `MSG_FALHA_FILA = "Não foi possível gravar agora. Tente de novo."`. No `main.py`, `def volta_ed(volta): return RedirectResponse(volta + ("&" if "?" in volta else "?") + "ed=1", status_code=303)`, usado nos 2 POST |
| Dono | modulo-web |

### RD-0142 · A troca das quebras de linha está escrita 2 vezes no `edicoes.py`, e o padrão mostrado é lido 2 vezes
| Campo | Conteúdo |
|---|---|
| Onde | web `web/app/edicoes.py:282` (`bruto.replace("\r\n", "\n").replace("\r", "\n")`, a mesma conta do `_norm_texto`); `:389` e `:414` (`str(form.get("p_" + ..., padrao))[:80]`) |
| Tipo | código |
| O que se repete | A troca CRLF/CR → LF, 2 vezes (o `_norm_texto` e a linha do `_checa`). A leitura do padrão mostrado no formulário, 2 vezes no `valores_do_novo` |
| Impacto | manutenção |
| Severidade | baixa |
| Proposta | **Depois:** `:282` `ctrl = _CTRL.search(_norm_texto(bruto).replace("\n", ""))`. No `valores_do_novo`, `def _mostrado(form, c): return str(form.get("p_" + c["campo"], c["padrao_txt"]))[:80]`, usado nas 2 linhas |
| Dono | modulo-web |

### RD-0143 · A tela da linha nova diz "nova" 2 vezes
| Campo | Conteúdo |
|---|---|
| Onde | web `web/app/templates/editar.html:5` (faixa: `acao ~ " · " ~ farol_nome` = "Nova garantia · Farol de Garantias") e `:9` (`<p class="sub">{{ tab }}{% if novo %} · linha nova{% endif %}</p>` = "Garantias · linha nova") |
| Tipo | texto |
| O que se repete | "linha nova" repete o "Nova garantia" da faixa, logo abaixo (2 vezes na mesma tela) |
| Impacto | leitura |
| Severidade | média |
| Proposta | **Antes:** `<p class="sub">{{ tab }}{% if novo %} · linha nova{% endif %}</p>`. **Depois:** `<p class="sub">{{ tab }}</p>` (como na edição da T-0021) |
| Dono | modulo-web |

### RD-0144 · O ticket sugerido aparece 2 vezes no formulário da linha nova
| Campo | Conteúdo |
|---|---|
| Onde | web `web/app/templates/editar.html:41` (`<small>Sugestão do PC: {{ c.padrao }}</small>`), com o campo já preenchido pelo mesmo valor (`novo_ctx`: `atual = c["padrao_txt"]`) |
| Tipo | texto |
| O que se repete | O número do ticket, 2 vezes ao abrir: dentro do campo e na linha "Sugestão do PC" logo abaixo |
| Impacto | leitura |
| Severidade | média |
| Proposta | **Depois:** `{% if novo and c.obrigatorio and c.padrao and c.atual != c.padrao %}<small>Sugestão do PC: {{ c.padrao }}</small>{% endif %}`. A sugestão só aparece quando o admin trocou o número, por exemplo ao voltar com erro |
| Dono | modulo-web |

### RD-0145 · As 9 colunas dos agrupamentos da NCC estão escritas 3 vezes na web
| Campo | Conteúdo |
|---|---|
| Onde | web `web/app/tabelas.py:263-279` (`COLUNAS_RID` de `("pl_ncc", "Por filial")`, `"Por vendedor"` e `"Por supervisor"`) |
| Tipo | código |
| O que se repete | `_c("NCC", "int"), _c("CLIENTES", "int"), _c("0-30 DIAS", "moeda"), … _c("COMPENSAR JÁ", "moeda")`, 3 vezes (só muda a 1ª coluna). O robô já usa uma função só (`_AGRUPA_NCC_WEB`) |
| Impacto | manutenção |
| Severidade | baixa |
| Proposta | **Depois:** `def _agrupa_ncc(nome): return [_c(nome), _c("NCC", "int"), _c("CLIENTES", "int"), _c("0-30 DIAS", "moeda"), _c("31-90 DIAS", "moeda"), _c("91-180 DIAS", "moeda"), _c("+180 DIAS", "moeda"), _c("SALDO", "moeda"), _c("COMPENSAR JÁ", "moeda")]` e `**{("pl_ncc", f"Por {k}"): _agrupa_ncc(k.upper()) for k in ("filial", "vendedor", "supervisor")}` |
| Dono | modulo-web |

### RD-0146 · O corte do "Histórico de compra" copia o corte do "Cliente a cliente"
| Campo | Conteúdo |
|---|---|
| Onde | robô `bap_automation.py:8640` (`_corte_cliente_a_cliente_web`) × `:8648` (`_corte_historico_web`) |
| Tipo | código |
| O que se repete | As mesmas 5 linhas (procura o título, filtra as `tabelas`, chama `_abas_fora_web`), 2 vezes. Só o título muda |
| Impacto | manutenção |
| Severidade | baixa |
| Proposta | **Depois:** ```def _corte_aba_web(titulo: str): """Tira a aba `titulo` do farol, com o aviso das abas fora (10.8.7, 10.10.4).""" def corte(rid: str, rel: dict) -> None: tabs = rel.get("tabelas") if tabs and any(t.get("titulo") == titulo for t in tabs): rel["tabelas"] = [t for t in tabs if t.get("titulo") != titulo] _abas_fora_web(rid, rel, [titulo]) return corte``` e, no `_cortar_farol_web`, `"cliente_a_cliente_fora": _corte_aba_web("Cliente a cliente")` e `"historico_fora": _corte_aba_web("Histórico de compra")` |
| Dono | modulo-robo |

## Redundância útil (não remover)
- **Cópias do lado da web**, porque o Render não importa o código do PC e cada cópia está presa ao contrato: `edicoes.MAX_TEXTO` (60), `MAX_TEXTO_TETO` (600), `REMOVIDO`, `DATA_MIN`, `_mais_um_ano`, `_norm_texto` e os padrões `RE_EMAIL`/`RE_DOC_*`/`RE_FONE`. Os padrões têm teste contra o bloco `padroes-pessoais`.
- **Contato fora em 2 fronteiras:** o robô tem o `_COLUNAS_FORA_TABELA_WEB`, que é preciso para a lista fechada bater, e a web tem o `tabelas.FORA_POR_TABELA`, que recusa o pacote. Na web há também a checagem pelo nome do campo e pela coluna ou rótulo. Por ser dado pessoal (RN-GER-011), a defesa dupla fica.
- **Listas fechadas de colunas e abas** dos 3 faróis no robô (`_COLUNAS_TABELAS_WEB`, `_ABAS_TABELAS_WEB`) e na web (`COLUNAS_RID`, `ABAS`): são as 2 pontas do contrato §10.10.2.
- `manter?`: o robô põe `caixa` de novo no campo `multilinha`, mesmo com o `mantem_caixa` do núcleo. Isso garante a regra da web "multilinha só com caixa".

## Fora do escopo: encaminhar ao `testes`
1. Um ticket de 41 a 60 caracteres é recusado pelo robô com "texto inválido (até 60 caracteres…)": o rótulo contradiz o limite (ligado ao RD-0136).
2. O contrato:1082 diz "max do pacote diferente do número do núcleo = edição recusada, com `MOTIVO_TEXTO_WEB`". O código (`edicao_web`, `:8189`) levanta `ValueError`, e aí a edição nem vai à web.
3. Os PRs do núcleo e do robô não têm teste novo para a RN-GER-002 (`pct_do_liquido`), a RN-GER-007 (`_uteis_ate_ontem`), o `edicao_garantia`, o `plano_garantia_web` e o `validar_edicao_web` com `novo` (regra 2 do CLAUDE.md).
4. O "% do faturado" do Farol de Fretes (`fretes`, `:8033`) ainda divide pelo faturado bruto (`_pedidos(ctx, "VND")`). É o mesmo rótulo com outra base, o que pode contrariar a RN-GER-002. Não é da T-0023.

## Para liberar
Os 16 achados fechados, com reteste nos novos head SHAs: o diff de cada trecho (antes → depois) e, nos RD-0143 e RD-0144, o print do formulário "Nova garantia".

---

# Reteste 1 · heads novos (corretor-redundancias, 27/11/2026)

- **Heads revisados:** núcleo `f0af112`, robô `371e04c` e web `928b3ea`, todos contra o `origin/main` `30ae65d`. Conferi com `git diff <head antigo> <head novo>` e com o arquivo inteiro de cada head.
- **Resultado:** **não libera.**
  - Fecharam 12 dos 16 achados.
  - Ficam 4 com resto em aberto: RD-0135, RD-0136, RD-0139 e RD-0146.
  - A correção trouxe 3 repetições novas, todas baixas: RD-0151 a RD-0153.
- **Numeração:** o maior RD usado nos anexos era o RD-0150, então os novos começam no RD-0151.

## Os 16 achados

| ID | Situação | Evidência no head |
|---|---|---|
| RD-0131 | fechado | `git diff origin/modulo-farois/T-0023-nucleo origin/modulo-robo/T-0023-robo -- relatorios_nucleo.py painel_farol.py` = vazio (o robô fez o merge do núcleo `f0af112` em `c5e610f`) |
| RD-0132 | fechado | o `_eventos_faturamento` chama o `_liquido`; a regra VND − DEV tem uma função só |
| RD-0133 | fechado | `pd_ = pct_do_liquido(...)` uma vez por cartão, em `devolucoes` e em `_abas_do_painel` |
| RD-0134 | fechado | o `"garantias"` saiu do `CAMPOS_EDICAO_WEB`; `_campos_garantia_web()` traduz o `CAMPOS_EDICAO_GARANTIA` do núcleo |
| RD-0135 | **resto em aberto** | abaixo (o `__getattr__`) |
| RD-0136 | **resto em aberto** | abaixo |
| RD-0137 | fechado | sai o `REMOVIDO_WEB`; o robô usa o `_rn.REMOVIDO` |
| RD-0138 | fechado | sai o `_RE_PESSOAL_EDICAO_WEB`; fica só o `_rn.texto_sem_contato(v) != v` |
| RD-0139 | **resto em aberto** | abaixo |
| RD-0140 | fechado | `edicoes.campo_tela` é usado pelo `form_ctx` e pelo `novo_ctx`; o `data_max` é público, e o `main.py` não chama mais o `_mais_um_ano` |
| RD-0141 | fechado | `edicoes.TITULO_SEM_NOVO`, `MSG_SEM_NOVO`, `MSG_FALHA_FILA` e `volta_ed(volta)` nos 2 POST |
| RD-0142 | fechado | `_CTRL.search(_norm_texto(bruto).replace("\n", ""))` e `edicoes.mostrado(form, c)` nos 2 usos |
| RD-0143 | fechado | `editar.html:9` = `<p class="sub">{{ tab }}</p>` |
| RD-0144 | fechado | `editar.html`: a "Sugestão do PC" só aparece com `c.atual != c.padrao` |
| RD-0145 | fechado | `tabelas._agrupa_ncc(nome)` monta os 3 agrupamentos |
| RD-0146 | **em aberto** | sem mudança: `_corte_cliente_a_cliente_web` (`bap_automation.py:8644`) e `_corte_historico_web` (`:8652`) seguem com as mesmas 5 linhas |

### RD-0135 (resto) · O `__getattr__` mantém 2 nomes para a mesma frase
- **Onde:** robô `bap_automation.py:9652-9655`:
  ```python
  def __getattr__(nome):
      if nome == "MOTIVO_TEXTO_WEB":
          return motivo_texto_web()
      raise AttributeError(nome)
  ```
- **O que mudou:** o 60 duplicado saiu (o `MAX_TEXTO_WEB` não existe mais, e o padrão vem do `_rn.MAX_TEXTO_PADRAO`). A correção trocou a constante por um gancho de módulo (PEP 562) no maior módulo do robô.
- **O que se repete:** a mesma frase continua com 2 nomes, o `motivo_texto_web()` e o `ba.MOTIVO_TEXTO_WEB`.
  - O código do robô não usa mais o `MOTIVO_TEXTO_WEB`. Só o usam as 2 linhas de `tests/test_T0021_edicao_web_robo.py:129-130` e o contrato:1082.
  - O gancho é código que existe só para os testes, e passa a responder por todo atributo que falte no `bap_automation`.
- **Severidade:** média (manutenção).
- **Proposta:**
  - O robô tira o `__getattr__`.
  - O `testes` troca as 2 linhas por `ba.motivo_texto_web()`.
  - O `engenheiro-software` troca, no contrato:1082, o "com `MOTIVO_TEXTO_WEB`" por "com `motivo_texto_web(teto)`".
  - Os 3 vão no mesmo lote.
- **Donos:** modulo-robo, testes (o arquivo de teste) e engenheiro-software (o contrato).

### RD-0136 (resto) · O 40 do ticket segue no regex do robô
- **Onde:** robô `bap_automation.py:9661`, `_RE_TICKET_WEB = re.compile(r"^[\w.\-/ ]{1,40}$")`.
- **O que fechou:**
  - O núcleo tem o `MAX_TEXTO_EDICAO[("garantias", "ticket")] = 40` e manda o `max` ao pacote.
  - O robô confere o `len(v) > teto` com o teto do núcleo.
- **O que se repete:** o 40 ainda aparece 2 vezes, no núcleo e no `{1,40}` do regex. O regex recusa antes, com outra frase (`MOTIVO_VALOR_WEB`), se o núcleo subir o teto.
- **Severidade:** média.
- **Proposta:** **Depois:** `_RE_TICKET_WEB = re.compile(r"^[\w.\-/ ]+$")`. O tamanho fica só com o `len(v) > teto`.
- **Dono:** modulo-robo.

### RD-0139 (resto) · A janela do PC ainda tem a própria cópia da regra da garantia nova
- **Onde:** `bap_relatorios.py` no head do núcleo (`f0af112`, sem mudança):
  - `:4330`: `padrao = {"status": "ABERTO", "resultado": "PENDENTE", ...}`;
  - `:4418`: `_prazo_padrao` (feriados com `try/except` + `gm.prazo_padrao` + `dd/mm/aaaa`);
  - `:4457-4459`: o prazo igual ao padrão fica em branco;
  - `:4476`: `campos["origem"] = "FAROL DE GARANTIAS"`.
- **O que fechou:**
  - O núcleo tem a regra numa função pura só: `PADRAO_NOVA_GARANTIA`, `ORIGEM_GARANTIA_FAROL`, `prazo_padrao_txt` e `campos_garantia_a_gravar`.
  - O `edicao_garantia` e o robô (`plano_garantia_web`) usam essas funções.
  - O `_padrao` do robô saiu.
- **O que se repete:** de 3 cópias, ficaram 2: o núcleo e a janela do PC. Uma mudança na regra ainda pode valer na web e não no PC. A leitura dos feriados com `try/except` também aparece 2 vezes (`_prazo_padrao` da janela e `aplicar_edicao_web` do robô).
- **Severidade:** alta (é a mesma regra de negócio, a RN-POS-005).
- **Proposta (**depois**, no `DialogoGarantia`):**
  - `:4330` vira `padrao = {**rn.PADRAO_NOVA_GARANTIA, "ticket": self.ticket}.get(campo, "")`;
  - o `_prazo_padrao` vira `return rn.prazo_padrao_txt(dt_sol, fer)`;
  - no `salvar`, o bloco `:4457-4459` e a linha `:4476` dão lugar a `campos = rn.campos_garantia_a_gravar(campos, fer, novo=self.novo)`.
- **Dono:** modulo-farois (`bap_relatorios.py` é dele, como o núcleo).

## Repetição nova trazida pela correção

### RD-0151 · O mesmo módulo é importado 2 vezes, com 2 nomes, na mesma função
| Campo | Conteúdo |
|---|---|
| Onde | robô `bap_automation.py`: `plano_garantia_web`, `:9881` (`import relatorios_nucleo as _rn`) e `:9897` (`import relatorios_nucleo as _rn2`), ambos novos nesta correção; `edicao_web`, `:8152` (`_rn`, no ramo `autorizacoes`) e `:8170` (`_rn2`) |
| Tipo | código |
| O que se repete | 2 nomes para o mesmo módulo na mesma função, 2 vezes |
| Impacto | manutenção (leitura) |
| Severidade | baixa |
| Proposta | **Depois:** um só `import relatorios_nucleo as _rn  # noqa: PLC0415` no começo de cada função, e `_rn2.` vira `_rn.` |
| Dono | modulo-robo |

### RD-0152 · O "código - nome → nome" está escrito 2 vezes na web
| Campo | Conteúdo |
|---|---|
| Onde | web `web/app/main.py`, `resumo_da_linha` (novo: `m = tabelas._RE_COD_NOME.match(v); v = m.group(2) if m else v`) × `web/app/tabelas.py:1272`, `cliente_so_nome` (`m = _RE_COD_NOME.match(...)`, `m.group(2)`) |
| Tipo | código |
| O que se repete | a separação código/nome, 2 vezes; o `main.py` usa o `_RE_COD_NOME`, que é privado do `tabelas.py` |
| Impacto | manutenção |
| Severidade | baixa |
| Proposta | **Depois:** no `tabelas.py`, `def cod_e_nome(v: str) -> tuple[str, str]: m = _RE_COD_NOME.match(str(v)); return (m.group(1), m.group(2)) if m else ("", str(v))`, usado pelo `cliente_so_nome` e pelo `resumo_da_linha` (`v = tabelas.cod_e_nome(v)[1]`) |
| Dono | modulo-web |

### RD-0153 · A regra `.ed-botoes` aparece 2 vezes no CSS
| Campo | Conteúdo |
|---|---|
| Onde | web `web/app/static/estilo.css:357` (`.ed-botoes{display:flex;gap:1rem;align-items:center;margin:1rem 0 .4rem}`) × `:667` (`.ed-botoes{display:flex;gap:.6rem;align-items:center;margin-top:.8rem}`), esta nova |
| Tipo | código |
| O que se repete | o seletor e 2 propriedades (`display`, `align-items`), 2 vezes; a 2ª muda o `gap` e o `margin-top`, e o `margin-bottom` fica com a 1ª |
| Impacto | manutenção: o espaço dos botões depende da ordem das 2 regras |
| Severidade | baixa |
| Proposta | **Depois:** só uma regra, na linha 357: `.ed-botoes{display:flex;gap:.6rem;align-items:center;margin:.8rem 0 .4rem}`, e sai a da linha 667 |
| Dono | modulo-web |

## Para liberar (reteste 2)
- Fechar os restos dos RD-0135, RD-0136 e RD-0139, o RD-0146 inteiro e os novos RD-0151 a RD-0153.
- O RD-0135 depende de 3 donos no mesmo lote: o robô, o `testes` e o `engenheiro-software`.
- Ordem do merge: a mesma do parecer anterior (o núcleo, depois o robô, depois a web).
