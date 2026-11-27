# T-0045 · PR #137 · Reteste final de redundância e excesso (corretor-redundancias)

- **Escopo:** `git diff 59864e7 e2c43ec` (2 commits: `25d54ac`, que renumera as RNs para RN-VIS-002 a 008, e `e2c43ec`, com a limpeza RN-GER-011 e o fechamento do reteste). São 5 arquivos (+91 −70), lidos no estado do head.
- **Head SHA retestado:** `e2c43ec4b193a38164ad272ebef6a4fe4e37a0b6`.
- **Pareceres anteriores:** `redundancias-pr137.md` e `reteste-redundancias-pr137.md`.
- **Resultado:** **não libera, por 1 achado baixo novo** (RD-0085, 3 itens de texto em docs). O resto do RD-0072 e os RD-0082, RD-0083 e RD-0084 estão fechados. Os RD-0073 a RD-0081 continuam fechados.
- **Dono:** engenheiro-software.

## 1. Situação

| RD | Situação | Evidência no head |
|---|---|---|
| RD-0072 (resto) | **Fechado.** "Proibido no cron" virou uma lista só, no contrato §1 (25-27: "a única lista", com uma parte para o ambiente e outra para o código, incluindo HAR, `console` e print). A ADR:223 só aponta para o contrato ("está numa lista só, no contrato, §1"). | contrato:25-27; ADR:223 |
| RD-0082 | **Fechado.** Em `medidas.espelho` ficam só `colunas_fora` e `limpos`. Os achados vão só no `achados` do `fim` (contrato:339: "Os achados vão só no `achados` do `fim` (§3.5)"). | contrato:335, 339 |
| RD-0083 | **Fechado.** A ADR:42 virou o resumo curto ("limpas e com varredura de dado pessoal (§7, RN-VIS-007)"). A ADR:233-234 traz só o porquê (limpar antes de procurar, com a contagem de 84 em 2.216 nomes, e parar antes de guardar). A ADR:218 explica agora por que o id do recado é registro e não controle: é informação nova, que não está na RN nem no contrato, e o contrato:276 aponta para lá. | ADR:42, 200, 218, 233-234 |
| RD-0084 | **Fechado.** O §8 do contrato saiu, e a linha 4 é o único ponteiro para a ordem. A frase do build vermelho saiu do desenho §4 e ficou só na ADR:279. A ADR:187 diz "os dias que ele fechou", sem o número 40. | contrato:4; desenho:113; ADR:187, 279 |

## 2. O que a correção trouxe

**Conferido, sem repetição nova:**
- **Renumeração RN-VIS-002 a 008:** está igual nos 3 arquivos, no diário e nos títulos dos testes da ADR §8. Não sobrou `RN-VIS-001` no PR (a 001 é a da Aderência, PR #135).
- **Limpeza RN-GER-011:** reaproveita `relatorios_nucleo.cliente_sem_documento` e `texto_sem_contato`. As 2 funções já existem no `main` (`relatorios_nucleo.py:846` e `:860`), e o contrato:211 diz "sem copiar o regex". Não é uma cópia da regra.
- **`limpos` e `colunas_fora`:** cada um está num lugar só (§3.6 e `medidas`), e o log leva só a contagem.

### RD-0085 · Três fatos novos escritos 2 vezes (ADR × desenho/contrato, e o custo do pior caso)
- **Onde:**
  1. **"só importam a biblioteca padrão no topo":** está na ADR:114 e no desenho:108, além do comentário do `Dockerfile` (desenho:82, que é o próprio texto do arquivo e fica).
  2. **Processo no contêiner:** a ADR:296 repete a solução que está no contrato:58-61 ("`tini` como PID 1, `SIGTERM` tratado e Chromium com `--disable-dev-shm-usage`").
  3. **Pior caso em 2 números:** ADR:125 ("cerca de US$ 6 por mês a mais") × ADR:170 ("limita o pior mês a cerca de US$ 7, com as voltas sem trabalho"). São 2 valores para o mesmo indicador, com bases diferentes, na mesma ADR.
- **Tipo:** doc · indicador. **Impacto:** manutenção (itens 1 e 2) e leitura (item 3: qual é o pior caso, US$ 6 ou US$ 7?).
- **Severidade:** baixa.
- **Proposta:**
  1. ADR:114, **antes:** "(a limpeza do §7; os dois só importam a biblioteca padrão no topo)." → **depois:** "(a limpeza do §7; desenho, §3)."
  2. ADR:296, **antes:** "… nem trataria o `SIGTERM` do Render. Por isso, `tini` como PID 1, `SIGTERM` tratado e Chromium com `--disable-dev-shm-usage` (contrato, §2; `Dockerfile` no desenho, §3)." → **depois:** "… nem trataria o `SIGTERM` do Render; a solução está no contrato, §2."
  3. ADR:125, **antes:** "**custo (o teto em dinheiro):** no pior caso, os 8 logins de todo dia com rodadas de até 45 min, são 360 min por dia, ou **cerca de US$ 6 por mês** a mais [SUPOSIÇÃO de preço]. Sem teto, …" → **depois:** "**custo:** no pior caso, os 8 logins de todo dia com rodadas de até 45 min são 360 min por dia (em dólar, §4). Sem teto, …". O número do pior mês fica só na ADR:170 (cerca de US$ 7). O `testes` confere o valor em relação à regra; isso não é deste parecer.

## 3. Manter (não é achado)
- **Lista do `buildFilter`:** está no desenho:24 e no `.diff`, e o teste "todo arquivo do `COPY` está no `buildFilter`" (desenho:109) pega se as duas divergirem. Ela é a explicação para quem dá o "autorizo" e foi aceita no 1º reteste.
- **Comentário do `Dockerfile`** (desenho:71-72 e 82): é o próprio texto do arquivo, e quem abre o `Dockerfile` precisa dele.
- **`MAXIMA_CAPTCHA` × `MAXIMA_CONFIRMACAO`:** continua `manter?`, como antes.

## 4. Pendências
- O catálogo `docs/redundancias/catalogo.md` e os recados não foram feitos, por instrução de quem chamou. [SUPOSIÇÃO] Quem chamou leva o RD-0085 ao engenheiro-software.
- Reteste do RD-0085 no próximo head.
