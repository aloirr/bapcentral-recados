# Revisão de código — T-0045, itens 6 e 8 (parte do robô do PC)

- **Revisor:** revisor-codigo · **Data:** 27/11/2026 (Manaus)
- **Branch:** `modulo-robo/T-0045-nuvem-robo` · **head SHA:** `11b24fcb8b0fdfd6f95b3984fc5879507a277527` (2 commits sobre `0f3106a`). Sem PR aberto.
- **Referências:** ADR 0004 §9 (itens 6 e 8) · contrato `.coord/contratos/visitas-nuvem.md` v1.1 (`42c81a1`) · o site do item 5 já no `main` (`web/app/visitas.py`).
- **Este parecer vale só para o head acima.** Commit novo = revisão nova.

## Veredito

**Não aprovado: 0 🔴, 5 🟡, 10 🟢.** O laço das edições ficou igual, o botão do PC continua igual no caminho feliz e a importação é só por acréscimo. Os 🟡 são três desvios de RN ou de contrato que o site já no `main` faz valer, uma detecção que pode barrar o login do botão do PC e a falta de teste no CI.

## O que rodei (numa cópia fora do repositório, venv 3.12 com tkinter)

| Conferência | Resultado |
|---|---|
| `python -m compileall -q visitas_maxima.py bap_automation.py visitas_nucleo.py` | ok |
| `pytest tests/` inteiro (a branch mais os 3 `test_T0045_*` do `main` `d9dd721`) | saiu 0, sem falha |
| `test_T0021_edicao_web_robo` + `test_T0045_*` | 63 passaram |
| Provas do autor, apontadas para a minha cópia: `cmp_edicoes.py` / `cmp_botao.py` / `visitas_web.py` | TUDO IGUAL (7 cenários) / TUDO IGUAL/OK / TUDO OK (14). O `ba_orig.py` e o `vm_orig.py` são byte a byte os do `0f3106a` |
| `coord.mjs verificar --por-commit 0f3106a..11b24fc` | OK, 2 commits do modulo-robo, nenhuma violação |
| `git merge-tree origin/main(e1d80a8) 11b24fc` | sem conflito |
| Arquivos da branch | só `visitas_maxima.py` e `bap_automation.py`. Nada em `RELATORIOS/`, `SISTEMA BAP/`, `BAP Ajuda 2.0/`, nas configs ou nos dados digitados |
| `bap_dados.VERSAO` | 27 (o arquivo não muda) |
| Sondas minhas (`rev45/sondas/s1.py`, `s2.py`) | as que sustentam os 🟡 1 e 4 |

## 🟡 Corrigir antes do merge

1. **`bap_automation.py:9955-9957` (`_aplicar_lote_visitas_web`): a importação rebaixa o índice do PC.** O `vn.anotar_baixado(raiz, dia, quando)` sobrescreve a hora com o `baixado_em` da nuvem, mesmo quando o PC baixou depois. A RN-VIS-002 (ADR 0004) diz: "entre a hora do PC e a da nuvem, vale a maior (`juntar_baixado`)".
   - Sonda `s1.py`: o PC tinha o dia 25/11 baixado às 26/11 10h00. Veio o lote da nuvem das 06h07 e o índice passou a dizer 06h07. Em seguida, o `fechados_pc` mandou 06h07 ao site.
   - Efeito: um lote atrasado da nuvem (botão no próprio dia, ou a fila puxada de novo depois de época nova) pode **reabrir** um dia que o PC já tinha fechado.
   - Correção: gravar a maior das duas horas, com `vn._quando_manaus`/`juntar_baixado`, sem reescrever a regra. Vale também para a chave do mês (9956-9957). Teste citando a RN-VIS-002.

