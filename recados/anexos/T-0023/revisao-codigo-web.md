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
