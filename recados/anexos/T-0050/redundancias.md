# T-0050 · Parecer de redundâncias · acesso aos faróis por usuário

- **Branch:** `modulo-web/T-0050-acesso-usuario` · **head:** `a5e723b`
- **Escopo:** `web/app/acesso.py` (novo), `main.py`, `usuarios.py`, `render.py`, `templates/usuarios.html`, `static/usuarios.js`, `static/estilo.css` e `web/tests/test_T0050_acesso.py` (mais os 3 testes de versão tocados no diff).
- **Prints olhados:** `sim-codigo/` (2-farois-aberto-pc, 3-salvo-pc, 4-novo-usuario-pc, 5-erro-nenhum-farol-pc e cel-a).
- **Resultado:** **10 achados em aberto** (3 médios, 7 baixos). O lote não sai até todos fecharem. Todos são do `modulo-web`.

## O que está limpo
- **`FAROIS[rid][1]` direto:** só aparece em `acesso.perfil_ve` (acesso.py:36). Em `main.py` sai também o `VERES` e o `PERFIS_PARCIAL`; o teste estrutural cobre isso. A única regra de perfil que ainda corre fora do `acesso` é o `render.farois_do_perfil` da página inicial (RD-0183).
- **Hex fora dos tokens:** nenhum. O CSS novo (estilo.css:714-788) usa só `var(--…)`, e os dois tokens novos `--t-apoio` e `--t-bloco` não repetem os que já existem.
- **Texto da tela:**
  - O "Do perfil" aparece uma vez por painel aberto. No "Novo usuário", das 8 cópias por perfil só a do perfil escolhido fica visível.
  - O confirmado "Acesso de … salvo. Liberado: …" (o que mudou) não repete o selo "2 faróis liberados" (o total).
  - O erro fica no lugar de sempre (`p.erro`), com o problema e a ação.
- **`usuarios.js`:** sem duplicação.
- **Redundância útil (manter):**
  - O selo da linha "1 farol tirado" junto com a marca "tirado" e o nome riscado no painel. A cor nunca vai sozinha (UX 4 e revisão de marca); a linha mostra a contagem e o painel mostra qual farol.
  - A nota "Liberado, o farol abre só no Resumo… O Painel Executivo abre completo." Ela diz o que o admin dá ao marcar (P4 A); entra na decisão, não é texto de funcionamento.

## Achados

