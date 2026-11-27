# T-0045 · Redundâncias no código (corretor-redundancias)

- **Escopo:** `origin/modulo-rota/T-0045-visitas-nucleo` @ **274d23a** (só o `visitas_nucleo.py`, +251 linhas) e `origin/modulo-web/T-0045-visitas` @ **8d7368f** (11 arquivos, +1716/−9), contra o `origin/main` @ 3a453d1. Leitura só por `git show`/`git diff`, sem trocar de branch.
- **Numeração:** o último RD nos anexos era o RD-0109. Este parecer usa do **RD-0110 ao RD-0122**.
- **Contexto que pesa em tudo:** o site sobe com `rootDir: web` (`render.yaml`), então o `web/app` não importa o `visitas_nucleo` da raiz. Uma cópia da regra no site é **forçada pelo deploy**. O problema não é ela existir: é não haver uma fonte da verdade declarada, nem um teste que prenda as duas cópias juntas. Hoje elas já dão resultados diferentes (RD-0110).
- **Tela:** os achados RD-0121 e RD-0122 saem do `visitas.html` e do `visitas.py`, e os prints da simulação no mesmo SHA confirmam os dois (`ux/antes-1-admin-agenda-desligada-pc.png` e `ux/antes-3-pausa-por-codigo-pc.png`). Não há print do teto do dia. [SUPOSIÇÃO] O item 4 do RD-0121 vem só do template.

---

### RD-0110 · `juntar_baixado`, `dia_fechado` e a leitura da hora em Manaus escritos 2 vezes (núcleo × site), e com resultado diferente no empate
| Campo | Conteúdo |
|---|---|
| Onde | `visitas_nucleo.py:1421` `_quando_manaus`, `:1437` `juntar_baixado`, `:1465` `dia_fechado_no_indice` × `web/app/visitas.py:123` `_dt`, `:161` `dia_fechado`, `:167` `juntar_baixado` |
| Tipo | código (regra de negócio RN-VIS-002 repetida) |
| O que se repete | a mesma regra em 2 funções, com 2 assinaturas e 2 resultados. **1. Empate:** no núcleo, `if p is None or (n is not None and n >= p)` (o empate fica com a **nuvem**). No site, `n > p` e a docstring diz "empate: o PC". **2. Forma:** no núcleo, `juntar_baixado(nuvem: {dia: …}, pc: {dia: …}) -> {dia: …}`, e `erros_vendedor`/`refeito` só aparecem com `origem: "nuvem"`. No site, a função recebe um dia por vez (`nuvem: dict, pc: str`) e sempre devolve `erros_vendedor: 0, refeito: False` para o PC. **3.** `_dt` e `_quando_manaus` fazem a mesma leitura (ISO; sem fuso = Manaus). **4.** "fechado = `baixado.date() > d`" aparece 2 vezes (núcleo:1468, site:164). |
| Impacto | decisão. No contrato §4.4, item 3, a importação faz `anotar_baixado` com o `baixado_em` **da nuvem**, e o `fechados_pc` (§4.3) devolve essa mesma hora ao site. Ou seja, o empate é o **caso comum** depois da importação. No site, o dia vira `origem: "pc"` com `erros_vendedor: 0`, e a regra 8 do `deve_rodar` (a retentativa, RN-VIS-006) deixa de ver o dia com erro. Manutenção: quem corrigir um lado não vê o outro. |
| Severidade | **alta** (confunde: os 2 lados não dão o mesmo índice, e a ADR §5.2 manda "o PC e o site usam o mesmo resultado") |
| Proposta | 1. **Fonte da verdade:** `visitas_nucleo.juntar_baixado` e `dia_fechado_no_indice`. 2. **No site, a cópia fica igual à fonte**, com a mesma assinatura e a mesma regra. `web/app/visitas.py:167`, **depois:**<br>`def juntar_baixado(nuvem: dict | None, pc: dict | None) -> dict:`<br>`    """RN-VIS-002. Espelho de visitas_nucleo.juntar_baixado (o site sobe com rootDir web e não importa a raiz); test_RN_VIS_002_site_igual_ao_pc prende os dois."""`<br>com `n >= p` (empate = nuvem) e com `erros_vendedor`/`refeito` só na origem nuvem. O `_dt` passa a ser o espelho do `_quando_manaus`, com a mesma docstring de espelho. 3. **Um teste só para a regra:** `tests/test_T0045_paridade_visitas.py::test_RN_VIS_002_site_igual_ao_pc`. Ele importa os 2 módulos e roda a mesma tabela: nuvem maior, PC maior, empate, só um lado, hora sem fuso, hora inválida, baixado no próprio dia e baixado no dia seguinte. O `test_RN_VIS_002_juntar_baixado_a_maior_hora_e_dia_fechado` do site (`web/tests/test_T0045_visitas.py:116`) sai, porque repete os casos da tabela. Fica só o teste do uso (índice no `/trabalho`). |
| Dono | modulo-web (site) · modulo-rota (fonte) · testes (teste de paridade em `tests/`) |

