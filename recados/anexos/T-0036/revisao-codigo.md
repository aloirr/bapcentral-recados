# Revisão T-0036: faróis do Analista na web, perfis analista e trade

Revisor: revisor-codigo · 27/11/2026 (Manaus) · base `origin/main`.

Heads revisados:
- `modulo-farois/T-0036-correcao-codigo` f66e9ff
- `modulo-robo/T-0036-pacotes` 9d886fa
- `modulo-web/T-0036-analista` d3589da
- `testes/T-0036-testes` 33c6d81
- `engenheiro-software/T-0036-desenho` 506408f
- `gerente-projetos/T-0036-regras` 84e9aae

Parecer: **não aprovado** (1 🔴 e 2 🟡). Commit novo pede revisão nova.

## 🔴 Bloqueia
1. `painel_diretor.py:175-191` e `:478-484` (f66e9ff). O Diretor passa a mostrar o desconto comercial cheio (15,1%), mas o cartão do `vc_saldo` mostra "15%". Isso contraria três pontos:
   - o contrato §10.11 (`.coord/contratos/relatorio.md:1428`): "o valor do farol é igual ao da aba RRM";
   - o desenho §3: o modulo-farois só tem `codigo_do_cliente` e `correcao_linhas`, e o PC não muda de tela;
   - a regra 10: um número do Diretor muda sem simulação.

   **Correção:** reverter f66e9ff no farois e no testes. Os testes `tests/test_T0036_analista_robo.py:752-775` saem junto. Se o Alexandre quiser uma casa decimal, ela entra no próprio cartão do Saldo e passa por simulação.

## 🟡 Corrigir antes do merge
2. `painel_diretor.py:175` `desconto_comercial_cheio` reescreve Σ DESC ÷ Σ TABELA. Essa conta já existe em `relatorios_nucleo.py` (`resumo().pcom` do Saldo, `:11638`). É redundância. Ela some com o item 1. Se o número cheio for mantido por decisão, o farol deve expô-lo, e o Diretor só lê.
3. Ordem de merge. O PR do robô carrega `relatorios_nucleo.py`, e o do testes carrega `bap_automation.py`, `relatorios_nucleo.py` e `painel_diretor.py`. Com `--base origin/main`, o `verificar` acusa arquivo de outro dono enquanto as branches de origem não entrarem. **Ordem:** regras → farois → robô → web → testes. O testes é atualizado do `main` antes do PR dele, para o xfail `test_RN_GER_011_colunas_positivas_web_aceita_o_robo...` virar teste real.

## 🟢 Sugestões
4. `web/tests/test_T0036_analista.py:279`: renomear para `test_RN_GER_017_correcao_so_admin`. "Excel de correção só admin" é RN-GER-017, não RN-GER-012.
5. `web/app/tabelas.py` não limpa telefone nem e-mail no texto livre da Pesquisa (`OBSERVAÇÃO`). Só o robô limpa (`bap_automation.py`, `_COLUNAS_LIMPAS_WEB`). Uma checagem também na web daria uma segunda barreira.
6. Quando a T-0025 v2 entrar, conferir que o `analista` não ganha o TOTAL A PAGAR (P3 = A, RN-GER-015), porque `LEITURA_GERAL` monta as tuplas.

## Conferido sem achado
- **Dado pessoal.** Nos 4 faróis, o cliente aparece só pelo código: `_cliente_por_codigo_web` e `codigo_do_cliente`, que recusa CPF/CNPJ. A lista positiva de colunas é a mesma no robô (`_COLUNAS_TABELAS_WEB`) e na web (`COLUNAS_RID`), e a web confere com assert de contagem. A aba sai se a coluna PONTO trouxer coordenada. O anexo `correcao` vem sem CLIENTE e com lista fechada dos dois lados, e o texto do `acao` não traz nome. A fixture é fictícia.
- **Perfis no servidor.** As tabelas dos 4 faróis são de `LEITURA_GERAL`; o diretor vê só o Resumo. O `correcao.xlsx` exige `usuario(request, ("admin",))`. O `EDITA` e o `COBRA` continuam sem o analista. Não há rota de meta RH.
- **Segredos.** Nenhum. `bap_dados.VERSAO = 27`. Nenhuma base congelada nem config `.json` foi alterada.
- **Testes.** `verificar --por-commit` limpo nas 6 branches. Na branch testes, `tests/test_T0036_analista_robo.py`, `test_T0017` e `test_T0024` deram 85 passed e 1 xfailed (o xfail é esperado). No checkout da web, `web/tests` deu 418 passed. O `pytest tests/` inteiro para em `test_T0021` (sem tkinter no Linux), que é falha de ambiente.

