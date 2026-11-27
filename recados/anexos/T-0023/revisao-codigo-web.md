# Parecer do revisor-codigo: web da T-0023 v2 (Garantias, Devoluções e NCC, edição só do admin)

- **Data:** 27/11/2026 (Manaus) · **Revisor:** revisor-codigo.
- **Branch:** `modulo-web/T-0023-web` · **head revisado:** `3cc4fe06cfeff7a9d494fdfa71a74acb83d6730b` (web 0.7.0). Commit novo = revisão nova.
- **Base:** `origin/main` em `30ae65d`. O merge-base é `f3c4569`. O merge com o `main` de hoje não tem conflito (só o `.coord/quadro.md` entra).
- **Referência:** contrato §10.9 e §10.10 (`.coord/contratos/relatorio.md`, no `main`), `docs/desenho/T-0023.md`, RN-GER-006, 011, 012 e 014, RN-POS-005 e 006, e a edição da T-0021 v4 (`web/app/edicoes.py` do `main`).
- **Clone:** `/home/user/bapcentral`, só leitura (`git fetch`, `git diff origin/main...origin/modulo-web/T-0023-web`, `git show`, `git archive`), sem trocar a branch.

## Resultado

**Sem 🔴 · 🟡 2 · 🟢 9.** Não está aprovado: os 2 🟡 precisam de correção, com um teste para cada, num head novo.

## O que rodei (cópias fora do clone, na pasta de rascunho da sessão)

1. **Suíte web** (`git archive` do head; `cd web && pytest tests/`): **454 passed**, 0 falhas. `compileall` de `web/app` e `web/tests`: ok.
2. **Pacote real do robô:**
   - Fonte: `modulo-robo/T-0023-robo` em `f86adfa`, com o merge do núcleo `7ebfe4e`.
   - Montagem: `simular_pacote_farol(["vc_painel", *FAROIS_WEB], ...)` sobre as bases congeladas, `hoje=24/11/2026`, 11/2026. Saíram os 14 relatórios, 25 MB, e o JSON ficou só no rascunho.
   - Conferido com o `pacotes.validar_relatorio` desta web: **os 14 OK**.
   - Conferido com a web do `main` (0.5.0): os 11 de hoje OK e os 3 novos recusados ("relatório não aceito"). Isso mostra que as chaves proibidas novas não quebram nenhum farol existente.
3. **Ponta a ponta com o pacote real** (`TestClient`, numa cópia da suíte):
   - `POST /api/pacote` deu 200, e as 14 abas dos 3 faróis deram 200 para o admin;
   - matriz de perfis: o diretor tem 200 no Resumo e 403 nas 14 abas; gerente e pos_venda têm 200 em tudo; vendas tem 403 em tudo. Em `GET ...editar?novo=1` e no `POST`, os 4 perfis não admin recebem 403, e a fila fica com 0 linhas;
   - admin com CSRF errado no `POST` da linha nova: 403, fila com 0 linhas;
   - os cartões do pacote no Resumo do diretor: 6/6 nas Garantias, 5/5 nas Devoluções e 7/7 na NCC, texto a texto. A web não calcula número;
   - Garantia nova com o pacote real: o formulário traz o `padrao` do ticket que veio do pacote (G-0002 na base) e o `p_ticket` igual. O `POST` deu 303. Na fila: `NOVO-xxxxxxxx`, `novo: true` e `antes == {"ticket": "G-0002"}`, com `valores` = cod_cliente, reclamacao e ticket;
   - estado: o `uf_linhas` das Devoluções e da "NCC pendentes" segue a `FILIAL`. Nas Devoluções, 2 linhas têm UF do cliente diferente da filial e seguem a filial (P3 A, RN-GER-006). Com `uf=PA`: Devoluções 3 → 1 e NCC 11 → 3. A "Por cliente" da NCC mostra o `AVISO_SEM_ESTADO`;
   - **reenvio sem mudança de cada linha editável:** o formulário foi reenviado inteiro, como o navegador faz. NCC 11/11 e Devoluções 3/3 deram "Nada mudou". **Garantias deu 11/12** (🟡 1). As 5 células reais com "[removido]" (RECLAMAÇÃO e OBSERVAÇÃO) não foram reenviadas.
4. `node scripts/coord.mjs verificar --por-commit f3c4569..origin/modulo-web/T-0023-web`: **OK**, 2 commits com `Agente: modulo-web`, nenhuma violação. Só há arquivos em `web/`.

## 🟡 Corrigir antes do merge

### 🟡 1. Texto sem `caixa`: o valor de hoje com minúscula vai à fila sem ninguém ter mexido