| ID | Onde | Tipo | O que se repete | Impacto | Sev. | Dono |
|---|---|---|---|---|---|---|
| RD-0182 | `acesso.py:53-56` e `:98-105` | código | A regra de quem vê (RN-GER-018) está em 3 lugares: `pode_ver`, `liberado` (que nada em produção usa, só o teste) e `contagem`, que refaz à mão o "menos/mais/perfil". | manutenção (regra copiada) | média | modulo-web |
| RD-0183 | `render.py:285-305` + `main.py:303-309` | código | A regra "o liberado só abre a página inicial se nada do perfil sobrou" está em dois lugares: os faróis no `render` (laço `so_perfil`) e o Painel no `main` (`com_painel and perfil_ve` + o conserto `"/senha"→"/painel"`). E o `render` relê o perfil com `farois_do_perfil` (regra de perfil fora do `acesso`). | manutenção, regra partida | média | modulo-web |
| RD-0184 | `usuarios.py:213` | código | Formata a data à mão: `astimezone(MANAUS).strftime("%d/%m/%Y %H:%M")`, o que o `main.fmt_manaus` (filtro `manaus` do Jinja, main.py:55 e :91) já faz. | manutenção | média | modulo-web |
| RD-0185 | `usuarios.py:146-151` + `acesso.py:88-97` | código | O `normalizar` refaz os filtros que o `excecoes` acabou de aplicar ("conhecido" e "perfil vê"), e o `- menos` nunca tira nada. O `normalizar` só é chamado ali. | manutenção | baixa | modulo-web |
| RD-0186 | `usuarios.py:85` e `:176`; `main.py:22-24` | código | `{k: list((u.get("acesso") or {}).get(k, ())) for k in ("menos", "mais")}` escrito 2×; o módulo `usuarios` importado 2× (`import usuarios as usuarios_mod` só para `MSG_LISTA_MUDOU`). | manutenção | baixa | modulo-web |
| RD-0187 | `main.py:198` e `render.py:272` | código | A regra do "Atualizar visitas" (`PODEM_PEDIR` + vê o farol de Visita) está nos 2 lugares; a T-0050 teve de acrescentar o mesmo "vê o farol" duas vezes. | manutenção | baixa | modulo-web |
| RD-0188 | `acesso.py:12, 27, 114` × `render.py:266, 269` | código | Texto de tela sem constante: "Painel Executivo" e "Diretoria" (2× cada) e o nome curto do farol (`NOME_MENU.get(...)` / `removeprefix("Farol de ")`) feito de dois jeitos. | manutenção (nome muda em um, não no outro) | baixa | modulo-web |
| RD-0189 | `estilo.css` | layout/código | **(a)** :717 `.u-farois>summary::-webkit-details-marker` repete o :537 (o `.u-farois` também é `.u-det`); **(b)** :721 `.u-linha{position:relative}` é um 2º bloco do `.u-linha` do :539; **(c)** :772 `.u-selos{…}` no celular sobrescreve o `.u-selos` do :615, no mesmo `@media`; **(d)** a sombra `0 10px 28px var(--c-0000001f)` aparece 2× (:723 e :767); **(e)** `border:0` (:762) e `border-top:0` (:782) zeram uma borda que o `.f-rodape` nunca teve. | manutenção | baixa | modulo-web |
| RD-0190 | `test_T0050_acesso.py:183-194` | teste | O `test_RN_GER_018_cortes_de_dado_por_cima` repete o `…_liberado_ve_so_o_resumo`: o mesmo vendas com `pl_inadimplencia` liberado e o mesmo `?aba=cobrar` → 403. Os casos de gerente e analista não têm exceção nenhuma: testam a edição por perfil, que a T-0021 já cobre, e não o "por cima". | manutenção, tempo de CI | baixa | modulo-web |
| RD-0191 | `test_T0023_posvenda.py:459`, `test_T0035_pacote_por_farol.py:40`, `test_T0036_analista.py:353` | teste | A mesma versão literal `"0.10.0"` em 3 testes; cada subida de versão mexe nos 3. | manutenção | baixa | modulo-web |

## Propostas (antes → depois)

### RD-0182 · `acesso.py`
Antes: o `liberado()` (linhas 53-55) e o `contagem()` com dois `sum(...)` (linhas 98-105).
Depois: apague o `liberado` e reescreva o `contagem` sobre as funções que já existem:
```python
def contagem(usuario: dict) -> tuple[int, int]:
    """(tirados, liberados) com efeito para o usuário: os selos da linha."""
    perfil = usuario.get("perfil", "")
    vis, pad = visiveis(perfil, usuario.get("acesso")), padrao_do_perfil(perfil)
    return len(pad - vis), len(vis - pad)
```
- **Teste,** linha 49: `assert "pv_pedidos" in acesso.visiveis("vendas", u["acesso"]) - acesso.padrao_do_perfil("vendas")`.
- **Conferido:** 24.000 combinações aleatórias de perfil × `menos`/`mais` (com rid desconhecido), com **0 divergências** entre o `contagem` atual e o proposto.

### RD-0183 · página inicial numa regra só
`render.pagina_inicial(perfil, vistos=None, painel=None, padrao=None)`:
- `padrao` = `acesso.padrao_do_perfil(perfil)` (inclui `vc_painel`);
- sai o `do_perfil = dict(farois_do_perfil(perfil))`;
- o laço usa `r in padrao`;
- o Painel do perfil abre com `if painel and "vc_painel" in padrao: return "/painel"`;
- o fim vira `return "/painel" if painel else "/senha"`.

No `main.home`:
```python
destino = render.pagina_inicial(u["perfil"], vistos, com_painel, acesso.padrao_do_perfil(u["perfil"]))
```
Saem as linhas 307-309 (o `and perfil_ve` e o conserto `"/senha"`).
- **Conferido:** simulei as duas versões em 24.000 usuários aleatórios (8 perfis), com **0 divergências**.
- Sem `padrao` (testes antigos da T-0030/0034/0036/0045), vale o perfil puro, como hoje.

