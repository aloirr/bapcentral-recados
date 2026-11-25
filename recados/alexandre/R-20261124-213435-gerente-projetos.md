---
id: R-20261124-213435-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: alta
tarefa: null
responde_a: R-20261124-213034-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T21:34:35-04:00
---
# Rotina diária da pasta de produção: há DUAS pastas Regionais - Leandro — segure a atualização da pessoal; 5 decisões

## ATENÇÃO antes de tudo (pare a atualização da pasta pessoal)
Existem DUAS pastas "Regionais - Leandro":
- a da EMPRESA (OneDrive - PMZ DISTRIBUIDORA SA): é a que o robô usa hoje (o bap_automation.py trabalha na própria pasta; as instalações de 23/11, 375 KB, foram nela); a TABELA_BAP, as assistentes e o Power BI vivem nela;
- a PESSOAL (onedrive.live.com): a única que o conector enxerga; está antiga (257 KB), e o notebook não a lê.
Atualizar a pessoal (decisão "1 C" do R-20261124-212744) NÃO atualiza a produção do robô. Peço ao po que SEGURE essa atualização até o Alexandre responder a decisão 1 abaixo.

## Recomendação (engenheiro-software)
Tarefa agendada do Windows no notebook do robô, às 06h30, rodando o atualizar_do_github.py (T-0003) em modo diário contra a pasta da EMPRESA: backup ANTES_<...>, SHA-256 conferido, só .py/.bat da raiz, sem .json, bases, dado digitado ou segredo; o OneDrive leva aos outros PCs. Sem Microsoft Graph (regra 9). O Alexandre faz uma vez: grava um token de leitura do GitHub no cofre do Windows e dá duplo clique num .bat que cria a tarefa (~10 min). Código: engenheiro-software (1 dia) + testes (0,5 dia); previsão 2 dias úteis depois das decisões. A 1ª atualização dos 75 programas passa primeiro por --simular (imagem antes/depois ao Alexandre).

## Decisões para o Alexandre (resposta pronta "N X")
1. Pasta de produção: (A) a da EMPRESA, onde o robô e o time já estão (a pessoal vira cópia) · (B) a pessoal (exige mover o robô, a TABELA_BAP e o compartilhamento das assistentes e do Power BI; alto risco). Recomendo A. Resposta: "1 A".
2. Onde a rotina roda: (A) notebook do robô, 06h30 · (B) desktop · (C) junto com o robô das 08h. Recomendo A. Resposta: "2 A".
3. Repositórios privados + token de leitura no cofre do notebook: (A) sim (casa com o R-20261124-212625) · (B) continuam públicos. Recomendo A. Resposta: "3 A".
4. "Instale" automático (muda a regra 11 do CLAUDE.md, governança) com 5 limites: commit há 2 h ou mais no main; CI verde no PR de origem; versão do site no ar igual à do main; janela 06h00–07h30 sem o robô rodando; parar se a trava "instalado por fora" disparar. .bat de instalação e configs continuam pedindo "instale". (A) sim · (B) só com os 3 últimos limites · (C) mantém o "instale" a cada versão. Recomendo A. Resposta: "4 A".
5. Se a 1ª rodada travar por arquivo de versão antiga: (A) opção --primeira-vez, manual, com backup total · (B) arquivo a arquivo por PR. Recomendo A. Resposta: "5 A".

## Desenho completo (engenheiro-software; nomes de máquina omitidos — o repositório de recados está público)

## 0. Achado que muda o problema (ler primeiro)
- São DUAS pastas com o mesmo caminho relativo `1 - PMZ\2025\IM PMZ\Regionais - Leandro`:
  - **empresa** (`OneDrive - PMZ DISTRIBUIDORA SA`, [SharePoint da empresa]): é a que o robô usa. `bap_automation.PASTA_LOCAL` = pasta do próprio .py (`PASTA_TRABALHO_FIXA=None`, `LOCAL_DA_PLANILHA="mesma_pasta"`, `URL_PASTA_PLANILHA` aponta pmz365). `instalar_bap.bat` cria a tarefa 08h/14h na pasta onde ele está. O legado (agente_bap_tools.md, INSTALACAO_ROTA_1710.md) dá o notebook [máquina] e o desktop [máquina] nessa pasta. Instalações de 23/11 (375 KB) foram nela.
  - **pessoal** (onedrive.live.com, ): a única que o conector do Cowork enxerga; arrumação antiga, 257 KB.
