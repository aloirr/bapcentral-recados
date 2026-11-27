# T-0054: revisão de código (revisor-codigo)

- Heads revisados (diff `origin/main...<head>`, base `57cf6fa`):
  - web: `modulo-web/T-0054-entregas-edicao` em **c9feadb0859c54dad7fca468576200b122351675** (antes, 1862a53);
  - robô: `modulo-robo/T-0054-entregas-edicao` em **f0b895b3c2837bb4ff142d74cb55cd747a252705**;
  - contrato §10.9.7 conferido no `engenheiro-software/T-0054-desenho` em 4c0a990, que já traz a linha do `pl_fretes`. Regras: PR #178, já no `main` (7f8d980).
- Testes:
  - web: `pytest web/tests -q` deu **612 passed** no c9feadb (no 1862a53 foram 613; o c9feadb tirou 1 teste duplicado, RD-0255);
  - robô: `pytest` arquivo por arquivo, com xvfb e `/usr/bin/python3.12`. Os 48 arquivos de `tests/` passaram, sem falha (só os skips e xpassed de sempre);
  - `compileall` limpo nos dois heads.
- `coord verificar --base origin/main`: OK no modulo-web (11 arquivos) e no modulo-robo (1 arquivo).
- Sondas minhas, num teste temporário que já apaguei, todas com o pós-venda:
  - CSRF ausente: 403;
  - `rid` trocado para `pv_pedidos`, `pl_ncc`, `pl_garantias` ou `pl_devolucoes`: 403;
  - `tab=Garantias` no `pl_entregas`: 403;
  - `novo=1` nas Entregas: 404 ou 409. `novo=1` na Garantia (GET e POST): 403;
  - XSS no que foi digitado: sai escapado, com um só `aria-invalid`. A fila ficou vazia em todas.
  - No robô, `validar_edicao_web`: `gerente`, `None`, `""` e `["admin"]` dão `MOTIVO_PERFIL_WEB`; `pos_venda` e `admin` passam pelo perfil; o `pos_venda` no NCC é recusado; o Fretes cai em `MOTIVO_LUGAR_WEB`.

## Parecer: nenhum 🔴, dois 🟡

### 🟡 corrigir antes do merge
1. **A branch da web conflita com o `main`.** O conflito está em `web/app/__init__.py` e em `web/tests/test_T0036_analista.py`, porque o `main` (a86aa85, T-0052) já está na web 0.10.1.
   - O que fazer: trazer o `main` para a branch com merge, sem rebase. A VERSAO fica 0.12.0, ou o número que o gerente fixar pela ordem de merge (desenho §7).
   - Depois, rodar `web/tests` de novo. O commit novo pede revisão nova.
2. **A linha nova só do admin está garantida por acaso, não por regra.** A RN-POS-011 diz "a linha nova e os outros faróis seguem só do admin", e o contrato §10.9.7 diz "a linha nova continua só do admin". Mas o código decide de outro jeito:
   - `main.py`, em `novo_tela`, no `editar_get` com `novo == "1"` e no `editar_novo`, decide pelo `pode_editar`. A docstring do `novo_tela` (c9feadb) agora diz "só quem edita o lugar", o contrário do contrato.
   - **Hoje isso não abre a criação de linha para o pós-venda.** Há três travas independentes:
     - o robô só põe `edicao.novo` onde `EDICOES_WEB` tem `"novo": True`, ou seja, só na Garantia;
     - a web recusa o pacote com `novo` fora de `edicoes.LUGARES_NOVO`, que é só a Garantia (`erro_spec`, `edicoes.py:151`);
     - o `validar_edicao_web` recusa `novo` onde o lugar não tem `novo`.
   - O risco: no dia em que o `LUGARES_NOVO` ganhar um lugar do `EDITA_LUGAR` (Entregas ou Fretes), o pós-venda passa a criar linha sem que ninguém decida isso.
   - Correção, de uma linha por ponto: no caminho do `novo`, exigir `u["perfil"] in edicoes.EDITA`, voltar a docstring para "só o admin" e criar um `test_RN_POS_011_linha_nova_so_do_admin`.
   - Robô, opcional: com `novo` e com `perfil`, exigir `admin`.