- **Onde:** `web/app/edicoes.py:325-326` (`_checa`, ramo texto).
- **O que acontece:**
  - o código põe o digitado em maiúsculas (`v.upper()`) e compara com o `_norm_texto(atual)` sem maiúsculas;
  - no pacote real, 1 das 12 garantias tem o `CÓD. CLIENTE` com minúscula (o campo `cod_cliente` vem sem `caixa` do núcleo);
  - o reenvio sem mudança dessa linha dá **303, não "Nada mudou"**, e a fila recebe `cod_cliente` em maiúsculas;
  - pior: **qualquer** edição dessa linha (por exemplo, só a OBSERVAÇÃO) leva junto um `cod_cliente` que o admin não tocou, e o PC grava isso no `_GARANTIAS`.
- **Regra:** contrato §10.9.1, regras do texto livre, item 1 ("sem mudança, o campo não vai"). Regra 7 (dado digitado só muda quando a pessoa muda).
- **Origem:** a comparação é a mesma da T-0021 no `main`. Ela só aparece agora porque os lugares novos trazem valor digitado no PC com minúscula.
- **Pronto quando:**
  - a comparação aplica a mesma transformação nos 2 lados, por exemplo `ref = _norm_texto(atual)` e `ref = ref if c.get("caixa") else ref.upper()`, e `if v == ref: return None, None, ""`;
  - há um teste (`test_RN_GER_012_...`) com uma linha da fixture com minúscula num campo sem `caixa`: o reenvio sem mudança dá 200 "Nada mudou", e a edição de outro campo leva só esse campo.

### 🟡 2. Linha nova: depois de um erro, o formulário perde as datas e o ticket mostrado, e a garantia nasce sem data de solicitação

- **Onde:** `web/app/main.py:681`, `:685` e `:689` (`novo_ctx`, chamado com `f` depois do 400).
- **O que acontece:**
  - o navegador manda a data em ISO (`2026-11-27`);
  - o `novo_ctx` usa esse texto como `atual` e calcula `atual_iso = edicoes.iso_de_br(atual)`, e o `iso_de_br` de um ISO dá `""`;
  - reproduzido: `POST` com o ticket vazio dá 400, e a página volta com `c_dt_solicitacao` **vazio** (o mesmo vale para `dt_prazo` e `dt_retorno`);
  - o admin corrige o ticket e salva: 303, e a fila recebe `valores = {"dt_solicitacao": "", "cod_cliente": ..., "ticket": "G-0013"}`;
  - a garantia nova vai ao PC sem a DT. SOLICITAÇÃO, que é a base do prazo de 15 d.u. (RN-POS-005);
  - na mesma volta, o `p_ticket` escondido passa a ser o `padrao` do pacote **de agora** (`"mostrado": c["padrao_txt"]`), e não o que o formulário mostrou. Com um pacote novo no meio, o `antes.ticket` muda, e a regra do pacote atrasado (§10.9.2) deixa de valer.
- **Pronto quando:**
  - na volta com erro, a data do formulário é convertida, por exemplo com `atual = edicoes.br_data(bruto)` em `data`, que já aceita ISO, e o `atual_iso` sai certo;
  - o `mostrado` vem de `valores.get("p_" + campo, padrao)`;
  - há um teste (`test_RN_GER_012_...`): 400 por ticket vazio → a página traz `c_dt_solicitacao` = hoje (ISO) e o `p_ticket` enviado → o reenvio corrigido não leva `dt_solicitacao` em `valores`.

## 🟢 Sugestões

1. **"[removido]" em campo sem `caixa`** (`edicoes.py:325` e `:328`): a conferência vem depois do `upper()`, então "[REMOVIDO]" passa. Hoje nenhuma coluna limpa é campo sem `caixa`, então o risco é baixo. Confira antes do `upper()` ou sem diferenciar maiúsculas.
2. **Corpo acima do `FORM_MAX`** (`main.py:189`): o corpo é cortado e lido mesmo assim, e o último `textarea` pode chegar cortado e passar. O navegador não chega lá: 4 × 600 caracteres dão no máximo cerca de 22 KB codificados. Mesmo assim, 413 é mais seguro que o corte. A regra vem de antes desta tarefa.
3. **`p_ticket` sem conferência de formato** (`edicoes.py`, `valores_do_novo`): ele só passa pelo `_CTRL` e pelo corte em 80. O risco é baixo, porque só o admin chega aqui. Sugestão: o mesmo `RE_CHAVE` das chaves.
4. **Clique duplo em "Salvar" na garantia nova:** cada `POST` gera um `uuid` novo, então o clique duplo cria 2 garantias (G-0013 e G-0014 no PC). Sugestão: desabilitar o botão no envio, ou um token de formulário de uso único.
5. **Aviso de estado nas abas das Garantias:** o "Sem filtro por estado" aparece no Resumo e não aparece nas 4 abas de tabela, porque o farol não tem seletor e a faixa só avisa quando `tela` existe. O §10.10.1 diz "leva o aviso". O designer-ux confirma se basta o do Resumo (RD-0023).
6. **Testes:**
   - `test_T0023_posvenda.py:189`: a asserção com `or` passa quase sempre. Melhor conferir que todas as linhas com `uf=PA` são da `FILIAL PA`;
   - `:90`: a docstring diz 400, e o teste confere 422;
   - faltam os testes dos 2 🟡.
