# Parecer do revisor-codigo: desenho da T-0023 v2 e da T-0025 v2 (contrato §10.9 e §10.10, ADR 0005)

- **Branch:** `engenheiro-software/T-0023-T-0025-contrato` · **head SHA revisado:** `75d66f577499f2af8b7bd36e4cbfb3996e7eff78` · base `main` em `a32b610`.
- **Data:** 27/11/2026 (Manaus) · **Revisor:** revisor-codigo. Clone usado só para leitura (`git fetch`, `git diff origin/main...`, `git show`).
- **Arquivos:** `.coord/contratos/relatorio.md` (+321), `docs/decisoes/0005-config-editada-pela-web.md` (novo), `docs/decisoes/README.md`, `docs/desenho/T-0023.md` e `T-0025.md` (novos), `.coord/diario/engenheiro-software.md`.
- Commit novo na branch = revisão nova.

## Resultado: sem 🔴, 8 🟡 e 10 🟢

O desenho segue as decisões do Alexandre e o `main`. Os 🟡 precisam entrar no contrato antes de os donos começarem os PRs de código. As linhas citadas são do arquivo na branch.

## O que está certo (conferido)
- **Decisões de 26/11** (R-20261126-171559-alexandre, citado pelo plano R-20261126-175814-gerente-projetos):
  - o diretor vê só o Resumo, com 403 nas abas (§10.10.1, critério 4);
  - `RESTRITAS` dá o TOTAL A PAGAR só a admin, gerente e diretor, com o corte no servidor, também no Excel, no PDF, na busca, no total e nos cartões (§10.9.4);
  - o furo do diretor (ele não vê as abas, e o Resumo não tem o número) virou a P1, e o desenho não decidiu sozinho;
  - `champions_config.json` editado só pelo admin, com 403 para os outros, e gravado pelo robô (§10.9.5).
- **6 A** (R-20261126-180314-alexandre): um "autorizo" por arquivo, escrito na ADR 0005 §3.5 e no §10.9.5. A T-0042 fica de fora.
- **Regra 7:**
  - `_NCC`, `_GARANTIAS`, `_AUTORIZACOES` e `_EDICOES_POS_VENDA` só recebem linha, pela função do PC;
  - `garantias.gravar` e `garantias.renomear` só acrescentam (`_anexar`), conferido no `main`;
  - há cópia antes da config (passo 6, antes do `gravar`), e a gravação é idempotente pelo `id` (`APLICADAS_WEB`, que já guarda os `valores`).
- **Regra 6:**
  - `CONTATO CLIENTE` sai das Garantias, numa lista própria da tabela, sem mexer na lista `colunas-fora` nem no teste dela;
  - os campos de contato (`contato_nome`, `contato_fone`, `cli_telefone`) não estão entre os editáveis;
  - `garantia`, `campanha_export` e `_champions` nunca vão;
  - o `TELEFONE` da NCC sai;
  - a P2 está bem posta.
- **Pacote (§10.8):** o teto de 8 MB / 10 MB vale por farol. Os cortes do `pl_garantias` e do `vc_champions` estão em `_CORTES_FAROL_WEB`, e os outros usam o "todas as tabelas saem" que já existe.
- **Coerência com o `main`:**
  - a forma da T-0021 v4 (`LUGARES`, `MAX_CAMPOS` 10, `MAX_TEXTO` 60, `FORM_MAX` 16 KB, `EDICOES_WEB`, `MOTIVO_*`, `APLICADAS_WEB`) foi registrada com fidelidade;
  - T-0035: formato 2, `pacotes.validar_farol`, `_AVISO_SO_PC_WEB`;
  - as RNs 014 a 016 e POS-005/006 batem com a branch `gerente-projetos/T-0023-regras`;
  - `bap_dados.VERSAO` fica em 27, sem cache novo.
- **Donos:** os 6 arquivos são do engenheiro-software (`verificar --por-commit a32b610..75d66f5`: OK, 2 commits com `Agente: engenheiro-software`). A divisão por dono nos desenhos confere com o `coord.mjs dono`.
- Não há segredo nem dado pessoal no diff. Nenhum dado digitado é tocado.

## 🟡 Corrigir antes de virar PR de código