### Pendência fora destas branches (segura o merge do robô)
- O `tests/test_T0054_edicao_entregas.py` do `testes` (desenho §5, item 5) ainda não existe. Faltam:
  - a igualdade web × robô × contrato;
  - a recusa do perfil fora da lista e a aceitação do registro sem perfil;
  - o `grava_so_acrescentando`.
- O PR do robô não traz teste próprio. A regra 7 está conferida só na leitura: o diff não toca em `aplicar_edicao_web`, `gravar_edicoes_pc` nem `pos_venda.gravar_edicoes`, e só acrescenta `perfil_web` ao `APLICADAS_WEB`, que é append. A demonstração cabe ao `testes`.

### 🟢 sugestões
1. **Fila sem `perfil`: hoje não há brecha.**
   - Só a web grava a fila, pelos dois `fila.registrar` do `main.py`. Os dois passam `u["perfil"]` da sessão, nunca do formulário, e a `/api/edicoes` exige o token do robô.
   - Para não depender disso no futuro:
     - tirar o padrão `perfil: str = ""` do `Fila.registrar` e deixar o argumento obrigatório;
     - no robô, depois que a fila de 11/2026 for drenada, marcar uma data de corte a partir da qual registro sem `perfil` vai a `MOTIVO_PERFIL_WEB`.
2. **Formulário que volta com erro:**
   - `form_ctx` marca o campo por `erro.startswith(rotulo + ":")`. Isso fica preso ao texto da mensagem. É mais firme o `valores_do_form` devolver o `campo` recusado.
   - O caminho 503 (falha da fila) não devolve o que foi digitado.
   - Os campos depois do primeiro erro voltam sem validar: um valor de lista estranho vira opção. Sai escapado e o servidor confere de novo, então é inofensivo.

## Itens do pedido
1. **Permissão:**
   - o POST barra pelo `perfis_do_rid(rid)` antes do `formulario()`, e depois confere o `pode_editar(perfil, (rid, tab))` no lugar exato;
   - trocar o `rid` ou o `tab` dá 403;
   - o CSRF continua;
   - o farol liberado por RN-GER-018 não dá edição, porque só o perfil conta (`test_RN_GER_018_farol_liberado_nao_da_edicao`);
   - o robô confere de novo, pelo `EDITA_LUGAR_WEB`. OK.
2. **Fila antiga sem `perfil`:** aceita, conforme o contrato. Não há brecha hoje (ver 🟢 1).
3. **Regra 7:** OK na leitura. Falta a demonstração do `testes` (ver a pendência).
4. **`pl_fretes`:**
   - está igual na web e no robô e no contrato em 4c0a990;
   - no `main`, sem efeito: o robô recusa por `MOTIVO_LUGAR_WEB` antes do perfil, e a web dá 404 ou 409 (`tabela_editavel` volta `None`);
   - o `perfis_do_rid("pl_fretes")` deixa o pós-venda passar da pré-checagem. Isso é inofensivo, porque o `exige_farol` e o `pode_editar` continuam valendo. OK.
5. **Erro com o que foi digitado:**
   - o autoescape está ligado (`main.py:89`);
   - o único `|safe` é a constante `' aria-invalid="true"'`;
   - só o campo recusado volta vazio e marcado. OK.
6. **Versão:** 0.12.0 OK, mas conflita com o 0.10.1 do `main` (🟡 1).
7. **Segredos e dados pessoais:**
   - não há segredo nem dado pessoal nos diffs, e as fixtures são fictícias;
   - o `perfil_web` é o papel, não a pessoa;
   - o login continua só no `usuario` da fila e no `usuario_web` do `APLICADAS_WEB`, como já era. OK.
- Outros pontos conferidos:
  - `bap_dados.VERSAO = 27`, sem regra de cache nova;
  - nenhum dado digitado nem `.json` de configuração tocado;
  - não há número do Diretor nesta tarefa.
