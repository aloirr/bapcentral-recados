# Parecer de redundâncias — T-0045, itens 6 e 8 (parte do robô do PC)

- **Corretor:** corretor-redundancias · **Data:** 27/11/2026 (Manaus)
- **Branch:** `modulo-robo/T-0045-nuvem-robo` · **head SHA:** `ed640e12afe818a746cc57ebfbb5b1bb4db3a32b` (3 commits sobre `0f3106a`). Sem PR aberto.
- **Escopo:** o diff `origin/main...ed640e1`, que mexe só em `visitas_maxima.py` (+383) e `bap_automation.py` (+417). Comparei com o `visitas_nucleo.py` e o `web/app/visitas.py` do `main` (`4fc6429`), com o contrato `.coord/contratos/visitas-nuvem.md` e com o parecer do revisor (`revisao-codigo-nuvem-robo.md`, aprovado no `ed640e1`).
- **Este parecer vale só para o head acima.** Commit novo pede reteste.
- **Numeração:** o maior RD usado era o RD-0171 (`T-0023/redundancias-final.md`), então este lote começa no **RD-0172**.

## Resultado: **não libera, por 8 achados** (RD-0172 a RD-0179)

| ID | Onde | Tipo | Severidade | Dono |
|---|---|---|---|---|
| RD-0172 | `bap_automation.py:9565, 9677, 9686, 9871` | código morto | média | modulo-robo |
| RD-0173 | `visitas_maxima.py:368-371` | código morto | média | modulo-robo |
| RD-0174 | `tests/test_T0045_paridade_visitas_web.py` | teste (cópia sem trava) | média | testes |
| RD-0175 | `visitas_maxima.py:456-475` · `bap_automation.py:9960-9965` | código (regra repetida) | média | modulo-robo |
| RD-0176 | `visitas_maxima.py:290, 307-317` · `bap_automation.py:9890-9902` | código (regra repetida) | média | modulo-robo |
| RD-0177 | `visitas_maxima.py:688-697, 1322-1328` | código (log repetido) | baixa | modulo-robo |
| RD-0178 | `bap_automation.py:9766` × `10018` | código (log repetido) | baixa | modulo-robo |
| RD-0179 | `visitas_maxima.py:409-417, 772-792` | código (regra repetida) | baixa | modulo-robo |

Nenhum dos 8 é só comentário ou título de teste, então todos seguram o lote (inclusive os de gravidade baixa).

## O que rodei (cópia fora do repositório, `git archive` do `ed640e1`, Python 3.12)

| Conferência | Resultado |
|---|---|
| `compileall -q` dos 2 arquivos | ok |
| `pylint --enable=duplicate-code` / `vulture` | não instalados. Fiz a busca de referências com `git grep -w` para cada nome novo do diff |
| Referências dos nomes novos | `CODIGOS_LOGIN`, `baixar_edicoes_web`, `confirmar_edicoes_web` e `gravar_estado_edicoes_web` só aparecem na própria definição (nenhum `.py`, teste, `.bat` ou doc). O `FASES` do robô também (o outro `FASES` é o da web) |
| Sonda `sonda_rd.py` (log por eventos, `eventos=True`) | por vendedor saem 4 linhas, e o `fase=grade` aparece 2 vezes seguidas (RD-0177) |
| Sonda `sonda_rd.py` (`fechados_pc` × `vn._quando_manaus`) | iguais para hora sem fuso; para `…T10:07:00+00:00` o `fechados_pc` manda `10:07-04:00`, e o núcleo dá `06:07-04:00` (RD-0175) |
| Sonda `sonda_rd2.py` (as propostas do RD-0176 e RD-0177) | a regra única do nome dá o mesmo motivo da validação atual em 13 casos (pasta com `/`, `..`, controle, minúscula, outro dia, outro nome, `.xls`, sufixo `-2`, vazio, `None`); o `_fase` proposto dá 3 linhas por vendedor e o mesmo número de chamadas ao `ao_fase` (7) |

## Achados

### RD-0172 · Três funções das edições ficaram sem quem chame, e um `import` repetido

| Campo | Conteúdo |
|---|---|
| Onde | `bap_automation.py:9565` (`gravar_estado_edicoes_web`), `:9677` (`baixar_edicoes_web`), `:9686` (`confirmar_edicoes_web`), `:9871` (`import base64` dentro do `_validar_lote_visitas_web`) |
| Tipo | código |
| O que se repete | No `main`, as 3 funções eram usadas só pelo `sincronizar_edicoes_web`. Com a extração, o laço chama direto o `_baixar_fila_web`, o `_confirmar_fila_web` e o `_gravar_estado_fila_web`. Sobraram 3 embrulhos com **0 chamadas** (`git grep -w` no head inteiro, testes incluídos). O `base64` já é importado no topo (`:174`), e o `import` local repete. |
| Impacto | manutenção: são 3 portas para a mesma fila. Quem corrigir o laço pode corrigir o embrulho errado |
| Severidade | média |
| Proposta | Apagar as 3 funções e o `import base64` da linha 9871. O `ler_estado_edicoes_web` **fica**, porque o `test_T0021_edicao_web_robo.py` (linhas 233-262) usa. Depois: `git grep -nwE "baixar_edicoes_web\|confirmar_edicoes_web\|gravar_estado_edicoes_web"` vazio, e `test_T0021` + `test_T0045_*` verdes |
| Dono | modulo-robo |