### RD-0111 · "Dia fechado" em 3 funções e "quais dias baixar" em 2 (main × núcleo)
| Campo | Conteúdo |
|---|---|
| Onde | main: `visitas_nucleo.py:149` `dia_fechado(raiz, d)`, `:158` `mes_fechado` e `visitas_maxima.py:306-313` `plano`. Núcleo: `:1465` `dia_fechado_no_indice` e `:1472` `dias_a_baixar` |
| Tipo | código |
| O que se repete | `bool(quando and quando.date() > d)` em `dia_fechado` (main) e em `dia_fechado_no_indice` (núcleo). `ate = min(ate, hoje)` + `[d for d in dias_entre(de, ate) if refazer or not <fechado>(d)]` no `plano` (main:308-311) e no `dias_a_baixar` (núcleo:1477-1480). A ADR 0004 (tabela do §9, linha 3) diz que o `dias_a_baixar` "sai do `visitas_maxima.plano` e do `dia_fechado`". Mas o `plano` continua com a cópia dele. |
| Impacto | manutenção: o robô do PC e a nuvem escolhem os dias por 2 códigos. Mudar a regra de fechamento (fuso, hoje) exige mexer em 2 lugares. |
| Severidade | média |
| Proposta | No `visitas_nucleo.py`, uma função nova e o `dia_fechado` delegando:<br>`def indice_do_pc(raiz, de: date, ate: date) -> dict:`<br>`    """{AAAAMMDD: baixado_em} dos dias com arquivo no PC (arquivo posto à mão vale pela data do arquivo)."""`<br>`    out = {}`<br>`    for d in dias_entre(de, ate):`<br>`        arq = arquivo_do_dia(raiz, d)`<br>`        q = baixado_em(raiz, f"{d:%Y%m%d}", arq) if arq.exists() else None`<br>`        if q: out[f"{d:%Y%m%d}"] = q`<br>`    return out`<br><br>`def dia_fechado(raiz, d: date) -> bool:`<br>`    return dia_fechado_no_indice(indice_do_pc(raiz, d, d), d)`<br><br>No `visitas_maxima.plano` (modulo-robo), **antes:** `ate = min(ate, hoje)` + `dias = [d for d in vn.dias_entre(de, ate) if refazer or not vn.dia_fechado(raiz, d)]` → **depois:** `dias = vn.dias_a_baixar(vn.indice_do_pc(raiz, de, ate), de, ate, hoje, refazer)`. Os meses continuam iguais, mas com `ate = min(ate, hoje)` mantido para eles. O mesmo `indice_do_pc(raiz, hoje - 40, hoje)` é o `fechados_pc` do contrato §4.3. Assim, o `sincronizar_visitas_web` não ganha um 3º montador de índice. |
| Dono | modulo-rota (`visitas_nucleo.py`) · modulo-robo (`visitas_maxima.plano`) |

