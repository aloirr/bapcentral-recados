# Reteste do revisor-codigo — PR #137 (T-0045)

- **Head SHA retestado:** `59864e7fdb1f602847581c497d692a5e34731836`. É filho do `a6c719c`, o do parecer `revisao-codigo-pr137.md`.
- **Lido:** `git diff a6c719c 59864e7` e os arquivos do 59864e7 inteiros (contrato, ADR 0004 e desenho), sem trocar de branch.
- **Renumeração das RN-VIS:** a mudança para 002…008 é sabida, por colisão com a Aderência (#135). Não entra aqui como achado.
- **Data:** 27/11/2026 (Manaus).

## Resultado: os 4 🟡 fecharam; há 1 🟡 novo, que impede aprovar

## Os 4 🟡 do parecer anterior

| # | Achado | Situação | Onde |
|---|---|---|---|
| 1 | O lote pode levar CNPJ, telefone e e-mail | **fechado** | contrato §3.6: `ESPELHO_PERMITIDAS` com teste contra a tabela; `filtrar_espelho` manda só o `destino`; `achar_dado_pessoal` procura e-mail, CNPJ, CPF, telefone e formato; achado = o dia não sobe e o código `DADO_PESSOAL` **pausa** (§5); `achados` sem valor de célula; o diagnóstico com achado não liga a agenda (§5.1, §6). ADR §0, §6, §7, §8 |
| 2 | As novas tentativas não têm limite | **fechado** | `tentativas_hoje` no `trabalho` (§3.1); `TENTATIVAS_DIA` por motivo e `LOGINS_DIA_MAX` 8; contado **na concessão** (§3.2); `refeito: true` já na concessão da retentativa; 429 "teto do dia"; `NOVA_TENTATIVA` fechada; `deve_rodar` com o teto nos passos 3, 4, 6, 7 e 8 |
| 3 | O `render.yaml` "no mesmo PR" | **fechado** | `docs/desenho/T-0045-render-yaml.md:12`: num PR próprio (`alexandre/T-0045-render-yaml`), no item 10 do §9 da ADR |
| 4 | A ADR cita a branch antiga | **fechado** | não há mais `engenheiro-software/T-0045-render-yaml`; ADR `:106` e `:265` apontam para os arquivos deste PR |

## Conferências que continuam valendo

- **`.diff` do `render.yaml`:**
  - aplica limpo sobre o a32b610 (`git apply --check` numa cópia fora do clone);
  - só os comentários mudaram;
  - `sync: false` nas 2 secretas;
  - o site no Starter.
- **`verificar --por-commit origin/main..59864e7`:** OK, 4 commits, nenhuma violação.
- **Governança:** nenhuma no diff.
- **`.dockerignore` novo:** vai como texto, e o dono proposto entra na governança 1, junto com o Dockerfile.
- **Segredos:** nenhum valor secreto. O plano B do token agora usa `secrets.token_urlsafe(32)`, gerado no PC do Alexandre.
- **CI no head:** o check `conferir` ainda estava `in_progress` (GitGuardian `neutral`).

## 🟡 Novo (corrigir antes do merge)

**5. Com o desenho atual, o `DADO_PESSOAL` deve disparar quase todo dia, e o caso já tem solução no repositório.**
- Onde:
  - contrato §3.6 (`:201`: `CLIENTE` é texto livre, e `:204-211`: a varredura pausa);
  - ADR `:218`.
- O problema:
  - o mesmo cadastro de clientes traz CPF ou CNPJ **no nome**, medido no `.coord/contratos/relatorio.md:760`:
    - "Pedidos": 222 no começo e 84 com CPF no fim, de 2.216 linhas;
    - "Cliente a cliente": 198 e 30, de 1.441;
  - um dia do Espelho tem 15 vendedores com vários clientes cada, e a chance de ao menos uma linha com documento é quase certa;
  - o diagnóstico já deve sair `DADO_PESSOAL`, e cada rodada vai pausar;
  - o "Retomar" com recado vira rotina, e a nuvem não funciona.
- Redundância:
  - a ADR deixa a "saída (b) mascarar no filtro" para depois;
  - a função já existe: `relatorios_nucleo.cliente_sem_documento` / `sem_documento` (contrato do relatório §10.7, RN-POS-004), usada no pacote do site (`bap_automation.py:7229`).
- Correção:
  - no `filtrar_espelho`, aplicar `cliente_sem_documento` no `CLIENTE`, reusando a função e sem reescrever o regex, **antes** da varredura;
  - a varredura fica como rede para o que sobrar;
  - pôr `relatorios_nucleo.py` (ou só o que ele precisa) no `COPY` e no `buildFilter`;
  - o teste de igualdade passa a ser "igual, fora o `arquivo` e o `CLIENTE` sem documento", com o efeito no `VISITAS_POR_CLIENTE` e no acompanhamento conferido pelo código do cliente;
  - na ADR, tirar o (b) da lista de saídas "para depois", porque passa a ser o desenho.

## As perguntas do gerente

- **"Retomar só com o id do recado do Alexandre" funciona?**
  - Na mecânica, sim: o regex `^R-\d{8}-\d{6}-alexandre$`, 400 sem o id e o registro no `pedidos.jsonl`, sem nome.
  - **Mas o site não confere** se o recado existe nem se é do Alexandre (e não deve ter token do repositório de recados). Qualquer admin digita um id bem formado. É **trilha de auditoria, não controle**. 🟢: dizer isso na ADR `:218` e na RN-VIS-006 ("só vale com a decisão" → "fica registrado com o id da decisão").
  - **Retomar sem mudar o contrato não adianta:** as 3 saídas da ADR `:218` mudam o contrato (v2) e o código do cron. Com o mesmo código, a primeira rodada depois do Retomar acha o mesmo dado, pausa de novo e gasta um login do teto. Nenhum dado vaza, porque o lote não sobe.
  - 🟢: o Retomar de `DADO_PESSOAL` volta o `diagnostico` a `pendente`, com 2 vendedores e sem lote, em vez de soltar a agenda direto. A agenda só volta com o diagnóstico limpo, rodado no código novo.
- **O vigia com `os._exit(1)` aos 58 min resolve?**
  - **Sim, para o que se pedia:** some a saída 3, e a regra 0/1 fica fechada (contrato §5, `:302`).
  - A concessão vence, o site grava `RODADA_INTERROMPIDA`, e a tentativa já foi contada na concessão.
  - O `CMD` em forma exec deixa o Python como PID 1. Quando ele sai, o contêiner acaba e leva o driver e o Chromium junto.
  - Pelo `RODADA_MAX_MIN` de 45 min, conferido no fim de cada dia (2,5 a 5 min por dia), o `parar` aos 55 vem antes.
  - 🟢 que sobram para o Dockerfile e o `rodar.py`:
    - Python como PID 1 não recolhe os zumbis do Chromium e ignora o SIGTERM do Render sem um handler: usar `tini` (ou `dumb-init`) no `ENTRYPOINT`, ou instalar um handler de SIGTERM que liga o `parar`;
    - o `/dev/shm` do contêiner costuma ser pequeno: lançar o Chromium com `--disable-dev-shm-usage`, senão aparece `NAVEGADOR_FALHOU` sem causa clara.

## 🟢 Outros

- **Pior caso de custo com o teto:** 8 logins × até 45 min = 360 min/dia, ~US$ 6/mês, acima do "~US$ 1 a 3". O típico continua na faixa. Pôr essa linha na conta da ADR §4, para o Alexandre ver o teto em dinheiro.
- **`buildFilter`:** pôr também o `.dockerignore`, que muda o que entra no build.

## Observação de processo

- Por instrução de quem pediu, o parecer ficou só neste arquivo, sem commit e sem recado.
- O gerente-projetos encaminha ou pede o registro em `docs/revisao/T-0045.md`.
