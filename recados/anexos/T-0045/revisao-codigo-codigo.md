# T-0045 — revisão de código (revisor-codigo), 27/11/2026

Este parecer vale para os head SHAs abaixo. Se entrar commit novo, a revisão tem de ser refeita.

| Branch | Head | Parecer |
|---|---|---|
| `modulo-rota/T-0045-visitas-nucleo` | `274d23a` | **1 🔴 · 5 🟡 · 2 🟢** (revisado só o `visitas_nucleo.py`) |
| `modulo-web/T-0045-visitas` | `8d7368f` (web 0.6.0) | **2 🔴 · 4 🟡 · 4 🟢** |

Base: contrato `.coord/contratos/visitas-nuvem.md` v1, ADR 0004 (RN-VIS-002 a 008, §7 a §9) e CLAUDE.md, tudo no `origin/main`. O clone foi só lido: nenhuma troca de branch. Os testes rodaram numa cópia (`git archive`) no scratchpad.

## Conferido em comum
- `verificar --por-commit <merge-base>..<branch>`: **OK nas duas** (1 commit cada, trailer `Agente:` certo). A web tem só a exceção do próprio diário.
- `bap_dados.VERSAO = 27` nas duas. Nenhum dado digitado foi tocado (`_EDICOES_POS_VENDA`, `_NCC`, `_GARANTIAS`, `_AUTORIZACOES` e os 3 `.json`), nem o `planner_config.json`.
- Nenhum segredo em código, teste ou doc: o `BAP_VISITAS_TOKEN` só vem do ambiente (`web/app/config.py`). Nenhum `screenshot` no diff (D5, regra 6 B).
- `compileall` limpo. Web: `pytest web/tests` deu **445 passed**, e o `test_T0045_visitas.py` sozinho deu **48 passed**. O ramo da rota não traz teste.
- Número do Diretor: não se aplica.

---

## 1. RN-VIS-002: dia fechado e junção PC × nuvem

**Hoje a regra está em 3 lugares:**
- `visitas_nucleo.dia_fechado(raiz, d)`, do PC, com o recurso da data do arquivo;
- `visitas_nucleo.dia_fechado_no_indice` / `juntar_baixado`, novos no ramo da rota, onde o **empate fica com a nuvem** (`n >= p`, `visitas_nucleo.py:1450`);
- `web/app/visitas.dia_fechado` / `juntar_baixado`, no ramo da web, onde o **empate fica com o PC** (`n > p`, `web/app/visitas.py:173`).

**O que o contrato manda.** O §3.1 diz: "`baixado_em` = o maior dos dois (**`visitas_nucleo.juntar_baixado`**, RN-VIS-002)". A RN-VIS-002 diz: "o PC e o site usam o mesmo resultado". O contrato não escreve o empate por extenso, mas aponta a função do núcleo como a regra. Então vale o empate da nuvem, e a web diverge.

**Por que é 🔴 e não 🟡.** O empate não é raro: é o caso normal.
- O PC importa o lote com `anotar_baixado(..., baixado_em da nuvem)` (contrato §4.4, passo 3).
- Na volta seguinte, ele devolve o mesmo horário no `fechados_pc` (§4.3).
- Daí em diante, a web marca todo dia importado como `origem: "pc"`, com `erros_vendedor: 0` e `refeito: false`.

O `deve_rodar` do cron (§3.1, item 8) deixa de ver o vendedor que falhou. Assim a retentativa da RN-VIS-006 fica dependendo de ela acontecer antes do PC importar. Conferido com um script:

```
nucleo empate: {'origem': 'nuvem', 'erros_vendedor': 2, ...}
web empate:    {'origem': 'pc',    'erros_vendedor': 0, ...}
```

**Uma fonte só, já que o Render publica só `web/` (`rootDir: web`).** A web não importa módulo da raiz em produção; conferi, e ela não importa nenhum. O reaproveitamento das regras do PC já é feito por **teste de paridade na raiz**: `tests/test_T0017_pacote_tres_farois.py` (fixture `web_app`, que põe `web/` no `sys.path` e roda `app.tabelas`/`app.pacotes` contra o `relatorios_nucleo`) e `tests/test_T0024_lote2_robo_web.py`. Proposta:
1. A regra é a do `visitas_nucleo` (`juntar_baixado`, `dia_fechado_no_indice`, `dias_a_baixar`).
2. A web mantém só um **espelho mínimo**, com a docstring "espelho de `visitas_nucleo.juntar_baixado` (contrato §3.1)", e passa a usar `n >= p`.
3. O agente `testes` cria `tests/test_T0045_paridade_web_nucleo.py`, com a fixture `web_app` e uma tabela de casos: nuvem maior, PC maior, **empate**, só um lado, horário sem fuso × `-04:00` e virada do dia em Manaus. O teste exige `baixado_em`, `origem`, `erros_vendedor` e `dia_fechado` iguais nos dois. A mesma tabela pega as cópias de `RE_PESSOAL` e de `RE_NOME_ARQ` (achados 🟡 W2 e 🟢 W8).
4. O engenheiro-software registra o empate no §3.1 (v1, aviso): "empate: nuvem, porque o PC anota o `baixado_em` da nuvem".