### RD-0173 · `FASES` e `CODIGOS_LOGIN` declarados e nunca lidos

| Campo | Conteúdo |
|---|---|
| Onde | `visitas_maxima.py:368` (`FASES`) e `:370` (`CODIGOS_LOGIN`) |
| Tipo | código |
| O que se repete | `FASES` é cópia literal do `web/app/visitas.FASES`, mas o robô não lê: as 11 chamadas `self._fase("…")` usam texto solto. `CODIGOS_LOGIN` repete 4 dos 5 códigos do `PAUSAM` da web e não tem uso nenhum, nem no contrato. São 2 listas a mais para manter iguais à web, sem ganho. |
| Impacto | manutenção: lista que ninguém lê fica velha sem aviso |
| Severidade | média |
| Proposta | (a) Apagar o `CODIGOS_LOGIN` (linhas 370-371). (b) Dar uso ao `FASES` no `_fase`, como o revisor sugeriu (🟡 2): logo no começo do `Robo._fase`, `if fase not in FASES: raise ValueError(f"fase fora do contrato: {fase}")`. Assim, uma fase digitada errado aparece no teste, e não como 400 do site. Se o modulo-robo preferir, pode apagar o `FASES` também. Nesse caso, o RD-0174 passa a conferir as fases literais do `_fase` direto contra a web |
| Dono | modulo-robo |

### RD-0174 · Cópias robô × web sem teste de paridade (`FASES`, `FECHADOS_PC_DIAS`, códigos)

| Campo | Conteúdo |
|---|---|
| Onde | `visitas_maxima.FASES` / `FECHADOS_PC_DIAS = 40` / os códigos que o robô levanta (`"MAXIMA_*"`, `"NAVEGADOR_FALHOU"`, `"TELA_MUDOU"`, `"ERRO_INTERNO"`) × `web/app/visitas.FASES` / `FECHADOS_PC_DIAS = 40` / `CODIGOS` |
| Tipo | teste |
| O que se repete | São 3 constantes do contrato (§3.3, a tabela do §2 e o §5), escritas nos 2 lados. A cópia é **necessária**: o Render publica só `web/` e não importa a raiz (cabeçalho do `web/app/visitas.py`). Mas o teste de paridade do `main` prende só a RN-VIS-002 e a RN-VIS-007. Hoje a igualdade só foi conferida na `sonda2.py` do autor, que não roda no CI |
| Impacto | decisão: se um lado mudar e o outro não, o site devolve 400 no `progresso`/`fim` (o 🟡 2 do revisor foi exatamente isso) ou a janela do `fechados_pc` deixa de bater com a do `indice` |
| Severidade | média |
| Proposta | Acrescentar ao `tests/test_T0045_paridade_visitas_web.py`, usando o mesmo `web_app` dos testes que já estão lá: `assert vm.FASES == web.FASES`; `assert vm.FECHADOS_PC_DIAS == web.FECHADOS_PC_DIAS`; e `set(re.findall(r'"((?:MAXIMA\|NAVEGADOR\|TELA\|ERRO)_[A-Z_]+)"', Path("visitas_maxima.py").read_text("utf-8"))) <= set(web.CODIGOS)`. Os nomes seguem o arquivo (ex.: `test_RN_VIS_002_fechados_pc_dias_igual_no_robo_e_na_web`). Cabe no item 9 da ADR 0004 §9, junto dos testes do 🟡 5 do revisor. Se o gerente puser este achado na mesma condição do 🟡 5 (no `main` antes do item 10), a decisão é dele e fica registrada; até lá, o achado segue aberto |
| Dono | testes |

### RD-0175 · A hora de Manaus reescrita em 2 lugares, com o `vn._quando_manaus` ao lado

| Campo | Conteúdo |
|---|---|
| Onde | `visitas_maxima.fechados_pc` (`:470-475`: `datetime.fromisoformat(...)` + `replace(tzinfo=None).isoformat(...) + "-04:00"`) e `bap_automation._aplicar_lote_visitas_web` (`:9960-9965`: `fromisoformat(...)` + `replace(tzinfo=None)`) |
| Tipo | código (regra repetida: data) |
| O que se repete | Os 2 lugares trazem de volta a regra "iso → hora de Manaus; sem fuso = Manaus", que já está no `visitas_nucleo._quando_manaus` (a função do RN-VIS-002, a mesma que o `juntar_baixado` usa). As cópias jogam o fuso fora em vez de converter. Na sonda, `…T10:07:00+00:00` vira `10:07-04:00` no `fechados_pc`, contra `06:07-04:00` no núcleo. O revisor viu metade disso (🟢 6) |
| Impacto | manutenção e decisão: a mesma hora, lida de 2 jeitos, decide se o dia está fechado |
| Severidade | média |
| Proposta | No `fechados_pc`, trocar o `try` e o `saida[chave] = …` por: `q = vn._quando_manaus(v)` / `if q is None: continue` / `if corte <= dia <= hoje: saida[chave] = q.isoformat(timespec="seconds")`. Isso mantém o `strptime` do dia. No `_aplicar_lote_visitas_web`, trocar o `try/except` das linhas 9960-9965 por: `q = vn._quando_manaus(corpo.get("baixado_em"))` / `quando = (q or _agora_manaus()).replace(tzinfo=None)    # o indice guarda a hora de Manaus sem fuso`. Na sonda, a hora sem fuso continua saindo igual |
| Dono | modulo-robo |

