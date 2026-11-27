# Parecer do revisor-codigo: código da T-0023 v2 (Garantias, Devoluções e NCC na web)

- **Data:** 27/11/2026 (Manaus) · **Revisor:** revisor-codigo. Usei o clone `/home/user/bapcentral` só para leitura (`git fetch`, `git diff origin/main...`, `git show`), sem trocar a branch. Base: `origin/main` em `f3c4569`.
- **Heads revisados.** Commit novo = revisão nova.

| Parte | Branch | Head revisado | Observação |
|---|---|---|---|
| Núcleo | `modulo-farois/T-0023-nucleo` | `7ebfe4e` | |
| Robô | `modulo-robo/T-0023-robo` | `f86adfa` | chegou o merge do núcleo `7ebfe4e`; o `bap_automation.py` é igual ao do `11c9bfc` |
| Testes | `testes/T-0023-testes` | `165f299` | o `db7e699` foi superado por `c9b4a7e` (merge do main) e `165f299` (sai o xfail) |
| Contrato | `engenheiro-software/T-0023-contrato-dado-pessoal` | `36ecf9d` | só o §10.10.3 |

- **Referência:** contrato §10.9 e §10.10 e `docs/desenho/T-0023.md` (no `main`); RN-GER-002, 007, 011, 012 e 014, RN-POS-005 e 006 (`docs/produto/03-regras.md`).
- **O que rodei:**
  - `py_compile` dos arquivos das branches;
  - `verificar --por-commit` nas 4 branches: sem violação;
  - `montar("pl_devolucoes")` com o núcleo da branch e com o do `main`, sobre as bases congeladas (hoje = 24/11/2026). Isso mediu o achado N1.
  - A suíte não foi rodada, como combinado.

## Resultado

| Branch | Parecer |
|---|---|
| Núcleo `7ebfe4e` | **🔴 1** · 🟡 3 · 🟢 1 |
| Robô `f86adfa` | sem 🔴 · 🟡 2 (condições de merge) · 🟢 3 |
| Testes `165f299` | sem 🔴 · 🟡 2 · 🟢 2 |
| Contrato `36ecf9d` | **aprovado** · 🟢 1 |

## O que está certo (conferido)

- **Regra 7 / RN-GER-012:**
  - a Garantia grava só por `garantias.gravar` e `garantias.renomear` (`_gravar_garantia_pc`, `bap_automation.py:9692`), que só acrescentam (`_anexar`);
  - a NCC grava por `ncc_controle.gravar`, e a Devolução por `pos_venda.gravar_edicoes` (primeiro o diário `_EDICOES_POS_VENDA`, depois as colunas da assistente);
  - nenhuma linha de diário é reescrita;
  - o `antes` e o `novo` vão para o `APLICADAS_WEB` (`_registrar_aplicada_web`, `:9986`);
  - a gravação é idempotente pelo `id`;
  - os testes usam só `tmp_path` e conferem `startswith(antes)`.
- **Ticket (§10.9.2), em `plano_garantia_web` (`:9844`), função pura:**
  - padrão = `antes.ticket` e já existe → `garantias.novo_ticket` da hora: cobre o pacote atrasado e a 2ª garantia da mesma rodada, porque o `novo_ticket` é lido de novo a cada edição;
  - digitado que já existe → `MOTIVO_TICKET_WEB`;
  - troca → `renomear` antes do `gravar`, como o `DialogoGarantia.salvar`;
  - o prazo igual ao padrão fica em branco (RN-POS-005), com a mesma conta do PC (`bap_relatorios.py:4457`);
  - `origem` = "FAROL DE GARANTIAS", igual ao PC.
- **"[removido]":** o robô recusa qualquer texto livre ou longo com `[removido]` (`MOTIVO_REMOVIDO_WEB`). O teste confirma que o diário fica com o original.
- **Dado pessoal fora do pacote:**
  - `CONTATO CLIENTE` sai por `_COLUNAS_FORA_TABELA_WEB`, e o `CAMPOS_EDICAO_GARANTIA` não tem contato;
  - o `TELEFONE` da NCC sai pela `colunas-fora`;
  - o `garantia` (tabela e farol) fica fora pela lista branca;
  - as colunas "limpa" e o texto livre seguem o §10.10.3;
  - no robô, `texto_sem_contato(v) != v` recusa.
- **Tetos do texto:**
  - número único em `relatorios_nucleo.MAX_TEXTO_EDICAO`, 600 nos 4 longos;
  - o robô põe o `max` e confere a edição pelo `max_texto_edicao` do núcleo;
  - a spec com outro `max` não vai (`:8189`, preso no `except` do `_tabela_web7`, sem derrubar o farol);
  - não há tabela de teto no robô.