1. **O TOTAL A PAGAR sai, mas a conta fica na tela.** Locais: `relatorio.md:1295` (Vendedores) e a linha do "Supervisores" logo abaixo; `docs/desenho/T-0025.md:152`.
   - No núcleo, TOTAL A PAGAR = PTS VÁLIDOS + PTS RELÂMPAGO (`relatorios_nucleo.py`, comentário "TOTAL A PAGAR (validos + relampago)", e o `kpi("Total a pagar", ..., "válidos + N da relâmpago")`).
   - As duas parcelas ficam visíveis para `vendas`, linha a linha e na linha de total. A aba "Campanha relâmpago" também mostra os PTS por pessoa. Qualquer vendedor refaz o número que a decisão de 26/11 quer restrito.
   - **Pedido:** escrever isso no §10.9.4 e levar ao Alexandre uma pergunta P4 com recomendação. Opções: (A) cortar também PTS VÁLIDOS ou PTS RELÂMPAGO para `vendas`; (B) aceitar que a soma é visível. O critério 3 da T-0025 ("os valores da coluna não aparecem") hoje dá uma garantia que não existe.

2. **Ordem de merge: "faróis primeiro" abre a manhã sem edição.** Locais: `docs/desenho/T-0023.md:70`, `T-0025.md:77` e `:82`, `relatorio.md:1220`.
   - A rotina das 06h30 instala o head do `main` se ele tiver 2 h ou mais (ADR 0002, limite 1).
   - Se o PR dos faróis entra e o do robô perde a janela das 04h30 (CI vermelho, revisão), o PC fica só leitura sem o robô novo. A web também não mostra edição, porque o `edicao` vem do robô novo. Ninguém edita naquele dia, que é o risco que o próprio texto quer evitar.
   - **Pedido:** inverter para **robô primeiro, faróis depois**. Robô sozinho no PC = as duas edições funcionam pela mesma função do PC, sem perda. Ou escrever a trava: o PR dos faróis só entra com o do robô já no `main`, e se o robô atrasar, os faróis esperam o dia seguinte.

3. **Falta o adendo da ADR 0001 para cliente nas tabelas e para a edição.**
   - O §10.1 do `main` diz que "tabela com cliente na web só numa onda futura, com ADR própria".
   - O adendo 5 vale **só** para `pv_pedidos`, `pl_entregas` e `vc_visitas`, e o item 4 dele diz que o site "continua só leitura".
   - O §10.10 leva nome de cliente às tabelas de `pl_garantias`, `pl_devolucoes`, `pl_ncc` e `tm_expositores`, mais o "Histórico de compra", com 4.949 linhas. O §10.9 registra a edição pela web. Nenhum adendo cobre isso.
   - **Pedido:** ADR 0001, adendo 6 (engenheiro-software), com a fonte de cada decisão (migração completa 1 A; RN-GER-012). Ele substitui o item 4 do adendo 5 e estende o item 2 aos 4 `rid` novos.

4. **`parametros_edicao` acima de 256 KB derruba o farol inteiro.** Local: `relatorio.md:1187` e `:1339`.
   - O corte 1 do `vc_champions` só roda acima do teto do farol (8 MB), e isso nunca acontece com um bloco de no máximo 256 KB.
   - O caso real é outro: o bloco passa de 256 KB, a web recusa o farol (como os anexos do §10.8.7), e as Campanhas param de atualizar para todos.
   - **Pedido:** tratar o `parametros_edicao` como os anexos do §10.8.7. Acima de 256 KB, o robô tira só o bloco, com `AVISO_PARAMETROS_FORA`, antes do teto do farol. Mais um teste.

5. **A seção da config não casa 1 para 1 com as chaves do arquivo.** Local: `relatorio.md:1180-1183`.
   - `fora` ↔ `fora_do_jogo` e `equipe_mes` ↔ `equipes_mes` não estão escritos.
   - O `equipes_mes` é um dicionário com **todos** os meses, e o `_mesclar` diz "o que foi gravado vale inteiro". Se a seção for o dicionário inteiro, ela passa dos 32 KB em cerca de 18 meses (cerca de 21 KB por ano), e o admin perde a edição.
   - O `sha` é "como o PC a leu", e o `valor` é "como está no arquivo". O `bap_champions.ler` mescla com o `PADRAO`, então os dois diferem quando falta chave no arquivo, e o passo 2 do robô recusa sem motivo.
   - **Pedido:** uma tabela seção → chaves do arquivo; `equipe_mes` = só o mês do pacote (`equipes_mes["AAAA-MM"]`); `sha` e `valor` sempre do `bap_champions.ler`, nos dois lados (pacote e robô).

6. **O padrão de telefone da web é fraco para o texto longo (regra 6).** Local: `relatorio.md:1075` e `:1190`.
   - O `edicoes.RE_PESSOAL` e o `_RE_PESSOAL_EDICAO_WEB` do robô só pegam o telefone com hífen (`\(?\d{2}\)?\s?9?\d{4}-\d{4}`).
   - O `relatorios_nucleo.texto_sem_contato` pega de 8 a 13 dígitos, com ou sem máscara.
   - Com 600 caracteres em "Retorno do cliente" e "Pendências", um "92999998888" passa pela web e fica gravado na fila do Render (`EDICOES_WEB_*.jsonl`). É dado pessoal no disco do Render.
   - São três cópias da mesma regra (redundância).
   - **Pedido:** no contrato, a recusa da web e do robô usa os mesmos padrões do `texto_sem_contato` (fonte única, com o teste comparando as cópias), também na config.