### RD-0112 · `ESPELHO_PERMITIDAS` copia as tabelas do `ler_espelho`, e o site tem a 3ª lista (`COLUNAS_PROIBIDAS`)
| Campo | Conteúdo |
|---|---|
| Onde | núcleo `:1483-1496` × main `visitas_nucleo.py:677` `_ROTULOS_ESPELHO` e `:692` `_COLUNAS_ESPELHO` × site `web/app/visitas.py:104` `COLUNAS_PROIBIDAS` |
| Tipo | código |
| O que se repete | `"cabecalho"`: os **19 de 19** rótulos de `_ROTULOS_ESPELHO`, na mesma ordem, escritos de novo. `"colunas"`: **15 das 18** chaves de `_COLUNAS_ESPELHO`. As 3 que faltam (`KM DIST`, `BONIF`, `OBSERVACAO`) estão escritas de novo no site, como `COLUNAS_PROIBIDAS`. O contrato §3.6 pede "usa as mesmas tabelas `_ROTULOS_ESPELHO` e `_COLUNAS_ESPELHO` do `ler_espelho`, **sem cópia**". |
| Impacto | manutenção: uma coluna nova no `ler_espelho` não entra na lista, e o teste de igualdade do §3.6 só pega isso tarde. |
| Severidade | média |
| Proposta | `visitas_nucleo.py:1483`, **depois:**<br>`_FORA_DO_ESPELHO = ("KM DIST", "BONIF", "OBSERVACAO")      # contrato 3.6: nunca saem do contêiner`<br>`ESPELHO_PERMITIDAS = {`<br>`    "cabecalho": tuple(_ROTULOS_ESPELHO),`<br>`    "colunas": tuple(c for c in _COLUNAS_ESPELHO if c not in _FORA_DO_ESPELHO),`<br>`}`<br>O teste que compara com a tabela do contrato continua (por conjunto). No site, o `COLUNAS_PROIBIDAS` fica (é o rootDir), com o comentário "espelho de `visitas_nucleo._FORA_DO_ESPELHO`", e entra no teste de paridade do RD-0110: `set(visitas.COLUNAS_PROIBIDAS) == set(vn._FORA_DO_ESPELHO)`. |
| Dono | modulo-rota · modulo-web (comentário) · testes |

### RD-0113 · `filtrar_espelho` reescreve o laço de leitura do `ler_espelho`
| Campo | Conteúdo |
|---|---|
| Onde | núcleo `:1560-1657` × main `visitas_nucleo.py:741-800` |
| Tipo | código |
| O que se repete | 1. A detecção da linha de títulos `"DATA" in rot and "CLIENTE" in rot and "CODIGO" in rot` (main:762, núcleo:1605). 2. O passeio do cabeçalho: "termina em `:`" → `_rotulo(txt[:-1])` → `chave == p or chave.startswith(p + " ")` → o laço `while j < len(cel) and not _texto(cel[j][1]).endswith(":")` (main:776-790, núcleo:1630-1651). 3. O `try: from xlsx_rapido import load_workbook / except: from openpyxl …` (main:744-747, núcleo:1568-1571). Total: 2 parsers do mesmo Excel. |
| Impacto | manutenção e risco: se a Máxima mudar o layout, a correção tem de ser feita nos 2. O teste de igualdade do §3.6 (`ler_espelho(destino) == ler_espelho(origem)`) depende de os 2 lerem igual. |
| Severidade | média |
| Proposta | Um gerador só, usado pelos 2:<br>`def _percorrer_espelho(ws):`<br>`    """Uma aba do Espelho: ("titulos", ri, cel) · ("linha", ri, cel, colunas) · ("rotulo", ri, k, chave, vals) · ("solto", ri, i, v)."""`<br>O `ler_espelho` monta `cab`/`linhas` a partir dele, e o `filtrar_espelho` copia ou descarta a partir dele. O `load_workbook` com o fallback vira `_abrir_excel(caminho)`, chamado nos 2. |
| Dono | modulo-rota |

### RD-0114 · A rede de dado pessoal escrita de novo no site, e os tipos de achado em 2 listas
| Campo | Conteúdo |
|---|---|
| Onde | núcleo `:1513-1516` (`_RX_EMAIL`, `_RX_CNPJ`, `_RX_CPF`, `_RX_FONE`) e `:1530` `achar_dado_pessoal` × site `web/app/visitas.py:96-102` `RE_PESSOAL` ("a mesma rede do cron (contrato §3.6), repetida aqui") e `:87` `TIPOS_ACHADO` |
| Tipo | código |
| O que se repete | os 4 regex, iguais no efeito e diferentes no texto: no e-mail, `(\.[\w-]+)+` no núcleo e `(?:\.[\w-]+)+` no site. Os 5 tipos (`cnpj`, `cpf`, `telefone`, `email`, `formato`) aparecem na docstring do `achar_dado_pessoal` e no `TIPOS_ACHADO`. |
| Impacto | manutenção: se o contrato §3.6 apertar um regex, só um lado acompanha. |
| Severidade | média |
| Proposta | A **segunda guarda** do site fica: é redundância útil (lote com dado pessoal não é gravado). Só o texto dos regex vira espelho declarado. 1. No site, `RE_PESSOAL` com o texto do núcleo, caractere a caractere (o e-mail com `(\.[\w-]+)+`), e o comentário "espelho de `visitas_nucleo._RX_*` (rootDir web)". 2. No núcleo, `TIPOS_ACHADO = ("cnpj", "cpf", "telefone", "email", "formato")` como constante, usada no laço do `achar_dado_pessoal` e citada na docstring. 3. No teste de paridade do RD-0110: `{t: r.pattern for t, r in visitas.RE_PESSOAL.items()} == {"email": vn._RX_EMAIL.pattern, …}` e `visitas.TIPOS_ACHADO == vn.TIPOS_ACHADO`. |
| Dono | modulo-web · modulo-rota · testes |