- Logo o notebook NÃO sincroniza a pasta pessoal [SUPOSIÇÃO: conta pessoal não costuma estar no OneDrive do notebook da empresa]. O time das assistentes, o Power BI e a TABELA_BAP vivem na pasta da empresa.

## (a) Opções de rotina diária
| Opção | Custo | Risco | O que o Alexandre faz UMA vez |
|---|---|---|---|
| A. Tarefa agendada do Windows na máquina do robô (notebook), rodando `atualizar_do_github.py --diario` contra a pasta da EMPRESA; o OneDrive leva aos outros PCs | ~1 dia de código + testes; zero nuvem | baixo: backup+SHA já existem; OneDrive propaga | duplo clique num `AGENDAR_ATUALIZACAO.bat` (cria a tarefa 06h30, só com o usuário logado, sem pedir senha) + gravar o token no cofre |
| A'. Igual à A, mas contra a pasta PESSOAL | igual | alto: o robô e o time não leem essa pasta; vira cópia morta ou exige mudar o robô de lugar | adicionar a conta pessoal ao OneDrive da máquina |
| B. GitHub Actions → OneDrive | Actions + app no Graph | **viola a regra 9** (registro de app) e põe token de conta no GitHub; contra "economizar Actions" | — (descartada) |
| C. po/conector do Cowork, arquivo a arquivo | horas por rodada; depende de sessão | alto, sem SHA local confiável; só alcança a pasta pessoal | nada, mas não é rotina |
| D. Encadear no `executar_bap.bat` das 08h (antes do robô) | menor (sem tarefa nova) | médio: falha da atualização atrasa o robô; troca o robô minutos antes de rodar | nada (dono modulo-robo) |
| E. Desktop com Git (`--origem` clone + `git pull`) | igual à A | depende do desktop ligado; não é a máquina do robô | clonar o repositório no desktop |

## (b) Repositório privado (dono: engenheiro-software; teste: testes)
- `baixar_main`: trocar `github.com/…/archive/refs/heads/main.zip` por `https://api.github.com/repos/aloirr/bapcentral/zipball/main` com `Authorization: Bearer <token>` (urllib, só biblioteca padrão). O 302 vai ao codeload com credencial própria; testar que o cabeçalho não vaza no log nem no redirecionamento.
- Token: fine-grained, só `aloirr/bapcentral`, **Contents: read** (+ Actions: read se o portão do CI for ligado), validade 1 ano; quem cria é o Alexandre. Ordem de leitura: variável `BAP_GITHUB_TOKEN` → cofre do Windows serviço `BAP_GITHUB` (keyring se houver; senão `ctypes` CredReadW). `--salvar-token` grava com `getpass` (nunca na linha de comando). Erro 401/404 → "token ausente/vencido", código 1, sem mostrar o token.
- O comentário do zip do GitHub traz o SHA do commit: gravar `SISTEMA BAP\VERSAO_INSTALADA.txt` (SHA, data, n.º de arquivos).
- `tests/test_atualizar_do_github.py` é do testes: casos token por env/cofre, 401, SHA no comentário, modo diário.

## (c) Robô e pasta
- Hoje: notebook lê a pasta da EMPRESA (pasta do `bap_automation.py`); `planner_pastas.json` só tem as chaves `tabela_bap`, `base_cliente`, `saida`. Robô não muda se a produção for a da empresa.
- Unificar = declarar a pasta da EMPRESA como a de produção (decisão 1). A pessoal vira cópia de leitura do conector, ou é atualizada pela mesma rotina com um 2º `--producao` SE a máquina sincronizar as duas (só código; nunca bases).
- Se o Alexandre insistir na pessoal: mover o robô (reinstalar `instalar_bap.bat` lá), a TABELA_BAP e o RELATORIOS, e recompartilhar com as assistentes/Power BI — tarefa do modulo-robo, alto risco, não recomendo.