2. **`visitas_maxima.py:1318` e `:429` (`rodar` / `codigo_da_excecao`): a fase `"navegador"` está fora da lista do §3.3.**
   - O `_fase("navegador")` chama o `ao_fase("navegador", None, None, None)`. Para falha ao abrir o navegador, o `codigo_da_excecao` devolve `("NAVEGADOR_FALHOU", "navegador")`.
   - O site no `main` recusa as duas coisas: `web/app/visitas.py` linha 560 (`progresso`: fase ∉ `FASES` → 400) e linha 691 (`fim`: "fase fora da lista" → 400). O primeiro progresso da rodada da nuvem e o `fim` do `NAVEGADOR_FALHOU` voltariam 400. Pior: o `fim` recusado vira `RODADA_INTERROMPIDA`.
   - Correção: guardar "navegador" só como marca interna. Não chamar o `ao_fase` com ela e devolver `fase=None` no `NAVEGADOR_FALHOU` (que não está em `PEDE_FASE`). Ou então acrescentar a fase ao contrato, com aviso aos consumidores. O `FASES` (linha 359) pode validar o `_fase`.

3. **`visitas_maxima.py:116` e `:753-760` (`CAPTCHA_JS` e o `pronto()` do `entrar`): falso positivo pode barrar o login do botão do PC.** O `entrar` é o mesmo no PC e na nuvem, e a detecção nova roda a cada 0,4 s logo depois do "Entrar", ainda no `/login`. Há dois riscos:
   - O seletor `[class*="captcha" i]` / `iframe[src*="captcha" i]` também casa com elemento **invisível**: o selo do reCAPTCHA v3 (`.grecaptcha-badge`) e o iframe do reCAPTCHA invisível, comuns em páginas de login. Se a página de login da Máxima tiver um deles, o botão do PC passa a falhar sempre com "A Máxima pediu captcha.", e a nuvem pausa no diagnóstico.
   - O `_RX_URL_VERIFICACAO` olha a URL **inteira**, com a query. Um token na query com "otp", "mfa" ou "2fa" faz o `pronto()` ler o texto da página. Uma página inicial com "Termos de uso" no rodapé vira então `MAXIMA_CONFIRMACAO`. A sonda `s1.py` mostra o caso `…/home?t=abOTPx9` + "Termos de uso" → `MAXIMA_CONFIRMACAO`.
   - Nenhuma prova do autor passa pelo `entrar`/`pronto()`: o `cmp_botao.py` só testa o `classificar_login` puro.
   - Correção: contar só captcha **visível** (tamanho > 0, fora do `.grecaptcha-badge`) e aplicar o regex só ao `urlparse(url).path`. Prova: uma rodada real do botão do PC com "Mostrar o navegador" (login ok), ou o DOM da página de login conferido pelo modulo-robo, registrada na entrega.

4. **`bap_automation.py:9963` (`_aplicar_lote_visitas_web`): exceção inesperada segura a fila para sempre.** Avaliação da suposição do autor:
   - Para `PermissionError`/`OSError` (Excel ou CSV aberto, disco), `pendente` está certo: é passageiro.
   - Para qualquer outra exceção (`ValueError`, `AttributeError`…), o mesmo lote volta como `pendente` a cada 30 min. **Nenhum lote seguinte entra**, e o único sinal é uma linha de log. A sonda `s2.py`, com `equipe.filiais` torto, deu o mesmo `pendente` em 3 voltas seguidas, e o seq 2 nunca foi importado.
   - O site já valida `equipe`/`extras` (`validar_lote`), então hoje isso só acontece com defeito no `montar_dia`/`montar_mes`. Mas é exatamente o caso que ninguém vê.
   - Correção: validar `equipe` (3 dicionários) e `extras` (dicionário) no `_validar_lote_visitas_web`, como no site, com `erro`/`dia`. Para exceção não prevista, um teto de voltas por seq (ex.: 3) e depois `erro`/`dia`, com linha própria no log. Tirar a parte da nuvem do índice faz a nuvem baixar de novo, dentro do teto do dia.

