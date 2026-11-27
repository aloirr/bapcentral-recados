# T-0033 · Revisão de código: o merge do main (T-0024 lote 2) e o A1 (revisor-codigo)

- **Branch:** `modulo-web/T-0033-revisao-geral`.
- **Delta revisado:** `f188d73` → **`034a9ca42abefd729a91026e27cbe98e894ac20e`** (head).
  - Merge `034a9ca` (pais `f188d73` e `0bb251b`).
  - Traz do main `a32b610` (quadro), `a178af2`, `8dab048` e `0bb251b` (T-0024).
- **Régua:**
  - o diff da T-0024 contra o merge-base `767a389`;
  - o `git show --remerge-diff` do merge, nos 10 arquivos com conflito;
  - o meu A1 em `anexos/T-0034/revisao-codigo-2.md`;
  - o contrato §10.7.2 (`kpis_padrao`) e o §10.7.6 (`AVISO_CARTOES`).
- O parecer vale só para este head. Commit novo pede revisão nova.

## Resultado
**Aprovado.** 0 🔴 · 0 🟡 · 4 🟢.

## O que foi rodado
- **Cópia:** `git archive 034a9ca` no scratchpad. O clone não mudou de branch, e nada foi alterado nele.
- **`python -m compileall -q web/app`:** limpo.
- **Testes direcionados** (sem a suíte inteira, que está com o testes):
  - `test_T0024_lote2_estrutura.py`, `test_T0024_farois_lote2.py` e os 3 testes da faixa em `test_abas.py` (A1, cartão com `linhas`, Solicitação sem estado): **25 passed**;
  - `test_T0033_tokens.py` e `test_T0033_grade.py`: **11 passed**.
- **Mutação do A1:** voltei a linha 12 do `_bc3_cab.html` para `ks_todos if e_tab`. O teste novo falhou, com 4 números no Resumo da Inadimplência contra 5 na aba Títulos. O teste pega o defeito.
- **Celular (390 px, Chromium):** abri as 7 abas do Giro com a fixture `lote2_fixture` e medi as abas da barra (`scrollWidth` contra `clientWidth`). Nenhuma passa da largura, com ou sem a regra do 🟢 G2.
- **Donos:** `node scripts/coord.mjs verificar --por-commit f188d73..034a9ca` deu "OK — 4 commit(s), nenhuma violação".
  - Esse modo ignora o commit de merge. O que o merge resolveu (remerge-diff) fica todo em `web/`, que é do modulo-web, e o commit traz `Agente: modulo-web`.
- **Regras:**
  - `bap_dados.VERSAO = 27`;
  - nenhum `.json` de config, base congelada ou dado digitado no delta;
  - nenhum segredo nas linhas novas (varredura por padrões de token e senha).

## 1. Nada da T-0024 se perdeu
| Item | Onde está no head |
|---|---|
| GRADE dos 5 faróis | `tabelas.py`, `GRADE.update({...})` com as 25 entradas do lote 2. Não há chave em comum com a GRADE da T-0033 (43 no total). Todas têm `cel` com 4 posições e a chave dentro da grade. Agora são lidas pelo mecanismo da T-0033 (`grade_de`, `preparar_grade`, `dados_do_popup`, `popup_linha.js`) |
| DICA_BUSCA | `tabelas.dica_busca`, `main.py:384`, `_bc3_cab.html:58` (sem busca até 15 linhas) e `:66` (placeholder; os faróis antigos ficam com o `dicas` da T-0033) |
| Rótulos curtos | `tabelas.rotulo_aba`, `abas_do_farol` e `main.py:353` (barra). Depois a T-0033 ainda aplica o `aba_curta` no template (ver 🟢 G1) |
| NOME_MENU | `render.py:168` e `:193`: `NOME_MENU.get(r, meus[r].removeprefix("Farol de "))`, as duas regras juntas |
| Select longo no celular | `estilo.css:576-577` |
| Perfis e 403 | `render.FAROIS` (5 faróis com os perfis do PC), `tabelas.VE_TABELAS`, `main.py:331` (aba fora do perfil = `PermissionError`) e `main.py:498` (exportar usa `abas_do_farol`) |
| Faixa igual em todas as abas do lote 2 | `main.py:400-404`: `topo["kpis"]`, e o `AVISO_CARTOES` com filtro ou estado. É a mesma semântica do `0bb251b` |
| Resto do lote 2 | `LOTE2`, `agrupar_periodos` e `sem_graficos_repetidos` (`render.py:602-603`), os períodos em `_resumo.html`, o CSS `.per-*` (convertido para os tokens), o `livres` no Jinja, o `.bc3-sub` condicional e o `scrollIntoView` da aba ativa |

- **O que saiu de propósito**, porque a T-0033 substituiu:
  - `tab["grade"] = GRADE.get(...)`, `colunas_fora_da_grade` e a variante antiga de `colunas_do_celular`/`dados_do_popup`;
  - o `pop-chave`/`data-titulo` e o `popup_pedido.js`;
  - os globais `fora_da_junta` e `cols_celular`;
  - o rodapé `bc3-rod`.
  - Não sobrou nenhuma referência a eles no `web/`, fora o 🟢 G3.