### RD-0115 · Dentro do `visitas.py`, o mesmo cálculo 2 ou 3 vezes
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/visitas.py` |
| Tipo | código |
| O que se repete | 1. **O índice juntado**, 2 vezes: `trabalho` (466-470, laço) e `tela` (862, compreensão), as 2 com `juntar_baixado(e["indice"].get(d), e["pc"].get(d))` sobre `set(e["indice"]) | set(e["pc"])`. 2. **Os lotes pendentes**, 2 vezes: `tela` (861) e `saude` (893), as 2 com `x["status"] == "pendente"` sobre `self.fila.itens()`. 3. **O diagnóstico pendente** `{"estado": "pendente", "em": None, "codigo": None}`, 3 vezes: 108, 806 e 814. 4. **O caminho do corpo do lote** `self.pasta / "lotes" / f"{seq}.json.gz"`, 3 vezes: 616/625, 703 e 743. 5. **O corte de 40 dias** `dia_ymd(agora_ - timedelta(days=FECHADOS_PC_DIAS))`, 2 vezes: 382 e 729. 6. **O `_tentativa`** (408-411) recebe `agora_` e lê `t` sem usar. |
| Impacto | manutenção |
| Severidade | média |
| Proposta | 1. Com o RD-0110, o índice sai numa chamada só: `indice = juntar_baixado(e["indice"], e["pc"])`, em `trabalho` e em `tela`. 2. `def _pendentes(self): return [x for x in self.fila.itens() if x["status"] == "pendente"]`, usado em `tela` e em `saude` (`len(self._pendentes())`). 3. `_DIAG_PENDENTE = {"estado": "pendente", "em": None, "codigo": None}`, e `dict(_DIAG_PENDENTE)` nos 3 lugares. 4. `def _arq_lote(self, seq): return self.pasta / "lotes" / f"{seq}.json.gz"`. 5. `def _corte(agora_): return dia_ymd(agora_ - timedelta(days=FECHADOS_PC_DIAS))`. 6. `_tentativa(self, e, motivo)`, sem `agora_` e sem `t`. |
| Dono | modulo-web |

### RD-0116 · O `visitas.py` reimplementa o que o site já tem
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/visitas.py` × main `web/app/edicoes.py`, `pacotes.py`, `arquivos.py`, `cobranca.py` |
| Tipo | código |
| O que se repete | 1. `agora()` (visitas:115) = `edicoes.agora` (edicoes:61), com o mesmo corpo. O `visitas.py` já importa `MANAUS`, `ErroEdicao` e `Fila` do `edicoes`. 2. `_int` (visitas:144) = `edicoes._int` (edicoes:65), igual. 3. `_gravar_corpo` (visitas:614-631: tmp + fsync + chmod 600 + replace) = `pacotes._gravar_bytes` (pacotes:495) e o mesmo molde do `arquivos.gravar_json`. 4. `descomprimir` (visitas:305, gzip com teto contra bomba) = `pacotes.descomprimir` (pacotes:511). 5. `_acrescentar` (visitas:391, jsonl + fsync) = `Fila._acrescentar` (edicoes:314) e o `Diario` da cobrança (cobranca:470). |
| Impacto | manutenção. A trava da bomba de gzip e a gravação atômica são guardas de segurança: uma correção num lugar não chega ao outro. |
| Severidade | média |
| Proposta | 1 e 2. `from .edicoes import MANAUS, ErroEdicao, Fila, agora, _int`. As 2 definições locais saem. 3. `pacotes._gravar_bytes` vira `arquivos.gravar_bytes(caminho, dados)`, usado por `pacotes` e por `visitas._gravar_corpo` (que fica com uma linha). 4. `arquivos.descomprimir_com_teto(bruto, maximo) -> bytes | None` (None = inválido ou grande). O `pacotes.descomprimir` traduz o None no `ErroPacote` dele, e o `visitas.descomprimir` sai. 5. `arquivos.acrescentar_linha(caminho, reg)` (abre, escreve, flush, fsync), usado por `Fila._acrescentar` e por `Visitas._acrescentar`. A troca no `cobranca.Diario` pode ficar para o lote seguinte. |
| Dono | modulo-web |