7. **O "[removido]" pode sobrescrever o texto digitado (regra 7).** Locais: `relatorio.md:1322` (texto livre limpo) e `:1103` (Garantias editáveis).
   - O formulário mostra o valor de hoje já limpo.
   - Se o admin mexe em outra parte de RECLAMAÇÃO, OBSERVAÇÃO, PENDÊNCIAS ou RETORNO DO CLIENTE de uma linha que tinha contato, o texto com "[removido]" vai ao PC e troca o original no diário.
   - **Pedido:** o robô recusa valor com "[removido]" (frase fixa) ou a web não deixa editar o campo cujo valor foi limpo. Mais um teste.

8. **A edição no lugar de DDR e Expositores contra o texto da regra 7 e da RN-GER-012.** Locais: `relatorio.md:1104-1105`, `:1115-1126`; `T-0025.md:142`.
   - O §10.9.3 diz que cumpre a regra 7 e a RN-GER-012 ("só acrescentando linha").
   - Mas o `farol_ddr.gravar_marcacoes` e o `expositores.gravar_edicoes` trocam células da linha. Na regra 7, o `ACOMPANHAMENTO_EXPOSITORES.xlsx` é "planilha de acompanhamento: só acrescentar linha". O PC já fazia assim.
   - A cópia é uma só por dia. A segunda troca do dia perde no PC o valor anterior. O `APLICADAS_WEB` guarda só os `valores` novos.
   - **Pedido:**
     - declarar a exceção (a mesma função do PC, com cópia antes) no §10.9.3 e na ADR 0005, ou num adendo;
     - o robô grava também o `antes` da fila (que a web já manda) na linha do `APLICADAS_WEB`. Assim, cada troca no lugar pode ser desfeita;
     - um recado ao gerente-projetos para alinhar o texto da RN-GER-012 a essa exceção.

## 🟢 Sugestões
1. `MOTIVO_TEXTO_WEB` diz "até 60 caracteres", e o `valores_do_form` corta em `len(bruto) > 200`. Os dois precisam seguir o `max` do campo. O contrato pode dizer isso (`relatorio.md:1079`).
2. `multilinha` deve implicar `caixa: true`, com a comparação depois de normalizar `\r\n` e o `strip` dos dois lados. Senão, o texto em minúsculas do PC volta como "mudou" mesmo sem edição.
3. `FORM_MAX` de 32 KB contra uma seção de até 32 KB: o JSON no form urlencoded cresce até cerca de 3 vezes. O certo é um teto próprio da rota `/parametros`, ou medir o teto no form (`relatorio.md:1077`).
4. `AVISO_PARAMETROS_FORA` só serve ao admin: mostrar só para ele. O aviso do PC "Parâmetros alterados em ... por web:<login>" vai a todos os perfis do farol e pode ficar só para o admin.
5. Duas garantias novas na mesma rodada recebem o mesmo `padrao` de ticket, e a segunda volta "já existe". A tela pode somar as novas pendentes ao sugerir o número.
6. `tela-bc3.md` não está no `main` (só na branch `engenheiro-software/T-0033-contrato-bc3`). Ponha o merge dele como passo 0 na ordem dos dois desenhos.
7. `T-0023.md`, §3, PR 2 dos testes: `web/tests/` é do modulo-web (`coord.mjs dono`), não do testes. Troque "só o que for do testes" por "pedido ao modulo-web".
8. O PR 2 dos testes "junto do 5" (`T-0023.md:71`): se ele entrar depois das 04h30, o head fica com menos de 2 h, e nada é instalado naquele dia. Merge antes das 04h30 ou depois das 07h30.
9. `parametros_edicao` deve entrar explicitamente na lista branca do §10.1 (`relatorio.md:1328` diz "só as chaves do §10.1").
10. `docs/decisoes/README.md`: quando o #137 (ADR 0004) entrar, liste a 0004 e evite conflito na linha "A próxima é a 0006". Data livre sem faixa: aceitar só um intervalo razoável (por exemplo, de 2020 a hoje + 1 ano).

## Conferências
- `node scripts/coord.mjs verificar --por-commit a32b610..75d66f5`: OK, nenhuma violação.
- Sem código no diff: não há `compileall` nem testes a rodar. P1, P2 e P3 estão com o Alexandre e não bloqueiam.
