# bapcentral-recados

Recados do time de agentes do BAP Tools, fora do repositório de código (`aloirr/bapcentral`). **Repositório privado.** É a mesma estrutura do `aloirr/macuxifdv-recados`.

## Estrutura
- `recados/<destino>/R-AAAAMMDD-HHMMSS[-n]-<remetente>.md`: um arquivo por recado e por destino. Recados são imutáveis.
- `recados/anexos/`: anexos citados nos recados (prints, PDFs de simulação).
- `lidos/<agente>.txt`: um id por linha. Com `merge=union` no `.gitattributes`, duas marcações ao mesmo tempo não geram conflito.
- `estado/`: marcadores das Actions.

Destinos: `gerente-projetos`, `po`, `engenheiro-software`, `engenheiro-dados`, `modulo-robo`, `modulo-farois`, `modulo-posvenda`, `modulo-rota`, `modulo-metas`, `modulo-web`, `testes`, `revisor-codigo`, `alexandre` e `todos`.

## Como chega e sai
- **Time (nuvem):**
  - o `node scripts/coord.mjs` do repositório de código grava (`enviar`, `lido`) e lê (`caixa`, `pendencias`, `ler`, `fio`) direto aqui, pela API do GitHub;
  - um commit por envio;
  - o token fica na variável `BAP_RECADOS_TOKEN` dos ambientes do claude.ai/code.
- **Alexandre:**
  - conversa com o **po** na sessão BapCentral-PO (o po grava os recados);
  - ou abre uma issue com o formulário **Recado** (celular ou computador): a Action `issue-recado.yml` vira o arquivo do recado, comenta o link e fecha a issue. Só vale para issue aberta pela conta `domontecristo`.
- **Telegram (opcional, desligado):**
  - `aviso-telegram.yml` avisa cada recado novo em `recados/alexandre/`;
  - `status-horario.yml` manda o resumo de hora em hora.
  - Para ligar:
    1. crie os secrets `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`;
    2. crie a variável `TELEGRAM_LIGADO` = `sim`;
    3. tire o `#` do `schedule` do resumo.

## Token do time (Settings da conta → Developer settings → Fine-grained tokens)
- Repositório: só o `aloirr/bapcentral-recados`.
- Permissão: **Contents: Read and write** (e Metadata: Read).
- Cole o valor só na variável `BAP_RECADOS_TOKEN` dos ambientes BapCentral-PO e BapCentral-GP do claude.ai/code. Nunca em arquivo, recado ou chat.

## Regras
- Não edite nem apague recado: responda com um recado novo.
- Não faça force push.
- Testes das Actions: `node --test .github/scripts/recados-lib.test.mjs` (Node 22+).