- **RN-GER-002 no Painel Executivo:** o detalhe do cartão "Devoluções" usa a mesma regra do farol de origem (DEV ÷ (VND − DEV)). O R$ do cartão = o detalhe do cartão "Devoluções" do farol (R$ 5.552). Os dois testes conferem.
- **RN-GER-007 na NCC (`montar`):** o D.U. S/ MOV. conta até ontem (`:6924`), e o SLA (hoje > prazo) não muda.
- **Geral:**
  - `bap_dados.VERSAO = 27` nas branches;
  - nenhuma base congelada nem `.json` de config no diff;
  - os trailers e os donos estão certos (`verificar --por-commit` limpo).
- **Testes:**
  - o xfail do "% do faturado" saiu (`165f299`), e setembro separa as contas: 12,0% no líquido contra 10,7% no bruto;
  - nada foi afrouxado: o exemplo "fora da lista" trocou `pl_garantias` por `vc_markup`, com o mesmo efeito;
  - a isenção larga de dado pessoal saiu;
  - os nomes citam a RN.

## Núcleo `modulo-farois/T-0023-nucleo` @ `7ebfe4e`

🔴 **N1. O "% devolvido do faturado" do Resumo fica negativo ou absurdo** (`relatorios_nucleo.py:19103`, `_painel_devolucoes`).
- **Causa:** o denominador passou a ter `-abs(DEV)` por evento. O `painel_farol._juntar("pct")` só se protege do denominador 0. Num dia em que DEV ≥ VND, o valor sai negativo.
- **Medido nas bases** (`montar("pl_devolucoes", MÊS=10)`): "% devolvido do faturado · dia a dia · OUT/26", dia 06 = **−1.636,01%**. No `main`, o mesmo dia mostra 106,51%.
- Em 21 dos 99 dias com devolução, VND − DEV ≤ 0.
- É o Resumo que o diretor vê (RN-GER-014).
- **Correção:** o faturado líquido ≤ 0 não dá percentual (`None`/"—"), como o cartão do Painel Executivo já faz (`if atual["vnd"] - dev > 0`). Vale também para o `pct_de` do `devolucoes()`: o `fat_mes` e o `fat_vend` (FATURADO 12M e % DEVOLVIDO) podem ficar ≤ 0 num vendedor. Hoje nenhum fica ≤ 0, mas o maior % já chega a 147%.
- Se a guarda entrar no `painel_farol._juntar`, o dono é o mesmo (modulo-farois).

🟡 **N2. Duas regras na mesma coluna D.U. S/ MOV.**
- O `montar` conta até ontem (`:6924`).
- O `ao_mudar` da mesma tabela (`:7020`, `nc.sla(..., ctx.uteis, ...)` em `:7027`) ainda conta o hoje. Depois de uma edição no PC (que só fica leitura no PR 2), a coluna ganha +1.
- **Correção:** uma função só, por exemplo `_uteis_ate_ontem(ctx)`, usada nos dois lugares.

🟡 **N3. Redundância: a regra VND − DEV foi reescrita, mas já existe:**
- em `devolucoes()` (`:7836`), o `v = ... -abs(...)` repete o `_liquido(it)` (`:2615`);
- no cartão do Painel Executivo (`:9575`), `atual['vnd'] - dev` refaz o `atual['real']`, que já é o líquido pelo `_liquido` (mesmos itens, mesmo período e mesmos pedidos em aberto);
- em `_painel_devolucoes`, o denominador pode vir de `_eventos_faturamento(ctx, liquido=True)` (`:557`).

🟡 **N4. Regra 10: muda o número do diretor sem simulação.**
- O detalhe do cartão "Devoluções" do Painel Executivo vai de 4,7% para 4,9% em NOV/26.
- O gráfico "% do faturado" do farol muda (SET/26 vai de 10,7% para 12,0%).
- Falta a imagem antes × depois ao Alexandre antes do PR. [SUPOSIÇÃO: não há simulação em `recados/anexos/T-0023/`.]

🟢 **N5.** Com a `edicao` na tabela Garantias, o rodapé do PC passa a mostrar "Duplo clique na linha para editar" (`bap_relatorios.py:353`), porque o par ainda não está no `EDICAO_SO_WEB`.
- O duplo clique continua abrindo o `DialogoGarantia` (o `garantia` tem prioridade), e o "Novo" não aparece (a chave é `novo_web`).
- Não há gravação errada. Some no PR 2.

## Robô `modulo-robo/T-0023-robo` @ `f86adfa`

🟡 **R1. Um PR por dono.**
- A branch carrega os commits do núcleo (`9b8543d` e o merge de `fce7888`). O `relatorios_nucleo.py` está no diff e é idêntico ao do núcleo.
- Abra o PR do robô só depois do squash do núcleo no `main` e de um merge do `origin/main`, para o diff ficar só com o `bap_automation.py`.

