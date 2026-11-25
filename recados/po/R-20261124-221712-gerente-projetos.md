---
id: R-20261124-221712-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T22:17:12-04:00
---
# Pareceres do revisor-codigo: #62, #63, #64 — 1 🟡 cada; decisão: NOME sem documento no site

> Pareceres do revisor-codigo, com checagem de redundância (subagente do gerente-projetos; gravados pelo gerente sem alteração; varredura: limpo).

---
# Revisão T-0017, entrega 2 · PR #62 (modulo-posvenda) · cobranca_whatsapp.py

- Head revisado: `b9da388051626431815a6e5bf503f5eef612c82e` (commit novo = revisão nova).
- Contrato: §10.6.3 e §10.6.7 de `.coord/contratos/relatorio.md` (main). Regras: RN-POS-001 a 003.
- Parecer: **sem 🔴; 1 🟡 (decisão do gerente sobre o contrato) e 3 🟢.**

## Conferido
- `pacote_web`: as 6 chaves do bloco e as 14 do `ItemFila` batem com o §10.6.3. Sem `telefone_cad`. `ultimo` com `origem` PC/WEB, `web_epoca` e `web_ate_seq` vindos do robô. `gerado_em` em ISO `-04:00`.
- `importar_web`: só acrescenta ao `COBRANCA_WEB.csv`, com `CAMPOS_CSV + ("id",)`, `maquina = "WEB"`, `em_atraso` com 2 casas, BOM só na criação. Pula `id` repetido. Erro de disco levanta. Os `COBRANCA_<MAQUINA>.csv` ficam intocados (regra 7). O `historico()` e a janela não mudam.
- `nome_saudacao`: tira CPF/CNPJ do começo do nome só na saudação. No pacote simulado das bases congeladas: 0 mensagens com documento.
- Sem segredo e sem dado pessoal no código. `bap_dados.VERSAO` não foi tocado. Nenhum dado digitado alterado.
- Testes: o merge temporário dos 3 PRs com `testes/T-0017-testes-cobranca` (56ae5db) dá `pytest tests/` 214 passed e `web/` 109 passed. Os testes de dono (pós-venda e robô) dão 27 passed. O `verificar modulo-posvenda --base origin/main` sai OK, e os 3 commits trazem `Agente: modulo-posvenda`.

## 🟡 corrigir antes do merge
1. `cobranca_whatsapp.py:131` e `:309`: o campo `nome` da fila leva o NOME cru. No pacote simulado das bases congeladas, 1 item da fila tem o NOME começando por documento (MEI: CPF ou raiz de CNPJ). As tabelas do PR #64 têm o mesmo caso em 8 linhas. Isso esbarra na RN-POS-004 ("CNPJ não vai ao site") e no foco "nenhum CNPJ/CPF no pacote". O código segue o contrato: o §10.6.3 manda o NOME da aba "Por cliente", e o §10.6.2 manda igualdade célula a célula. Por isso a saída é uma **decisão do gerente**, pelo engenheiro-software, numa destas formas:
   - um acréscimo ao §10.6.2 e ao §10.6.3 que mande passar o NOME do pacote (fila e tabelas) pelo `nome_saudacao`, com o `testes` comparando célula a célula "PC depois da máscara";
   - ou o registro de que o NOME de MEI é aceito como está.

