---
id: R-20261124-182755-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:27:55-04:00
---
# Pareceres do revisor-codigo: #47 e #48 aprovados; #49 1 🟡 (baixado_em); #50 1 🔴 (000040) e 1 🟡 (fotos)

> Pareceres do revisor-codigo (subagente do gerente-projetos; gravados pelo gerente sem alteração, pela limitação do --de no coord.mjs).

---
# Revisão PR #47 — T-0017 contrato forma "farol" (§10.1) e adendo 2 da ADR 0001
- Branch: engenheiro-software/T-0017-contrato-farol
- Head SHA revisado: 45019f236cf319bfdcf7df0ada01661801fe2cb6 (commit novo = revisão nova)
- Revisor: revisor-codigo · 24/11/2026

## Veredito: APROVADO (sem 🔴 nem 🟡; 🟢 abaixo)

Conferido:
- Pedido atendido sem mudança a mais: só `.coord/contratos/relatorio.md` (§10.1) e `docs/decisoes/0001-bap-central-web-render.md` (adendo 2). Contrato segue v1 (acréscimo compatível).
- Fiel às decisões R-20261124-175838-alexandre (2 A / 3 A / 4 A) e R-20261124-181912-alexandre: nome de vendedor/supervisor nos gráficos; sem cliente, CNPJ e tabelas; filtro por estado só nos cartões, "—" em estado sem recorte; ordem web antes do robô.
- Coerência com o robô (#49) e a web (#48): chaves, `recortes` chaveado por UF, `kpis[i].estados` com 5 posições, proibidas `edicao/editar/abrir`, `_` e `tabelas/juntas`. Validado ponta a ponta: pacote real montado pelo robô (#49+#50, bases congeladas) passa no `pacotes.validar` da web (#48) sem erro.
- Sem segredo, sem dado digitado tocado, `verificar engenheiro-software --base origin/main` OK (2 arquivos), commits com `Agente: engenheiro-software`.

## 🟢 Sugestões
1. `.coord/contratos/relatorio.md:347` — diz que bloco de outro tipo "é aceito no pacote e a web mostra 'ainda não disponível'", mas o robô (#49, `bap_automation.py:6835`) descarta tudo fora de insights/barras/hbarras e nem avisa. Deixar explícito: "o robô manda só insights/barras/hbarras nesta entrega; a web tolera outros tipos".
2. `.coord/contratos/relatorio.md:356` — texto do aviso ("Cartões por estado; gráficos da BAP inteira.") difere do que a web mostra (`web/app/render.py:139`, "Cartões: {uf}. Resumo e gráficos: BAP inteira.", o aprovado na simulação). Alinhar o contrato ao texto aprovado.
3. `docs/decisoes/0001-bap-central-web-render.md:379` — "Nunca vão ao Render nesta fase: nome de cliente, CNPJ..." já tem data para mudar (R-20261124-181913-alexandre: visões Títulos/Por cliente e "Cobrar no WhatsApp" no farol de inadimplência, na entrega seguinte). Uma linha de remissão ("revisto no adendo 3, entrega seguinte") evita leitura errada.
4. `.coord/contratos/relatorio.md:338` (`baixado_em`) — a definição está certa ("quando a base foi baixada do ERP, não o `gerado_em`"); o robô não a cumpre (ver 🟡 no PR #49). Nada a mudar aqui, só manter o texto.

---
# Revisão PR #48 — T-0017 web: validador, render, templates, CSS e perfis dos faróis
- Branch: modulo-web/T-0017-farois-web
- Head SHA revisado: 9211d8b29a1f6465ba005349652daccac7c5762c (commit novo = revisão nova)
- Revisor: revisor-codigo · 24/11/2026

## Veredito: APROVADO (sem 🔴 nem 🟡; 🟢 abaixo)

Conferido:
- Testes da web: `pytest web/tests` = 49 passed (inclui os 11 novos de `test_farois.py`: aceitação, recusa de chave proibida aninhada, filtro por UF, malformado, mini-barras, 403 por perfil, menu).
- XSS: autoescape ligado (`main.py:67`). Injetei `<script>`, `<img onerror>` e `" onload=` em titulo, avisos, insights, kpis (rotulo/valor/detalhe), hbarras/barras (titulo, rótulos, nome de série) e `baixado_em`, e cor `red;background:url(x)` / `#fff" onload=1`: tudo saiu escapado (11 ocorrências `&lt;script&gt;`), cor fora de `#RRGGBB` vira a padrão (`render._cor`), classes de tom passam por lista fechada (`render._tom`). Sem `|safe` no `farol.html`.
- Validador: `pacotes._chave_proibida` recusa `tabelas/juntas/edicao/editar/abrir` e chave `_` em qualquer nível (dict e lista), com teto de aninhamento (12) que também recusa; formato de kpis, estados (5 posições), blocos, insights, recortes (UF por `RE_UF`, teto `MAX_RECORTES`).
- 403 por perfil: `/farol/{rid}` confere `render.FAROIS[rid][1]` no servidor; rid desconhecido = 403; perfis novos não entram em `/painel` nem `/usuarios` (`VERES`).
- Regras: estado sem recorte mostra "—" e nunca o número da BAP inteira (contrato §10.1, RN-GER-006); `baixado_em` exibido em Manaus (`fmt_manaus`). Nada recalculado na web.
- Coerência: pacote real do robô (#49+#50) passa no `validar` sem erro e a página abre.
- Tela: simulação em PNG aprovada pelo Alexandre (R-20261124-181912-alexandre, "1 A / 2 A").
- `verificar modulo-web --base origin/main` OK (11 arquivos), commits com `Agente: modulo-web`, sem segredo real (as senhas de `simular_farol.py` são de simulação, em pasta temporária).

## 🟢 Sugestões
1. `web/app/pacotes.py:109` — docstring cita "contrato §8"; a forma farol é o §10.1.
2. `web/app/render.py:139` — `AVISO_UF` difere do texto do contrato §10.1 (ver PR #47, 🟢 2). Alinhar num dos dois lados.
3. `web/simular_png.mjs:6` — `createRequire('/opt/node-tools/node_modules/')` fixa um caminho da máquina da sessão; usar `require('playwright')` normal ou variável de ambiente.
4. `web/tests/test_farois.py` — falta um teste explícito de escape (texto com `<script>` no pacote → `&lt;script&gt;` na página). Hoje passa (conferi), mas sem teste fica sem guarda.
5. Defesa em profundidade (opcional): o validador poderia recusar texto com padrão de CNPJ (`\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}`) em qualquer string do farol, já que cliente/CNPJ "nunca" vai ao Render nesta fase.

---
# Revisão PR #49 — T-0017 robô: Farol de Inadimplência no pacote web
- Branch: modulo-robo/T-0017-farol-inadimplencia
- Head SHA revisado: 84afe047606230ded5b558eac3ccc41de35fe7a9 (commit novo = revisão nova)
- Revisor: revisor-codigo · 24/11/2026

## Veredito: NÃO APROVADO — 1 🟡 a corrigir antes do merge

Conferido:
- Testes do 2º PR do `testes` (scratchpad, copiados para pasta temporária): sobre o código deste PR, `test_T0017_farol_web_robo` + `test_T0017_extra` = **23/23 passam** (os 3 de internos falham aqui, esperado: são do PR #50). Com #49+#50 juntos: **26/26**. Suíte `tests/` inteira (com o `test_T0013_pacote_web.py` atual do main): 179 passed. `compileall` OK.
- Ponta a ponta com as bases congeladas (`simular_pacote_farol`, hoje 24/11/2026): pacote passa no `pacotes.validar` da web (#48) sem erro; recortes AM, AP, MA, MT, PA, RR (filial da nota, RN-GER-006); 2 cartões com mini-barras; **0 de 383 nomes de cliente** da tabela Títulos aparecem no pacote; nenhum CNPJ (as 22 ocorrências com forma de CNPJ são floats das barras); a única frase removida é "Maiores devedores: ..." (8 de 9 frases ficam: o filtro não tira demais). Vendedor no hbarras, conforme D1 "2 A".
- Falha isolada por farol (`coletar_relatorios_web`, `montar_pacote_web`): o `vc_painel` segue.
- `bap_dados.VERSAO` = 27, sem regra de cache nova. `verificar modulo-robo --base origin/main` OK (1 arquivo), commits com `Agente: modulo-robo`. Sem segredo, sem dado digitado.

## 🟡 Corrigir antes do merge
1. `bap_automation.py:6859` — `"baixado_em": agora.isoformat()` grava a hora em que o pacote foi montado (= `gerado_em`), e o contrato §10.1 (PR #47) define `baixado_em` como "quando a base do farol foi baixada do ERP. Não confundir com o `gerado_em`". Se o download do dia falhar e o 4f rodar sobre a base velha, o site mostra "Baixado em <agora>" sobre número velho, para o Diretor. Usar a hora real da base (ex.: mtime de `RELATORIOS/TABELA_BAP.xlsx` convertido para America/Manaus, ou a hora do download registrada pelo robô) e `null` se não houver. O teste `test_T0017_forma_do_farol_json_puro_com_fuso_manaus`/`test_T0017_agora_sem_fuso_vira_manaus` (2º PR do testes) precisa acompanhar.

## 🟢 Sugestões
1. `bap_automation.py:6599-6600` — comentário "D1 do Alexandre pendente... fica FORA enquanto for False" está velho: a D1 foi decidida (R-20261124-175838-alexandre, "2 A") e a constante já é `True`.
2. `bap_automation.py:6609` / `_linhas_insight` — o filtro de cliente é lista de termos (`devedor`, `cnpj`) e só olha frases e títulos de hbarras; `kpis[].detalhe`/`linhas` e rótulos de `barras` não passam por ele. Hoje está limpo (0/383), mas uma frase nova do PC com nome de cliente sem a palavra "devedor" vazaria. Sugestão: conferir também contra o conjunto de nomes/códigos de cliente da tabela "Títulos" (que o `selecionar_farol_web` já recebe em `r`) e tirar o que bater, com aviso.
3. `bap_automation.py:6835` — bloco de tipo fora de insights/barras/hbarras some sem aviso; o contrato §10.1 diz que a web mostraria "ainda não disponível". Ou manda o bloco (a web já tolera), ou acrescenta em `avisos` como faz com o gráfico com nome.

---
# Revisão PR #50 — T-0017 Farol de Inadimplência sem CNPJs internos e sem a conta 000040
- Branch: modulo-farois/T-0017-inadimplencia-internos
- Head SHA revisado: f8257232e0b1dac7d385ca122a630acb3ff8bf36 (commit novo = revisão nova)
- Revisor: revisor-codigo · 24/11/2026

## Veredito: NÃO APROVADO — 1 🔴 e 1 🟡

Conferido:
- Testes do 2º PR do `testes` (scratchpad, em pasta temporária): `test_T0017_inadimplencia_internos` = **3/3 passam** sobre este PR (os 23 do robô falham aqui, esperado: são do PR #49); #49+#50 juntos: 26/26. Suíte `tests/` 179 passed. `compileall` OK.
- `bap_dados.VERSAO` = 27; o filtro roda depois do cache (`Contexto.__getattr__` → `_sem_internos`), sem marca nova necessária. `verificar modulo-farois --base origin/main` OK (1 arquivo), commit com `Agente: modulo-farois`.

## 🔴 Bloqueia
1. `relatorios_nucleo.py:727` e `:734` — `CONTA_TESTE = "000040"` é comparado com `t["cod"]`, que é o **código do cliente** (E1_CLIENTE). Em todo o sistema 000040 é **código de vendedor** (a conta de teste do Alexandre): `planner_nucleo.py:6309` (`COD_VENDEDOR`), `email_inadimplencia.py:59` (`cod_protheus` da pessoa), `respostas_bap_ajuda.py:43`, `bap_champions.py:67`. Nas bases congeladas o **cliente 000040 existe, é real, não é interno** (vendedor 000006), e os clientes do vendedor 000040 são 390 (a carteira do Amapá). Resultado: o filtro tiraria do farol e do Diretor a dívida de um cliente real se ele tiver título, e não faz o que a RN pede. Além disso a RN-GER-005 (`docs/produto/03-regras.md:10`) tira a 000040 de "prospecção, indicação, pesquisa e e-mails", não do saldo a receber. Corrigir: tirar a condição do 000040 dos títulos (a carteira é real; o e-mail/WhatsApp de cobrança já trata a conta de teste), ou, se o Alexandre quiser outra coisa, pedir a regra ao po antes. O teste `test_RN_GER_005_titulo_da_conta_000040_fica_fora` (2º PR do testes) codifica a leitura errada e precisa mudar junto.

## 🟡 Corrigir antes do merge
1. `relatorios_nucleo.py:755` — só `titulos` é filtrado; as `fotos` do mesmo bloco (montadas em `bap_dados.py:1437-1482` a partir dos títulos brutos) continuam com os internos. Elas alimentam no farol os gráficos "Em atraso (R$, última foto)", "Recebido" e "Recuperado", e no Diretor os indicadores "Inadimplência" e "Recuperado de atraso" (`relatorios_nucleo.py:12926-12933`). Com interno em aberto, o cartão do farol (sem interno) e o número do Diretor (com interno) deixam de bater. Nas bases congeladas não há título interno (diferença 0 hoje). Corrigir o filtro nas fotos também (exige mexer em `bap_dados._bloco_inadimplencia` com marca nova na assinatura do bloco `inadimplencia`, `bap_dados.py:324`, recado ao dono), ou registrar a limitação com recado ao po antes do merge.

## 🟢 Sugestões
1. `relatorios_nucleo.py:735` — o interno é detectado só pelo `E1_NOMCLI` do título (o título não tem `fantasia`, então `t.get("fantasia")` é sempre `None`). O bloco `tabela` já tem a lista de códigos internos pelo cadastro (`bd._clientes_internos`, `bloco["internos"]`); reusar o código do cadastro pega também o interno identificado pela fantasia e evita a regra reescrita.