### RD-0117 · `edicoes.Fila`: o `registrar_item` copia o `registrar`, o `itens` copia o `desde`, e o `epoca_atual` não tem quem chame
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/edicoes.py` na branch web: `registrar` (323-334) × `registrar_item` (336-348); `desde` (362-370) × `itens` (350-355); `epoca_atual` (357-359) |
| Tipo | código |
| O que se repete | 1. O `quando` (`(agora_ or agora()).astimezone(MANAUS).strftime("%Y-%m-%d %H:%M:%S")`), o `ultimo_seq += 1`, o `gravar_json(estado)` e o `_acrescentar`: 2 cópias. O mesmo `strftime` aparece 3 vezes (com o `confirmar`). 2. `dict(r, status=(st.get(r["seq"]) or {}).get("status", "pendente"))`: no `desde` e no `itens`. 3. `epoca_atual`: `git grep` na branch não acha nenhuma chamada. |
| Impacto | manutenção. O contrato §4.1 pede a `Fila` "parametrizada, não uma cópia", e hoje há uma cópia dentro dela. |
| Severidade | média |
| Proposta | 1. O `registrar` passa a chamar o genérico:<br>`return self.registrar_item({"id": str(uuid.uuid4()), "usuario": usuario, "rid": rid, "tabela": tabela, "modulo": modulo, "chave": chave, "valores": valores, "antes": antes}, agora_=agora_)`<br>`def _quando(agora_=None) -> str` serve aos 3. 2. `def _com_status(eds, st)` monta a lista, e `desde` e `itens` usam. 3. O `epoca_atual` sai. |
| Dono | modulo-web |

### RD-0118 · `main.py`: o token do cron é uma cópia do `sem_token`, e o corpo é lido com teto mais 2 vezes
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/main.py` na branch web: `sem_token` (843-850) × `sem_token_cron` (907-914); `corpo_json` (916-925) e o laço do `api_visitas_lote` (961-964); as 5 rotas `api_visitas_*` com `except visitas.ErroVisitas as e: return JSONResponse(e.corpo, status_code=e.status)` |
| Tipo | código |
| O que se repete | 1. Bearer + `hmac.compare_digest` + 401 `WWW-Authenticate`: 2 funções iguais, que só mudam no `esperado` (`cfg.token` × `vis.token`). 2. O laço `async for parte in request.stream()` com teto: o arquivo já tinha 4 (`formulario`, `api_pacote`, `api_pacote_farol`, `api_pacote_fechar`) e passa a ter 6. 3. O mesmo `try/except` em 5 rotas. |
| Impacto | manutenção (a checagem de token é guarda de segurança) |
| Severidade | média |
| Proposta | 1. `def _bearer(request, esperado)`, com o corpo atual do `sem_token`. Depois, `sem_token = lambda r: _bearer(r, cfg.token)` e `sem_token_cron = lambda r: _bearer(r, vis.token)`. 2. `async def ler_corpo(request, limite) -> bytes | None` (None = passou do teto). O `corpo_json` e o `api_visitas_lote` usam. As 4 rotas antigas podem trocar no lote seguinte. 3. `@app.exception_handler(visitas.ErroVisitas)` devolve `JSONResponse(e.corpo, status_code=e.status)`, e os 5 `try/except` saem. |
| Dono | modulo-web |

