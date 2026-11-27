# T-0045 · Reteste das redundâncias no código (corretor-redundancias)

- **Heads retestados:**
  - `modulo-rota/T-0045-visitas-nucleo` @ **c82ce92** (antes 274d23a; só o `visitas_nucleo.py`);
  - `modulo-web/T-0045-visitas` @ **134efc8** (antes 8d7368f);
  - contrato `engenheiro-software/T-0045-contrato-v1-1` @ **3ffcc06**.
- **Leitura:** só por `git show` e `git diff` contra os heads anteriores. As 2 branches trazem também um merge do `main` (T-0033/T-0034), que fica fora deste reteste.
- **Também conferi** `origin/testes/T-0045-testes` @ eb6e145, porque o teste de paridade seria do `testes`.
- **Numeração:** o maior RD nos anexos era o RD-0122. Os achados novos vão do **RD-0123 ao RD-0128**.
- **Tela:** a avaliação vem do `visitas.html` e do `visitas.py` em 134efc8. Os PNGs em `ux/` são do SHA anterior, e não há print novo. [SUPOSIÇÃO] O RD-0125 se confirma no print da tela pausada, quando for refeito.

## 1. Situação dos RD-0110 a RD-0122

| RD | Situação | Evidência no head |
|---|---|---|
| RD-0110 | **parcial** | **Fechado:** a regra ficou igual nos 2 lados. No site, `juntar_baixado(nuvem: dict, pc: dict) -> dict` (visitas.py:194) usa `n >= p` (no empate, vale a nuvem), e `erros_vendedor`/`refeito` só aparecem com origem nuvem. O `_dt` virou espelho declarado do `_quando_manaus`, e o `dia_fechado(dia, baixado_em)` saiu, trocado por `dia_fechado_no_indice`. O teste do fluxo foi criado: `test_RN_VIS_002_importado_pelo_pc_com_a_mesma_hora_mantem_os_erros_da_nuvem`. **Aberto:** o teste de paridade na raiz **não existe** em nenhuma branch da T-0045, nem na `testes/T-0045-testes`. Mesmo assim, 3 lugares dizem que ele prende os 2 lados: a docstring do módulo (visitas.py:11), a docstring do teste (web/tests:584) e o contrato §3.1 (3ffcc06:101). Hoje a mesma regra tem 2 tabelas de teste diferentes, `tests/test_T0045_visitas_nucleo.py` (testes, eb6e145:24-50) e `test_RN_VIS_002_espelho_juntar_baixado_empate_e_dia_fechado` (web/tests:119), e nenhuma delas roda os 2 módulos. **Falta** o `tests/test_T0045_paridade_visitas.py`, do `testes`: uma tabela só, rodada em `visitas_nucleo` e em `web/app/visitas`. Com ele no ar, os casos de regra do teste da web (web/tests:119-133) saem, e fica só o teste do uso. |
| RD-0111 | **parcial** | **Fechado:** o `dia_fechado(raiz, d)` delega a regra ao `dia_fechado_no_indice` (c82ce92:149-157). **Aberto:** o `visitas_maxima.plano` (c82ce92:306-313, modulo-robo) continua com o filtro próprio (`ate = min(ate, hoje)` + `refazer or not vn.dia_fechado(...)`). Também não existe o `indice_do_pc`. Contando o espelho do site (visitas.py:224), o filtro "dias a baixar" está em 3 lugares, e o do `plano` é o único que não está declarado como espelho. **Falta:** `plano` → `vn.dias_a_baixar(vn.indice_do_pc(raiz, de, ate), de, ate, hoje, refazer)` (modulo-rota cria `indice_do_pc`, modulo-robo troca o `plano`). |
| RD-0112 | **parcial** | **Fechado no núcleo:** `ESPELHO_PERMITIDAS` sai das tabelas do `ler_espelho` (`tuple(_ROTULOS_ESPELHO)` e o filtro por `_COLUNAS_FORA_DA_NUVEM`, c82ce92:1503-1508). **Aberto:** a docstring do site aponta para `_FORA_DO_ESPELHO` (visitas.py:10), nome que não existe no núcleo. O nome certo é `_COLUNAS_FORA_DA_NUVEM`. A lista também está escrita mais 2 vezes: em `COLUNAS_PROIBIDAS` (visitas.py:105) e literal no teste da web (web/tests:587). Sem o teste de paridade, nada prende as 3 cópias. **Falta:** corrigir o nome na docstring e pôr `set(visitas.COLUNAS_PROIBIDAS) == set(vn._COLUNAS_FORA_DA_NUVEM)` no teste de paridade. O literal do web/tests:587 sai. |
| RD-0113 | **parcial** | **Fechado:** o laço do Espelho é um só, `_eventos_espelho` (c82ce92:743), usado pelo `ler_espelho` e pelo `filtrar_espelho`. **Aberto (baixa):** o `try: from xlsx_rapido import load_workbook / except: openpyxl` continua 2 vezes (c82ce92:798 e :1600). **Falta:** `_abrir_excel(caminho)`, usado nos 2. |
| RD-0114 | **parcial** | **Fechado:** o regex de e-mail do site tem o mesmo texto do núcleo, `(\.[\w-]+)+` (visitas.py:100). **Aberto:** o site diz `TIPOS_ACHADO … # espelho de visitas_nucleo.TIPOS_ACHADO` (visitas.py:96), mas o núcleo não tem essa constante. Os tipos ainda só existem na docstring do `achar_dado_pessoal`. A paridade dos 4 regex também depende do teste que não existe. **Falta:** `TIPOS_ACHADO` no núcleo (modulo-rota) e os 4 `pattern` mais os tipos no teste de paridade (testes). |
| RD-0115 | **fechado** | O índice sai numa chamada só, `juntar_baixado(e["indice"], e["pc"])` (`trabalho` e `tela`). Também ficaram uma vez só: `_pendentes()`, `_DIAG_PENDENTE` (nos 3 lugares), `_arq_lote()` (nos 3), `_corte()` (nos 2) e `_tentativa(e, motivo)` (sem `agora_` e sem `t`). |
| RD-0116 | **fechado** | `from .edicoes import … _int, agora`. Agora vêm de `arquivos.py` o `gravar_bytes`, o `acrescentar_linha` e o `descomprimir_com_teto` (com `GzipGrande`/`GzipInvalido`), e o `pacotes.py` passou a usar os 3. O `_gravar_bytes` do `pacotes` e o `descomprimir` do `visitas` saíram. |
| RD-0117 | **fechado** | O `registrar` chama o `registrar_item`. `_quando()` serve aos 3, e `_com_status()` serve ao `desde` e ao `itens`. O `epoca_atual` saiu. |
| RD-0118 | **fechado** | `bearer(request, esperado)`, com `sem_token` e `sem_token_cron` de uma linha. `ler_corpo()` serve ao `corpo_json` e ao lote, e há um `@app.exception_handler(visitas.ErroVisitas)`. O `.replace("-", "")` saiu do `main.py`. |
| RD-0119 | **fechado** | `dia_br`, `dia_data` e `dia_hora` viraram funções, e as 2 que a tela usa (`dia_br` e `dia_hora`) também são filtros do Jinja. Não há mais fatia de data no template nem no `tela()`. (A leitura da data do formulário criou uma cópia nova: RD-0128.) |
| RD-0120 | **fechado** | `_PC` é usado em 6 textos. O contrato §5 (3ffcc06) diz "a fonte única é a web" e não repete mais os textos. No teste, `PAUSAM_CONTRATO` serve ao `assert` e ao `parametrize`. |
| RD-0121 | **fechado, com repetição nova** | A faixa não mostra mais a última rodada nem o código. A hora tem um formato só, `dia_hora` ("27/11 06h06"). "Acessos à Máxima hoje" ficou sem `cor: alerta`. O texto da pausa saiu da lista. Mas a correção trouxe a "Situação" para a faixa e o selo "Pausou" com "Pausou a atualização (motivo acima).", e com isso a pausa aparece 4 vezes: RD-0125. |
| RD-0122 | **fechado** | O h2 virou "Período". A faixa de rodada em andamento ficou só com "Baixando agora" e a etapa. Os textos de sucesso ficaram curtos ("Pedido enviado.", "Diagnóstico pedido.", "Retomado."). O diagnóstico aparece como "sem problema", e o código só quando não é OK. O botão fica desabilitado com pedido, com pausa ou no teto. |

