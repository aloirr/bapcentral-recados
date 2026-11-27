# T-0054: auditoria de redundância (corretor-redundancias)

- Heads revisados (diff `origin/main...<head>`):
  - web: `modulo-web/T-0054-entregas-edicao` em `1862a53085d24681118e7e109ba4f29579116893`;
  - robô: `modulo-robo/T-0054-entregas-edicao` em `f0b895b3c2837bb4ff142d74cb55cd747a252705`;
  - desenho: `engenheiro-software/T-0054-desenho` em `ccc2e70204d1feedee51e83af9346b38051e52bd`;
  - regras: `gerente-projetos/T-0054-regras` em `b52f7457372eed3395082a256b0cec7b460a6d9a`.
- Evidência: leitura dos 4 diffs e os prints de `sim/` (edição aberta e com erro no PC e no celular, grade e cartão salvos).
- Faixa de IDs: RD-0250 a RD-0255 (todas usadas).

## Parecer: **6 achados em aberto, que seguram o lote**
- RD-0250 é média.
- RD-0251 a RD-0255 são baixas e estão em código, CSS ou teste, não só em comentário. Por isso também seguram o lote.

### Sem achado
- **Tabela de quem edita, web × robô:** `edicoes.EDITA_LUGAR` e `bap_automation.EDITA_LUGAR_WEB` têm as mesmas 3 entradas. Essa duplicação foi aceita no desenho, com o teste de igualdade.
- **Não há 4ª cópia em código:** os testes da web repetem os lugares só para conferir. Já a 3ª cópia, a do contrato, divergiu (RD-0250).
- **`EDITA` × `EDITA_LUGAR`:** não se sobrepõem. O `EDITA` é o padrão (`.get(lugar, EDITA)`), e o `EDITA_LUGAR` guarda só as exceções. No robô, o padrão é o literal `("admin",)`, que faz parte da duplicação aceita.
- **Dica da data:** "Apague a data para voltar à calculada pelo PC." aparece uma vez por tela, só na DT. PREVISTA (`SEM_CALCULO`, `test_RN_POS_011_dica_da_data_calculada_so_na_prevista`). Os prints confirmam.
- **"Aguardando o PC" na grade e "Edição enviada: aguardando o PC." na faixa de aviso (print `posvenda-entregas-salvo-pc`):** os dois ficam (`manter?`, resolvido). A faixa confirma a ação que acabou de ser feita e fica na área de avisos. A marca diz qual linha está pendente e continua depois. Isso já existia desde a T-0021 e a T-0054 não mexeu.
- **Robô:** `MOTIVO_PERFIL_WEB` e `perfil_web` são novos e únicos. Não há código morto.
- **03-regras:** a RN-POS-011 e os acréscimos à RN-GER-012, à RN-GER-018 e à RN-POS-010 não se repetem com outro texto dentro do arquivo.

### Achados

