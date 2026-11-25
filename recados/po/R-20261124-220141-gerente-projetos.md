---
id: R-20261124-220141-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0018
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T22:01:41-04:00
---
# Parecer do revisor-codigo: PR #59 head 46f6ee2 — 3 🟡

> Parecer do revisor-codigo, com checagem de redundância (subagente do gerente-projetos; gravado pelo gerente sem alteração; varredura de dado pessoal e nome de máquina: limpo).

# Revisão T-0018: rotina diária de atualização da produção

- **Branch:** `engenheiro-software/T-0018-rotina-diaria` · **head revisado:** `46f6ee2` (base `origin/main` 9edfee9)
- **Parecer:** **não aprovado ainda**. Não há 🔴. Há 3 🟡 a corrigir antes do merge.
- Commit novo exige revisão nova.

## O que foi conferido
- `python -m compileall -q atualizar_do_github.py`: ok.
- Testes do rascunho (`test_T0018_rotina.py`) contra o head numa cópia temporária: **56 passed**. `pytest tests/ -q`: **184 passed**.
- `node scripts/coord.mjs verificar engenheiro-software --base origin/main` e `verificar --base origin/main`: **OK**, sem violação (5 arquivos; o diário é exceção do protocolo).
- Regra 7 e segredos:
  - o `--diario` filtra com `so_com_instale`, que chama `eh_excluido` da T-0003 (`.json`, bases, prefixos `_EDICOES_POS_VENDA`/`_NCC`/`_GARANTIAS`/`_AUTORIZACOES`, `auth`, `.env`);
  - só entram `.py`/`.bat` da raiz do zip; não há leitura de arquivo de chave;
  - a URL do `/saude` vem de `BAP_WEB_URL` ou do cofre e não vai para o log.
- Segurança da troca:
  - backup `ANTES_DIARIO_<MÊS><ANO>` conferido por hash, troca atômica e restauração no código 4 (reusa o `executar` da T-0003);
  - o zip é baixado por `archive/{sha}.zip` do SHA que passou nos limites 1 e 2, sem TOCTOU;
  - nenhum código baixado é executado: a `VERSAO` da web é lida por regex.
- Limites em funções puras:
  - `commit_maduro`, `pr_de_origem` + `ci_verde`, `versoes_batem`, `dentro_da_janela` + `robo_rodando` e a trava do `planejar`;
  - códigos 10 a 16 batem com a ADR.
- API e fuso:
  - no máximo 4 chamadas por rodada (`/rate_limit` não gasta cota);
  - API fora do ar (HTTP 503 simulado) sai **15** com 1 linha de log;
  - a janela converte para America/Manaus.
- Opções da linha de comando:
  - `--primeira-vez` sem `--confirmar`/`--simular` sai 1;
  - `--agendar` usa `schtasks` sem `/RU` nem senha e sem nome de máquina.
- O log tem data, modo, código, SHA curto e nomes de programa, sem dado pessoal.
- ADR 0002 fiel às decisões 1 B, 2 A, 3 B, 4 A e 5 A do R-20261124-214958-alexandre e aos 5 limites do R-20261124-213435-gerente-projetos §(e).

## 🟡 Corrigir antes do merge
1. **`atualizar_do_github.py:248`: o `pr_de_origem` cai no "primeiro PR mesclado" quando nenhum PR tem `merge_commit_sha == sha`.**
   - Um commit sem PR próprio (push direto, commit de governança) herda o CI verde de outro PR. Isso enfraquece o limite 2.
   - Conferido: com um PR de `merge_commit_sha` diferente, a função devolve esse PR.
   - Correção: aceitar só o PR com `merge_commit_sha == sha`. Sem esse PR, sair com o código 11.
2. **`atualizar_do_github.py:881`: a conferência do SHA do zip só vale quando o comentário existe.**
   - Zip sem comentário, ou com comentário inválido, passa sem conferência.
   - A URL é pelo SHA, então o risco é baixo. Mesmo assim, a ADR (ordem 7) promete a conferência.
   - Correção: sem SHA no comentário, sair com o código 1 (falhar fechado).
3. **Testes fora do CI.**
   - Os 56 casos estão só no rascunho (ADR:86). O CI do head não roda nenhum teste da T-0018.
   - Faltam casos para:
     - API fora do ar ou HTTP de erro (código 15);
     - zip de outro commit ou sem comentário (código 1);
     - falha na troca dentro do `--diario` (código 4, com restauração e sem `VERSAO_INSTALADA.txt`);
     - o caso do item 1.
   - Pronto quando o agente testes levar os testes para `tests/` (no mesmo lote ou num PR dele antes do merge) e o CI ficar verde.

## 🟢 Sugestões
- `atualizar_do_github.py:826` e `:1080`: no `--simular` o log ganha uma linha, mas a tela diz "SIMULACAO: nada foi gravado" (`:552`). Não gravar o log na simulação, ou dizer na tela que ele foi gravado.
- `atualizar_do_github.py:901`: usar `agora.astimezone(_fuso_manaus()).date()`. Com um `agora` em UTC depois das 20h, o mês do backup sai errado (hoje só o teste passa `agora`).
- No dia em que só há arquivos "pendente de instale", o SHA é gravado no `VERSAO_INSTALADA.txt`. A partir do dia seguinte, a rodada sai "nada a fazer" e o aviso de pendente some do log. Repetir a pendência no log (ou no arquivo de versão) até haver o "instale".
- `--confirmar` sem `--primeira-vez` é ignorado em silêncio (`:980`). Recusar ou avisar.
- ADR:54: "os limites 1 a 3 não valem no `--primeira-vez`" não está escrito no R-20261124-214958. Marcar como [SUPOSIÇÃO] ou levar ao po.
- Não há RN para a rotina em `docs/produto/03-regras.md`. O po pode criar uma (ex.: RN-GER-xxx) para os nomes dos testes citarem (regra 2).
- `.coord/diario/engenheiro-software.md:5`: falta o "- " no início da linha, como nas outras.

## Redundância (T-0003)
- **Sem achado.** O código reusa `planejar`, `executar`, `eh_excluido`, `baixar_main`, `pasta_backup`/`nome_backup` e `_sha256`.
- `hoje_manaus` passou a usar `_fuso_manaus`/`agora_manaus`, sem segunda regra de fuso.
- A única cópia é o caminho da trava do robô (`TRAVA_ROBO_REL`). Ela tem justificativa: não importar o `bap_automation`.