🟡 **R2. Ordem do §10.9.6: o robô (passo 4) só entra depois da web v2 (passo 2).**
- A web da T-0023 v2 não está no `main` e não tem branch v2 publicada.
- O limite 3 da ADR 0002 não protege: a versão da web no `main` seria igual à do `/saude`.
- No formato 2, o farol desconhecido fica "fora" (404) ou "manter" (422), sem derrubar os outros. Mesmo assim, a ordem é a do contrato.
- Condição de merge, não defeito do código.

🟢 **R3.** O tipo `ticket` não passa pelo `texto_sem_contato`: um ticket de 11 dígitos passa no robô.
- Acima de 40 caracteres, a frase diz "até 60", porque o `max` do campo `ticket` no pacote é 60.
- Sugestão: ou o `ticket` passa pela mesma conferência de dado pessoal, ou o `max` do campo vai 40.

🟢 **R4.** Em `aplicar_edicao_web`, o `ValueError` do `renomear` (corrida no número) vira `MOTIVO_LINHA_WEB`, e não `MOTIVO_TICKET_WEB`. Além disso, o `chave_pc` vai ao `APLICADAS_WEB` mesmo quando a gravação dá erro.

🟢 **R5.** O `APLICADAS_WEB` grava os `valores` brutos também no `erro`. Isso já era assim desde a T-0021.
- Com campos de 600 caracteres, um texto recusado por telefone fica no arquivo local.
- Sugestão: no erro de texto ou de `[removido]`, gravar o `valores` sem o campo recusado (regra 6).

## Testes `testes/T-0023-testes` @ `165f299`

🟡 **T1. `docs/testes/T-0023.md` está desatualizado.**
- O doc ainda descreve o combinado `fcd66cb` + `9b8543d`: xfail ❌, 4 falhas (§4.1, já resolvido em `1429ab6`) e a observação do D.U. com o hoje (já corrigida).
- Refazer o combinado com núcleo `7ebfe4e` + robô `f86adfa` e registrar os números e o resultado no head do PR.

🟡 **T2. Faltam valor × regra em 2 números que o núcleo mudou:**
- (a) o "% devolvido do faturado" do Resumo (`_painel_devolucoes`), com um dia em que VND − DEV ≤ 0 (06/10/2026). Esse teste pega o N1;
- (b) o FATURADO 12M do "Por vendedor (12 meses)" = Σ(VND − DEV) dos 12 meses do vendedor. Hoje o teste só confere % = VALOR ÷ FATURADO 12M, que passa com qualquer base.
- Quando o N2 for corrigido, falta também o D.U. depois do `ao_mudar`.

🟢 **T3.** O `FAROIS_T0023` continua "permitido, não obrigatório". Ele tem de vir antes do robô para destravar o CI. Com o robô no `main`, promover os 3 a obrigatórios: senão, tirar o `pl_ncc` do `FAROIS_WEB` passa.

🟢 **T4.** A busca do `FONE` usa as listas do robô (`_COLUNAS_TEXTO_LIVRE_WEB`, `_COLUNAS_LIMPAS_WEB`), e não o texto do §10.10.3. Uma coluna que o robô esquecer não é pega. Sugestão: ler a lista do contrato, como o teste da `colunas-fora`.

## Contrato `engenheiro-software/T-0023-contrato-dado-pessoal` @ `36ecf9d` (§10.10.3)

**Aprovado.** O texto novo ("onde o testes procura") bate, linha a linha, com o `test_RN_GER_011_json_dos_3_farois_sem_cpf_cnpj_email_nem_telefone`:
- as chaves, em qualquer nível;
- `EMAIL`, `DOC_MEIO` e `DOC_SOLTO` em toda string, menos o código de produto só com dígitos;
- inteiro de 11 ou 14 dígitos fora das colunas de código reprova;
- `FONE` só no texto livre e nas colunas "limpa".

Não afrouxa a regra do robô, só onde o teste procura.

🟢 **C1.** Os campos digitados `AUTORIZADO POR` e `RESPONSÁVEL` (Devoluções) e `DESCRIÇÃO PRODUTO` (Garantias) não estão no "texto livre". Então o `FONE` não é procurado neles, nem limpo.
- Medido nas bases: 0 ocorrências hoje.
- Sugestão: incluir esses campos na lista do texto livre, ou registrar por que ficam fora.

## Para o merge

1. Corrigir N1 a N4 e T1/T2, e rever no head novo.
2. Ordem: testes (destrava) → web v2 → núcleo → robô, com o merge do `main` antes do PR → PC só leitura (PR 2) → testes finais.