## 🟢 sugestões
1. `cobranca_whatsapp.py:261`: o `historico_origem` repete, linha a linha, o laço do `historico()` (`:212`). O `historico()` pode virar `{c: (q, a) for c, (q, a, _) in historico_origem(raiz).items()}`, com o mesmo comportamento.
2. `cobranca_whatsapp.py:282`: o `_gerado_em` usa o deslocamento fixo `-4`. É correto para Manaus, que não tem horário de verão, mas o resto do time usa `ZoneInfo("America/Manaus")`. Na produção, o robô sempre passa o `gerado_em`.
3. `importar_web`: um registro sem `id` é pulado em silêncio, mas o robô conta o `seq` dele no `ate_seq` (PR #64). A web sempre manda `id`, então o caso é teórico. Vale um aviso no log, sem dado pessoal.

**Redundância:** o `historico_origem` duplica o laço do `historico()` (🟢 1). A regra do `celular()` e a da mensagem não foram reescritas: o PR reusa `fila`, `mensagem` e `celular`.

---
# Revisão T-0017, entrega 2 · PR #63 (modulo-web) · web/

- Head revisado: `4406fe0f8c85a87fcee93c6529bcde0b73b5abeb` (commit novo = revisão nova).
- Contrato: §10.6.1 a §10.6.6 e §10.6.8 de `.coord/contratos/relatorio.md` (main). Regras: RN-POS-002, RN-POS-003 e RN-POS-004.
- Parecer: **sem 🔴; 1 🟡 e 8 🟢.**

## Conferido (segurança)
- **CSRF:** o `POST /farol/pl_inadimplencia/cobranca` passa pelo `formulario()`, que confere com `hmac.compare_digest`. Sem o campo ou com valor errado, a resposta é 403 (há teste).
- **Perfil no servidor:** o corte é feito antes do HTML. `?aba=titulos|cliente` responde 403 para quem não é admin, pós-venda ou gerente; `?aba=cobrar` e o POST respondem 403 para quem não é admin ou pós-venda. Uma aba de tabela em outro farol também dá 403.
- **XSS:** o Jinja escapa tudo sozinho. O JS só usa `textContent` e `createElement`, sem `innerHTML`. O `href` do wa.me leva só dígitos e `encodeURIComponent`. As cores do `style` passam pelo `RE_COR` (`#RRGGBB`). A CSP é `default-src 'self'` e não há script inline.
- **Bearer só na API:** o `GET /api/cobranca` e o `POST /api/cobranca/confirmar` usam o `sem_token` (401 com `WWW-Authenticate`) e não aceitam cookie de sessão (há teste). A rota da tela não aceita Bearer.
- **Idempotência:** o mesmo usuario + cliente + acao em menos de 60 s devolve o registro original com `repetido: true`. O `confirmar` também é idempotente, e a limpeza roda até no repetido.
- **Trava entre processos:** `threading.Lock` mais `fcntl.flock` em `cobranca/.trava`. O `estado.json` é gravado de forma atômica (tmp, fsync e replace), e o jsonl só acrescenta, com fsync.
- **503:** um `OSError` no diário devolve JSON 503 e nenhuma linha é gravada (há teste).
- **Dado pessoal:** a validação recusa as colunas TELEFONE, CNPJ, CPF e E-MAIL, o `telefone_cad` e chaves extras. O registro de acesso guarda login, rid, aba, ação e hora, sem cliente nem telefone. As páginas saem com `no-store` e `noindex`.
- **Fuso:** `ZoneInfo("America/Manaus")` no `quando`, na situação, no "hh:mm" e na limpeza. São 7 pacotes guardados. O `pacote_sha` é calculado sobre os bytes do arquivo guardado. O item sai primeiro do pacote da página, depois do vigente, senão 404.
- **Contrato:** colunas 20 e 19 com as ocultas, bloco de status inteiro ou ausente, `chip` só nas 3 colunas, `web_epoca` e `web_ate_seq` de acordo com o §10.6.3, e a API de acordo com o §10.6.6. O pacote simulado das bases congeladas (PR #64) passa no `pacotes.validar` com 0 erros.
- Testes: o merge temporário dá `web/` 109 passed e `pytest tests/` 214 passed. O `verificar modulo-web --base origin/main` sai OK, e os 5 commits trazem `Agente: modulo-web`.

## 🟡 corrigir antes do merge
1. `web/app/cobranca.py:296` (`aviso_curto`): o aviso "telefone inválido (repetido)" do `celular()` do PC fala de **dígitos repetidos** (ex.: `99 99999999`, §10.6.3). A tela mostra "Número repetido em outro cliente: digite o certo", e esse texto está errado. No pacote simulado, 2 itens da fila recebem esse aviso. Sugestão: "Número inválido (dígitos repetidos): digite o certo".

## 🟢 sugestões
1. `web/app/static/cobranca.js:104` (`numero()`): é uma terceira versão da regra do número, diferente do `celular()`. O celular de 8 dígitos não ganha o 9, e o número inválido abre o link mesmo assim. Com isso, o link aberto pode ter um número diferente do que o servidor grava, ou o servidor responde 400 depois de a mensagem já ter sido enviada. Vale mostrar o número normalizado vindo do servidor ou espelhar o `celular()`.
2. `web/app/cobranca.py:592`: o selo procura a chave com `str(v)`. O §10.6.2 pede o texto sem espaços nas pontas e em maiúsculas (`str(v).strip().upper()`).
3. `web/app/cobranca.py:492`: a limpeza usa `> timedelta(days=30)`, e o §10.6.5 diz "30 dias ou mais", ou seja, `>=`.
4. `web/app/main.py:397`: `bruto.isdigit()` aceita dígitos Unicode (ex.: `²`), e o `int()` estoura em 500. Use `bruto.isascii() and bruto.isdigit()`.
5. `web/app/cobranca.py:398` (`_Tranca.__enter__`): se o `open` ou o `flock` falham depois do `acquire`, o trinco da thread nunca é solto e as rotas seguintes travam. Solte o trinco num `try/except`.
6. A idempotência de 60 s fica na memória do processo (`_rec`). Vale enquanto o `startCommand` rodar um só worker. Se um dia houver mais workers, ela precisa ir para o disco.
7. `web/app/pacotes.py:285`: o `_MEMO_SHA` cresce sem limite a cada pacote novo. Vale limitar aos arquivos de `listar()`.
8. Citações antigas do contrato: `web/RENDER.md:12` cita "§10.2.5", e a linha 1 de `web/tests/test_cobranca.py` e de `web/tests/cobranca_fixture.py` cita "§10.2". O certo é §10.6.5 e §10.6. A troca do `autoDeploy` no `RENDER.md` (`:27`) não faz parte da entrega 2: é texto de apoio, mas foge do lote.

**Redundância:** a web reimplementa o `celular()` e o `fone_bonito()` do PC. Isso é aceitável, porque a web roda sem os módulos da raiz e há teste de paridade (`test_celular_mesma_regra_do_pc`). O `numero()` do JS é a terceira cópia e diverge (🟢 1). Não há texto na tela que a pessoa não use para agir.

---
# Revisão T-0017, entrega 2 · PR #64 (modulo-robo) · bap_automation.py (passo 4f)

- Head revisado: `50182bc4167ea3bda79df3cf589a61d4d11ac80a` (commit novo = revisão nova).
- Contrato: §10.6.2, §10.6.6, §10.6.7 e §10.6.8 de `.coord/contratos/relatorio.md` (main). Regras: RN-POS-001, RN-POS-003 e RN-POS-004.
- Parecer: **sem 🔴; 1 🟡 (a mesma decisão do PR #62) e 5 🟢.**

## Conferido
- `tabelas_cobranca_web` (`:6947`): confere nome, ordem, `tipo` e `oculta` das duas tabelas, com o bloco de status inteiro (3 colunas) ou ausente. Tira TELEFONE, põe `chip` só em SITUAÇÃO, FAIXA e STATUS e confere o tamanho das linhas. Se algo não bate, o farol vai sem `tabelas` e sem `cobranca`, com aviso no log sem dado pessoal. `tabelas` e `cobranca` vão juntas, e só no `pl_inadimplencia`.
- Rodada do 4f na ordem do §10.6.7: GET (paginado, com trava de laço) → `importar_web` → estado gravado de forma atômica → confirmar em toda rodada com `ate_seq > 0` → montar e enviar o pacote. Época nova: o robô descarta a resposta e puxa de novo com `desde=0`. Falha no GET (404, 401, 5xx ou rede): não importa nem confirma, e o estado fica como estava. Erro de disco: não confirma. 401 aparece no log como "token da web recusado".
- `web_ate_seq` segue a definição única: o maior `seq` gravado, tenha a confirmação dado certo ou não. O `gerado_em` é tirado depois da importação, em Manaus.
- O arquivo `ESTADO_COBRANCA_WEB.json` fica fora do glob `COBRANCA_*.csv`. Os CSV das máquinas ficam intocados (regra 7).
- Só https na porta 443. O token não aparece no log (o `log` mascara o token). A simulação não toca na rede nem grava no diário.
- Pacote simulado das bases congeladas: "Títulos" com 20 colunas, "Por cliente" com 19, fila com 136 itens. Nenhuma chave TELEFONE, CNPJ, CPF ou `telefone_cad`. Nenhum telefone fora de `whatsapp`. O `pacotes.validar` da web devolve 0 erros. Os cartões do farol não mudam: o número que vai ao Diretor continua igual ao do farol de origem.
- Testes: o merge temporário dá `pytest tests/` 214 passed e `web/` 109 passed. Os testes de dono dão 27 passed. O `verificar modulo-robo --base origin/main` sai OK, e os 5 commits trazem `Agente: modulo-robo`.

## 🟡 corrigir antes do merge
1. `bap_automation.py:6947` (`tabelas_cobranca_web`): a coluna NOME vai crua. No pacote simulado das bases congeladas, 8 linhas (7 em "Títulos" e 1 em "Por cliente") têm o NOME começando por documento (MEI). É a mesma decisão do 🟡 1 do PR #62: o contrato (§10.6.2) manda igualdade célula a célula, e a RN-POS-004 diz que CNPJ não vai ao site. O gerente decide entre um acréscimo ao contrato (máscara com `cobranca_whatsapp.nome_saudacao` no NOME do pacote) e a aceitação registrada.

## 🟢 sugestões
1. `bap_automation.py:7232` (`_base_web`): repete o mesmo `urlparse` e a mesma checagem de https:443 do `enviar_pacote_web`. Vale extrair uma função e usar nos dois.
2. `bap_automation.py:7199` (`_pasta_cobranca`): repete o `cobranca_whatsapp.pasta(raiz)`, e o módulo já está importado no 4f.
3. `bap_automation.py:7394` (`_fantasias_clientes`): é cópia do `trabalho()` interno do `cobrar_whatsapp` (`bap_relatorios.py:926`). Vale um pedido ao modulo-posvenda para criar `cobranca_whatsapp.nomes_fantasia(raiz)`, que o PC e o robô passariam a usar. Ela usa `date.today()`, não a hora de Manaus, mas isso não afeta o cadastro.
4. `bap_automation.py:7344`: o `maior` conta o `seq` de linha sem `id`, que o `importar_web` pula. É um caso teórico, porque a web sempre manda `id`.
5. `bap_automation.py:7451`: o `log` consulta o cofre (`_segredo_web`) a cada mensagem. Vale ler o token uma vez antes.

**Redundância:** há 3 repetições pequenas (🟢 1 a 3). A lista de colunas existe também na web (`web/app/cobranca.py`), mas o contrato pede a conferência dos dois lados, então não conta como redundância.

## Decisão do gerente sobre o 🟡 do NOME
No site, a coluna NOME e o nome da fila vão sem o CPF/CNPJ do começo (função nome_sem_documento do pós-venda), pela RN-POS-004; o PC continua igual. Acréscimo ao §10.6 pelo engenheiro-software.