## 2. Repetições novas

### RD-0123 · "O que é linha de cliente" decidido 2 vezes no núcleo, com critérios diferentes
| Campo | Conteúdo |
|---|---|
| Onde | `visitas_nucleo.py` @ c82ce92: `ler_espelho` (811) × `filtrar_espelho` (1644-1646). Também `_RX_FORMATO["codigo"]` (1532) e o ramo `titulo` do `filtrar_espelho` (1635) |
| Tipo | código |
| O que se repete | 1. O `ler_espelho` guarda a linha quando `_texto(reg.get("codigo")) or _texto(reg.get("cliente"))`. O `filtrar_espelho` pula o rodapé quando `not (_data_espelho(reg.get("data")) or re.fullmatch(r"\d{6,8}", _texto(reg.get("codigo"))))`, e o comentário diz "(o ler_espelho também ignora)". São 2 regras para a mesma decisão. Uma linha com `CLIENTE` preenchido, sem data válida e sem código, entra no `ler_espelho(origem)` e some do `destino`. 2. O `r"\d{6,8}"` repete o `_RX_FORMATO["codigo"]`. 3. No ramo `titulo`, o `_COLUNAS_ESPELHO.get(_rotulo(v))` é calculado de novo para cada célula, e o evento já traz esse `colunas` (`ev[3]`). |
| Impacto | manutenção, e o risco de quebrar a igualdade do §3.6 (`ler_espelho(destino) == ler_espelho(origem)`) |
| Severidade | média |
| Proposta | Um predicado só, chamado pelos 2:<br>`def _linha_de_cliente(reg: dict) -> bool:`<br>`    """Linha da lista que conta (rodapé e total ficam fora); a mesma no ler_espelho e no filtrar_espelho."""`<br>O critério é decisão do modulo-rota, e precisa valer para os 2. No `filtrar_espelho`, `_RX_FORMATO["codigo"].match(...)` em vez do `re.fullmatch` solto, e `campo = ev[3].get(i)` no ramo `titulo`. |
| Dono | modulo-rota (o caso de valor vai ao `testes`: fixture com linha "só cliente" na igualdade do §3.6) |