7. **Redundância:** o `form_ctx` × `novo_ctx`, as mensagens repetidas e o "Sugestão do PC" já estão no parecer do corretor (RD-0140 a RD-0145) e não repito aqui. Na correção do RD-0140, o `main.py:665` e o `:687` deixam de chamar a privada `edicoes._mais_um_ano`: uma função `edicoes.faixa_data(c, hoje)` serve aos 2 formulários e ao `_checa`.
8. **Código de produto com 8 dígitos parece telefone:** o `FONE` do bloco `padroes-pessoais` recusa um código só com 8 dígitos. No "Histórico de compra" real, 1 de 4.949 códigos seria recusado num `cod_produto` da garantia nova. A regra é do contrato (§10.9.1 vale para todo `texto`), então é assunto do engenheiro-software, não do PR.
9. **Ordem com a T-0045** (`modulo-web/T-0045-visitas`, 0.6.0): o merge das 2 branches dá conflito em `web/app/__init__.py` (VERSAO), em `web/app/edicoes.py` (`Fila.registrar`, que a T-0045 generaliza) e em `web/tests/test_T0035_pacote_por_farol.py`. Com a T-0045 no `main` antes, como a 0.6.0 pede, esta branch precisa do merge do `main`, e isso gera um head novo e uma revisão nova.

## O que está certo (conferido)

- **Só o admin edita (RN-GER-012):**
  - `editar_get` e `editar_post` dão 403 antes de ler o formulário;
  - o `novo_tela` não manda nem o botão nem a contagem para quem não é admin;
  - o CSRF vale também no ramo `novo=1`, porque passa pelo mesmo `formulario()`.
- **O diretor só vê o Resumo (RN-GER-014):** pelo `VE_TABELAS` dos 3 `rid`, com 403 nas abas e no Exportar.
- **`antes.ticket` e nenhum número calculado:**
  - o `padrao` do ticket vem do pacote;
  - a chave é `NOVO-` + 8 hexadecimais (`uuid4`);
  - vai só o que difere do padrão, mais o obrigatório;
  - sem nada além do padrão, a resposta é 400 com `MSG_NOVO_VAZIO`.
- **O contato fica fora:**
  - o `FORA_POR_TABELA` recusa o pacote com `CONTATO CLIENTE`;
  - o `erro_spec` recusa campo `contato*`, `fone*` e `telefone*`, e também coluna ou rótulo de contato;
  - a tela e o formulário reais não têm "CONTATO".
- **Os tetos vêm do pacote:**
  - `max` de 1 a 600, só em `texto` e `numero`;
  - o `maxlength` usa o `c.teto`;
  - o corte do valor bruto é em `max` + 100;
  - a `multilinha` só vale com `caixa`.
- **O "[removido]" nunca volta ao PC:** o texto é recusado quando muda e não vai quando não muda. Os padrões são iguais ao bloco `padroes-pessoais`, e o `tem_pessoal` é equivalente a `texto_sem_contato(v) != v` (o mesmo split do `VALOR_RS`).
- **Estado:** a web só usa o `uf_linhas` do robô, que é a `FILIAL`.
- **A edição da T-0021 é reusada:** o `valores_do_form` passou a chamar o `_checa`, que a linha nova também usa. Não há cópia da validação.
- **Versão:** 0.7.0 no `/saude`.
- **Fixtures fictícias:** "CLIENTE FICTICIO nn", códigos `9xxxxx` e `FILIAL XX`. As senhas são só de teste e o token sai de `secrets`. Não há segredo nem dado pessoal no diff.
- **O resto do checklist:**
  - nada fora de `web/`;
  - nenhum dado digitado nem config de raiz tocado;
  - `bap_dados.VERSAO` = 27 (o arquivo não muda).

## Condições do merge (fora deste parecer)

- Ainda não há PR nem CI no head `3cc4fe0` (consultei pela API REST). O merge pede CI verde no head SHA.
- O parecer de UX e marca do mesmo head (`revisao-ux-marca.md`) tem **🔴 2 · 🟡 7** em aberto, e o do corretor tem os RD-0140 a RD-0145.

---

# Reteste: 27/11/2026 (Manaus), heads novos da T-0023

| Parte | Branch | Head retestado | Parecer |
|---|---|---|---|
| Web | `modulo-web/T-0023-web` | `928b3ea007b44d95cb13afb76088afb47675b8b2` | **aprovado** · 🟢 3 |
| Núcleo | `modulo-farois/T-0023-nucleo` | `f0af112` | **aprovado** (N1 a N3 fechados; N4 com a simulação) · 🟢 2 |
| Robô | `modulo-robo/T-0023-robo` | **`08b042f`**: o head andou depois do `371e04c` | sem 🔴 · 🟡 1 (condição de merge) · R1 e R2 seguem como condição |