### RD-0184 · `usuarios.ultima_mudanca`
- **Antes:** `return {"quando": quando_formatado, "quem": …}`, com o `fromisoformat/astimezone/strftime` (linha 213).
- **Depois:** `return {"quando": r["quando"], "quem": r.get("quem", "")}`. Sai o `try/strftime`, e o filtro `manaus` já devolve o texto cru se a data vier inválida.
- **No `usuarios.html`:** `Alterado em {{ x.alterado.quando|manaus }} por {{ x.alterado.quem }}`.
- O teste de regex da linha 206 continua valendo.

### RD-0185 · `excecoes` + `normalizar`
Junte as duas numa só, `acesso.excecoes(perfil, marcados, antigo=None)`: ela devolve `menos = pad - marcados` e `mais = marcados - pad`, mais os rids desconhecidos do `antigo`. Com isso:
- o `normalizar` sai;
- `usuarios._excecoes` chama só `ac.excecoes(perfil, marcados, antigo)`;
- o teste da linha 64 passa a usar o `excecoes`.

### RD-0186 · `usuarios.py` / `main.py`
- **Função nova** em `usuarios.py`:
  ```python
  def _acesso_de(u): return {k: list((u.get("acesso") or {}).get(k, ())) for k in ("menos", "mais")}
  ```
- **Usos:** `obter` (linha 85) e `definir_acesso` (linha 176) passam a chamar `_acesso_de(u)`.
- **`main.py`:** apague o `from . import usuarios as usuarios_mod` e use `from .usuarios import PERFIS, Erro, ErroGravacao, Usuarios, MAX_ERROS, MSG_LISTA_MUDOU`; na linha 974, `raise Erro(MSG_LISTA_MUDOU)`.

### RD-0187 · "Atualizar visitas"
- **Antes:**
  - main.py:198 calcula `ctx["pode_visitas"]`;
  - render.py:272 refaz `"vc_visitas" in meus and perfil in visitas.PODEM_PEDIR`.
- **Depois:**
  - `menu_lateral(..., atualizar_visitas: bool | None = None)`: com `None`, vale a regra atual, para os testes antigos;
  - no `main`, calcule `pode_vis = u["perfil"] in PODEM_PEDIR and acesso.pode_ver(u, "vc_visitas")` uma vez e passe `atualizar_visitas=pode_vis` e `ctx["pode_visitas"] = pode_vis`.

### RD-0188 · nomes
- **Constantes no `render`:** `NOME_PAINEL = "Painel Executivo"`, `GRUPO_PAINEL = "Diretoria"` e `def nome_curto(rid): return NOME_MENU.get(rid) or FAROIS[rid][0].removeprefix("Farol de ")`.
- **`menu_lateral`:** usa as 3.
- **`acesso`:** `NOME_PAINEL = render.NOME_PAINEL`; `nome_do` = `NOME_PAINEL if rid == PAINEL else render.nome_curto(rid)`; e `"Diretoria"` vira `render.GRUPO_PAINEL`.

### RD-0189 · `estilo.css`
- **(a)** Apague a linha 717.
- **(b)** Ponha o `position:relative` no `.u-linha` da linha 539 e deixe na linha 721 só `.u-acoes .u-farois{position:static}`.
- **(c)** No celular, mude o `.u-selos` da linha 615 para `grid-column:1/-1;justify-content:flex-start` (fica junto o `.u-selos:empty{display:none}`) e apague o da linha 772.
- **(d)** `.u-farois[open]>form,.u-novo[open]>form.u-novo-form{box-shadow:0 10px 28px var(--c-0000001f)}` numa regra só, sem a sombra nas linhas 723 e 767.
- **(e)** Na linha 762, `.u-novo-form .f-rodape{padding:0;justify-content:flex-start}`; na linha 782, tire o `border-top:0`.

### RD-0190 · testes
Leve o `assert "telefone" not in v.get("/farol/pl_inadimplencia").text.lower()` para dentro do `test_RN_GER_018_liberado_ve_so_o_resumo` e apague o `test_RN_GER_018_cortes_de_dado_por_cima`.

Se quiser manter um teste de "corte por cima" com sentido, ele tem de usar exceção: por exemplo, um gerente com `pl_inadimplencia` tirado e liberado de volta continua sem o Cobrar. Hoje o gerente e o analista sem exceção só repetem a T-0021.

