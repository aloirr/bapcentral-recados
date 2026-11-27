# T-0024: parecer do revisor-codigo sobre os merges do main (T-0035) nos PRs #89 e #91

- Data: 2026-11-27 (Manaus)
- Base: `origin/main` = a32b610
- Heads revisados:
  - **#89 web** (`modulo-web/T-0024-farois-lote2`): **07328de** (antes 820330f)
  - **#91 robô** (`modulo-robo/T-0024-farois-lote2-robo`): **b21ba62** (antes 9753598)
- Como olhei: `git show --remerge-diff` dos dois merges, `git diff origin/main..<head>`, cópia das duas árvores (`git archive`) no scratchpad para compilar e rodar testes direcionados. O clone não foi alterado e a suíte combinada não rodou (o testes está rodando).

## Resultado
- **#89 web (07328de): aprovado.** Sem 🔴 e sem 🟡.
- **#91 robô (b21ba62): aprovado.** Sem 🔴 e sem 🟡. O merge depende do CI "conferir" fechar verde nesse head; na hora da revisão ele ainda rodava.

## O que o merge trouxe e como os conflitos foram resolvidos

### #91 robô
- Só um conflito, em `bap_automation.py`, na linha de `RIDS_TABELAS_WEB`. A resolução guarda o bloco do main inteiro: `WEB_FAROL_TETO_MB = 8`, `_ANEXOS_FAROL_WEB`, os tetos dos anexos (`MAX_PNG_B64`, `MAX_CSVS_WEB`, `MAX_CSV_BYTES_WEB`, `MAX_CSVS_TOTAL`), os 4 avisos, `_CORTES_FAROL_WEB` e `_FRACOES_ENTREGAS_WEB`. Também acrescenta o lote 2: `RIDS_TABELAS_WEB = (pv_pedidos, pl_entregas, vc_visitas) + RIDS_LIVRES_WEB`.
- `RIDS_LIVRES_WEB` é definido antes, na linha 6624, junto de `FAROIS_WEB`. A ordem de importação está certa.
- Contra o main, o diff só traz o lote 2. Nada da T-0035 sai: `_cortar_farol_web`, `_limitar_anexos_web`, `enviar_pacote_por_farol`, o `cortar=False` do `montar_pacote_web` e a pasta do lote continuam iguais aos do main.
- **Formato por farol (§10.8) nos 5 faróis do lote 2:**
  - eles estão em `FAROIS_WEB` e por isso entram no `montar_pacote_web` e no `enviar_pacote_por_farol` (um POST por farol);
  - sem entrada em `_CORTES_FAROL_WEB`, caem no corte padrão `("tabelas",)` e recebem o `AVISO_ABAS_FORA`;
  - no formato 1, os passos 1 a 3 do `_cortar_pacote_web` também valem para eles, porque estão em `RIDS_TABELAS_WEB`;
  - conferi com um farol `vc_base` fictício acima do teto: as abas saem e o aviso "Abas fora desta atualização: Clientes, Por UF" entra.
- O "baixado em" vem de `_FONTE_BAIXADO_WEB`: os 5 apontam para os Movimentos do Protheus.
- **RN-GER-006:**
  - pl_giro e pl_frw recortam pela FILIAL;
  - vc_base recorta pelo `montar` com UF (`RIDS_KPIS_POR_UF_WEB`);
  - pv_indicadores e vc_planner não têm recorte e levam o aviso "Sem filtro por estado".
  - Bate com a trava do main (`tests/escopo_farois_web.py`, `FAROIS_LOTE2`).
- **Dados pessoais:**
  - continuam fora as colunas de `_COLUNAS_FORA_WEB` (telefone, CNPJ, CPF, e-mail, contato, foto, endereço), mais `Nº`/`NÚMERO` e as colunas internas `_*`;
  - os campos CLIENTE, NOME, FANTASIA e RAZÃO SOCIAL passam por `cliente_sem_documento`/`sem_documento` (RN-GER-011).
- `bap_dados.VERSAO = 27`. Nenhuma base congelada, `.json` da raiz ou dado digitado no diff.