## O que rodei

- **Web `928b3ea`:** a suíte web deu **459 passed** (eram 454; entraram 5 testes), e o `compileall` está ok.
- **Ponta a ponta, web `928b3ea` com o pacote real do robô `08b042f`:**
  - o pacote real foi aceito nos 14 relatórios; a web do `main` só recusa os 3 novos;
  - a matriz de perfis, o CSRF e a fila vazia ficaram como no primeiro parecer;
  - os cartões do Resumo do diretor: 6/6, 5/5 e 7/7.
- **Reenvio sem mudança de cada linha editável:** Garantias **12/12** (era 11/12), NCC 11/11 e Devoluções 3/3 deram "Nada mudou".
- **Linha nova depois de um 400:**
  - a página volta com `c_dt_solicitacao` = hoje (ISO), e não vazio;
  - o reenvio corrigido grava `valores = {"cod_cliente", "ticket"}`, sem `dt_solicitacao` vazio.
- **Núcleo `f0af112` × `7ebfe4e`:**
  - `montar` dos 14 faróis com `hoje=24/11/2026` e o mesmo `PYTHONHASHSEED`: tudo igual, menos o `max: 40` do `ticket` (RD-0136);
  - `pl_devolucoes` de SET, OUT e NOV: só muda o dia 06/10 do "% devolvido do faturado · dia a dia", que ia de −1.636,01 para 0. Os cartões, o "Por vendedor (12 meses)" e o "Devoluções" do Painel Executivo (R$ 5.552, 4,9%) não mudam;
  - a suíte da raiz no núcleo, com Python 3.12 e tkinter num venv de rascunho: **652 passed, 2 xpassed**.
- **Robô + testes `25b2633`:** `test_T0021_edicao_web_robo`, `test_T0023_*`, `test_T0013`, `test_T0017` e `test_T0024_trava`:
  - com o robô `08b042f`: **252 passed, 1 skipped**;
  - com o robô `371e04c`: falha o `test_RN_GER_011_a_frase_do_texto_leva_o_teto_do_campo`, que exige que o `MOTIVO_TEXTO_WEB` não exista.
- **Robô com os testes do `main`** (`tests/test_T0021_edicao_web_robo.py`):
  - `371e04c`: 30 passed;
  - `08b042f`: **erro de coleta** (`AttributeError: MOTIVO_TEXTO_WEB`).
- **`verificar --por-commit`** nas 3 branches: OK. `bap_dados.VERSAO` = 27.

## Web `928b3ea`: aprovado

- **🟡 1 fechado:** `_checa` compara os 2 lados no mesmo formato (`v, ref = v.upper(), ref.upper()` sem `caixa`). Teste: `test_RN_GER_012_texto_sem_caixa_com_minuscula_reenviado_sem_mudar_da_nada_mudou`.
- **🟡 2 fechado:** o `edicoes.campo_tela` converte a data (`br_data`, que aceita ISO), e o `edicoes.mostrado(valores, c)` devolve o `p_` enviado. Teste: `test_RN_GER_012_linha_nova_volta_do_erro_com_datas_e_ticket_mostrado`.
- **Fechados também:**
  - 🟢 1: o "[removido]" é conferido com `casefold`, com teste;
  - 🟢 3: o `p_ticket` passa pelo `RE_CHAVE`;
  - 🟢 7 e RD-0140 a 0145: um `campo_tela` para os 2 formulários, o `data_max` público, as mensagens únicas (`MSG_SEM_NOVO`, `TITULO_SEM_NOVO`, `MSG_FALHA_FILA`) e o `volta_ed`; o "Sugestão do PC" só aparece quando o ticket mudou; o aviso de dado pessoal aparece uma vez só; o `_agrupa_ncc` serve às 3 tabelas da NCC.
- **Cidade das Garantias no popup:** a grade fica com 8 colunas, e a CIDADE vai ao bloco "Cliente". A chave e os `cel` não mudam, e a `CIDADE` segue no pacote.
- **UX:** o formulário largo (`ed-largo`, mais de 6 campos) vai em 4 colunas no PC, com alvos de 44 px no celular. O resumo da linha no Editar segue a `GRADE` (chave, nome e UF). O cliente só com o nome na grade das Devoluções (`cliente_so_nome` com `NF DEV.`) só mexe na tela.
- 🟢 **W1.** O `main.py` (`resumo_da_linha`) usa a privada `tabelas._RE_COD_NOME`. Ela pode ficar pública, ou o resumo pode ir para o `tabelas`.
- 🟢 **W2.** O `estilo.css` troca a rolagem lateral das `.filtros.recortes` no celular pela quebra de linha **em todos os faróis**, não só nos 3 novos. O designer-ux confere os outros faróis no reteste dele.
- 🟢 **W3.** Ficam abertos do primeiro parecer: o 🟢 2 (corte em vez de 413), o 4 (clique duplo), o 5 (aviso de estado nas abas das Garantias), o 6 (asserção fraca da `FILIAL`), o 8 (código de 8 dígitos) e o 9 (conflito com a T-0045 e um reteste depois do merge do `main`).