Opção descartada (v2): o site mandar as duas partes cruas e o cron, que tem o `visitas_nucleo` na imagem, juntar. A tela e o `periodo_padrao` do site precisariam do espelho de qualquer jeito, então isso não dá uma fonte só.

---

## Branch `modulo-rota/T-0045-visitas-nucleo` @ 274d23a

**🔴 R1 — `visitas_nucleo.py:1634`: `filtrar_espelho` põe valor de célula em `colunas_fora`.**
- No trecho do cabeçalho, todo texto que não termina em ":" vai para `_fora(_rotulo(txt))`. Isso inclui título, valor solto e nome.
- O `_rotulo` mantém os dígitos, então CPF ou telefone saem do contêiner sem varredura, pelo `medidas.espelho.colunas_fora` (§6), e ficam gravados no `rodadas.jsonl` do site.
- Teste com dado fictício: a linha `"FULANO DE TAL 12345678901"` saiu como `colunas_fora: ['ESPELHO DE ROTAS', 'FULANO DE TAL 12345678901', 'OBSERVACAO']`.
- Contraria o §3.6 ("nenhum valor de célula na saída") e a regra 6.
- Correção: só entra em `colunas_fora` o rótulo ("...:" ou título de coluna). Valor solto vira só uma contagem (por exemplo `soltos: n`).

**🟡 R2 — `visitas_nucleo.py:1613`: rodapé e título dentro da lista são mantidos e varridos.**
- Depois do título da lista, toda célula numa coluna permitida é copiada e varrida, mesmo numa linha sem `CODIGO` nem `CLIENTE`. O `ler_espelho` ignora essas linhas.
- Teste: `"Pagina 1 de 2"` na coluna DATA deu `achados: [{'coluna': 'DATA', 'tipo': 'formato'}]`. Isso é um falso `DADO_PESSOAL`, que pausa a nuvem.
- O §3.6 manda tirar rodapé e título de página.
- Correção: na lista, aplicar a mesma regra do `ler_espelho` (`codigo` ou `cliente` não vazio). A linha que não passar fica vazia.

**🟡 R3 — `visitas_nucleo.py:1540`: `achar_dado_pessoal` não varre número quando o formato é "texto" ou "numero".**
- `int` ou `float` nesses formatos devolve `None` sem passar pelos regex. Um CPF, CNPJ ou telefone gravado como número no `ENDERECO`, no `PDV`, na `JUSTIFICATIVA` ou num campo de texto do cabeçalho passa direto.
- Teste: `achar_dado_pessoal(12345678901, "texto")` deu `None`.
- Correção: no formato texto, aplicar os 4 regex em `str(int(v))`.

**🟡 R4 — `visitas_nucleo.py:1483`: `ESPELHO_PERMITIDAS` é cópia literal das chaves de `_ROTULOS_ESPELHO` e `_COLUNAS_ESPELHO`.**
- O §3.6 diz "as mesmas tabelas ... **sem cópia**".
- Correção: derivar a lista, com `cabecalho = tuple(_ROTULOS_ESPELHO)` e `colunas = tuple(k for k in _COLUNAS_ESPELHO if k not in ("KM DIST", "BONIF", "OBSERVACAO"))`, e manter o teste que compara com a tabela do contrato.

**🟡 R5 — a regra de dia fechado ficou duplicada.**
- `dia_fechado(raiz, d)` (`:149`) e `visitas_maxima.plano` continuam com a comparação própria.
- A ADR §9, item 3, diz que o `dias_a_baixar` "sai do `visitas_maxima.plano` e do `dia_fechado`".
- Correção: o `dia_fechado` passa a usar o `dia_fechado_no_indice` para comparar a hora (o PC mantém a conferência de que o arquivo existe), e o `plano` passa a usar o `dias_a_baixar`, no mesmo lote.
- Como o ramo partiu de um main antigo, o `visitas_maxima.py` não estava nele.