### RD-0119 · O dia `AAAAMMDD` é formatado à mão em 6 lugares
| Campo | Conteúdo |
|---|---|
| Onde | `visitas.py:867` (`f"{x['dia'][6:]}/{x['dia'][4:6]}"`), `:848` (`strftime("%d/%m")`, o mesmo formato por outro caminho), `:870` (`de_iso`/`ate_iso` por fatia), `visitas.html:44` (`e.pedido.de[6:]}}/{{ e.pedido.de[4:6]` 2 vezes), `main.py` (`f.get("de", "").replace("-", "")` em `visitas_atualizar` e `visitas_refazer`). O `edicoes.py` do main já tem `br_data` e `iso_de_br`. |
| Tipo | código |
| O que se repete | 2 conversões (`AAAAMMDD → dd/mm` e `AAAAMMDD ↔ AAAA-MM-DD`), escritas 6 vezes |
| Impacto | manutenção |
| Severidade | média |
| Proposta | No `visitas.py`: `def dia_br(ymd: str) -> str: return f"{ymd[6:]}/{ymd[4:6]}"` e `def dia_iso(ymd: str) -> str: return f"{ymd[:4]}-{ymd[4:6]}-{ymd[6:]}"`. Os 2 viram filtros do Jinja (`modelos.env.filters["dia_br"] = visitas.dia_br`), e o template passa a usar `{{ e.pedido.de|dia_br }} a {{ e.pedido.ate|dia_br }}`. O `.replace("-", "")` sai do `main.py` para dentro do `vis.pedir`, que recebe a data do formulário como chega. |
| Dono | modulo-web |

### RD-0120 · Códigos de erro: "Use o Atualizar visitas do PC" escrito 6 vezes, os textos do §5 sem teste e o `PAUSAM` 2 vezes no teste
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/visitas.py:59-86` (`_CONF`, `CODIGOS`, `TETO_DIA_TEXTO`); `web/tests/test_T0045_visitas.py:112` e `:225` |
| Tipo | código · teste |
| O que se repete | 1. "Use o Atualizar visitas do PC" em `_CONF`, `MAXIMA_BLOQUEIO`, `DADO_PESSOAL`, `TELA_MUDOU` e `TETO_DIA_TEXTO`: 5 literais, 6 textos na tela. 2. O `CODIGOS` copia a coluna "Texto no site" do contrato §5, mas o teste (`test_RN_VIS_005_007_…`) só confere o status. O texto pode sair do contrato sem nenhum teste falhar. 3. Os 5 códigos que pausam estão escritos 2 vezes no teste: no `assert set(visitas.PAUSAM) == {…}` (112) e no `parametrize` (225). |
| Impacto | manutenção. Se o nome do botão do PC mudar, a troca é em 5 lugares, e o RD-0079 já tratou 3 nomes para esse mesmo botão. |
| Severidade | baixa (1 e 2) · baixa, só teste (3, não segura o lote) |
| Proposta | 1. `_PC = "Use o Atualizar visitas do PC"`. Depois, `_CONF = f"A Máxima pediu uma confirmação. {_PC}; o admin retoma aqui depois."`, e o mesmo molde nos outros 4. 2. `test_RN_VIS_005_textos_iguais_ao_contrato`: lê a tabela do §5 de `.coord/contratos/visitas-nuvem.md` (a fonte da verdade) e compara com `CODIGOS`, trocando `HHhMM`/`<fase>`/`<coluna>` pelos campos `{h}`/`{f}`/`{c}`. 3. No teste, `PAUSAM_CONTRATO = ("MAXIMA_SENHA", "MAXIMA_CONFIRMACAO", "MAXIMA_CAPTCHA", "MAXIMA_BLOQUEIO", "DADO_PESSOAL")`, usado no `assert` e no `parametrize`. |
| Dono | modulo-web |

### RD-0121 · Tela: o código e a hora da última rodada em 3 lugares, o texto da pausa 2 vezes e o teto 2 vezes (reincidência do RD-0080)
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/templates/visitas.html`: faixa (9-11), faixa de pausa (19-20), "Últimas rodadas" (82-87); `visitas.py:868` `pausa_texto` e `:847` `texto` |
| Tipo | layout · texto |
| O que se repete | 1. **Última rodada, 2 vezes:** a faixa mostra "Última rodada" (hora · dia) e "Código". A 1ª linha da lista (`vz-topo`, em destaque) mostra a mesma hora, o mesmo dia e o mesmo código. O contrato §4.5 (depois do RD-0080) diz "a mais recente em destaque, no topo" e não fala em cartão à parte. 2. **Texto da pausa, 2 vezes:** `pausa_texto` e o `texto` da linha do topo saem do mesmo `texto_do_codigo(codigo)`. Com a tela pausada, a mesma frase ("A Máxima pediu uma confirmação. Use o Atualizar visitas do PC; …") aparece na faixa de pausa e na lista. O código aparece 3 vezes. 3. **3 formatos para a mesma hora:** "HHhMM · dd/mm" na faixa, "dd/mm/aaaa hh:mm" em "Pausado desde" (`|manaus`) e "dd/mm HHhMM" na lista. 4. **Teto, 2 vezes, e um aviso fora da área de alertas:** "Entradas hoje 8 de 8" em vermelho (`"cor": "alerta"`) na faixa, mais a faixa "Limite de hoje" com o texto. |
| Impacto | leitura e espaço acima da dobra (regras 1 e 2). No print `antes-3-pausa-por-codigo-pc.png`, "MAXIMA_CONFIRMACAO" aparece 2 vezes (faixa e lista), a frase "A Máxima pediu uma confirmação. Use o Atualizar visitas do PC; o admin retoma aqui depois." também 2 vezes (alerta e lista), e a hora 06h06 3 vezes, em 3 formatos. No `antes-1-…-pc.png`, "08h36 · 27/11" + "OK" na faixa repetem a 1ª linha da lista. |
| Severidade | média |
| Proposta | 1. Na faixa, saem os itens "Última rodada" e "Código". Ficam `{"rot": "Agenda 06h00", …}` e `{"rot": "Entradas hoje", "valor": v.logins ~ " de " ~ v.logins_max}`, **sem** o `"cor": "alerta"`: o aviso do teto fica só na faixa "Limite de hoje". 2. Na lista, a linha que causou a pausa fica sem o texto, porque ele já está no alerta: `{% if not (e.pausado and loop.first and r.codigo == e.pausado.codigo) %}<span class="vz-texto">{{ r.texto }}</span>{% endif %}`. 3. Um formato só para a hora, o da lista: "Pausado desde {{ e.pausado.desde\|manaus_curto }}", ou um filtro `dia_hora` com "dd/mm HHhMM", usado na pausa e na lista. 4. O teste `test_tela_mostra_o_ultimo_codigo_sem_print_e_o_limite` continua valendo ("8 de 8" e "Limite de hoje"). |
| Dono | modulo-web (com o designer-ux na simulação) |

