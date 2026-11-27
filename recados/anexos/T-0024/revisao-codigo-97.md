# Revisão de código — PR #97 (T-0024, testes do lote 2)

- Branch: `testes/T-0024-farois-lote2-testes`
- Head revisado: **cd50254** (cd50254c7ae254f95800b9086c7f6ce345ec4bfc)
- Base: `origin/main` a32b610 (já com o merge do main em de3939d)
- Revisor: revisor-codigo, 27/11/2026 (Manaus)
- Leitura só por `git diff origin/main...<branch>` e `git show`; nada alterado e nenhuma suíte rodada (o combinado já passou: 576 + 353, segundo o `docs/testes/T-0024.md`).

## Parecer: **APROVADO** (sem 🔴 e sem 🟡)

Este parecer vale só para o head cd50254. Um commit novo pede uma revisão nova.
No momento da revisão, o CI do head estava rodando (`conferir` in_progress). O merge continua exigindo o CI verde nesse SHA.

## O que foi conferido

| Item | Resultado |
|---|---|
| Pedido atendido, sem nada a mais | ✅ Entraram 8 arquivos, todos de testes, docs de testes e diário. Nenhum `.py` de produção, config ou base foi tocado. |
| Testes provam a regra | ✅ §10.8.7: acima de 8 MB, o farol perde todas as `tabelas` de uma vez, com um aviso só em 1º. Cartões, painel, recortes, insights e `baixado_em` ficam iguais, o farol cabe no teto e a entrada não muda (`_tam_sem_anexos`). Abaixo do teto, volta o mesmo objeto (`is f`). De ponta a ponta: o robô usa o formato 2 e a web guarda os 5 faróis sem herança, o Giro sem abas e os outros 4 com as abas. O pacote real confere o sha256 = bytes do `_cortar_farol_web` e o 200/403 por perfil no Resumo e em cada aba. A matriz `VE_FAROL`/`VE_ABAS` foi escrita à mão e comparada com `render.FAROIS` e `tabelas.VE_TABELAS`. |
| Skip só com motivo real | ✅ `test_T0024_robo_lote2.py` e `test_T0024_pacote_real_lote2.py` pulam o módulo só quando falta `RIDS_LIVRES_WEB`/`params_farol_web` + o lote 2 em `FAROIS_WEB` (#91). O `_web_tem_lote2` pula quando o lote 2 falta em `render.FAROIS` (#89). O `_fixture_lote2(so_web=True)` pula sem a `web/tests/lote2_fixture.py`. O `web_mod` pula sem fastapi/httpx. Os testes de teto (função pura) **não** pulam: sem a fixture da web, rodam sobre o `_farol_minimo`. Nenhum `xfail` novo. |
| Trava `tests/escopo_farois_web.py` (#130) | ✅ O arquivo está igual ao do main. `problemas_escopo(ba) == []` continua em `test_T0013_pacote_web.py:374`, `test_T0017_tres_farois.py:90` e `test_T0024_trava_escopo_farois_web.py`. O T0017 só ganhou a checagem da fonte do "baixado em" do lote 2, igual à do `vc_meta`, que bate com o `_FONTE_BAIXADO_WEB` do #91. |
| Fixture do `RELATORIOS/painel_diretor_hist.json` | ✅ Está em `tests/conftest.py`: fixture `_historico_do_diretor_fora_do_repositorio` (session, autouse), que copia o arquivo para `tmp_path_factory` e troca `pdr._hist_path` só para a raiz do repositório. O `painel_diretor.py` (linhas 301 e 785) e o `painel_cartoes.py:197` chamam pelo nome global do módulo, então a troca pega. A prova está em `tests/test_suite_nao_grava_base_congelada.py`: o destino fica fora do repo, outra raiz segue o caminho normal e o hash do arquivo é o mesmo antes e depois do `montar("vc_painel")`. |
| Dados pessoais nas fixtures | ✅ Os dados são fictícios: "000001 - LOJA TESTE", "9299999", "RUA X", "FILIAL FICTICIA AM", logins `t24.<perfil>` e senhas de teste. O pacote real só gera mensagens de falha com id, perfil, status, títulos de aba e hashes. No doc, só contagens e tamanhos. Nenhum CNPJ, e-mail ou telefone real no diff. |
| Donos | ✅ `verificar --por-commit origin/main..cd50254`: 10 commits, nenhuma violação. Todos os arquivos são do `testes` (`tests/**`, `docs/testes/**` e o diário do próprio agente). Todo commit traz o `Agente: testes`. |
| Dado digitado, configs, `VERSAO`, segredos | ✅ Nada tocado. O `TOKEN`/`SESSION_SECRET` vêm do harness da T-0035 e são valores de teste. Nenhuma leitura de arquivo de chave. |

## 🟢 Sugestões (não bloqueiam)

1. `tests/test_T0024_lote2_robo_web.py:193`: `assert "aba=todos-os-produtos" not in h.text` olha um slug só. Seria mais firme conferir que nenhum `?aba=` aparece na tela do Giro, ou nenhum slug de `tabelas.abas_do_farol("pl_giro", p["relatorios"]["pl_giro"])`. Hoje o `"tabelas" not in giro` já cobre a regra.
2. `tests/test_T0024_lote2_robo_web.py:260`: `x.split(" | ")[-1] in txt` procura o valor como substring do JSON do farol inteiro. Um valor curto ("3") sempre acha. Seria melhor comparar com o conjunto de `valor` dos `kpis` (e dos `recortes`) do farol. O valor × regra exato do PC contra o pacote continua no `test_T0024_pacote_real_lote2.py`.
3. O CI da raiz (`.github/workflows/ci.yml`) não instala fastapi, então os testes de ponta a ponta robô × web (T-0035 e este) só rodam no combinado local. Fica a sugestão ao gerente de um passo no CI que rode `tests/test_T00*_robo_web.py` com o `web/requirements-dev.txt`. É governança e fica fora deste PR.