5. **Sem teste no CI.** A branch não acrescenta teste. O contrato §4.4 pede que "os testes do laço são os das edições, rodados nos dois", e a regra 2 do CLAUDE.md pede teste citando a RN para cada função pura nova: `classificar_login`, `codigo_da_excecao`, `fechados_pc`, `aviso_site_baixando` e `gravar_excel_importado`. As provas `cmp_edicoes.py`, `cmp_botao.py` e `visitas_web.py` estão só no scratchpad. Pela ADR §9, o item 9 é do `testes`; antes do merge, o gerente pede a ele os testes, ou a decisão explícita de que o merge fica para depois do item 9. Mínimo: o laço `puxar_fila_web` rodado com as 2 rotas, o caso do 🟡 1, o 404 da web antiga e a validação do lote (sha256, `..`, dia futuro, nome × dia).

## 🟢 Sugestões

1. `visitas_maxima.py:773`: "O login não respondeu em 45 s." sai sem código e vira `TELA_MUDOU`. Duas seguidas na fase `login` pausam a agenda. Para Máxima lenta, `MAXIMA_FORA` (nova tentativa) descreve melhor o caso.
2. `visitas_maxima.py:777` (suposição "login não reconhecido = `MAXIMA_SENHA`"): **aceita**. É o lado seguro (nunca repete o login), e o texto do PC continua o de antes. A sonda mostra "Erro de comunicação com o servidor" e "Serviço indisponível" virando `MAXIMA_SENHA`, que pausa a nuvem. Sugiro um regex de indisponibilidade → `MAXIMA_FORA` e registrar a regra no §5.1 do contrato.
3. `bap_automation.py:9925` (suposição "lote 404 = `erro`/`sha256`"): **aceita**. Dos motivos do §4.3, é o único que leva o site a tirar a parte da nuvem do índice. Registrar no §4.2 do contrato ("404 = erro/sha256").
4. Tetos no PC: o contrato põe `LOTE_GZ_MAX`, `ARQUIVO_MAX` e `ARQUIVOS_MAX` no site, e o PC não confere. Conferir no PC custa pouco (`len(arquivos) <= 60`, `len(dados) <= 2 MB`, corpo gzip até 8 MB antes do `gzip.decompress`) e protege do gzip-bomba se o site falhar.
5. `visitas_maxima.py:471-481` (`consultar_saude`): no primeiro clique, o `import bap_automation` (pandas, openpyxl) roda na thread da tela. E `timeout=5` vale para a conexão **e** para a leitura (até ~10 s). Sugestão: `timeout=(3, 2)` e ler o `BAP_WEB_URL` sem importar o `bap_automation` inteiro.
6. `bap_automation.py:9952`: `replace(tzinfo=None)` supõe `-04:00`. `vn._quando_manaus` (ou `astimezone(Manaus)`) já trata outro fuso.
7. `bap_automation.py:9845`: o registro `IMPORTADOS_VISITAS_WEB.jsonl` traz `motivo`, além das chaves do §4.4, e o `em` não sai em ISO `-04:00`. São inofensivos e sem nome. Acertar o contrato (v1, chave opcional) ou o código.
8. `bap_automation.py:9635`: com `rotulo="Visitas web"`, a linha diz "falha ao puxar as **edicoes** do site". Trocar por "a fila do site".
9. `bap_automation.py:9727`: o 409 de época só zera o estado no caminho principal (9777). No caminho `not res` + `fechados_pc`, um 409 fica sem reação até a próxima volta com GET ok. Não chega a quebrar nada.
10. `bap_automation.py:10002`: o `depois_de_baixar` só roda quando entra lote novo. Se o acompanhamento falhou (Excel aberto), ele só se recupera na próxima importação ou no botão. Vale guardar a falha e repetir na volta seguinte. Redundância: o `FECHADOS_PC_DIAS = 40` está no `visitas_maxima` e também em `web/app/visitas.py`. Pode morar no `visitas_nucleo` (o núcleo que os dois usam), por pedido ao modulo-rota.

## Conferências pedidas: o que está certo

