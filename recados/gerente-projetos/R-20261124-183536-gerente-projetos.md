---
id: R-20261124-183536-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:35:36-04:00
---
# Pareceres do revisor-codigo: #47, #48 e #49 aprovados; #51 aprovado no 44c6e3b; #50 1 🟡 (usar bd.titulos_sem_internos)

> Pareceres do revisor-codigo (subagente do gerente-projetos; gravados pelo gerente sem alteração, pela limitação do --de no coord.mjs).

---
# Re-revisão PR #47 — T-0017 contrato forma "farol" (§10.1) e adendo 2 da ADR 0001
- Branch: engenheiro-software/T-0017-contrato-farol
- Head SHA revisado: 1cde84dfb4a2febae533e708d01260a9975eb5d1 (antes 45019f2; commit novo = revisão nova)
- Revisor: revisor-codigo · 24/11/2026

## Veredito: APROVADO (sem 🔴 nem 🟡)

Conferido no diff 45019f2..1cde84d (2 arquivos, 3+/3-):
- RD-0001: o ADR só remete ao contrato §10.1 para o formato de `kpis[i]["estados"]`; fonte única no contrato.
- RD-0002: o contrato não fixa mais o texto do aviso; cita `web/app/render.py`, `AVISO_UF` (que existe no #48, head 18d65d9).
- `baixado_em` = hora em que a base foi baixada do ERP, não a da montagem (essa é o `gerado_em`). Bate com o robô do #49 (`_baixado_em_da_base`, `null` sem arquivo).
- `verificar engenheiro-software --base origin/main`: OK, 2 arquivos. Os 3 commits trazem `Agente: engenheiro-software`. Sem segredo e sem dado digitado.

## 🟢 Sugestões (não bloqueiam)
1. `.coord/contratos/relatorio.md:336` (linha `avisos`): "o robô pode acrescentar (ex.: bloco tirado)". Depois do RD-0010, o robô (#49) não acrescenta mais aviso. Vale trocar para "os do PC" numa próxima mexida.
2. Seguem as 🟢 1 e 3 do parecer anterior: tipo de bloco fora de insights/barras/hbarras (o robô descarta) e a remissão ao adendo seguinte sobre cliente/CNPJ.

---
# Re-revisão PR #48 — T-0017 web: faróis (RD-0003..0008, macro `_estados.html`)
- Branch: modulo-web/T-0017-farois-web
- Head SHA revisado: 18d65d977ae1e1b642ed2209220775a5510f5247 (antes 9211d8b; commit novo = revisão nova)
- Revisor: revisor-codigo · 24/11/2026

## Veredito: APROVADO (sem 🔴 nem 🟡)

Conferido no diff 9211d8b..18d65d9 (8 arquivos):
- **O Painel no ar (T-0013/T-0014) continua igual.** Renderizei `/painel`, `/painel?aba=produtividade`, `/painel?uf=AM` e `/painel?aba=produtividade&uf=PA` com o `pacote_ficticio` do `web/tests/conftest.py`, no `origin/main` e no merge dos 5 PRs. Normalizado o espaço em branco e tirado o csrf, o HTML é **idêntico** (611 linhas, 8 blocos `rc-barras` nos dois). A macro `barras_estados` reproduz o trecho antigo do `painel.html` linha a linha, e o `{% if est %}` equivale ao `{% if c.estados %}`. A única diferença é no menu `/`: os 4 faróis novos, com "ainda não disponível na web". Isso é escopo da T-0017 e veio do RD-0005.
- CSS: as regras `.mini*` saíram. A `.gb-txt` agora é uma só (RD-0008). O ajuste das barras no cartão do farol fica no escopo `.kpi-est .rc-barras` e não atinge o painel. O painel não usa `.kpi`/`.kpis`.
- RD-0003: o aviso virou `AVISO_UF = "Resumo e gráficos: BAP inteira."` e saiu o "· BAP inteira" do h2. RD-0004: com estado sem recorte, aparece "—" sem a dica por cartão e um aviso só ("Sem números de RR neste pacote. Resumo e gráficos: BAP inteira."; conferi 0 ocorrências de "só na BAP inteira" e 6 traços). RD-0005: um texto só (`render.INDISPONIVEL` no contexto). RD-0007: "Baixado do ERP em …".
- `pytest` em `web/`: 49 passed. `verificar modulo-web --base origin/main`: OK, 13 arquivos. Os 5 commits trazem `Agente: modulo-web`.
- A tela mudou pouco: só textos e as barras do cartão, que agora usam o componente do painel. O print desta versão fica com o `designer-ux`. [SUPOSIÇÃO] A simulação aprovada (R-20261124-181912-alexandre) continua valendo para essa mudança de texto e componente.

## 🟢 Sugestões (não bloqueiam)
1. `web/tests/test_farois.py:64`: o teste do RR só confere "—". Falta afirmar `"Sem números de RR neste pacote."` e a ausência de `"só na BAP inteira"`, que são o ramo novo do RD-0004.
2. `web/app/render.py:333`: `((SEM_DADO_UF…) if sem_dado else "") + AVISO_UF if uf else ""` está certo pela precedência, mas é difícil de ler. Um `if` antes do `return` deixa claro.
3. Seguem as do parecer anterior: `web/app/pacotes.py:109` cita "contrato §8" (o certo é §10.1); `web/simular_png.mjs:6` fixa `/opt/node-tools/node_modules/`; falta um teste explícito de escape de `<script>`.

---
# Re-revisão PR #49 — T-0017 robô: Farol de Inadimplência no pacote web
- Branch: modulo-robo/T-0017-farol-inadimplencia
- Head SHA pedido: e8bd178c6687ca51aba4a3bce9aab035883f0fae (antes 84afe04)
- **O branch andou durante a revisão:** o `origin` está em **cb2f6078bb750f39ce52e1a3631bdf3f5809c3db** (22:33 UTC, 1 commit a mais, 5+/5-). Revisei os dois heads.
- Revisor: revisor-codigo · 24/11/2026

## Veredito: APROVADO em e8bd178 e em cb2f607 (sem 🔴 nem 🟡). O merge vale para o cb2f607.

O meu 🟡 do `baixado_em` está resolvido:
- `selecionar_farol_web(rid, r, baixado_em=None, grafico_com_nome=None)` recebe a hora da base e grava `null` quando ela não existe. Não usa mais o `agora`.
- `montar_pacote_web(..., raiz=None, arquivos_base=None)` chama `_baixado_em_da_base(rid, raiz, arquivo)`. A função pega o mtime do `Relatorio_Titulos_em_Abertos_*.xlsx` mais novo em `BKP_RELATORIOS_BAPTOOLS` (pelo mapa `_FONTE_BAIXADO_WEB`) e põe o fuso de Manaus. O nome usa data ISO (`AAAA-MM-DD`), então a ordenação por nome dá o mais novo. A raiz é o `PASTA_LOCAL`, a mesma do `coletar_relatorios_web`/`_rn.montar` e das fotos do `bap_dados._fotos_de_titulos`. Sem arquivo, sem pasta ou com rid sem fonte, devolve `None`. Conferi: raiz inexistente dá `None`, rid `xx` dá `None`, e datetime sem fuso vira `-04:00`.
- A assinatura mudou de `agora` para `baixado_em`. O único chamador no código é o `montar_pacote_web`, e os testes do `testes` (versão `.final`) já usam a forma nova.

Corretor:
- RD-0009: uma lista só (`_CHAVES_FORA_FAROL_WEB = _PACOTE_WEB_CHAVES_ACAO | {...}`) e uma varredura só (`_para_json(..., fora=...)`). O `_sem_chaves_de_acao` saiu.
- RD-0010: saiu o aviso de gráfico tirado.
- RD-0011: `_com_fuso_manaus` está nas duas funções.
- cb2f607: o RD-0012 está resolvido (comentário da D1 atualizado, docstring sem citar arquivo de teste) e o caminho reusa `BKP_BAPTOOLS`.

Outras conferências:
- `bap_dados.VERSAO` = 27, sem regra de cache nova. Sem segredo e sem dado digitado.
- `verificar modulo-robo --base origin/main`: OK, 1 arquivo. Os 6 commits trazem `Agente: modulo-robo`.

## 🟢 Sugestões (não bloqueiam)
1. `bap_automation.py` `_baixado_em_da_base`: o `except Exception` largo esconde até erro de programação. Um `log.debug` com o tipo do erro ajudaria a investigar um "baixado em" vazio no site.
2. Segue a 🟢 2 anterior: o filtro de cliente é por termos (`devedor`, `cnpj`). Conferir também contra os nomes da tabela "Títulos" daria mais garantia.

---
# Re-revisão PR #50 — T-0017 Farol de Inadimplência sem CNPJs internos
- Branch: modulo-farois/T-0017-inadimplencia-internos
- Head SHA revisado: 5ef155b78db85bdaa0b34eef7409517eb1ab3878 (antes f825723; commit novo = revisão nova)
- Revisor: revisor-codigo · 24/11/2026

## Veredito: NÃO APROVADO. O 🔴 está resolvido e fica 1 🟡.

Resolvido:
- 🔴 anterior: saíram a `CONTA_TESTE` e a condição `cod != "000040"`. `titulos_sem_internos` filtra só os CNPJs internos (`bd._interno`, RN-GER-004). A docstring registra que o 000040 é vendedor de teste e não sai do saldo a receber.
- 🟡 anterior (fotos): está no PR #51.

Conferido:
- `verificar modulo-farois --base origin/main`: OK, 1 arquivo. Os commits trazem `Agente: modulo-farois`. VERSAO 27: o filtro roda depois do cache (`_sem_internos`).
- Testes dos 5 PRs juntos: `test_T0017_inadimplencia_internos` passa.

## 🟡 Corrigir antes do merge
1. `relatorios_nucleo.py:727-732` (`titulos_sem_internos`): o corpo é **idêntico** ao do `bap_dados` do PR #51. No head pedido, 464711a, a função se chama `fotos_sem_internos`. No head atual do #51, 44c6e3b, foi renomeada para `titulos_sem_internos` e marcada "fonte única" (RD-0016). É a mesma regra escrita duas vezes. Corrigir assim:
   - com o #51 no `main`, trocar o corpo por `return bd.titulos_sem_internos(titulos)`, ou chamar `bd.titulos_sem_internos` direto no ramo `"inadimplencia"` do `_sem_internos` e apagar a função daqui;
   - ajustar o teste `test_T0017_inadimplencia_internos` se ele importar `rn.titulos_sem_internos`;
   - ordem de merge: #51 antes do #50.

## 🟢 Sugestões
1. Segue a 🟢 anterior: o interno é detectado só pelo `E1_NOMCLI` (o título não tem `fantasia`). Reusar os códigos de `bloco["internos"]` do cadastro pegaria também o interno identificado pela fantasia. Se for feito, fazer na fonte única (`bap_dados`).

---
# Revisão PR #51 — T-0017 fotos do Farol de Inadimplência sem CNPJs internos
- Branch: engenheiro-dados/T-0017-fotos-sem-internos
- Head SHA pedido: 464711ae378c4abf13e2d2bbb8b79e1e925825f4
- **O branch andou durante a revisão:** o `origin` está em **44c6e3bd441c4b9026c5228c736502ac89e597d6** (22:33 UTC, renomeia para `titulos_sem_internos`, "fonte única", RD-0016). Revisei os dois heads.
- Revisor: revisor-codigo · 24/11/2026

## Veredito
- **464711a: NÃO APROVADO.** 1 🟡: a mesma função existe no #50. O 44c6e3b já corrige isso.
- **44c6e3b: código APROVADO.** Fica 1 🟡 fora do PR: os testes do `testes` usam o nome antigo. Merge depois de o teste acompanhar.

Conferido:
- `bap_dados.VERSAO` = 27. Regra nova de cache = marca nova: o bloco `inadimplencia` passa de `""` para `"fi1"` em `_fontes`, e a marca entra na `_assinatura`. Só esse bloco é refeito.
- `_bloco_inadimplencia`: cada foto diária passa pelo filtro antes do `resumo_da_foto` e do cálculo de recebido/recuperado. Atraso, recebido e recuperado (farol e indicadores do Diretor, `relatorios_nucleo.py:12926-12933`) ficam sem interno, como os títulos do #50. O número do Diretor e o cartão do farol passam a sair da mesma regra. Nas bases congeladas não há título interno, então a diferença é 0 hoje.
- Função pura, com teste RN-GER-004 no PR do `testes` (`test_T0017_fotos_sem_internos`). Sem segredo e sem dado digitado.
- `verificar engenheiro-dados --base origin/main`: OK, 1 arquivo. Os 2 commits trazem `Agente: engenheiro-dados`.

## 🟡 Corrigir antes do merge
1. (464711a) `bap_dados.py:1427` `fotos_sem_internos` tem o mesmo corpo de `relatorios_nucleo.titulos_sem_internos` (#50). O 44c6e3b resolve deste lado. O outro lado é o 🟡 do #50.
2. (44c6e3b) A renomeação quebra os 3 testes de `test_T0017_fotos_sem_internos.py` (o PR do `testes`), com `AttributeError: module 'bap_dados' has no attribute 'fotos_sem_internos'`. O teste precisa passar a `bd.titulos_sem_internos`. Dono: `testes`. Não é defeito do código do #51, mas a definição de pronto pede os testes verdes no lote.

## 🟢 Sugestões
1. A docstring de `titulos_sem_internos` repete o porquê do 000040. Basta citar a RN-GER-004. O 000040 é assunto da RN-GER-005 e já está explicado no #50.