### RD-0176 · A regra do nome do Excel importado escrita 2 vezes, com textos diferentes

| Campo | Conteúdo |
|---|---|
| Onde | `bap_automation._validar_lote_visitas_web` (`:9890-9902`) × `visitas_maxima.gravar_excel_importado` (`:307-312`). O nome-base `f"VISITA-{…}-{dia:%d-%m-%Y}-{quando:%H-%M}"` aparece em `visitas_maxima.py:290` (`arquivo_analitico`) e `:317` |
| Tipo | código (regra repetida) |
| O que se repete | A conferência "pasta = `nome_limpo`; nome casa com `_RX_ARQ_ANALITICO`, com o grupo `nome` igual à pasta, sem `/`, `\` nem `..`" está nos 2 módulos, e só um deles barra caractere de controle. Dentro do `_validar_lote_visitas_web`, 2 testes não acrescentam nada: o `startswith(f"VISITA-{pasta}-")` (o grupo `nome == pasta` já garante) e o `[/\\\x00-\x1f]` na pasta (o `nome_limpo(pasta) != pasta` já pega). O formato do nome-base está escrito 2 vezes |
| Impacto | manutenção: é a trava de segurança do disco do PC (RN-VIS-003). Ajustar um lado e esquecer o outro abre a diferença sem que ninguém veja |
| Severidade | média |
| Proposta | Em `visitas_maxima.py`, uma função pura, usada pelos 2: `def conferir_importado(pasta, nome, dia=None):` → `(motivo, None)` ou `(None, (dia, quando))`. Ela confere: `pasta` str não vazia, sem `..` e `nome_limpo(pasta) == pasta` (senão `"pasta"`); `m = vn._RX_ARQ_ANALITICO.match(nome)`, `m["nome"] == pasta`, `nome` sem `[/\\\x00-\x1f]\|\.\.` e, com `dia`, `f"{m['a']}{m['m']}{m['d']}" == dia` (senão `"nome"`); data e hora válidas (senão `"nome"`). No `gravar_excel_importado`: `motivo, dq = conferir_importado(pasta, nome)` / `if motivo: raise ValueError(motivo)` / `dia, quando = dq` (a última trava continua, agora com a mesma regra). No `_validar_lote_visitas_web`, o bloco das linhas 9890-9902 vira `motivo, _ = vm.conferir_importado(pasta, nome, dia)` / `if motivo: return None, motivo`. O nome-base fica numa função só, `def _base_analitico(nome, dia, quando): return f"VISITA-{nome}-{dia:%d-%m-%Y}-{quando:%H-%M}"`, usada pelo `arquivo_analitico` e pelo `gravar_excel_importado`. A sonda deu o mesmo motivo nos 13 casos. O teste (RN-VIS-003) entra no item 9 |
| Dono | modulo-robo |

### RD-0177 · O tique do vendedor sai 2 vezes no log da nuvem

| Campo | Conteúdo |
|---|---|
| Onde | `visitas_maxima.py:1323-1325` (`self.evento("vendedor", fase="grade", …)` seguido de `self._fase("grade", feitos=…)`) e `:1322` × `:1328` (`self.vendedores = len(feitos)`) |
| Tipo | código (log) |
| O que se repete | A cada vendedor, o `_fase` volta de `salvar` para `grade` e escreve `evento=fase fase=grade`, logo depois do `evento=vendedor fase=grade n=k`. São 4 linhas por vendedor, e "fase=grade" aparece 2 vezes seguidas: com 15 vendedores, 15 linhas a mais por dia no único log que o Render mostra (contrato §5, "uma linha por evento"). O `self.vendedores = len(feitos)` depois do laço repete a última atribuição de dentro do laço: só se chega ali depois de pelo menos um vendedor, senão o `ErroRobo` "Não achei o olho" sai antes |
| Impacto | leitura do log do cron |
| Severidade | baixa |
| Proposta | No `Robo._fase`, trocar `if mudou: self.evento("fase", …)` por `if feitos is not None: self.evento("vendedor", fase=fase, dia=self.dia_atual, n=feitos)` / `elif mudou: self.evento("fase", fase=fase, dia=self.dia_atual)`. No laço, apagar a linha 1323 (`self.evento("vendedor", …)`) e a 1328 (`self.vendedores = len(feitos)`). Na sonda, ficam 3 linhas por vendedor (`espelho`, `salvar`, `vendedor … n=k`), e o `ao_fase` é chamado as mesmas 7 vezes |
| Dono | modulo-robo |

### RD-0178 · O número de lotes importados sai 2 vezes seguidas no log

