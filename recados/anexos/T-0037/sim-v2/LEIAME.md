# T-0037 — simulação v2 do Farol de Fretes (web 0.9.0, refeita após o parecer de UX)

Servidor real (uvicorn) com a fixture fictícia `web/tests/fretes_fixture.py`, que espelha campo a campo a saída do robô (`blocos_resumo_fretes_web`, modulo-robo 91e6f8a) e os rótulos do PC (`rotulo_agrupa_fretes`, modulo-farois 48c6577). PC 1366 px e celular 390 px, escala 2, Chromium com `--lang=pt-BR` e `LANG=pt_BR.UTF-8` (datas dd/mm/aaaa), America/Manaus. Perfil admin. Dados inventados.

- 01-resumo: frases curtas do robô, gráfico de 12 meses em largura total (cor neutra da marca; rótulos de 12 px no PC, "DEZ" de 3 letras com 11 px no celular), 3 tabelas com TOTAL e os rótulos "Sem UF", "SERRA BONITA / Sem UF", "Sem cidade / MA", "Sem transportadora" (1, igual ao cartão) e "Sem acompanhamento".
- 02 a 05: abas Notas, UF, Cidade e Transportadora (rótulos do PC).
- 06-popup-da-nota: título "NF 700101"; PC com o mouse sobre a NF, celular com o item da lista aberto.
- 07-editar-admin: edição da nota (5 campos), datas 10/11/2026.