### RD-0122 · Textos da tela além do problema e da ação, e o título "Atualizar visitas" 3 vezes no topo
| Campo | Conteúdo |
|---|---|
| Onde | `visitas.html:7` (h1 da faixa), `:37` (h2), `:42` (botão) e `:32` (faixa "Baixando agora"); `visitas.py:786`, `:808`, `:816` e `:779` |
| Tipo | texto |
| O que se repete | 1. "Atualizar visitas" no h1 da faixa, no h2 do cartão logo abaixo e no botão: 3 vezes em menos de uma tela. 2. "Baixando agora" + "O site está na Máxima (etapa: …)": a 2ª frase repete a 1ª. 3. O que o sistema faz por trás (regra 3): "Pedido na fila. **A próxima volta do site na Máxima baixa os dias.**", "Diagnóstico pedido. **Roda na próxima volta do site na Máxima.**" e "Retomado. **O diagnóstico volta a rodar.**" (o cartão Admin já mostra "Diagnóstico: pendente"). 4. Linha do diagnóstico no cartão Admin (`visitas.html:67`): "Diagnóstico: **ok** · OK · 25/11/2026 15:46" (print `antes-1`), com o estado e o código dizendo o mesmo. 5. "A nuvem está pausada. O admin precisa retomar antes." é o erro do botão que a tela deixa apertar com a faixa de pausa à vista. |
| Impacto | leitura |
| Severidade | média |
| Proposta | 1. O h2 "Atualizar visitas" (`:37`) sai. O cartão fica com o formulário e o botão. 2. `<b>Baixando agora</b>{% if e.rodada_ativa.fase %}<span>Etapa: {{ e.rodada_ativa.fase }}{% if e.rodada_ativa.total %}, {{ e.rodada_ativa.feitos or 0 }} de {{ e.rodada_ativa.total }}{% endif %}.</span>{% endif %}`. 3. Depois: "Pedido na fila.", "Diagnóstico pedido." e "Retomado.". 4. O código só aparece quando é diferente do estado: `{% if e.diagnostico.codigo and e.diagnostico.codigo != "OK" %} · {{ e.diagnostico.codigo }}{% endif %}`. Assim, o ok fica "Diagnóstico: ok · 25/11/2026 15:46" e a falha fica "Diagnóstico: falhou · MAXIMA_FORA · …". 5. Com a nuvem pausada, o botão fica desabilitado, como já fica com pedido na fila: `{{ ' disabled title="Pausado"'\|safe if e.pedido or e.pausado }}`. A checagem no servidor continua, com o texto "A nuvem está pausada.". |
| Dono | modulo-web |