| Campo | Conteúdo |
|---|---|
| Onde | `bap_automation.py:9766` (dentro do `puxar_fila_web`: `"Visitas web: N gravada(s) no PC, M recusada(s)."`) e `:10018` (no `sincronizar_visitas_web`: `"Visitas web: N lote(s), X Excel, D dia(s)."`) |
| Tipo | código (log) |
| O que se repete | Na mesma volta, as 2 linhas dizem o mesmo N, a quantidade de lotes gravados |
| Impacto | leitura do log do robô |
| Severidade | baixa |
| Proposta | Linha 10018-10019 → `log(f"Visitas web: {res['arquivos']} Excel de {len(res['dias'])} dia(s).")`. A contagem de lotes e de recusados fica na linha do laço, que é a mesma das edições |
| Dono | modulo-robo |

### RD-0179 · A regra "ainda está no login" escrita 4 vezes entre o `pronto()` e o `classificar_login`

| Campo | Conteúdo |
|---|---|
| Onde | `visitas_maxima.py:416-417` (`classificar_login`) e `:774-775`, `:784`, `:790` (`entrar.pronto`) |
| Tipo | código (regra repetida) |
| O que se repete | `"/login" in _caminho(url).lower()` aparece 4 vezes, e `_RX_URL_VERIFICACAO.search(_caminho(url))` 2 vezes. O `_caminho(url)` é calculado 4 vezes por volta de 0,4 s. O `pronto()` precisa da conferência antes do `evaluate`, para não ler a página quando o login já passou; o motivo é bom, mas a regra fica copiada. A nota R3 do revisor (rota em `#`) teria de ser acertada em 2 funções |
| Impacto | manutenção |
| Severidade | baixa |
| Proposta | Uma função pura, `def _no_login(url) -> tuple[bool, bool]:` com o corpo `c = _caminho(url)` / `return "/login" in c.lower(), bool(_RX_URL_VERIFICACAO.search(c))`. No `classificar_login`: `no_login, verif = _no_login(url)` / `if not (no_login or verif): return None`. No `pronto()`: `no_login, verif = _no_login(pg.url)` no começo; `if not (no_login or verif): return "ok"`; depois, `if not msg and not no_login:` e `if not no_login: return "ok"` |
| Dono | modulo-robo |

## Redundância útil (manter)

- **O PC confere de novo o lote que o site já validou** (`_corpo_do_lote_visitas_web` com o sha256 do cabeçalho e o da linha; `_validar_lote_visitas_web` × `web/app/visitas.validar_lote`). É a fronteira de confiança: o PC não grava no disco o que não conferiu. Fica. A parte repetida *dentro* do robô é a do RD-0176.
- **`gravar_excel_importado` como "última trava"**: fica, mas com a mesma função do RD-0176.
- **`AVISO_SITE_BAIXANDO`**: o texto literal do contrato §4.5, num lugar só no código. Fica.
- **Os textos do `ErroRobo` para `MAXIMA_*` × `web.CODIGOS`**: aparecem em telas diferentes (a janela do PC e o Farol de Visita), cada um com a ação de quem lê. Não são repetição na mesma tela.

## Conferido, sem achado

- **`puxar_fila_web` é mesmo compartilhado pelas 2 filas.** O `sincronizar_edicoes_web` (`:9787`) e o `sincronizar_visitas_web` (`:9985`) passam pelo mesmo laço. O GET paginado é um só (`_baixar_fila_web`), o POST também (`_confirmar_fila_web`), e o estado tem um par só de leitura e gravação (`_ler/_gravar_estado_fila_web`). Cada fila só traz a parte dela (`aplicar`, `ja_feitos`, `registrar`, `preparar`, `extra_confirmar`). O parâmetro `raiz` do `puxar_fila_web` não é usado, mas está na assinatura do contrato §4.4; não catalogo.
- **Empate e "baixado" (RN-VIS-002):** o `_anotar_maior_visitas_web` usa o `vn.juntar_baixado` e o `vn.anotar_baixado`, sem copiar a regra. O empate fica com a nuvem.
- **Fechado (RN-VIS-002):** o robô não reimplementa o `dia_fechado`/`dia_fechado_no_indice`. O `fechados_pc` só manda o índice do PC, e quem decide é o site. A única repetição é a da hora (RD-0175).
- **Dado pessoal (RN-VIS-007):** o `Robo.evento`/`_campo`, o `msg = type(e).__name__` e o `_texto_login` sem `msg` na nuvem não repetem o `achar_dado_pessoal` do núcleo: cada um tapa uma saída diferente (o log, a lista `erros` que vai no `ao_fechar_dia`, o texto do erro). Não há regex de dado pessoal no diff.
- **`depois_de_baixar`:** saiu do `executar` e é chamado 1 vez pelo botão e 1 vez por importação. Não é cópia.

## Fora do meu escopo (encaminhado, não catalogado)

- `bap_automation.py:9635`: com `rotulo="Visitas web"`, a linha diz "falha ao puxar as **edicoes** do site". É texto errado, não repetido. Já está no 🟢 8 do revisor.
- Observação para depois (vem de antes, está no `main` e fora deste diff): o `baixar_cobranca_web` (`:9370`) é quase igual ao `_baixar_fila_web`, só muda o texto do log. O contrato §4.4 separou de propósito o laço da cobrança, que confirma só o `ate_seq`, mas o GET paginado poderia passar a usar o `_baixar_fila_web`. Fica como sugestão de tarefa futura do modulo-robo, sem segurar este lote.

## Para o reteste