### RD-0124 · A rede de dado pessoal escrita 2 vezes dentro do `achar_dado_pessoal`
| Campo | Conteúdo |
|---|---|
| Onde | `visitas_nucleo.py` @ c82ce92: `_varrer_digitos` (1543-1548) × o laço do `achar_dado_pessoal` (1571-1574) |
| Tipo | código |
| O que se repete | os pares `("cnpj", _RX_CNPJ), ("cpf", _RX_CPF), ("telefone", _RX_FONE)` estão escritos 2 vezes. A 2ª cópia é a mesma lista com o e-mail na frente. |
| Impacto | manutenção (um tipo novo na rede tem de entrar nos 2) |
| Severidade | baixa |
| Proposta | `_REDE = (("email", _RX_EMAIL), ("cnpj", _RX_CNPJ), ("cpf", _RX_CPF), ("telefone", _RX_FONE))` e `TIPOS_ACHADO = tuple(t for t, _ in _REDE) + ("formato",)`, que também fecha o RD-0114. Depois, `def _varrer(s, rede=_REDE)`: o número chama `_varrer(s, _REDE[1:])` e o texto chama `_varrer(s)`. |
| Dono | modulo-rota |

### RD-0125 · Tela: a "Situação" da faixa repete o alerta e a lista, e a pausa aparece 4 vezes
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/templates/visitas.html` @ 134efc8: faixa (10), caixa de pausa (20), "Últimas rodadas" (79-83 e 87). `visitas.py` `tela()` (`situacao`: "Pausado", "Baixando", "Sem rodadas") |
| Tipo | layout · texto |
| O que se repete | 1. **Pausada:** a faixa diz "Situação: **Pausado**" (cor de alerta), a caixa diz "**Pausado** desde 27/11 06h06", e a 1ª rodada tem o selo "**Pausou**" e o texto "**Pausou** a atualização (motivo acima)." São 4 vezes, e "(motivo acima)" só aponta para o que já está na tela (regras 1 e 3). 2. **Baixando:** "Situação: Baixando" na faixa e "Baixando agora" na caixa. 3. **Vazia:** "Situação: Sem rodadas" na faixa e "Nenhuma rodada ainda." no cartão. É estado vazio com 2 frases. 4. **Parada:** "Situação: Em dia" na faixa e o selo "Em dia" na 1ª linha, em destaque. |
| Impacto | leitura e espaço acima da dobra |
| Severidade | média |
| Proposta | A "Situação" na faixa fica, porque foi pedida pelo designer-ux (revisão de UX e marca, 🟡 3) e é o resumo de quem olha só a faixa. O que sai é a repetição no corpo: (a) caixa de pausa: `<b>Desde {{ e.pausado.desde\|dia_hora }}</b><span>{{ v.pausa_texto }}</span>`; (b) a linha da rodada que pausou fica só com o selo e o código: `{{ '' if pausou else r.texto }}`, e "(motivo acima)" sai; (c) caixa de rodada em andamento: `<b>Etapa: {{ e.rodada_ativa.fase }}…</b>`, sem "Baixando agora", e sem a caixa se ainda não houver etapa; (d) estado vazio com uma frase só: na faixa, `"valor": "—"` quando não há rodada, e o cartão continua com "Nenhuma rodada ainda.". O item 4 (parada) fica como `manter?`, porque a faixa resume e a linha traz a hora e o texto. |
| Dono | modulo-web (com o designer-ux no print) |

### RD-0126 · Botão travado e erro do servidor dizem o mesmo motivo com 2 redações
| Campo | Conteúdo |
|---|---|
| Onde | `visitas.py` @ 134efc8: `tela()` `motivo_travado` (928-930) × `pedir()` (799 e 802). `CODIGOS["NADA_A_FAZER"]` (73) |
| Tipo | texto |
| O que se repete | 1. "Pausado: o admin retoma antes" (título do botão) × "A atualização está pausada. O admin retoma antes." (erro). "Já há um pedido na fila" × "Já há um pedido na fila. Espere ele terminar.". É o mesmo fato com 2 textos, e cada mudança tem de ser feita nos 2. 2. "Já estava em dia. Nada a baixar.": as 2 frases dizem a mesma coisa (regra 4). |
| Impacto | manutenção e leitura |
| Severidade | baixa |
| Proposta | `TRAVADO = {"pausado": "Pausado: o admin retoma antes.", "pedido": "Já há um pedido na fila.", "teto": "Limite de hoje atingido."}`, usado no `motivo_travado` e nos 2 `ErroVisitas` do `pedir`. `NADA_A_FAZER`: "Já estava em dia." |
| Dono | modulo-web |

### RD-0127 · Quem aperta "Atualizar visitas" escrito em 2 módulos
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/main.py:32` `PODEM_PEDIR = ("admin", "gerente")` × `web/app/render.py:245` `perfil in ("admin", "gerente")` (o item da lateral) |
| Tipo | código (regra de acesso, decisão 4 A) |
| O que se repete | a mesma lista de perfis, literal, em 2 arquivos. O link do cabeçalho usa `PODEM_PEDIR` (`pode_visitas`), e o item da lateral usa a cópia. |
| Impacto | manutenção. Se o Alexandre abrir o botão a outro perfil, a lateral e o cabeçalho divergem. |
| Severidade | média |
| Proposta | A constante fica num lugar que os 2 importam, sem ciclo, porque o `main` importa o `render`: `visitas.PODEM_PEDIR = ("admin", "gerente")`, com `SO_ADMIN` ao lado. Depois, `render.py:245` usa `perfil in visitas.PODEM_PEDIR`, e o `main.py` usa `visitas.PODEM_PEDIR`/`visitas.SO_ADMIN`. |
| Dono | modulo-web |

