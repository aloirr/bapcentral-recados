# Reteste do revisor-codigo: desenho da T-0023 v2 e da T-0025 v2

- **Branch:** `engenheiro-software/T-0023-T-0025-contrato`.
- **Head SHA:** `97ccba78a75a8d90aba932a832b9610ad10fdbe9`. Revisão anterior em `75d66f5` (`revisao-codigo-desenho.md`).
- **Data:** 27/11/2026 (Manaus). O clone foi usado só para leitura.
- **Commit novo:** `97ccba7`, com 7 arquivos:
  - o contrato §10.7.6, §10.9 e §10.10;
  - a ADR 0001, adendo 6 (novo);
  - a ADR 0005 e o README;
  - os 2 desenhos;
  - o diário.

## Resultado: aprovado. Sem 🔴 e sem 🟡 em aberto; 2 🟢 novos

## Os 8 🟡, um a um

| # | Achado | Situação | Onde fechou |
|---|---|---|---|
| 1 | TOTAL A PAGAR refeito pela soma PTS VÁLIDOS + PTS RELÂMPAGO | **fechado** | A conta está escrita no §10.9.4 ("O corte tira a coluna e o cartão, não o número"). A P4 vai ao Alexandre com a opção de cortar também os pontos. O critério 3 da T-0025 não promete mais o que não existe. O `RESTRITAS` agora cobre também o cartão do Resumo (P1 A, com o `Kpi.coluna` posto pelo núcleo) |
| 2 | "Faróis primeiro" abria uma manhã sem edição | **fechado** | §10.9.6: web → núcleo → robô → **PC só leitura por último** → testes. A rotina instala o `main` inteiro, então o PC só leitura nunca chega sem o robô que grava. Os desenhos citam o §10.9.6 como fonte única |
| 3 | Faltava o adendo da ADR 0001 | **fechado** | O adendo 6 estende o item 2 do adendo 5 aos 4 `rid`, com o "Histórico de compra". Ele troca o item 4 (o site edita nos lugares do §10.9.3) e cita as fontes (1 A, RN-GER-012, 26/11, P1 a P3) |
| 4 | `parametros_edicao` acima de 256 KB derrubava o farol | **fechado** | §10.9.5 e §10.10.4: o robô tira só o bloco antes do teto, como os anexos do §10.8.7. `AVISO_PARAMETROS_FORA` está na tabela do §10.7.6 e é mostrado só ao admin |
| 5 | Seção ↔ chave do arquivo | **fechado** | Há uma tabela das 6 seções: `fora` ↔ `fora_do_jogo`; `equipe_mes` ↔ `equipes_mes["<competencia>"]`, só o mês do pacote. `valor` e `sha` vêm os dois do `bap_champions.ler`, no pacote e no passo 2 do robô |
| 6 | Telefone sem hífen passava | **fechado** | Recusa por `texto_sem_contato(v) != v`. Os padrões ficam no bloco `padroes-pessoais`, que confere caractere a caractere com o `relatorios_nucleo` do `main` (`_EMAIL`, `_DOC_MEIO`, `_DOC_SOLTO`, `_FONE`, `_VALOR_RS`). O robô usa o núcleo, e a web tem uma cópia, com teste. Vale também na config |
| 7 | "[removido]" sobrescrevia o original | **fechado** | A web recusa com frase própria, e o robô recusa com `MOTIVO_REMOVIDO_WEB` (§10.9.1, regra 4) |
| 8 | Edição no lugar contra a regra 7 | **fechado** | Exceção declarada no §10.9.3, na ADR 0005 e na RN-GER-012 da branch `gerente-projetos/T-0023-regras` (`58760c0`). Duas garantias: o `antes` de cada troca no `APLICADAS_WEB` (na config, a seção anterior inteira) e a cópia do dia. Os critérios 5 e 8 da T-0025 testam as duas trocas no mesmo dia |

Os 🟢 da revisão anterior também entraram:
- o teto do texto num lugar só (`MAX_TEXTO_EDICAO`) e a frase com o `max`;
- `multilinha` implica `caixa`, e a comparação é normalizada;
- teto de 128 KB na rota `/parametros`;
- o aviso "Parâmetros alterados" só para o admin;
- o ticket somado às garantias novas pendentes;
- o passo 0 com o `tela-bc3.md`;
- o dono de `web/tests/`;
- a nota sobre merge entre 04h30 e 06h30;
- a lista branca do §10.1;
- o README com a 0004;
- a data livre de 2020 até hoje + 1 ano.

## 🟢 novos (não bloqueiam)
1. **Falso positivo no texto livre.** O `_FONE` pega número de 8 ou 10 dígitos com fronteira, como "pedido 12345678" e "NF 1234567890". Numa reclamação de garantia, a recusa pode irritar o admin.
   - O critério 3 da T-0023 pode ganhar 2 casos: um número de NF ou pedido no formato do Protheus e um código de produto. Assim, o comportamento fica conhecido.
   - A regra é a mesma que o site já usa para limpar a leitura, então a coerência está certa.
2. **Texto da RN-GER-016 divergente.**
   - `docs/desenho/T-0025.md:136` descreve a RN-GER-016 cobrindo DDR e Expositores (cópia antes e `antes`).
   - Na branch `gerente-projetos/T-0023-regras`, a RN-GER-016 trata só da config, e a exceção de DDR e Expositores está na RN-GER-012, sem citar a cópia do dia.
   - O contrato §10.9.3 manda (cópia e `antes` nos três). Basta alinhar uma das duas redações, dono a dono.

## Conferências
- `node scripts/coord.mjs verificar --por-commit a32b610..97ccba7`: OK, 3 commits, nenhuma violação. O commit novo traz `Agente: engenheiro-software`.
- O diff não tem segredo, documento, telefone nem e-mail. Nenhum dado digitado é tocado. Não há código, então não há `compileall` nem testes a rodar. `bap_dados.VERSAO` não é citado como mudado.
- Coerência com o `main` (T-0021 v4 e T-0035), conferida de novo nos trechos que mudaram: `MOTIVO_*`, `APLICADAS_WEB` (que já grava `valores`; o `antes` é acréscimo), o `_AVISO_SO_PC_WEB` e o §10.8.7.
- Este parecer vale para o head `97ccba7`. Commit novo = reteste novo.