Commit novo do modulo-robo com o RD-0172, o RD-0173 e o RD-0175 a RD-0179 corrigidos. O RD-0174 sai com os testes no `main`, ou com a decisão registrada do gerente, junto do 🟡 5. Depois, pedido de reteste com o head SHA novo. A prova é o `git grep` do RD-0172, o `test_T0021` + `test_T0045_*` verdes e uma sonda do log por eventos (3 linhas por vendedor).

---

# Reteste no head `f6ae758` (robô, PR #165) com o `5050cfe` (testes, PR #166) — 27/11/2026

- **Delta `ed640e1..f6ae758`:** `9a886ae` (merge do `main` 4fc6429; nada do robô), `69b14cc` (D1/D2: `classificar_login` pausa em caminho de verificação com qualquer redação e na troca de senha) e `f6ae758` (as correções dos RD). Contra o `main`, o PR continua só em `visitas_maxima.py` e `bap_automation.py`.
- **Testes:** `5050cfe` (`testes/T-0045-nuvem-testes`), delta `c30a0d5..5050cfe` em `tests/test_T0045_paridade_visitas_web.py` e `tests/test_T0045_robo_nuvem.py`.
- **Numeração:** os novos começam no **RD-0180**.

## Resultado: **não libera, por 2 achados novos** (RD-0180 e RD-0181). Os RD-0172 a RD-0179 estão fechados.

## O que rodei (cópia fora do repositório: `git archive f6ae758` + `tests/` do `5050cfe`, Python 3.12)

| Conferência | Resultado |
|---|---|
| `compileall -q visitas_maxima.py bap_automation.py` | ok |
| `pytest` dos 7 arquivos `test_T0045_*` | **1 falhou, 205 passaram, 3 pulados**. A falha é o `test_T0045_edicoes_web_igual_main.py::test_RN_GER_012_funcoes_publicas_das_edicoes_continuam`: `AttributeError: module 'bap_automation' has no attribute 'gravar_estado_edicoes_web'` (RD-0180) |
| `test_T0021_edicao_web_robo.py` | não rodou aqui: o ambiente não tem `tkinter` (`bap_relatorios` importa). `git grep` mostra que ele usa só o `ler_estado_edicoes_web`, que ficou |
| `git grep -nw` dos nomes apagados no `f6ae758` + `5050cfe` | só aparecem na régua congelada `tests/ref_T0045_edicoes_web_main.py` (cópia de propósito, ver abaixo) e no teste do RD-0180 |
| Sonda `sonda_rd3.py` no `f6ae758` | 3 linhas por vendedor e 7 chamadas ao `ao_fase`; `fechados_pc` com `…T10:07+00:00` → `06:07-04:00`, igual ao núcleo; `_fase("navegador")` → `ValueError`; `CODIGOS_LOGIN` não existe mais; fora do `/login`, num caminho de verificação, o `classificar_login` devolve código em 4 de 4 textos (base do RD-0181) |

## Os RD do parecer anterior

| ID | Situação | Evidência no `f6ae758` / `5050cfe` |
|---|---|---|
| RD-0172 | **fechado** | `gravar_estado_edicoes_web`, `baixar_edicoes_web`, `confirmar_edicoes_web` e o `import base64` local saíram. O `vn` que ficou sem uso no `_validar_lote_visitas_web` também saiu. O `ler_estado_edicoes_web` ficou. A consequência nos testes é o RD-0180 |
| RD-0173 | **fechado** | o `CODIGOS_LOGIN` saiu; o `Robo._fase` confere `if fase not in FASES: raise ValueError(...)` |
| RD-0174 | **fechado (no `5050cfe`)** | `test_RN_VIS_005_fases_iguais_no_robo_e_na_web`, `test_RN_VIS_002_fechados_pc_dias_igual_no_robo_e_na_web` e `test_RN_VIS_005_todo_codigo_do_robo_esta_na_web` (literais do `visitas_maxima.py` e retornos das funções puras ⊂ `web.CODIGOS`) passam com o robô novo. A cópia dos asserts que estava no `test_T0045_robo_nuvem.py` saiu. Fecha quando o #166 entrar |
| RD-0175 | **fechado** | `fechados_pc` e `_aplicar_lote_visitas_web` usam o `vn._quando_manaus` (sonda acima) |
| RD-0176 | **fechado** | `conferir_importado(pasta, nome, dia=None)` e `_base_analitico(...)` em `visitas_maxima.py`, usados pelo `gravar_excel_importado`, pelo `arquivo_analitico` e pelo `_validar_lote_visitas_web`. A regra do nome está escrita uma vez só (`_RX_PERIGO_NOME`) |
| RD-0177 | **fechado** | o `_fase` escreve o `evento=vendedor`; saíram a linha solta do laço e a segunda atribuição do `self.vendedores` |
| RD-0178 | **fechado** | `"Visitas web: {arquivos} Excel de {dias} dia(s)."` |
| RD-0179 | **fechado** | `_no_login(url)`, usado no `classificar_login` e no `pronto()` |

## Achados novos

### RD-0180 · Teste do PR #166 prende as 3 funções mortas que o RD-0172 tirou

