---
id: R-20261124-184926-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:49:26-04:00
---
# Parecer do revisor-codigo: testes/T-0017-testes-farol a94866f — 1 🟡 (teste repetido)

> Parecer do revisor-codigo, com checagem de redundância (subagente do gerente-projetos; gravado pelo gerente sem alteração).

# Revisão — T-0017 — testes/T-0017-testes-farol — head a94866f

Resultado: **não aprovado ainda**: 1 🟡 (redundância). Nenhum 🔴.

## Execução
- pytest no head a94866f: 1 falhou, 184 passaram. A falha é a esperada: `tests/test_T0017_inadimplencia_internos.py::test_RN_GER_004_bloco_inadimplencia_filtrado_no_contexto`, porque falta o `elif nome == "inadimplencia"` em `relatorios_nucleo._sem_internos` (#50).
- pytest com o `relatorios_nucleo.py` de origin/modulo-farois/T-0017-inadimplencia-internos aplicado (+3 linhas): 185 passaram e nada falhou. Arquivo devolvido e worktree limpo.
- Arquivos T0017: 32 casos (26 + 2 + 4). Nenhum skip ou xfail.
- compileall ok.
- `verificar testes --base origin/main`: OK, 3 arquivos e nenhuma violação.
- Commit com `Agente: testes`.

## Regras provadas
- RN-GER-004 nos títulos: `titulos_sem_internos` exclui os três internos e a variante "BAP AUTO PARTS", é pura e aceita None. O caminho do contexto `rn._sem_internos("inadimplencia")` também está coberto.
- RN-GER-004 nas fotos: o resumo da foto só conta o atraso de fora. A marca `fi1` e VERSAO 27 estão conferidas.
- 000040 continua no farol: coberto no filtro puro e no contexto.
- RN-GER-006: os 7 códigos de filial do 03-regras são parametrizados, com igualdade exata (a filial fora do mapa é descartada). A soma dos recortes bate com o total, e o mapa usa os nomes reais.
- Chaves proibidas e tipos de bloco: cobertos. O cliente ("devedores") não vai nem com `grafico_com_nome=True`. O vendedor sai com a chave False.
- baixado_em: no pacote vem do mtime do arquivo de origem, é diferente de gerado_em e vira null sem arquivo. A busca pelo Títulos em Abertos mais novo está coberta.
- Fuso de Manaus: o "agora" ingênuo recebe -04:00, e o epoch UTC é convertido para -04:00.
- Fixtures fictícias: FULANO, BELTRANO, CLIENTE FICTICIO e códigos 1000xx/0000xx. Não há CNPJ, telefone ou e-mail.
- Nomes: os testes de regra citam a RN (RN_GER_004/005/006). Os testes de encanamento usam o prefixo T0017, como diz a docstring.

## Achados
- 🟡 tests/test_T0017_farol_web_robo.py:224-235 (`test_T0017_coletar_monta_vc_painel_e_os_farois_do_mes`) repete `tests/test_T0013_pacote_web.py:548` (`test_T0013_coletar_chama_montar_vc_painel_e_farois_web`): mesmo monkeypatch e mesma asserção de `chamadas`. A única linha nova é `("pl_inadimplencia", par) in chamadas`, e quem já trava isso é `test_T0017_pacote_leva_o_farol_e_so_ele_dos_farois` (linha 182, `"pl_inadimplencia" in ba.FAROIS_WEB`). Correção: remover o teste.
- 🟢 tests/test_T0017_farol_web_robo.py:197 (`falha_de_um_farol`) repete `set(saida) == {"vc_painel", *FAROIS_WEB}` do T0013. Basta manter a parte nova (`erro_montagem` e a ausência no pacote).
- 🟢 tests/test_T0017_farol_web_robo.py:276-286: o arquivo mais novo por mtime também é o mais novo pelo nome, então o teste não diferencia os dois critérios. Sugestão: inverter os mtimes para provar o critério que o código usa.
- 🟢 tests/test_T0017_fotos_sem_internos.py: o filtro na leitura da foto (`bap_dados._fotos_de_titulos`, linha 1473) não é exercitado. Só o filtro puro e o resumo são testados. Sugestão: uma planilha mínima em tmp_path com um título interno.
- 🟢 tests/test_T0017_farol_web_robo.py:140: o teste "cliente nunca vai" checa o nome, mas não um CNPJ. Sugestão: pôr um CNPJ fictício na frase "devedores" e afirmar que ele não aparece no JSON.

Redundância: achados (1 🟡 em farol_web_robo.py:224, duplicata do T0013:548; 1 🟢 em :197).