### RD-0128 · `ymd_do_form` reimplementa os regex de data do `edicoes`
| Campo | Conteúdo |
|---|---|
| Onde | `web/app/visitas.py:156-161` × `web/app/edicoes.py:53-54` (`RE_DATA_BR`, `RE_ISO`) e `:182` `iso_de_br` |
| Tipo | código |
| O que se repete | `^(\d{2})/(\d{2})/(\d{4})$` e `^\d{4}-\d{2}-\d{2}$`, escritos de novo. O `dia_data` (AAAAMMDD → dd/mm/aaaa) faz o que o `edicoes.br_data` faz a partir do ISO. Agora as 2 telas (`editar.html` e `visitas.html`) usam o mesmo campo "dd/mm/aaaa", e cada uma tem o seu leitor. |
| Impacto | manutenção |
| Severidade | baixa |
| Proposta | `from .edicoes import RE_ISO, iso_de_br` e `def ymd_do_form(v): v = (v or "").strip(); return (iso_de_br(v) or (v if RE_ISO.match(v) else "")).replace("-", "")`. O `test_formatadores_de_dia` continua igual. |
| Dono | modulo-web |

## Redundância útil ou `manter?`
- **Espelhos no site** (`_dt`, `juntar_baixado`, `dia_fechado_no_indice`, `dias_a_baixar`, `RE_PESSOAL`, `COLUNAS_PROIBIDAS`, `TIPOS_ACHADO`): manter, porque o site sobe com `rootDir: web`. A condição é o teste de paridade (RD-0110), que ainda falta.
- **Link "Atualizar" no cabeçalho do Farol de Visita e item "Atualizar visitas" na lateral:** manter. São 2 entradas para a regra dos 3 toques (UX 8).
- **`title` dos botões** ("A agenda baixa o dia anterior todo dia às 06h00", "Baixa de novo os dias que já vieram", motivo do botão travado): manter. Explicam o botão sem ocupar a tela.
- **"Situação: Em dia" na faixa × o selo "Em dia" na 1ª rodada:** `manter?` (RD-0125, item 4).
- **As 4 leituras antigas do corpo no `main.py`** (`formulario`, `api_pacote`, farol e fechar), fora do `ler_corpo`: ficam para o lote seguinte, como dizia o RD-0118.