| Campo | Conteúdo |
|---|---|
| Onde | `tests/test_T0045_edicoes_web_igual_main.py:162-183` (`5050cfe`), `test_RN_GER_012_funcoes_publicas_das_edicoes_continuam` |
| Tipo | teste |
| O que se repete | O teste exige que `gravar_estado_edicoes_web`, `baixar_edicoes_web` e `confirmar_edicoes_web` continuem no `bap_automation`. No `main`, as 3 só eram chamadas pelo `sincronizar_edicoes_web`. A docstring diz "o PC e os testes da T-0021 usam", mas o `test_T0021` usa só o `ler_estado_edicoes_web`. O GET e o POST das edições já são comparados com a régua nos cenários do `sincronizar_edicoes_web`, no mesmo arquivo. Com o #165 e o #166 juntos, o teste falha (1 ❌): quem entrar por último deixa o CI vermelho |
| Impacto | manutenção e merge: o teste prende código morto e bloqueia o outro PR |
| Severidade | alta: o teste falha |
| Proposta | Na linha 166, a tupla vira `("ler_estado_edicoes_web", "sincronizar_edicoes_web")`. Na 171, `ba.gravar_estado_edicoes_web(tmp_path, est)` vira `r.gravar_estado_edicoes_web(tmp_path, est)` (a régua grava e os 2 leem). Saem os asserts do `baixar_edicoes_web` e do `confirmar_edicoes_web` (linhas 173-183). Docstring: `"""Assinaturas e efeito das 2 funções públicas das edições que ficam (o test_T0021 usa o ler_estado; o GET e o POST são comparados nos cenários do sincronizar)."""` Pronto quando: os 7 `test_T0045_*` verdes no `f6ae758` com os testes do #166 |
| Dono | testes |

### RD-0181 · Ramo que nunca roda depois do D1/D2 (`69b14cc`)

| Campo | Conteúdo |
|---|---|
| Onde | `visitas_maxima.py:827-828` (`pronto()`: `if not no_login: return "ok"`) e `:461` (`classificar_login`: `if no_login and t.strip() and …`) |
| Tipo | código |
| O que se repete | Depois do `69b14cc`, fora do `/login` e num caminho de verificação, o `classificar_login` sempre devolve um código: captcha, bloqueio, confirmação ou, no fim, `MAXIMA_CONFIRMACAO` (linha 457). O `pronto()` só chama o `classificar_login` com `no_login or verif`, então o `return "ok"` da 827-828 nunca é alcançado. Na 461, o `no_login` é sempre verdadeiro, porque o `if not no_login` da 457 já devolveu antes. Pela sonda, 4 de 4 textos dão código |
| Impacto | manutenção: o ramo morto sugere que a verificação pode passar como "ok", o que contradiz o comentário da linha 458 |
| Severidade | baixa |
| Proposta | Apagar as linhas 827-828 do `pronto()`; depois do `if cod: return f"cod:{cod}:{msg}"` vem direto o `return f"erro:{msg}" if msg else None`. Na linha 461, `if no_login and t.strip() and _RX_CREDENCIAL.search(t):` vira `if t.strip() and _RX_CREDENCIAL.search(t):` |
| Dono | modulo-robo |

## Redundância útil (manter)

- `tests/ref_T0045_edicoes_web_main.py`: cópia congelada do laço das edições do `main` `e1d80a8`, a régua do "sem mudança de comportamento". A docstring já diz que não é produção e quando muda. Fica.

## Para o reteste

- **modulo-robo:** commit novo no #165 com o RD-0181.
- **testes:** commit novo no #166 com o RD-0180.
- **Prova:** os 7 `test_T0045_*` verdes no head novo do robô junto com o head novo dos testes, e o `test_T0021` rodado num ambiente com `tkinter`. Os dois PRs liberam juntos, cada um no seu head SHA.

---

# Reteste 2 no head `a020b53` (robô, PR #165) — 27/11/2026

- **Delta `f6ae758..a020b53`:** 2 commits, só em `visitas_maxima.py` (+24 −6).
  - `3511814`: o RD-0181.
  - `a020b53`: o 🟡 A do revisor. O `_RX_URL_VERIFICACAO` passa a casar só segmentos inteiros, de uma lista fechada. O `pronto()` ganha a espera de 2 leituras e entra o `_texto_claro`.
- **Testes:** o `testes/T-0045-nuvem-testes` continua no `5050cfe`. O RD-0180 está com o testes.
- **Numeração:** o novo achado é o **RD-0200**. Os RD-0182 a RD-0191 são do corretor da T-0050, e a T-0037 usa do RD-0192 em diante (renumerado a pedido do gerente-projetos).

## Resultado: **o robô não libera, por 1 achado novo** (RD-0200). O RD-0181 está fechado. O RD-0180 (testes, #166) continua aberto e segura o par #165/#166.

## O que rodei (`git archive a020b53` + `tests/` do `5050cfe`, Python 3.12)

| Conferência | Resultado |
|---|---|
| `compileall -q visitas_maxima.py` | ok |
| `pytest tests/test_T0045_*.py` | 205 passaram, 3 pulados, **1 falhou**: o mesmo do RD-0180 (`gravar_estado_edicoes_web`) |
| `git grep _texto_claro` | 1 definição (`:443`) e 1 uso (`:836`, no `pronto()`). Nenhum teste |
| Sonda `sonda_rd4.py` (6 URLs × 8 textos × captcha sim/não = 96 casos) | a proposta do RD-0200 dá o mesmo código e a mesma decisão de esperar nos 96 casos. O `_RX_BLOQUEIO` dentro do `_texto_claro` não decide nenhum caso |

