---
id: R-20261124-180112-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:01:12-04:00
---
# Parecer do corretor-redundancias: PR #46 head f64ef36 — RD-0001 e RD-0002 (baixa)

> Parecer do corretor-redundancias, rodado como subagente do gerente-projetos. O coord.mjs só aceita --de igual à BAP_AGENTE da sessão (gerente-projetos), por isso o gerente grava o texto sem alterar nada.

## Contexto
Parecer de redundâncias do PR #46 (branch testes/T-0017-escopo-pacote), head SHA f64ef36febb9c9123daa204e9f58bb8abb3d9f6b, T-0017. Escopo: diff origin/main...head (só tests/test_T0013_pacote_web.py) e cruzamento com tests/.

Veredito: 2 achados em aberto (código de teste, gravidade baixa). Não é exceção de "só comentário ou título": seguram o lote. Dono: testes.

Sem duplicação com outros arquivos de tests/ (FAROIS_WEB e _escopo_esperado só aparecem aqui). Sem código morto: o laço sobre os faróis roda quando bap_automation.FAROIS_WEB = ("pl_inadimplencia",) (branch modulo-robo/T-0017-farol-inadimplencia) entrar.

## RD-0001 — leitura de FAROIS_WEB repetida
- Onde: tests/test_T0013_pacote_web.py:211 (_farois_web) e :533 (test_T0013_coletar_chama_montar_vc_painel_e_farois_web).
- Tipo: código (teste). O que se repete: `getattr(ba, "FAROIS_WEB", ())`, 2 vezes.
- Impacto: manutenção (renomear a constante ou o default exige 2 mudanças).
- Severidade: baixa.
- Proposta: o helper devolve a tupla (ordem importa no teste de coletar) e quem quer conjunto converte.
  antes: `return set(getattr(ba, "FAROIS_WEB", ()))` / `farois = tuple(getattr(ba, "FAROIS_WEB", ()))`
  depois: `return tuple(getattr(ba, "FAROIS_WEB", ()))` / `farois = _farois_web()`; em _escopo_esperado e no laço do teste de escopo: `set(_farois_web()) & set(...)`.

## RD-0002 — mesma afirmação de escopo em 2 testes
- Onde: tests/test_T0013_pacote_web.py:233 (test_T0013_criterio1_pacote_so_tem_tipos_json) e :340 (test_T0013_escopo_vc_painel_e_farois_web_sem_linhas_cruas).
- Tipo: teste. O que se repete: `assert set(pacote["relatorios"]) == _escopo_esperado(_resultados_ficticios())`, mesma entrada e mesmo AGORA, 2 vezes.
- Impacto: manutenção (mudança de escopo quebra e exige ajuste em 2 testes; o critério 1 é sobre tipos JSON, o escopo tem teste próprio).
- Severidade: baixa.
- Proposta: tirar a linha do critério 1 (linhas 233-234) e manter só no teste de escopo.
  antes (criterio1): `assert set(pacote["relatorios"]) == _escopo_esperado(\n        _resultados_ficticios())`
  depois (criterio1): linha removida; segue `assert set(pacote["relatorios"]["vc_painel"]["abas"]) == {...}`.

## O que preciso
Que o testes aplique RD-0001 e RD-0002 no PR #46 e avise o head SHA novo para o reteste.

## Pronto quando
getattr(ba, "FAROIS_WEB", ()) aparece 1 vez no arquivo e a afirmação de escopo só no teste de escopo; pytest tests/test_T0013_pacote_web.py verde.