## 2. Nada da T-0033 se perdeu
- **BC3:** `_grade.html` (`corpo`, `itens`, `grade`), a barra de 3 abas mais "Mais" no celular e a busca que vira ícone.
- **Tokens:** o bloco T-0024 do CSS foi convertido para `var(--...)`, e `test_T0033_tokens` passa.
- **PALETA_TOM:** `tabelas.py:232`.
- **AVISO_CARTOES com `kpis_padrao`:** `main.py:405-410`.
- **Faixa do Visita:** os `kpis_padrao` do Visita chegam do robô (`test_T0017_pacote_tres_farois.py:914`), e `test_faixa_da_aba_leva_o_cartao_com_linhas_no_padrao` passa.
- **Solicitação sem estado:** `main.py:368-370`, e `test_solicitacao_bap_ignora_o_estado_tambem_nos_cartoes_de_cima` passa.
- **Aviso de estado:** `AVISO_UF` ficou com o texto da T-0033 (RD-0034), e `sem_uf` exclui os faróis livres. O lote 2 continua sem os `avisos_info`, como na T-0024.

## 3. Os dois testes da T-0024 ajustados: legítimos
- **`test_GRADE_do_lote2_tem_ate_10_colunas_e_so_colunas_do_robo`**
  - O ajuste pula as entradas que não são de `FAROIS_LIVRES`.
  - É necessário: a GRADE passou a ter as entradas de Pedidos, Entregas, Inadimplência e Visita, que não existem no `pacote_lote2()`.
  - O teste segue cobrindo as 25 entradas do lote 2, como o nome diz. As da T-0033 são cobertas por `test_T0033_grade.py`.
- **`test_grade_esconde_colunas_e_abre_popup_na_chave`**
  - O ajuste troca `class="sel-link pop-chave"`/`data-titulo="900001"` por `class="sel-link"` mais `data-tit` com 900001.
  - É o mesmo comportamento (a chave abre o popup) no mecanismo único da T-0033.
  - As outras asserções (coluna `oc` no cabeçalho, SUGESTÃO na grade) não mudaram.

## 4. A1: resolvido
- **O que mudou:**
  - `main.py:399` e `:410`: `kpis_da_aba = True` só no ramo do `kpis_padrao`, no padrão, sem filtro;
  - `_bc3_cab.html:12`: `ks_todos if (e_tab and kpis_da_aba ...)`, e o resto passa pelo `rejectattr('estados')|rejectattr('linhas')`.
- **Efeito:** é a opção (a) do parecer. A Inadimplência (`main.py:729/747`, sem `kpis_da_aba`), a Solicitação e as abas sem `kpis_padrao` levam à faixa o mesmo que o Resumo. O Visita e Pedidos, com `kpis_padrao`, continuam com o cartão inteiro.
- **Teste:** `test_A1_aba_sem_kpis_padrao_leva_na_faixa_os_mesmos_numeros_do_resumo` compara os `<small>/<b>` da faixa (Títulos contra Resumo, Solicitação contra Resumo). A mutação confirmou que ele cobre o defeito.
- **Número do Diretor:** sem mudança. O Painel não está no delta, e o diretor só vê o Resumo.

## 🟢 Sugestões (não bloqueiam)
- **G1 · Redundância, duas tabelas para o nome curto da aba:**
  - `tabelas.ROTULO_ABA`/`rotulo_aba` (T-0024) e `tabelas.ABA_CURTA`/`aba_curta` (T-0033) são a mesma regra, aplicadas em série (`main.py:353` e depois `_bc3_cab.html`);
  - "Resumo por filial" vira "Por filial", que vira "Filial";
  - no Giro, a barra mostra "Categoria" ao lado de "Por família", porque o `ABA_CURTA` não tem "Por família".
  - Sugestão: um mapa só, com uma função só, e o slug da URL tirado dela. Encaminhar ao corretor-redundancias e ao designer-ux.
- **G2 · `estilo.css:580` `.bc3-abas a{white-space:nowrap}` (T-0024) sobra:**
  - no PC, a `:429` já faz o mesmo;
  - no celular, ela vence o `white-space:normal` da `:533` (mesma especificidade, vem depois).
  - Hoje não há efeito visível: medi no Giro a 390 px e nada passa. Pode sair ou ir para `@media(min-width:701px)`.
- **G3 · Código morto do lote 2 depois do merge:**
  - `estilo.css:596` `.pop-chave{cursor:default}`: nenhum HTML gera mais essa classe;
  - `bc3.js:24-25` `scrollIntoView`: a barra do celular agora mostra 3 abas mais "Mais" e não rola, e a aba ativa sempre está entre as 3.
- **G4 · `_bc3_cab.html:10-11`:**
  - o comentário ainda diz "Aba de tabela: a faixa leva o cartão inteiro, com `linhas` ou não";
  - depois do A1, isso vale só com `kpis_padrao` (`kpis_da_aba`).
  - Também: a correção do A1 entrou dentro do commit de merge. Isso dificulta a leitura no `git log`, mas o squash resolve.