## RD-0181: **fechado**

Saiu o `if not no_login: return "ok"` que nunca rodava, do `pronto()`. A linha do `MAXIMA_SENHA` no `classificar_login` ficou `if t.strip() and _RX_CREDENCIAL.search(t):`.

## Achado novo

### RD-0200 · O `_texto_claro` refaz o que o `classificar_login` acabou de decidir

| Campo | Conteúdo |
|---|---|
| Onde | `visitas_maxima.py:443-446` (`_texto_claro`) × `:449-470` (`classificar_login`); uso em `:836` (`pronto()`); `:840` e `:842` (debounce) |
| Tipo | código (regra repetida) |
| O que se repete | O `_texto_claro` normaliza o texto de novo (`_sem_acento_min`) e roda de novo o `_RX_CONFIRMACAO` e o `_RX_BLOQUEIO`. São os mesmos 2 testes que o `classificar_login` acabou de fazer, na mesma ordem, com o mesmo texto. A única pergunta do `pronto()` é: "o `MAXIMA_CONFIRMACAO` saiu só pelo caminho da URL?". Isso o `classificar_login` já sabe: é o ramo `if not no_login:` da linha 466. A metade do bloqueio nunca decide, porque com bloqueio no texto o código já seria `MAXIMA_BLOQUEIO`, e não `MAXIMA_CONFIRMACAO` (0 de 96 casos). No debounce, `vistos.get("caminho") != caminho` aparece 2 vezes seguidas (`:840` e `:842`) |
| Impacto | manutenção: são 2 cópias da regra de texto do §5.1. Uma frase nova no `classificar_login` sem a mesma frase no `_texto_claro` muda, sem aviso, quando a nuvem pausa |
| Severidade | média |
| Proposta | (a) O corpo do `classificar_login` vira `def _classificar(url, texto, tem_captcha, http_status) -> tuple:` e devolve `(codigo \| None, so_pelo_caminho)`, com `True` só no ramo da linha 466 (`return "MAXIMA_CONFIRMACAO", True`) e `False` nos outros. O público fica `def classificar_login(url, texto, tem_captcha, http_status) -> str \| None: return _classificar(url, texto, tem_captcha, http_status)[0]`: mesma assinatura, e os testes do #166 não mudam. (b) O `_texto_claro` sai. (c) No `pronto()`: `cod, so_caminho = _classificar(url, texto, captcha, None)` e depois `if so_caminho:` / `agora, caminho = _time.time(), _caminho(url)` / `if vistos.get("caminho") != caminho:` / `vistos.update(caminho=caminho, em=agora)` / `return None` / `if agora - vistos["em"] < 1.0:` / `return None`. A sonda deu o mesmo código e a mesma espera nos 96 casos |
| Dono | modulo-robo |

## Sem achado no resto do delta

O `_RX_URL_VERIFICACAO` novo continua num lugar só, usado só pelo `_no_login`. O acréscimo no `_RX_CONFIRMACAO` não duplica outra regex. O `vistos` é local do `entrar`.

## Para o reteste

- **modulo-robo:** commit novo no #165 com o RD-0200.
- **testes:** commit novo no #166 com o RD-0180.
- **Prova:** os `test_T0045_*` todos verdes com os 2 heads novos juntos, e uma sonda do `_classificar` com a mesma decisão que o código de hoje.

---

# Reteste dos testes no head `cd794d1` (PR #166), com o robô `a020b53` — 27/11/2026

- **Delta `5050cfe..cd794d1`:** 1 commit (`T-0045: testes ao robô a020b53 …`). Mexe em `tests/test_T0045_edicoes_web_igual_main.py`, `tests/test_T0045_robo_nuvem.py`, `tests/test_T0045_visitas_web_robo.py`, `docs/testes/T-0045.md` e no diário do testes.
- **Numeração:** o novo achado é o **RD-0201** (renumerado a pedido do gerente-projetos).

## Resultado