**🟡 R6 — o ramo não tem teste (regra 2).**
- Não há teste para `juntar_baixado`, `dias_a_baixar`, `achar_dado_pessoal` nem `filtrar_espelho`.
- O merge só pode entrar junto com os testes da ADR §8 do agente `testes`, inclusive `test_RN_VIS_007_saida_sem_valor_de_celula` (que pegaria o R1), o empate e o rodapé (R2).

**🟢 R7** — O `filtrar_espelho` repete o laço de leitura do `ler_espelho`. O contrato permite, mas uma função `_linhas_do_espelho` usada pelos dois evitaria que eles divergissem.

**🟢 R8** — O ramo partiu do main das 03h31. Depois disso, o `relatorios_nucleo.py` mudou no main (86 linhas), e o `filtrar_espelho` usa `cliente_sem_documento` e `texto_sem_contato`, que continuam lá. Rodar de novo no merge.

---

## Branch `modulo-web/T-0045-visitas` @ 8d7368f

**🔴 W1 — `web/app/visitas.py:173`: o empate fica com o PC.** É o caso do item 1 acima: o resultado diverge do `visitas_nucleo.juntar_baixado` e perde o `erros_vendedor` da RN-VIS-006. Correção: usar `n >= p`, documentar como espelho e cobrir com o teste de paridade.

**🔴 W2 — tela nova sem simulação aprovada (regra 10; ADR §9, item 4, de que depende o item 5).**
- `web/app/templates/visitas.html` e o botão em `_bc3_cab.html` são tela nova.
- Pelo R-20261127-011018, a simulação da tela "Atualizar visitas" está prevista para 28/11 às 12h, e ainda não há PNG nem aprovação do po por delegação (R-20261127-013010).
- O PR pode ser aberto, mas o merge só depois da aprovação, com designer-ux e design-de-marca sem 🔴.

**🟡 W3 — `web/app/visitas.py:208` e `:584`: a "segunda guarda" `achar_no_excel` está fora do contrato e é mais fraca do que promete.**
- **Contrato:** o §3.4 diz "o site **nunca abre** o Excel", e as respostas 422 previstas são só `sha256` e `esquema inválido`. A web acrescentou a abertura do zip, o 422 `{"erro": "dado pessoal"}` e a pausa `DADO_PESSOAL` gravada pelo próprio site. Ou isso entra no contrato (engenheiro-software; código novo = v1, aviso aos consumidores, inclusive dizendo que o cron trata esse 422 como `SITE_RECUSOU`), ou sai.
- **XXE:** não há risco, porque não usa parser XML, só regex.
- **Zip bomb, por membro:** o teto `ZIP_MEMBRO_MAX` de 8 MB vale de fato, porque o `zipfile` corta no `file_size` declarado e confere o CRC.
- **Zip bomb, no total:** não há teto. Teste: um xlsx de 1,6 MB (abaixo do `ARQUIVO_MAX`) com 200 membros de 8 MB foi descompactado para cerca de 1,6 GB em 2,9 s e **não foi recusado**. Isso roda síncrono dentro da rota async (`main.py:965`) e trava o site inteiro durante a leitura, por trás do token.
- **Lacunas:** ela não lê número (`<v>`), não decodifica entidade XML (`fulano&#64;x.com` passou) e não junta trechos de texto com formatação.
- **Correção:**
  - soma dos `file_size` até 16 MB e no máximo 64 membros, senão 413;
  - `run_in_threadpool` no `receber_lote`;
  - na docstring, dizer que é rede extra, não garantia (a garantia é o filtro do cron, §3.6).

**🟡 W4 — `web/app/visitas.py:97`: a terceira cópia dos regex de dado pessoal (`RE_PESSOAL`).** Se a W3 ficar, entra no teste de paridade com o `visitas_nucleo`, para as duas redes não divergirem.

**🟡 W5 — `visitas.html:67`: o diagnóstico não aparece na tela do admin.** O §6 diz que a linha do diagnóstico aparece "o mesmo na tela do admin": tempos, `pico_mb`, `colunas_fora` (só a contagem), `limpos` e `achados`. Hoje a tela mostra só `estado · codigo · em`, e o Alexandre precisa desses números para dar o "ok" antes de ligar a agenda.

**🟡 W6 — `web/app/visitas.py:179`: `periodo_padrao` reescreve a conta dos "dias abertos" do `dias_a_baixar`.** Fica aceitável se entrar no espelho com paridade (item 1). Senão, é a mesma regra em mais um lugar.

**🟢 W7** — `main.py:907`: o `sem_token_cron` é cópia do `sem_token`. Basta um `_bearer(request, esperado)` para os dois.