| ID | Onde | Tipo | O que se repete | Impacto | Sev. | Proposta (antes → depois) | Dono |
|---|---|---|---|---|---|---|---|
| RD-0250 | `.coord/contratos/relatorio.md:1293-1299` (§10.9.7); `docs/desenho/T-0054.md:66`, `:87` e `:136` | doc | A regra "quem edita" está escrita em 5 lugares: web, robô, contrato, desenho e 03-regras. A cópia do contrato e a do desenho divergem das outras em 3 pontos: (1) a tabela do contrato tem 2 linhas, enquanto a web e o robô têm 3, porque falta `("pl_fretes", "Notas com frete")`; (2) a assinatura escrita é `pode_editar(perfil, rid, tabela)`, mas o código tem `pode_editar(perfil, lugar)`; (3) a RN-POS-011 citada no desenho (§4) e o P2 ("padrão: não, o Fretes fica só do admin") contradizem a RN-POS-010/011 do 03-regras, que dá o Fretes ao pós-venda. O teste "web = robô = contrato" vai acusar diferença. | manutenção, decisão | média | Contrato §10.9.7: acrescentar a linha <code>\| `("pl_fretes", "Notas com frete")` \| `admin`, `pos_venda` (RN-POS-010; vale quando o lugar entrar em `LUGARES`/`EDICOES_WEB`) \|</code> e trocar `pode_editar(perfil, rid, tabela)` por `pode_editar(perfil, (rid, tabela))`. Desenho: o §4 passa a remeter ao 03-regras, sem copiar o texto: "Texto da RN-POS-011: `docs/produto/03-regras.md` (fonte da verdade)." O §5.3 também troca a assinatura para `pode_editar(perfil, (rid, tabela))`. Na linha P2 do §6, a coluna "Padrão adotado" fica assim: "sim (P2 A do R-20261127-103925-alexandre; RN-POS-010)". | engenheiro-software |
| RD-0251 | `web/app/main.py:653,660,661,663,665` e `web/app/templates/_grade.html:36`; comentários em `web/app/edicoes.py:1`, `web/app/main.py:648`, `web/app/static/estilo.css:342` e `web/app/templates/_grade.html:3` | código | A troca de `admin` por `pode` ficou pela metade. A `dica` recebe `pode`, mas quem chama ainda guarda o resultado de `pode_editar` em `admin` (5 usos) e o entrega como `"admin"` ao template (`ed.admin`). Os comentários continuam dizendo "só admin" ou "(admin)". | manutenção | baixa | `main.py`: `admin = edicoes.pode_editar(...)` → `pode = edicoes.pode_editar(...)`, com as linhas 660, 661 e 663 usando `pode`. Na linha 665, `{"cab": ..., "admin": admin}` → `{"cab": ..., "pode": pode}`. `_grade.html:36`: `ed.cab if ed.admin else "Edição"` → `ed.cab if ed.pode else "Edição"`. Comentários: `edicoes.py:1` "só do perfil admin" → "por perfil e lugar (RN-GER-012, RN-POS-011)"; `main.py:648` "(admin com chave)" → "(quem edita, com chave)"; `estilo.css:342` "(só admin)" → sai; `_grade.html:3` "(admin)" → sai. | modulo-web |
| RD-0252 | `web/app/edicoes.py:49` (`perfis_do_rid`) | código | `tuple(dict.fromkeys(...)) + EDITA` tira as repetições antes de somar o `EDITA`. Assim, para o `pl_entregas` o resultado é `("admin", "pos_venda", "admin")`: o admin sai 2 vezes. | manutenção | baixa | `return tuple(dict.fromkeys(...)) + EDITA` → `return tuple(dict.fromkeys([p for (r, _t), ps in EDITA_LUGAR.items() if r == rid for p in ps] + list(EDITA)))` | modulo-web |
| RD-0253 | `web/app/templates/editar.html:27,32,35,38,40` | código | O trecho `{% if c.invalido %} aria-invalid="true"{% endif %}` está copiado 5 vezes, uma em cada tipo de campo, e em posições diferentes da tag. | manutenção | baixa | Logo depois do `<label class="ed-campo...">`, criar uma vez `{% set inv = ' aria-invalid="true"'\|safe if c.invalido else '' %}`. Nas 5 tags, trocar o trecho por `{{ inv }}`, sempre logo depois do nome da tag (`<select{{ inv }} name=...>`, `<input{{ inv }} type=...>`, `<textarea{{ inv }} ...>`). O teste `test_RN_POS_011_erro_devolve_...` procura `<input type="text" aria-invalid="true" name="c_responsavel"`: o regex passa a ser `<input aria-invalid="true" type="text" name="c_responsavel"`. | modulo-web |
| RD-0254 | `web/app/static/estilo.css:610` | código | `.bc3-ed .ed-marca{display:inline-block;margin:0}` repete o `display:inline-block` que a `.ed-marca` (`:346`) já tem. E dentro do `.bc3-ed`, que agora é `display:flex`, esse `display` não tem efeito. | manutenção | baixa | `.bc3-ed .ed-marca{display:inline-block;margin:0}` → `.bc3-ed .ed-marca{margin:0}` | modulo-web |
| RD-0255 | `web/tests/test_T0054_entregas_edicao.py:127-128` × `web/tests/test_T0036_analista.py:353` | teste | O caso `VERSAO == "0.12.0"` é testado duas vezes. O teste da T-0036 já confere o mesmo valor e ainda confere o `/saude`. | manutenção | baixa | Apagar `test_T0054_versao` inteiro. O `test_T0036_versao_nova_no_saude` continua como o único teste da versão. | modulo-web |

### Fora do meu escopo (vai ao revisor-codigo, sem catálogo)
- `main.py:675` (`novo_tela`) e o `GET ...?novo=1` passaram a usar `pode_editar`. Por isso, a regra "linha nova só do admin" (contrato §10.9.7) depende agora de o pacote não trazer `edicao.novo` nas Entregas e no Fretes. É uma questão de regra, não de redundância.