### RD-0191 · versão
- **Fica o literal:** só no `test_T0036_analista.py:353` (`VERSAO == "0.10.0"`).
- **Nos outros dois:**
  - `test_T0023_posvenda.py:459` → `== VERSAO`;
  - `test_T0035_pacote_por_farol.py:40` → `s["versao"] == VERSAO`;
  - nos dois, `from app import VERSAO`.

## Fora do meu escopo (encaminhar, não catalogado)
- **`designer-ux` / `testes`:** o `sim-codigo/4-novo-usuario-pc.png` mostra o "Novo usuário" com o bloco "Do perfil" **por cima** do campo Senha (campos e partes sobrepostos). E, na parte "Liberar", a caixa fica acima do nome em vários itens (Painel Executivo, Inadimplência, Metas Equipe, Giro de produtos, Divergências).
- **`testes`:** o `5-erro-nenhum-farol-*` não mostra o painel "Faróis" reaberto, embora o código mande `reabrir=alvo`. Além disso, `5-erro-nenhum-farol-cel-a.png` e `-cel-b.png` são o mesmo arquivo (md5 `fb8f8038…`). Vale confirmar que a simulação é do head `a5e723b`.

## Conferência
- `pytest web/tests/test_T0050_acesso.py` no head `a5e723b`: **22 passed**.
- Próximo RD livre depois deste parecer: **RD-0192**.

---

# Reteste · head `e0a17f6` (delta `a5e723b..e0a17f6`; o commit da T-0050 é o `36b059e`, o resto é merge do `main`, T-0023)

**Resultado: não liberado.** RD-0182 a RD-0191 fechados. A correção abriu **4 achados novos baixos** (RD-0210 a RD-0213), todos do `modulo-web`.

## RDs do parecer anterior

| ID | Situação | Evidência no `e0a17f6` |
|---|---|---|
| RD-0182 | ✓ fechado | `liberado` saiu; `contagem` = `len(pad - vis), len(vis - pad)`; o teste da linha 49 usa `visiveis - padrao_do_perfil` e soma `contagem(u) == (1, 1)` |
| RD-0183 | ✓ fechado | `render.pagina_inicial(..., padrao)` tem a regra inteira (`return "/painel" if painel else "/senha"`); no `main.home` saiu o conserto `"/senha"→"/painel"` |
| RD-0184 | ✓ fechado | `ultima_mudanca` devolve o ISO; o template usa `\|manaus` |
| RD-0185 | ✓ fechado | `normalizar` saiu; `excecoes(perfil, marcados, antigo)` |
| RD-0186 | ✓ fechado | `_acesso_de(u)` nos 2 usos; `usuarios_mod` saiu, `MSG_LISTA_MUDOU` importado direto |
| RD-0187 | ✓ fechado | `pode_vis` calculado uma vez em `main.pagina`, passado como `atualizar_visitas=` e `ctx["pode_visitas"]` |
| RD-0188 | ✓ fechado | `render.NOME_PAINEL`, `GRUPO_PAINEL`, `nome_curto`; `acesso` usa os três |
| RD-0189 | ✓ fechado | (a) linha antiga 717 saiu; (b) `position:relative` no `.u-linha` do :539; (c) `.u-selos` do celular só no :615; (d) sombra numa regra só; (e) `border:0`/`border-top:0` saíram |
| RD-0190 | ✓ fechado | "telefone" foi para `liberado_ve_so_o_resumo`; o novo `corte_por_cima_com_excecao` usa exceção (tira e devolve `pl_inadimplencia`) |
| RD-0191 | ✓ fechado | T0023:459 e T0035:40 comparam com `VERSAO`; o literal fica só no T0036 |

## Achados novos (delta)