---

## Redundância útil ou `manter?` (não entra como achado)
- **Segunda guarda no site** (`achar_no_excel` + `COLUNAS_PROIBIDAS`): manter. É defesa em profundidade da RN-VIS-007. Só o texto dos regex e das colunas entra no espelho (RD-0112 e RD-0114).
- **`visitas_nucleo._RX_*` × `relatorios_nucleo._EMAIL`/`_CPF_FMT`/`_CNPJ_FMT`/`_DOC_SOLTO`** `manter?`: o e-mail e os documentos formatados são o mesmo regex. Mas a limpeza (RN-GER-011) e a rede (§3.6) têm papéis opostos: a rede é para o que a limpeza não pegou, e o contrato fixa os regex da rede literalmente. Se usassem o mesmo objeto, um ajuste na limpeza mudaria a rede sem aviso. Sugiro manter separados.
- **`edicoes.RE_PESSOAL` (main:56) × `visitas.RE_PESSOAL`** `manter?`: o nome é o mesmo no mesmo app, mas a cobertura é diferente. O de edições recusa qualquer `@` em texto livre (regra 6) e não pega 11 ou 14 dígitos soltos. Juntar os 2 mudaria o que a edição aceita, e isso é decisão de regra, não de redundância. Fica a sugestão de renomear o de edições para `RE_PESSOAL_TEXTO_LIVRE` quando aquele arquivo for mexido.
- **`FUSO_MANAUS` com fallback no núcleo (:1413-1418)** × o mesmo `try ZoneInfo / except timezone(-4)` dentro do `relatorios_nucleo.hoje_manaus` (main:788-792) e no `atualizar_do_github.py:200`: baixa. A troca só compensa se o `relatorios_nucleo` passar a expor a constante (modulo-farois). Fica como nota.
- **`title="Já há um pedido na fila"` nos 2 botões e a nota "Pedido na fila: …"**: manter. O título explica o botão desabilitado (acessibilidade), e a nota diz o período.
- **`_CONF` com `MAXIMA_CONFIRMACAO` e `MAXIMA_CAPTCHA` com o mesmo texto**: manter, como no parecer do PR #137.
- **`test_T0035…` com `"0.6.0"` literal**: manter. É o teste da versão do `/saude` (limite 3 da regra 11).

## Fora do meu escopo (vai ao `testes` e ao `revisor-codigo`, sem catálogo)
- **RN-VIS-002/006, valor:** com o empate do `fechados_pc` (§4.4, item 3), o `juntar_baixado` do site dá `origem: "pc"` com `erros_vendedor: 0`, e a retentativa do dia com erro de vendedor deixa de disparar depois da importação no PC. Pede um teste com o fluxo lote → confirmar (com `fechados_pc` igual ao `baixado_em` do lote) → `/trabalho` mostrando `erros_vendedor` > 0. A correção está no RD-0110.
- **`dias_a_baixar(…, hoje)` × `plano(hoje=date.today())`:** o `plano` usa a data do sistema, não a de Manaus (regra 4). Isso aparece quando o RD-0111 juntar os 2.
- **Paridade futura com o cron:** a lista de códigos, `FASES`, `NOVA_TENTATIVA` e `TIPOS_ACHADO` vão existir também no `nuvem/visitas/` (sem dono hoje, segundo o `coord.mjs dono`). Quando ele nascer, entra no teste de paridade do RD-0110, em vez de virar a 3ª cópia.

## Resultado
**Não libera.** Os RD-0110 a RD-0122 estão abertos. Só o item 3 do RD-0120 (lista repetida no teste) não segura o lote. O parecer vale para **274d23a** (`modulo-rota/T-0045-visitas-nucleo`) e **8d7368f** (`modulo-web/T-0045-visitas`).

- **Donos:**
  - modulo-web: RD-0110, RD-0112, RD-0114 a RD-0122;
  - modulo-rota: RD-0110 a RD-0114;
  - modulo-robo: RD-0111 (`plano`);
  - testes: o arquivo de paridade dos RD-0110, RD-0112 e RD-0114.
- **Catálogo, recados e diário:** por instrução de quem chamou ("não altere nada"), não atualizei o `docs/redundancias/catalogo.md`, não mandei recado aos donos nem ao gerente-projetos e não escrevi no diário. [SUPOSIÇÃO] Quem chamou leva os achados aos donos.