## Núcleo `f0af112`: aprovado

- **N1 fechado:** o `painel_farol.pct_do_liquido` dá `None` com o líquido ≤ 0, e o `_juntar("pct")` e os 4 usos do farol e do Painel passam por ele. Nos outros faróis, nada mudou em NOV/26 (conferido acima).
- **N2 fechado:** um `_uteis_ate_ontem(ctx)` serve ao `montar` e ao `ao_mudar` da NCC.
- **N3 fechado:** o `_liquido` é reusado no `_eventos_faturamento` e no `devolucoes()`. O Painel usa o `atual["real"]`, e o `_painel_devolucoes` usa o `_eventos_faturamento(liquido=True)`. Os números são iguais aos de antes (conferido).
- **N4:** a simulação está em `antes-depois-devolucoes.md`.
- **RD-0139:** `PADRAO_NOVA_GARANTIA`, `ORIGEM_GARANTIA_FAROL`, `prazo_padrao_txt` e `campos_garantia_a_gravar` são funções puras no núcleo, e o robô as chama.
- 🟢 **N6.** O `antes-depois-devolucoes.md` diz que o dia 06/10 fica "—". No gráfico do Resumo, a série leva **0** (`None` vira 0), e um 0% num dia com devolução engana. Sugestão: mandar `null` se o bloco `barras` da web aceitar; senão, corrigir a frase do anexo para "0 no gráfico".
- 🟢 **N7.** Fora da T-0023: o `vc_painel`, o `pl_giro` e o `pl_frw` mudam a ordem das linhas empatadas entre um processo e outro (ordem de `set`, `PYTHONHASHSEED`). Com a mesma semente, saem iguais. Isso vem de antes, mas faz o "Mudou no PC?" e o sha do pacote variarem sem dado novo. Vale um RD ou uma tarefa à parte.

## Robô `08b042f` (o pedido citava o `371e04c`)

**O `__getattr__` do `371e04c` é aceitável?**
- Como ponte temporária, sim: o `__getattr__` de módulo (PEP 562) que devolve `motivo_texto_web()` é limpo e não muda o comportamento.
- Mas ele já saiu no `08b042f` (RD-0135), e os testes `25b2633` exigem que ele não exista. Hoje vale o `08b042f`.

🟡 **R6. Ordem do merge do robô (condição, não defeito):**
- com o `08b042f`, o `tests/test_T0021_edicao_web_robo.py` do `main` quebra na coleta (`ba.MOTIVO_TEXTO_WEB`), e o CI do PR do robô fica vermelho;
- **Pronto quando**, uma das duas:
  - (a) a troca do `test_T0021_edicao_web_robo.py` que vem nos testes `25b2633` (`_MOTIVO_TEXTO_60` com `hasattr`, que passa no robô do `main` e no novo) entra no `main` antes do PR do robô;
  - (b) o robô volta com a ponte do `371e04c` até os testes entrarem, e ela sai num commit depois.

**O resto do robô:**
- o `_campos_garantia_web` traduz os campos do `CAMPOS_EDICAO_GARANTIA` do núcleo (RD-0134);
- o teto, inclusive o do ticket (40), vem do `max_texto_edicao`, e sai o `MAX_TEXTO_WEB`;
- sem o `_RE_PESSOAL_EDICAO_WEB` e o `REMOVIDO_WEB`, sobram só o `texto_sem_contato` e o `REMOVIDO` do núcleo (RD-0137 e 0138);
- o `plano_garantia_web` passa pelo `campos_garantia_a_gravar` com o `fer`: o prazo igual ao padrão fica em branco, com a solicitação da garantia existente na edição, e a origem vai só na nova;
- um `_corte_aba_web` serve aos 2 cortes (RD-0146).
- R1 (o diff ainda leva o `relatorios_nucleo.py` e o `painel_farol.py` até o squash do núcleo e o merge do `main`) e R2 (a web v2 vai antes) seguem como condições.
- 🟢 R3: o ticket não passa pelo `texto_sem_contato`; continua aberto, agora com o teto de 40.

## Para o merge (ordem do §10.9.6)

1. Testes PR 1 (destrava), com a troca do `test_T0021_edicao_web_robo.py` (R6 a).
2. Web `928b3ea`, ou o head depois do merge com a T-0045, com reteste.
3. Núcleo `f0af112`.
4. Robô, com o merge do `main` (fecha o R1).
5. PC só leitura.
6. Testes finais.