## Segunda volta (27/11/2026, Manaus)

Heads revisados:
- farois 19ae0cb
- robô d24a2ae
- web ae6b1ea
- testes f2314af
- desenho 0cc2a2e
- regras 84e9aae

Parecer: **não aprovado** (2 🟡). Commit novo pede revisão nova.

**Fechados:**
- 🔴 1: o f66e9ff foi revertido. O `painel_diretor.py` não aparece mais no diff do farois nem no do testes. O teste do Diretor voltou a xfail strict, como defeito antigo e com tarefa à parte.
- 🟡 2: a função duplicada saiu junto com o revert. Os cabeçalhos do Excel de correção agora vêm de um lugar só: `relatorios_nucleo.CAB_CORRIGIR` e `CAB_ANALISAR`.
- 🟢 4: o teste virou `test_RN_GER_017_correcao_so_admin`.
- 🟢 5: a web passou a ter `tabelas.limpar_texto` com "[removido]", aplicado na chegada do pacote (`pacotes.py:611`).

**Mudanças novas, sem achado:**
- `LEITURA_GERAL` e `VEEM_PAINEL` são a fonte única dos perfis, e o `cobranca.VE_TABELAS` deriva deles. O `COBRA` e o `EDITA` continuam sem o analista.
- `RIDS_ANALISTA_WEB` e `RIDS_ANALISTA` são únicos, a página do trade mostra só a frase e a `VERSAO` da web foi para 0.6.0.

**Em aberto:**
- 🟡 3 (continua): o `verificar --por-commit` está limpo nas 6 branches, mas nenhuma das 4 branches de código (farois, robô, web e testes) contém o `origin/main` atual. **Correção:** fazer o merge do `main` em cada uma (sem rebase) e seguir a ordem regras → farois → robô → web → testes. O robô e o testes carregam código do farois, e o testes carrega código do robô.
- 🟡 7 (novo): `bap_automation.py:9077` traz `import relatorios_nucleo as _rn_cab` no nível do módulo. O resto do arquivo importa o núcleo só dentro das funções (`:7234`, `:7984`, `:8285` e outras, todas com `# noqa: PLC0415`). Com o import no topo, o robô carrega o núcleo inteiro em toda execução, cerca de 0,3 s a mais, e um import circular futuro fica mais fácil. **Correção:** montar o `_COLUNAS_CORRECAO_WEB` dentro de `_correcao_divergencias_web`, ou numa função `_colunas_correcao_web()` com o import local.

**Testes:**
- Na branch testes, `tests/test_T0036_analista_robo.py`, `test_T0017` e `test_T0024` deram 84 passed e 2 xfailed; os dois xfails são esperados (a web sem a T-0036 e o defeito antigo do Diretor).
- No checkout da web, `web/tests` deu 448 passed.
- O `compileall` passou.

## Conferência final (27/11/2026, Manaus)

Heads revisados (todas as branches já contêm o `origin/main` 30ae65d):
- regras d9e9760
- desenho 845ff4a
- farois f4d197d
- robô 4de2cb1
- web a214659
- testes 6c33a72

Parecer: **aprovado**, sem 🔴 nem 🟡 em aberto. Commit novo pede revisão nova.

**Fechados:**
- 🟡 3: as 6 branches têm o `main` atual, e o `verificar --por-commit` está limpo em todas. O que o `--base` acusa no robô e no testes é código que veio por merge de outros donos, e isso some com a ordem de merge regras → farois → robô → web → testes.
- 🟡 7: `bap_automation.py:9077` agora tem `_colunas_correcao_web()`, com o import do núcleo dentro da função (commit 7bbdbc8).

Desde a segunda volta, só há duas mudanças além do merge do `main`: a do item 7 e a saída do relato da sessão da branch do desenho (7ea957f).

**Testes:**
- Na branch testes, `tests/test_T0036_analista_robo.py`, `test_T0017` e `test_T0024` deram 84 passed e 2 xfailed, os dois esperados.
- No checkout da web, `web/tests` deu 448 passed.
- O `compileall` passou.

O 🟢 6 fica como lembrete para a T-0025 v2: o analista não pode ganhar o TOTAL A PAGAR (RN-GER-015).