- **Testes (#166, `cd794d1`): libera.** O RD-0180 está fechado. O único achado novo (RD-0201) é de gravidade baixa e só em docstring e título de teste: não segura o lote e entra no seguinte.
- **Robô (#165, `a020b53`): não libera.** O RD-0200, do reteste 2, segue aberto.

## O que rodei (`git archive a020b53` + `tests/` do `cd794d1`, Python 3.12)

| Conferência | Resultado |
|---|---|
| `compileall -q tests/ visitas_maxima.py` | ok |
| `pytest tests/test_T0045_*.py` | **236 passaram, 3 pulados, 0 falhas**. Os 3 pulados são de `test_T0045_robo_nuvem.py:821` ("sem tkinter neste Python") |
| `git grep _texto_claro` no `cd794d1` | nenhum teste chama o `_texto_claro` direto: a correção do RD-0200 não mexe nos testes |

## RD-0180: **fechado**

`test_RN_GER_012_funcoes_publicas_das_edicoes_continuam` agora confere só o `ler_estado_edicoes_web` e o `sincronizar_edicoes_web`. O estado é gravado pela régua (`r.gravar_estado_edicoes_web`), e há 1 assert novo do estado vazio. Os asserts do `baixar` e do `confirmar` saíram, e a docstring diz por quê. O teste passa com o robô `a020b53`.

## Achado novo

### RD-0201 · A docstring diz que o teste confere a importação, mas ele não chama a importação (não segura o lote)

| Campo | Conteúdo |
|---|---|
| Onde | `tests/test_T0045_robo_nuvem.py:396-397`, `test_RN_VIS_003_conferir_importado_e_o_mesmo_no_robo_e_na_gravacao` |
| Tipo | teste (título e docstring) |
| O que se repete | A docstring diz "O mesmo motivo sai da importação (`_validar_lote_visitas_web`) e da última trava (`gravar_excel_importado`)". O corpo só compara o `conferir_importado` com o `gravar_excel_importado` e nunca chama o `_validar_lote_visitas_web`. O título fala em "no robô e na gravação", mas os 2 lados estão no robô |
| Impacto | leitura: promete uma cobertura que o teste não tem |
| Severidade | baixa (só título e docstring) |
| Proposta | Renomear para `test_RN_VIS_003_gravar_excel_importado_levanta_o_motivo_do_conferir_importado`, com a docstring `"""A última trava (`gravar_excel_importado`) levanta o mesmo motivo do `conferir_importado`."""`. Outra saída é acrescentar, no mesmo teste, a chamada ao `ba._validar_lote_visitas_web` com um lote fictício. Aí o texto atual passa a valer |
| Dono | testes |

## Sem achado no resto do delta

- Os testes novos do D1/D2, do 🟡 A, do `_fase`, da linha por vendedor, do `conferir_importado` (14 casos), do `_no_login` e do fuso não repetem casos que já existiam.
- A lista de URLs que seguem (`/hotpage`, `/devices/home`…) entrou no parametrize que já existia, sem teste novo.
- A matriz do `docs/testes/T-0045.md` foi atualizada sem linha repetida.

## Para liberar o par

- **modulo-robo:** commit novo no #165 com o RD-0200.
- **Depois:** reteste do robô e os `test_T0045_*` rodados de novo com o `cd794d1`, ou com o head do testes que estiver valendo.
- **testes:** o RD-0201 entra no próximo lote do testes.

---

# Reteste do RD-0200 no head `479b8f65b5ca7187a89b763a58719735b0c83f8a` (robô, PR #165) — 27/11/2026

- **Delta `a020b53..479b8f6`:** 1 commit (`T-0045: RD-0200 …`), só em `visitas_maxima.py` (+25 −28).

## Resultado: **o robô libera.** Não há achado em aberto no #165. O RD-0201 é do #166, de gravidade baixa e só em título de teste: não segura nenhum dos dois.

## O que rodei (`git archive 479b8f6` + `tests/` do `cd794d1`, Python 3.12)

| Conferência | Resultado |
|---|---|
| `compileall -q visitas_maxima.py` | ok |
| `pytest tests/test_T0045_*.py` | **236 passaram, 3 pulados, 0 falhas** (os 3 pulados são de "sem tkinter neste Python") |
| Sonda `sonda_rd5.py`, os mesmos 96 casos (6 URLs × 8 textos × captcha sim/não) | o `(codigo, so_pelo_caminho)` do `_classificar` novo é igual a `(classificar_login, cod == CONFIRMACAO and not _texto_claro)` do `a020b53` em **96 de 96 casos, 0 diferenças**; o `classificar_login` novo é igual a `_classificar(...)[0]` em todos |
| `git grep` no head | `_texto_claro` não existe mais. O `_classificar` está definido em 1 lugar (`:443`) e é usado em 2: no `classificar_login` (`:472`) e no `pronto()` (`:835`) |

## RD-0200: **fechado**

- O `_classificar` devolve `(codigo, so_pelo_caminho)`, com `True` só no ramo do caminho de verificação.
- O `classificar_login` passa a ser `_classificar(...)[0]`, com a mesma assinatura.
- O `_texto_claro` saiu, e a regra do texto do §5.1 ficou escrita uma vez só.
- O debounce virou uma comparação só: `vistos.setdefault(_caminho(url), agora)`.

## Fora do meu escopo (encaminhado, não catalogado)

O debounce novo guarda a 1ª leitura **por caminho**, e não só a do último caminho, como no `a020b53`. Na sequência `/mfa` → `/verificacao` → `/mfa` (1 s ou mais depois), o `a020b53` recomeçava a conta no segundo `/mfa`; o `479b8f6` já decide nesse segundo `/mfa`. Isso é comportamento, não repetição: fica com o revisor-codigo e o testes, se quiserem conferir. Nos testes do `cd794d1` (2 leituras do mesmo caminho e verificação de passagem), os dois dão o mesmo resultado.

## Situação final dos RD deste parecer

| RD | Dono | Situação |
|---|---|---|
| RD-0172 a RD-0181 | modulo-robo / testes | fechados |
| RD-0200 | modulo-robo | fechado no `479b8f6` |
| RD-0201 | testes | aberto, baixa, só título e docstring de teste. Não segura o lote e entra no próximo lote do testes |