Cada um com CI verde no head.

---

# Reteste 2: web `db0974a` e ponte do `test_T0021` (27/11/2026, Manaus)

**Web `modulo-web/T-0023-web` @ `db0974abca9bfdf25e7e3242b29abc3fbef314d3`: aprovado.** Este parecer troca o do `928b3ea`.

- **Delta revisado:** `git diff 928b3ea db0974a`, 4 arquivos.
  - **RD-0152:** a `tabelas.cod_e_nome` é pública e serve ao `cliente_so_nome` e ao `resumo_da_linha`. Isso fecha o 🟢 W1. O comportamento é o mesmo: só o nome quando há código, e o valor inteiro quando não há.
  - **RD-0153:** o `.ed-botoes` repetido saiu e ficou um só.
  - **Cancelar:** a cor `--texto` agora vem por seletor mais específico, `.ed-botoes a.ed-cancelar`.
  - **Fixture:** o cinza ficou `#E3E8E4`/`#5E6B63`, ainda fictício.
  - **Rótulos do gráfico:** `.gb-col .gb-rot` centralizado. Vale em todos os faróis com gráfico de colunas, então entra no 🟢 W2 para o designer-ux.
- **Suíte web no `db0974a`:** 459 passed. `compileall` ok. `verificar --por-commit 928b3ea..db0974a`: OK.

**🟡 R6 do robô: fecha com a ponte**, com uma condição.
- A branch `testes/T-0023-ponte-t0021` está em `06107f4`.
- Ela só muda o `tests/test_T0021_edicao_web_robo.py`, com 8 linhas a mais e 2 a menos.
- Rodei esse teste com o robô do `main`: 30 passed. Com o robô `08b042f`: 30 passed.
- `verificar --por-commit`: OK.
- **Condição:** a ponte entra no `main` antes do PR do robô, com CI verde no head dela. O PR do robô é aberto ou atualizado com o merge do `main` que já traz a ponte, e o CI dele roda verde nesse head. Com isso, o R6 fecha. R1 e R2 seguem como condições de merge.

---

# Reteste 3: merge do `main` (T-0045) na web, PR #154 @ `17722341e2a16aab6c76e2bb195ef0885e64bd13` (27/11/2026, Manaus)