- **`sincronizar_edicoes_web` sem mudança de comportamento:** li linha a linha contra o `0f3106a`.
  - O estado vai no mesmo arquivo (`.tmp` + `os.replace`).
  - Mesmo GET paginado e mesma regra de época.
  - O confirmar só sai com `a_confirmar`, como antes: `extra_confirmar=None`, e o 409 não zera o estado.
  - `opcoes`/`aplicadas_web` são lidos depois do GET, como antes, e os textos de log são iguais.
  - Confirmado pelo `cmp_edicoes.py` (7 cenários: resultado, log, chamadas HTTP, estado e registro) e pelo `test_T0021`.
- **Botão do PC:**
  - `executar` igual. O `depois_de_baixar` é o mesmo bloco, com as mesmas chaves (`excel`, `por_cliente`, `prospeccao`).
  - `Robo(raiz, log, parar, visivel)` com `canal=None` segue o laço Edge → Chrome → Chromium de antes.
  - `foto=True`, e `eventos=False` mantém o log de antes.
  - Mudanças declaradas conferidas: HTTP 403 no `goto` → `MAXIMA_BLOQUEIO` na hora; captcha e confirmação → erro claro; `/saude` só com `precisa` e sem token (só `https`, por `_base_web`). Ressalva: o 🟡 3.
- **Segredo e dado pessoal:**
  - Nada de segredo no código.
  - Log do robô com o token trocado por `***`, só nomes de classe de exceção e sem nome de pessoa.
  - Com `eventos=True`: `self.log` mudo; `evento()` só com campos higienizados (`[A-Za-z0-9_.:-]`, 40 caracteres); a mensagem crua da Máxima não sai, nem no `✖` do vendedor (vira o nome da classe) nem no `MAXIMA_SENHA` (sem o texto). O texto da página no `classificar_login` só passa por regex.
  - O registro `.jsonl` não leva nome.
- **Validação antes de gravar:** em cada lote, tudo é conferido antes do primeiro Excel.
  - O sha256 do corpo é comparado com o do cabeçalho e o da linha.
  - `versao == 1`; `dia` igual ao da linha, `AAAAMMDD` e não futuro.
  - `pasta` sem `/`, `\`, `..` nem caractere de controle, e igual ao `nome_limpo`.
  - `nome` casa com `_RX_ARQ_ANALITICO`, começa com `VISITA-<pasta>-`, e a data do nome é o dia.
  - `b64` validado; sha256 e `bytes` de cada Excel conferidos.
  - Última trava em `gravar_excel_importado`. Tetos: ver 🟢 4.
- **Só acréscimo:** `gravar_excel_importado` pula se o sha256 for igual (com ou sem sufixo). Outro conteúdo ganha `-2`, `-3`… (`arquivo_analitico`). `.tmp` + `os.replace`, sem nunca sobrescrever nem apagar. O registro `.jsonl` é só de acréscimo, com `fsync`. O `.xlsx.tmp` que sobrar não casa com o `_RX_ARQ_ANALITICO` (o `montar_dia` ignora).
- **Contrato:**
  - §4.1: o 404 da web antiga não gera log e não dispara POST, porque ainda não há época.
  - §4.3: o `fechados_pc` sai em toda volta com época conhecida, mesmo sem lote; 409 → `desde=0`; os motivos ficam na lista do site.
  - §4.4: assinatura, `puxar_fila_web` único para as 2 filas, passos 1–3, `depois_de_baixar` uma vez, registro e retorno.
  - §4.5: o aviso com o texto literal.
  - §5: os códigos por fase.
  - §3.3: ver 🟡 2. Os §3.4 e §6 são do `rodar.py`, fora deste lote.
  - §4.3 × site no `main`: formato do `fechados_pc` aceito (`dia_valido` + `_dt`, até 400).
- **Número do Diretor:** não se aplica. **Tela:** só o `askyesno` com o texto do contrato §4.5; não houve print. Como o texto é o do contrato aprovado, não peço simulação.

## Para o re-teste

Commit novo com os 🟡 1 a 4 corrigidos e a prova do 🟡 3 registrada. Os testes do 🟡 5 entram no CI, ou o gerente registra a decisão de esperar o item 9. Depois, novo pedido de revisão com o head SHA.