| ID | Onde | Tipo | O que se repete | Impacto | Sev. | Dono |
|---|---|---|---|---|---|---|
| RD-0210 | `main.py:569`, `:759`, `:780` | código | `rid not in render.FAROIS or not acesso.pode_ver(u, rid)` escrito 3×, logo depois de criar o `exige_farol` (main.py:168-172), que faz exatamente isso | manutenção (regra de acesso copiada) | baixa | modulo-web |
| RD-0211 | `render.py:302`, `:304`, `:310` | código | O rid `"vc_painel"` literal 3× no `render`, enquanto o `acesso.PAINEL` e o `main.PAINEL_RID` guardam o mesmo valor | manutenção | baixa | modulo-web |
| RD-0212 | `estilo.css:761-762` | código | Duas regras seguidas para o mesmo elemento: `.u-novo-form .f-rodape{…}` e `.u-novo-form>.f-rodape{grid-column:1/-1}` | manutenção | baixa | modulo-web |
| RD-0213 | `test_T0050_acesso.py:208` | teste | `diretor` → 200 em `/visitas/atualizar` já está em `test_T0045_visitas.py:415-416` (`td.status_code == 200`) | manutenção, tempo de CI | baixa | modulo-web |

### Propostas
- **RD-0210.**
  - `tabelas_para_exportar`: `exige_farol(u, rid)` e depois `if not rel: raise PermissionError`.
  - `editar_get` e `editar_post`: `exige_farol(u, rid)` e depois `if u["perfil"] not in edicoes.EDITA: raise PermissionError`.
  - O teste estrutural já aceita `exige_farol(`.
- **RD-0211.** No `render`, `PAINEL_RID = "vc_painel"` junto do `NOME_PAINEL`/`GRUPO_PAINEL`. As 3 linhas usam `PAINEL_RID`, e o `acesso` usa `PAINEL = render.PAINEL_RID`, como já faz no `NOME_PAINEL`.
- **RD-0212.** Uma regra só: `.u-novo-form>.f-rodape{grid-column:1/-1;padding:0;justify-content:flex-start}`. O `.f-rodape` do "Novo usuário" é filho direto do form, então o seletor é equivalente.
- **RD-0213.** Apague a linha 208. O controle de "quem tem pelo perfil abre" fica com o `vendas` (linha 207), que a T-0045 não cobre.

## Conferência
- `compileall` do `web/app` limpo.
- Pytest no `e0a17f6` (`web/` extraído do head): T0050, T0034, T0030, T0036 e T0045 verdes; T0023 e T0035: 82 passed (1 deselecionado). O `test_RN_GER_011_padroes_pessoais_da_web_iguais_ao_bloco_do_contrato` (T0023) falha só no meu ambiente, porque lê `.coord/contratos/relatorio.md`, que não está na extração. Não é regressão.
- **Tela:** o delta não muda texto visível; o "Alterado em" sai no mesmo formato pelo filtro. Os PNGs de `sim-codigo/` são das 11h48, anteriores ao `36b059e` (13h04). O efeito visual do C1/C2 é do reteste do `designer-ux`.
- Próximo RD livre: **RD-0214**.

---

# Reteste 2 · head `8586ab7` (delta `e0a17f6..8586ab7`)

| ID | Situação | Evidência no `8586ab7` |
|---|---|---|
| RD-0210 | ✓ fechado | `tabelas_para_exportar`, `editar_get` e `editar_post` chamam `exige_farol(u, rid)`; no `web/app` não sobra `rid not in render.FAROIS or …` |
| RD-0211 | ✓ fechado | `render.PAINEL_RID = "vc_painel"`; `acesso.PAINEL` e `main.PAINEL_RID` apontam para ele. O único literal que sobra no `web/app` é o `pacotes.py:22`, de antes da T-0050 e fora do diff |
| RD-0212 | ✓ fechado | `.u-novo-form>.f-rodape{grid-column:1/-1;padding:0;justify-content:flex-start}` numa regra só |
| RD-0213 | ✓ fechado | a linha do `diretor` saiu do `test_T0050_acesso.py`; o controle fica no `vendas` |

**Delta além dos RDs:** a regra nova `.u-novo-form .f-partes-sem-perfil{column-gap:14px}` (≥ 701 px) só muda o `column-gap` do contexto "Novo usuário". Não repete regra, não tem hex e não cria texto. Sem achado novo.

**Resultado: liberado.** Nenhum achado em aberto no head `8586ab7`.

**Conferência:**
- `compileall` do `web/app` limpo.
- `pytest` de T0050, T0034, T0030, T0021 e T0045 rodou 5 vezes no head `8586ab7`. Deu 1 falha na 1ª rodada (o nome não foi capturado) e 144 passed nas 4 seguintes. Instável, a ver pelo `testes`; não é assunto de redundância.