**Aprovado** · 🟢 1. Este parecer substitui o do `db0974a`. A base é o `main` em `4728880` (#151, web 0.6.0 da T-0045).

## Como conferi

- `git show --remerge-diff 1772234`: mostra só a resolução dos 4 conflitos, descontando o que veio do `main`. São eles:
  - `web/app/__init__.py`;
  - `web/app/edicoes.py`;
  - `web/app/static/estilo.css`;
  - `web/tests/test_T0035_pacote_por_farol.py`.
- `main.py`, `pacotes.py`, `render.py` e `_bc3_cab.html` entraram por merge automático. `visitas.py`, `visitas.html` e `config.py` ficaram iguais ao `main` (`git diff 4728880 1772234` vazio nesses arquivos).
- **Suíte web no `1772234`:** **523 passed**, igual ao que o modulo-web relatou. A T-0045 tem 50 testes, entre eles RN-VIS-005 a 008: pausa por código, retomar só pelo admin, tentativa que conta na concessão e lote com dado pessoal que pausa. `compileall` ok.
- **Ponta a ponta com o pacote real do robô `08b042f`** (as mesmas checagens dos retestes anteriores):
  - o pacote foi aceito;
  - "Nada mudou" em todas as linhas editáveis: Garantias 12/12, NCC 11/11 e Devoluções 3/3;
  - a garantia nova vai na fila com `NOVO-…`, `novo: true` e `antes.ticket`;
  - depois do 400, a data e o ticket mostrado voltam;
  - a matriz de perfis e o CSRF dão 403 com a fila vazia;
  - os cartões do diretor batem: 6/6, 5/5 e 7/7.
- **Import tardio:** importei, em processos novos, um módulo primeiro de cada vez (`render`, `visitas`, `edicoes`, `pacotes`, `tabelas` e `main`). Em todos, `edicoes._contato("CONTATO CLIENTE")` deu `True` e não houve erro de import circular.
- `verificar --por-commit db0974a..1772234`: OK. CI do #154 no head: `conferir` ainda em andamento quando conferi; GitGuardian ok.

## `edicoes.py`: nenhuma das 2 filas perde comportamento

- **`Fila.registrar` (T-0021/T-0023)** monta `campos` com `id`, `usuario`, `rid`, `tabela`, `modulo`, `chave`, `valores` e `antes`, mais `novo: true` na linha nova, e chama o `registrar_item` da T-0045. Na linha gravada, só muda a ordem das chaves:
  - o `quando` é o mesmo (`_quando` = `astimezone(MANAUS)` e o mesmo formato);
  - o seq é gasto antes da linha;
  - a tranca é a mesma.
  A troca no lugar, o "Nada mudou", o `situacao`, a `marca` e o `contagem_novas` não mudam: o reenvio e a contagem "N · Aguardando o PC" passaram.
- **`registrar_item` (T-0045)** ficou igual ao do `main`: `antes_de_gravar(seq)` dentro da tranca e antes da linha, e o `**campos`. As filas são separadas por `subpasta` e `prefixo`. O `tentativas_hoje` e a pausa por código ficam no `visitas.py`, que não mudou.
- **Import tardio de `coluna_fora`** em `_contato()`: é seguro, porque só roda em tempo de chamada (no `erro_spec`, ao receber o pacote), com todos os módulos carregados. O custo é uma busca no `sys.modules`.
- 🟢 **M1.** O `from .render import coluna_fora` ficou **antes** da docstring de `_contato` (`edicoes.py:86`). A docstring virou uma expressão solta, e o `_contato.__doc__` passa a ser `None`. Sugestão: pôr o import depois da docstring, sem mudar o comportamento.

## Outros conflitos

- `__init__.py` fica em 0.7.0, e o `test_T0035` também confere 0.7.0. Isso está certo, porque a T-0045 entrou como 0.6.0.
- No `estilo.css`, os blocos `.ed-*` (T-0023) e `.vz-*` (T-0045) ficam inteiros e seguidos, e nenhuma regra se perdeu.
- O `FORM_MAX` passa para 32 KB em todos os formulários, inclusive os da T-0045. O contrato §10.9.1 permite, e nenhum teste da T-0045 depende dos 16 KB.

**Condição de merge:** CI verde no `1772234`.

---

# Reteste 4: PR #154 @ `5c467217a197429e49c95232eb535e443a4d287a` (27/11/2026, Manaus)

**Aprovado.** Este parecer substitui o do `1772234`. Li o delta inteiro (`git diff 1772234 5c46721`, 2 arquivos), e o comportamento não muda.

- **M1 fechado:** o import tardio veio para depois da docstring, e `edicoes._contato.__doc__` volta a ser a docstring (conferido).
- **RD-0165:**
  - o `_checa` usa o `data_max(hoje)`, que é o mesmo `_mais_um_ano(hoje)`;
  - a `_texto_form(c, s)` (normaliza o texto e põe em maiúsculas sem `caixa`) troca as 2 contas iguais, no `_checa` (os 2 lados) e no obrigatório do `valores_do_novo`;
  - o resultado é igual, linha a linha.
- **RD-0164:** os alvos de toque do celular voltam a um `@media(max-width:700px)` só, agora com `var(--alvo)` (= 44px, `estilo.css:96`). O bloco subiu, mas `.ed-botoes .ed-cancelar` (0,2,0) segue mais forte que o `.ed-cancelar{min-height:36px}` que vem depois, e nenhuma regra posterior mexe nos outros seletores. A tela fica igual.
- **Suíte web no `5c46721`:** **523 passed**. `compileall` ok. `verificar --por-commit 1772234..5c46721`: OK.
- **Condição de merge:** CI verde no `5c46721`.

---

# Reteste 5: testes `d17632a`, ponte #153 `12ce390` e robô `03e9c9d` (27/11/2026, Manaus)

**Ordem decidida:** web #154 (no `main`, `e1d80a8`) → núcleo #155 → ponte #153 → testes → robô → contrato.

| Head | Parecer |
|---|---|
| Ponte `testes/T-0023-ponte-t0021` @ `12ce390` (#153) | **aprovado** |
| Testes `testes/T-0023-testes` @ `d17632a` | **aprovado como PR futuro**, com 1 condição de merge (C1) e 1 🟡 ligado ao robô (T5) |
| Robô `modulo-robo/T-0023-robo` @ `03e9c9d` | **aprovado no delta** (RD-0163). O R1 segue: o diff contra o `main` ainda leva o `relatorios_nucleo.py` e o `painel_farol.py` até o #155 entrar e o robô fazer o merge do `main` |

## Como conferi (repositório de rascunho, sem tocar no clone)

- **Cenário A, sem o robô:** `main` `ce7149e` + núcleo `9796772` + ponte `12ce390` + testes `d17632a`.
  - `pytest tests/` (Python 3.12 com tkinter): **704 passed, 2 skipped, 2 xpassed**;
  - os 2 skipped são os módulos `test_T0023_robo.py` e `test_T0023_valor_regra.py` inteiros ("robô da T-0023 v2 ainda não entrou");
  - os 2 xpassed são da T-0027 (`xfail` não estrito), que já existiam;
  - `web/tests`: **523 passed**.
- **Cenário B:** o cenário A + robô `03e9c9d`. `pytest tests/`: **813 passed, 0 skipped**, 2 xpassed (os mesmos).
- **Diferença para os números do testes** (671 e 780): são os +33 testes que o `main` ganhou depois (T-0036 e T-0045). A diferença entre A e B é igual nos dois relatos.
- **Merge:** o núcleo, a ponte e o robô entram sem conflito. O testes `d17632a` **conflita no `.coord/diario/testes.md`** com o `main` de hoje (C1).
- `verificar --por-commit`: OK nas 3 branches (testes com 9 commits, ponte com 1 e robô `08b042f..03e9c9d` com 2).

## Ponte #153 `12ce390`: aprovado

- Contra o `main`, o diff é só o `tests/test_T0021_edicao_web_robo.py` (8 linhas a mais e 2 a menos), e ele é igual ao do testes `d17632a`. O `12ce390` é só o merge do `main` sobre o `06107f4` já revisado.
- O `_MOTIVO_TEXTO_60` usa o `motivo_texto_web(60)` quando o robô tem a função e o `MOTIVO_TEXTO_WEB` quando não tem. Verde nos 2 cenários. Isso fecha o 🟡 R6.

## Testes `d17632a`: aprovado como PR futuro

**A trava, com o robô presente, não afrouxou nas regras:**
- `problemas_escopo(ba)` com o robô `03e9c9d` dá `[]`;
- trocar o estado das Devoluções para a UF do cliente reprova com "regra de UF ('UF', 'uf'), esperado ('FILIAL', 'filial')" (RN-GER-006, P3 A);
- a `FORA_DA_LISTA` e a `FORA` passam do `pl_garantias` para o `vc_markup`, com o mesmo efeito;
- `FAROIS_PERMITIDOS = obrigatórios | FAROIS_T0023`, conferido por igualdade.

**Com o robô presente, nada é pulado:** os skips dependem de `"pl_ncc" in FAROIS_WEB` e `CAMPOS_LUGAR_WEB` (módulo) e de `hasattr(rn, ...)` (núcleo f0af112). Todos ficam falsos no cenário B, que deu 0 skipped.

🟡 **T5 (ligado ao robô, não a este PR). Afrouxamento latente depois que o robô entrar:**
- O `FAROIS_T0023` continua "permitido, não obrigatório".
- Um robô futuro que tire o `pl_ncc` do `FAROIS_WEB` e do `_TABELA_RECORTE_WEB` passa na trava, porque a `problemas_escopo` dá `[]` (conferido). Além disso, os 2 módulos `test_T0023_robo.py` e `test_T0023_valor_regra.py` se pulam inteiros: o CI fica verde sem nenhum teste da T-0023 do robô.
- Era o 🟢 T3 do primeiro parecer. Com a ordem decidida, ele vira condição.
- **Pronto quando:** logo depois do robô no `main`, e antes do contrato, um PR do testes:
  - (a) passa o `FAROIS_T0023` para os obrigatórios;
  - (b) troca o `pytest.skip(..., allow_module_level=True)` dos 2 módulos por falha, ou por um teste que exige os 3 `rid` no `FAROIS_WEB`.

**C1 (condição de merge):** o testes precisa de um merge do `main` (o conflito no `.coord/diario/testes.md` é só de linhas acrescentadas). Isso gera um head novo, e eu revejo só o delta.

**Dado pessoal nas fixtures:** nenhum dado real.
- Os casos de recusa usam valores de exemplo: "92 99123-4567", "x@y.com", "12.345.678/0001-90", "123.456.789-00", "92999998888", "9233334444" e "33334444".
- Os nomes são "FULANO FICTICIO" e "RESPONSAVEL FICTICIO", e os tickets são `G-00nn`.
- Toda gravação vai para o `tmp_path`. Nenhum `gravar`, `aplicar_edicao_web`, `sincronizar_edicoes_web` ou `write_text` aponta para a `RAIZ`, que só é lida pelo `montar`.
- O teste do JSON dos 3 faróis procura documento e e-mail em toda string, e telefone no texto livre e nos nomes. Ele não imprime conteúdo.

## Robô `03e9c9d` (RD-0163, desde o `5176c2d`)

- O `_MOVIMENTOS_WEB = (Path(BKP_BAPTOOLS), "Relatorio_Movimentos_BAP_Protheus_*.xlsx")` troca as 7 tuplas iguais do `_FONTE_BAIXADO_WEB` (pv_pedidos, pl_entregas, lote 2, vc_meta, pl_devolucoes e pl_garantias). O valor é idêntico, e a NCC e o Visita não mudam.
- A trava (`_fonte_ok`) e os 813 testes do cenário B passam.
- O `5176c2d` (`_corte_aba_web`, RD-0146) já estava no reteste 1.
- R1 segue: abrir ou atualizar o PR depois do #155 no `main`, com o merge do `main`, para o diff ficar só com o `bap_automation.py`.