**🟢 W8** — `RE_NOME_ARQ` (`:95`) é uma cópia mais restrita do `visitas_nucleo._RX_ARQ_ANALITICO`: só `.xlsx` e sem `re.I`. Pode ficar assim (no site, mais restrito é melhor), mas vale pôr no teste de paridade.

**🟢 W9** — `LOTE_BRUTO_MAX` (24 MB), `lotes_sem_confirmar_vencidos` no `/saude` e o 200 do `confirmar` com `gravados` são acréscimos ao contrato, compatíveis com a v1. Registrar no §2 e no §4.5 (aviso).

**🟢 W10** — O `_validar_fim` aceita `medidas` livre até 8 KB. Validar `medidas.espelho.colunas_fora` com o `RE_ROTULO` seria uma segunda rede para o R1.

---

## 2. Segurança (resumo)

| Item | Resultado |
|---|---|
| `BAP_VISITAS_TOKEN` | só do ambiente; se for curto (menos de 32 caracteres) ou faltar, dá 401 em todo o §3; `hmac.compare_digest` ✓ |
| Separação dos tokens | o do cron não abre `/api/pacote`, `/api/edicoes` nem `/api/visitas/lotes`; o do robô não abre o §3 (teste) ✓ |
| 403 | as rotas da tela usam `usuario(request, perfis)`, que dá `PermissionError` e 403; há CSRF em todo POST; teste por perfil ✓ |
| Tetos do corpo | `content-length` e leitura em streaming até 8 MB; gzip limitado a 24 MB; JSON da API até 64 KB (confirmar até 256 KB); cada Excel até 2 MB ✓. Zip sem teto total: ver W3 |
| XXE | não há risco (regex, sem parser) ✓ |
| Recusa com dado pessoal | `detalhes` só com índice e tipo; `rodadas.jsonl` só com a contagem; o teste confere que o valor não aparece ✓ |
| Sem print (6 B) | nenhum `screenshot`, e o texto vem só dos códigos do §5 ✓ |
| Lado do núcleo | o 🔴 R1 deixa um valor sair no `medidas` |

## 3. Rotas do robô do PC (§4.1 a §4.3)

**Estão no contrato, e não foram feitas por conta própria:** a ADR §9, item 5, dá ao modulo-web "contrato §3, §4.1 a §4.3, §4.5 e §7". O que conferi:
- **§4.1:** mesmo formato da `/api/edicoes`, até 20 linhas, pela `edicoes.Fila` parametrizada (`subpasta`, `prefixo`), sem cópia ✓.
- **§4.2:** corpo gzip com `X-BAP-SHA256`, e 404 quando o lote saiu pela retenção ✓.
- **§4.3:** `fechados_pc` obrigatório; `motivo` dentro da lista; um `erro` tira só a parte da nuvem do dia; 409 `{"erro": "epoca"}` ✓.
- **Só por fora do contrato:** o `gravados` na resposta (W9).

## 4. Tetos, pausa, concessão e `/saude`

- **RN-VIS-004:** a concessão dura 10 min e é renovada a cada `progresso`. Se vencer, vira `RODADA_INTERROMPIDA`, gravada pelo site. Ela fica em disco, com `flock` e trava de thread, e passa por reinício. Uma segunda concessão dá 409 ✓.
- **RN-VIS-008:** conta na concessão; teto por motivo (4/3/1/2) e da soma (8); 429; zera na virada do dia em Manaus ✓.
- **RN-VIS-005 e RN-VIS-007:**
  - os códigos do `PAUSAM` pausam;
  - `TELA_MUDOU` 2 vezes na mesma fase também pausa;
  - o `Retomar` é só do admin;
  - com `DADO_PESSOAL`, ele exige o recado `^R-\d{8}-\d{6}-alexandre$`, grava no `pedidos.jsonl` só o perfil e volta o diagnóstico a `pendente` ✓.
- **RN-VIS-006:** o `refeito` é marcado na concessão ✓, mas a W1 anula isso depois que o PC importa.
- **Agenda:** só liga com o diagnóstico `ok` e o `fechados_pc_em` nas últimas 24 h ✓.
- **`/saude.visitas`:** agenda, estado do diagnóstico, última rodada, código, código da pausa, id da rodada ativa, fase, lotes a importar, total de tentativas e vencidos. Não há nome, usuário nem valor ✓.

## Pronto quando
- **Rota:** R1 a R5 corrigidos e os testes do R6 no mesmo lote, num head novo, com revisão nova.
- **Web:** W1 corrigido; W2 com a simulação aprovada; W3 a W6 corrigidos ou com o contrato v1 atualizado pelo engenheiro-software; revisão nova no head novo.