### #89 web
- **Conflitos:**
  - `.coord/diario/modulo-web.md`: as duas linhas ficaram, a do T-0024/T-0032 e a do T-0035;
  - `web/tests/test_T0024_farois_lote2.py`: ganhou `test_lote2_no_formato_por_farol_da_T0035`, que faz POST por farol + fechar com os 5 faróis, abre do disco e confere o perfil (`vendas` em pl_frw = 403).
- `web/app/pacotes.py`, `config.py`, `__init__.py` (0.4.0) e `base.html` são iguais aos do main: a T-0035 continua inteira.
  - `FAROIS = tuple(render.FAROIS)` aceita os 5 nas rotas por farol.
  - `validar_farol` usa `tabelas.validar` para conferir as abas livres (até 20 abas, título único, colunas sem `_`).
  - `tirar_abas_com_documento` tem o fallback para farol sem `ABAS` fixo.
- O selo "Desatualizado" (`pagina()`, T-0035 §4.4) é genérico por `rid` e vale para os 5.
- O `{% if rid not in livres %}` do `farol.html` esconde só os `avisos_info` (o "Sem filtro por estado", parecer de UX R5). "Abas fora desta atualização" e o selo continuam à vista.
- **Perfis:**
  - `render.FAROIS` segue o PC;
  - `tabelas.VE_TABELAS` não dá as tabelas ao diretor (teste `test_ve_tabelas_D1_recomendacao_A` mantido).
- **Fixtures:**
  - todos os nomes são fictícios ("CLIENTE FICTICIO nn");
  - o único documento é o CNPJ de exemplo 12.345.678/0001-95, usado no teste que recusa documento em célula.

## Testes (nas cópias das árvores, direcionados; não é a suíte combinada)
- `python -m compileall -q`: ok nos dois.
- Robô (b21ba62), 109 passaram:
  - `tests/test_T0024_trava_escopo_farois_web.py`
  - `tests/test_T0035_pacote_por_farol.py`
  - `tests/test_T0035_cortes_anexos_entregas.py`
  - `tests/test_T0017_tres_farois.py`
  - `tests/test_T0035_robo_web.py`
  - `tests/test_T0013_pacote_web.py`
- Web (07328de), 142 passaram:
  - `web/tests/test_T0024_farois_lote2.py`
  - `test_T0024_lote2_estrutura.py`
  - `test_T0035_pacote_por_farol.py`
  - `test_abas.py`
- `coord.mjs verificar --por-commit a32b610..<head>`: OK nos dois (12 e 2 commits; os merges ficam de fora). Todos os commits trazem `Agente: modulo-web` ou `Agente: modulo-robo`, e os arquivos são dos donos certos.
- CI no head: #89 "conferir" verde. #91 "conferir" ainda rodando.

## 🟢 Sugestões (não bloqueiam)
1. `bap_automation.py:7551` (`_CORTES_FAROL_WEB`): nos 5 faróis livres, o corte por farol é tudo ou nada. Acima de 8 MB, todas as abas saem. Se o vc_base "Clientes" ou o pl_giro "Todos os produtos" crescerem, vale um passo antes que tire só a maior aba. O robô #91 não tem teste próprio desse caminho: fica para o PR #97 do testes cobrir um farol livre acima do teto no formato por farol.
2. Redundância: o robô monta o aviso "Sem filtro por estado" para pv_indicadores e vc_planner (a trava do main exige), e a web o esconde nos faróis livres (`farol.html`). Fica registrado para o corretor-redundancias decidir se a regra mora num lugar só.

## Pendências e premissas
- [SUPOSIÇÃO] Não achei o parecer anterior do revisor sobre 820330f/9753598, nem nos comentários e reviews dos PRs #89/#91, nem nos anexos T-0024 (só PNGs). Revisei o merge e o diff inteiro contra o main.
- [SUPOSIÇÃO] A ordem de merge do R-20261127-005437-alexandre (#89 web antes do #91 robô, e o #97 depois) continua valendo.
- Por pedido do gerente, este parecer não foi commitado e não teve recado `revisao`.
