# Reteste final do revisor-codigo — PR #137 (T-0045)

- **Head pedido:** `e2c43ec4b193a38164ad272ebef6a4fe4e37a0b6`.
- **Head atual do PR**, durante o reteste: `6502495d025976241980d1cf06024cb45ea3a173`, filho do e2c43ec, lido também.
  - Muda só a ADR (`docs/decisoes/0004-visitas-maxima-no-render.md`) e o diário.
  - O conteúdo é o RD-0098: cada fato fica num lugar só; o custo do pior mês fica no §4, com a conta (8 × 45 min × 30 ≈ US$ 6,30, mais US$ 0,85 ≈ US$ 7); nenhuma regra muda.
- **Base:** `origin/main` a32b610.
- **Data:** 27/11/2026 (Manaus).
- **Pareceres anteriores:** `revisao-codigo-pr137.md` (a6c719c) e `reteste-codigo-pr137.md` (59864e7).

## Resultado: **aprovado no head `6502495`** (sem 🔴 e sem 🟡)

## CI `conferir`

| Head | Resultado |
|---|---|
| `e2c43ec` | **cancelado** (run 45946276221): "Canceling since a higher priority waiting request ... exists", por causa do push do 6502495. Pararam os "Testes da web"; o resto tinha passado |
| `6502495` | **verde** (run 45946513353): donos, governança, compileall, pytest da raiz, smoke dos processos, CLI e guardiões, testes da web. GitGuardian `neutral` |

Como o e2c43ec não tem CI concluído, o merge vale só no **6502495**: CI verde no head.

## O que fechou

- **🟡5 (o `DADO_PESSOAL` quase todo dia): fechado.**
  - Contrato §3.6: limpeza da RN-GER-011 **antes** da varredura, com as funções que já existem:
    - `relatorios_nucleo.cliente_sem_documento` no `CLIENTE`;
    - `texto_sem_contato` na `JUSTIFICATIVA`.
  - A varredura fica como rede; `limpos` só traz contagens, sem valor.
  - O teste de igualdade foi ajustado; a ADR §6 diz que a limpeza já é o desenho.
  - `relatorios_nucleo.py` e `bap_dados.py` estão no `COPY` e no `buildFilter`, com o teste "todo arquivo do `COPY` está no `buildFilter`".
  - Conferido aqui, numa cópia isolada (`python -I`) do main:
    - os dois só importam a biblioteca padrão no topo, e importá-los não carrega `pandas`, `openpyxl`, `meta_nucleo`, `pastas_bap` nem `xlsx_rapido`;
    - as duas funções existem, e com texto fictício tiram o documento do nome (mantendo o código) e trocam telefone e e-mail por `[removido]`.
  - `bap_dados.py` só entra na imagem: VERSAO continua 27.
- **A `JUSTIFICATIVA` com `texto_sem_contato`** (por conta do engenheiro): aceito.
  - É a mesma regra (RN-GER-011), aplicada com a função que já existe, num texto livre que só a varredura cobria.
  - Diminui as pausas falsas, sem mudar nenhuma decisão do Alexandre.
  - Não é mudança a mais: faz parte do 🟡1 (o lote não leva telefone nem e-mail).
- **Os 🟢 do reteste anterior: fechados.**
  - **Retomar:** a ADR §6 e a RN-VIS-007 dizem agora que o id do recado é **registro, não controle**. O Retomar de `DADO_PESSOAL` volta o `diagnostico` a `pendente`, e `deve_rodar` só roda com o diagnóstico `ok` (contrato §3.1, passo 5).
  - **Processo no contêiner:** o `tini` é o PID 1 (`ENTRYPOINT`), o `SIGTERM` é tratado com o `parar`, e o Chromium abre com `--disable-dev-shm-usage` (contrato §2; Dockerfile no desenho §3).
  - **Pior mês em dinheiro:** na ADR §4 (≈ US$ 7 com o teto; ≈ US$ 13 sem ele).
  - **`.dockerignore`:** entrou no `buildFilter`.
- **RN-VIS renumeradas** para 002 a 008: sabido, não é achado.

## Conferências gerais no head 6502495

- `.diff` do `render.yaml`: aplica limpo sobre o a32b610; `sync: false` nas 2 secretas; o site no Starter; o cron no Standard.
- `verificar --por-commit origin/main..6502495`: OK, 7 commits, nenhuma violação.
- Nenhuma governança no diff (`render.yaml`, `donos.json` e Dockerfile seguem como texto, para os PRs próprios do §9).
- Nenhum valor secreto; sem print; sem Graph; sem dado pessoal em exemplo (só marcadores como `<nome_limpo>`).

## 🟢 Para o próximo passo (não bloqueia)

- **Contra o risco da ADR §11** (o `relatorios_nucleo.py` muda muito e refaz a imagem): se os minutos de build pesarem, as 3 funções da RN-GER-011 (`sem_documento`, `cliente_sem_documento`, `texto_sem_contato`) vão para um módulo pequeno, por recado ao dono do `relatorios_nucleo` (modulo-farois).

## Observação de processo

- Por instrução de quem pediu, o parecer ficou só neste arquivo, sem commit e sem recado.
- O gerente-projetos encaminha ou pede o registro em `docs/revisao/T-0045.md`.
- Commit novo no PR = revisão nova.