## Fora do meu escopo (vai ao `testes`)
- RD-0123: a linha da lista só com `CLIENTE` (sem data válida e sem código) some do `destino` e continua no `ler_espelho(origem)`. É um caso para a igualdade do §3.6.

## Resultado
**Não libera.**
- **Fechados:** RD-0115 a RD-0122 (o RD-0121 com a repetição nova do RD-0125).
- **Parciais:** RD-0110, RD-0111, RD-0112, RD-0113 e RD-0114. O que falta em comum é o teste de paridade em `tests/`, que 3 textos já dão como existente; mais o `plano` e o `indice_do_pc`, os nomes errados nos comentários de espelho e o `_abrir_excel`.
- **Novos:** RD-0123 a RD-0128.

Vale para **c82ce92**, **134efc8** e **3ffcc06**.

- **Donos:**
  - modulo-rota: RD-0111 a RD-0114, RD-0123 e RD-0124;
  - modulo-robo: RD-0111 (`plano`);
  - modulo-web: RD-0112 (docstring), RD-0114 (comentário), RD-0125 a RD-0128;
  - testes: o arquivo de paridade dos RD-0110, RD-0112 e RD-0114.
- **Catálogo, recados e diário:** não atualizei o catálogo, não mandei recado e não escrevi no diário, como no parecer anterior. [SUPOSIÇÃO] Quem chamou leva os achados aos donos.
