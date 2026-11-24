---
id: R-20261124-185037-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:50:37-04:00
---
# Parecer do revisor-codigo: PR #53 head 6aaa757 — 🟡 só atualizar com o main (merge)

> Parecer do revisor-codigo, com checagem de redundância (subagente do gerente-projetos; gravado pelo gerente sem alteração).

# Revisão — T-0017 — testes/T-0017-testes-farol — head 6aaa757

Resultado: **não aprovado ainda**: 1 🟡 (o branch está desatualizado). Nenhum 🔴. Os achados da revisão anterior (a94866f) estão resolvidos.

## Conferência do que pedi
- 🟡 anterior, resolvido: o `test_T0017_coletar_monta_vc_painel_e_os_farois_do_mes` foi removido. A cobertura fica com `test_T0013_coletar_chama_montar_vc_painel_e_farois_web` (tests/test_T0013_pacote_web.py:548).
- 🟢 aplicado: a linha `set(saida) == {"vc_painel", *FAROIS_WEB}` saiu do teste `falha_de_um_farol`.
- 🟢 aplicado: os mtimes do teste `baixado_em` estão invertidos. O teste agora prova que vale o arquivo mais novo pelo nome (23/11) e que o carimbo é o mtime dele (18:13:20-04:00).
- 🟢 aplicado: entrou um CNPJ fictício (00.000.000/0001-00) na frase "devedores", e o teste afirma que ele não aparece no JSON.
- 🟢 não aplicado, sem bloqueio: o filtro na leitura da foto (`bap_dados._fotos_de_titulos`) segue sem teste próprio.

## Execução
- `pytest tests/ -q` no head 6aaa757: 1 falhou e 183 passaram. Falhou `test_RN_GER_004_bloco_inadimplencia_filtrado_no_contexto`, porque o merge-base do branch ainda é 0605f8b, anterior ao #50 (e56fe45).
- Head mesclado localmente com origin/main (73a8b4a, que já tem o #50 e o #52): 184 passaram e nada falhou.
- Nenhum skip ou xfail nos arquivos T0017. compileall ok.
- `verificar testes --base origin/main`: OK, 3 arquivos e nenhuma violação.
- Os dois commits trazem `Agente: testes`.

## Achados
- 🟡 Branch testes/T-0017-testes-farol: no próprio head ainda falha 1 teste, e a regra pede CI verde no head SHA. Correção: atualizar o branch com o main por **merge** (sem rebase e sem force push), para o main com o #50 entrar. Depois disso, o novo head precisa passar sem falha. Pelo teste local, o resultado esperado é 184 passaram. O conteúdo dos testes já está aprovado.

Redundância: sem achado.