## (d) 1ª atualização (≈75 programas)
- A trava compara `mtime` da produção com a data do item do zip (= data do HEAD do main, 24/11 21:15 no 9edfee9). Na pasta da empresa, os 7+3 instalados em 23–24/11 são iguais ao main → "igual", sem trava. Na pessoal, os arquivos são de out/nov → mais velhos → **não dispara**, salvo arquivo mexido depois do HEAD (ex.: gravação pelo conector).
- Passo: rodar `--simular` primeiro (regra 10: imagem antes/depois ao Alexandre). Se a trava disparar: comparar o SHA do arquivo da produção com o histórico do git (desktop); se for versão antiga do main → `--primeira-vez` (novo, só manual, pede "SIM", backup de TODOS os alterados); se for versão inédita → PR antes (regra atual).

## (e) Regra 11 — texto proposto
"11. Produção no PC: a rotina diária (`atualizar_do_github.py --diario`, tarefa agendada só na máquina do robô) leva os .py/.bat da raiz do `main` para a pasta de produção, com backup `SISTEMA BAP\BACKUP_RELATORIOS\ANTES_DIARIO_<MÊS><ANO>[_n]` e conferência byte a byte. Ela só instala se: (1) o commit tiver ≥ 2 h no main; (2) o PR de origem teve CI verde no head SHA; (3) a versão da web no main (`web/app/__init__.py`) for igual à do `/saude` — senão espera o 'aprovo deploy'; (4) janela 06h00–07h30 Manaus, nunca com o robô rodando (trava de arquivo); (5) sem a trava 'instalado por fora'. Nunca toca .json, bases, dado digitado nem segredos. Falha = nada trocado + registro. O Alexandre suspende a rotina com o arquivo `SISTEMA BAP\PAUSAR_ATUALIZACAO`. Mudança de .bat de instalação, `tarefa_bap.xml` e configs continua com 'instale'."
- Notas: o CI só roda em `pull_request` (`.github/workflows/ci.yml`); o portão (2) usa a API (commit → PR → runs), precisa Actions+Pull requests read; alternativa barata: confiar na regra de merge e ligar só (1),(3),(4),(5).
- Aviso de falha: v1 grava `SISTEMA BAP\LOGS\atualizacao_diaria.log`; v2 o robô manda `versao_codigo`/`status_atualizacao` no pacote e o `/saude` mostra (campo novo compatível; modulo-robo + modulo-web + contrato).

## (f) Recomendação: opção A na pasta da EMPRESA, no notebook do robô
1. Alexandre decide 1–5 (abaixo). 2. engenheiro-software: `--diario`, token/cofre, VERSAO_INSTALADA, `--primeira-vez`, `AGENDAR_ATUALIZACAO.bat`, ADR 0002 (regra 11) — 1 dia. 3. testes: casos do (b)/(d)/(e) + simulação na cópia da pasta — 0,5 dia. 4. 1ª rodada manual `--simular` → imagem ao Alexandre → rodada real. 5. Alexandre: token no cofre + duplo clique no agendador (10 min). 6. modulo-robo + modulo-web: status no pacote/`/saude` (v2, 0,5 dia). Previsão: v1 em 2 dias úteis após as decisões.
- Pendência de governança: o texto da regra 11 está no CLAUDE.md (só com autorização do Alexandre/po).

## (g) Decisões para o Alexandre
1. Pasta de produção: **A** a da empresa (OneDrive - PMZ DISTRIBUIDORA SA, onde o robô e o time já estão; a pessoal vira cópia) · B a pessoal (move o robô e o time) — **recomendo 1 A**.
2. Onde roda: **A** notebook do robô, 06h30 · B desktop · C encadeado no robô das 08h — **recomendo 2 A**.
3. Repositórios privados + token de leitura no cofre do notebook: **A** sim · B continuam públicos (zip sem login) — **recomendo 3 A**.
4. Regra 11 automática com os 5 limites do (e): **A** sim · B só com (3),(4),(5) · C mantém "instale" — **recomendo 4 A**.
5. Se a 1ª rodada travar por arquivo de versão antiga: **A** `--primeira-vez` com backup total · B arquivo a arquivo por PR — **recomendo 5 A**.