## Para fechar
- **RD-0250** (engenheiro-software): um commit no `T-0054-desenho`.
- **RD-0251 a RD-0255** (modulo-web): no mesmo PR da web.
- **Reteste:** heads novos com `pytest web/tests/test_T0054_entregas_edicao.py web/tests/test_T0021_edicao.py web/tests/test_T0036_analista.py` verde, mais a leitura do diff.
- O catálogo (`docs/redundancias/catalogo.md`) não foi atualizado: esta rodada foi feita sem commit, a pedido do gerente.

## Reteste: web `c9feadb0859c54dad7fca468576200b122351675`, desenho e contrato `4c0a990d715fa05f6ee20e7925b093e2005bb370`, robô `f0b895b` sem mudança (27/11/2026)

- Escopo: os diffs `1862a53..c9feadb` (web) e `ccc2e70..4c0a990`, só `docs/desenho/T-0054.md` e §10.9.7. O resto desse intervalo é o merge do `main`.
- Evidência: `pytest web/tests/test_T0054_entregas_edicao.py web/tests/test_T0021_edicao.py web/tests/test_T0036_analista.py` no `c9feadb`: 88 passaram. Também li os diffs.

| ID | Situação | Evidência |
|---|---|---|
| RD-0250 | **fechado** | A tabela do §10.9.7 tem as 3 linhas, iguais às da web e do robô. A assinatura ficou `pode_editar(perfil, lugar)`, com `lugar = (rid, tabela)`, no contrato e no desenho §5. O §4 do desenho só remete ao 03-regras, sem copiar o texto. O P1 e o P2 do §6 estão "decididos: A". |
| RD-0251 | **fechado** | `pode` em `main.py:653-665` e `ed.pode` em `_grade.html:36`. Não sobrou `ed.admin`. Os comentários de `edicoes.py:1`, `main.py:648`, `estilo.css:342` e `_grade.html:3` foram alinhados. |
| RD-0252 | **fechado** | `perfis_do_rid` usa `dict.fromkeys([...] + list(EDITA))`, então o admin sai uma vez só. |
| RD-0253 | **fechado** | `{% set inv %}` aparece uma vez por campo e é usado nas 5 tags. O regex do teste continua passando. |
| RD-0254 | **fechado** | A regra `.bc3-ed .ed-marca` saiu inteira. Ela também levava o `margin:0`, então agora a marca do cartão no celular soma o `margin-left:.3rem` da `.ed-marca` ao `gap:.5rem`. Isso é espaçamento, não redundância: fica com o designer-ux, sem ID. |
| RD-0255 | **aberto (resíduo)** | `test_T0054_versao` saiu, mas ficaram 3 linhas em branco entre `test_RN_GER_018_farol_liberado_nao_da_edicao` e `test_RN_POS_011_formulario_diz_a_nota_e_o_cliente` (`web/tests/test_T0054_entregas_edicao.py:125-127`). Antes → depois: 3 linhas em branco → 2. Baixa, modulo-web. O caso é o mesmo do resíduo do RD-0239 (T-0052). |

### Novo
- **Sem achado novo de redundância.**
  - A troca de `--alerta` por `--erro` no `.ed-campo [aria-invalid]` e no `.ed-erro` usa o token da marca, que já existia no `main`. Os dois tokens terem o mesmo valor (`#B42318`) vem de antes do lote e não é da T-0054.
  - O `--erro` do pedido não mexeu em texto de tela.
- Encaminhado, sem catálogo:
  - O comentário de `novo_tela` (`main.py:671`) agora diz "só quem edita o lugar", e o contrato §10.9.7 diz "a linha nova continua só do admin". É a regra da linha nova, que vai ao revisor-codigo, como já estava encaminhado.
  - No desenho §5, a branch (`T-0054-edicao-posvenda`) e o nome do teste (`test_T0054_edicao_posvenda.py`) não são os reais (`T-0054-entregas-edicao`, `test_T0054_entregas_edicao.py`). Na linha 6, falta a vírgula em "RN-GER-018 RN-POS-010". As duas coisas são exatidão do documento, não repetição.

### Parecer do reteste
- **1 achado em aberto:** RD-0255 (resíduo), baixa, em arquivo de teste e não só em comentário ou título. Pela regra de liberação, segura o lote até as 3 linhas em branco virarem 2.
- O desenho e o contrato (`4c0a990`) e o robô (`f0b895b`) estão liberados quanto a redundância.
