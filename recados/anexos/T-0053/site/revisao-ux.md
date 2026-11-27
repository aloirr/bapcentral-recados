# T-0053 · Revisão de tela (designer-ux) · Farol de Pedidos no SITE

- **Head revisado:** `b56f121` (`modulo-farois/T-0053-cadastro-do-pedido`, só `relatorios_nucleo.py`).
- **Antes:** `relatorios_nucleo.py` do `main` `6ebdb6f`.
- **Site:** `web/` do `main` `6ebdb6f`.
- **Dados:** fixture fictícia do autor (códigos 900001 a 900004, nomes "CLIENTE FICTICIO …"). Usuário `admin.sim` fictício. Nenhum dado real.

## Como foi gerado

O pacote seguiu o caminho do robô até a web, nesta ordem:

1. `bap_automation.coletar_relatorios_web(2026, 11)`, com `FAROIS_WEB=("pv_pedidos",)` e o `montar` real sobre o `Contexto` da fixture;
2. `montar_pacote_web` e `_cortar_pacote_web`;
3. `POST /api/pacote` no FastAPI do `main` (`BAP_WEB_DADOS` em pasta temporária), pelo `web/simular_farol.paginas`;
4. Playwright (Chromium) a 1366 px e a 390 px, `locale pt-BR`, fuso America/Manaus, escala 2.

Os cartões dos pedidos foram fotografados de dois jeitos:
- no computador, com o pop da linha (o foco no número do pedido);
- no celular, com o cartão aberto.

O `vc_painel` de teste do robô não passa no esquema da web, então ficou fora do pacote. Isso não afeta o Farol de Pedidos.

## Arquivos

Cada arquivo existe em `antes_` e `depois_`.

| Tela | Computador (1366) | Celular (390) |
|---|---|---|
| Pedidos, visão BAP | `*_pedidos_BAP_pc.png` | `*_pedidos_BAP_cel.png` |
| Pedidos, visão BAP: pedido 000001 (filial RR, código com loja RR e AM) | `*_pedidos_BAP_pc_cartao_000001.png` | `*_pedidos_BAP_cel_cartao_000001.png` |
| Pedidos, visão BAP: pedido 000005 (2 lojas AM com nomes diferentes) | `*_pedidos_BAP_pc_cartao_000005.png` | `*_pedidos_BAP_cel_cartao_000005.png` |
| Pedidos, filtro RR | `*_pedidos_RR_pc.png` | `*_pedidos_RR_cel.png` |
| Pedidos, filtro RR: cartões 000001 e 000004 | `*_pedidos_RR_pc_cartao_*.png` | `*_pedidos_RR_cel_cartao_*.png` |
| Resumo, visão BAP | `*_resumo_BAP_pc.png` | `*_resumo_BAP_cel.png` |

**"Crédito a analisar" não existe no site.** A tabela Pedidos vai como `enxuta` e por isso sai sem recortes (`recortes_em_linhas` devolve lista vazia). O pacote não tem `recortes_linhas`, nem antes nem depois. Não há tela para fotografar.

## A linha corrigida

| Pedido | Antes (main) | Depois (b56f121) |
|---|---|---|
| 000001, filial BOA VISTA | LOJA AM · AM · MANAUS · limite R$ 80.000 · "Com Limite" | LOJA RR · RR · BOA VISTA · limite R$ 20.000 · DISP./ATRASO vazios · "Crédito não apurado" |
| 000005, filial MANAUS | FICT A · AM · MANAUS · R$ 9.000 · "Com Limite" | "(loja não identificada)" · AM · sem cidade e sem limite · "Crédito não apurado" |
| 000004, filial BOA VISTA (o código só tem 1 loja, em AM) | UNICO AM · AM | igual (HERDA_LOJA_UNICA) |
| 000006 (sem cadastro) | "CLIENTE FICTICIO" · "Sem Limite" | igual |

Larguras medidas:
- nenhuma página passa da tela (`scrollWidth` = 1366 e 390, antes e depois);
- no celular, "(loja não identificada)" e "Crédito não apurado" cabem numa linha só (altura 18 px na coluna de 214 px do cartão);
- no computador, "(loja não identificada)" cabe na coluna RAZÃO SOCIAL;
- no computador, ANÁLISE CRÉDITO é coluna oculta e aparece só no pop da linha, onde também cabe.

## Parecer

**Nenhum 🔴.** Marca, nome "BAP AUTOPARTS", paleta e largura no celular estão iguais ao `main`, e nenhum número do Diretor mudou. Ficam 2 🟡 para corrigir antes do merge e 3 🟢.

### 🟡 1. No celular, o cartão do pedido sem loja perde o nome do cliente
- **Tela:** Farol de Pedidos › Pedidos, celular (`depois_pedidos_BAP_cel.png`, pedido 000005).
- **O problema:** o título do cartão no celular usa a coluna FANTASIA (`web/app/tabelas.py`, `GRADE[("pv_pedidos","Pedidos")]["cel"]`). O `cadastro_do_pedido` devolve `fantasia=""` quando a loja não é identificada. Antes o cartão mostrava "000005 FICT A"; agora mostra só "000005", sem cliente. O aviso "(loja não identificada)" só aparece com o cartão aberto. É uma regressão desta mudança. O gerente que bate o olho na lista não vê que aquele pedido está sem loja.
- **Regra quebrada:** hierarquia (o principal primeiro) e estado vazio.
- **Correção proposta, neste PR (modulo-farois):** quando a loja não é identificada, `cadastro_do_pedido` devolve em `fantasia` o mesmo texto de `nome`. Pode ser `LOJA_NAO_IDENTIFICADA` ou o nome comum das lojas. Assim o título do cartão fica "000005 (loja não identificada)", que cabe na linha a 390 px. No computador a FANTASIA é oculta, então nada se repete na grade.

### 🟡 2. "Crédito não apurado" fora do padrão dos outros valores da coluna
- **Tela:** ANÁLISE CRÉDITO, no pop do computador e no cartão do celular (`depois_pedidos_BAP_*_cartao_000001/000005.png`).
- **O problema, em duas partes:**
  - **Caixa:** os vizinhos da coluna estão em Caixa de Título: "Com Limite", "Sem Limite", "Com Limite Parcial", "Com Limite, mas em Atraso". "Crédito não apurado" é o único em caixa de frase.
  - **Redundância:** a palavra "Crédito" repete o título da coluna (ANÁLISE CRÉDITO). Os outros valores não repetem: dizem só o estado do limite.
- **Clareza para o gerente:** "não apurado" é melhor que um falso "Sem Limite" e está certo no sentido. Mas no 000001 o pop mostra LIMITE R$ 20.000 ao lado de "Crédito não apurado", e o que falta ali é o saldo daquela loja. O texto curto e neutro serve aos dois casos: sem loja (000005) e loja sem saldo (000001).
- **Correção proposta:** `CREDITO_NAO_APURADO = "Não Apurado"`. Fica curto, na caixa da família e sem repetir o título. Se o po preferir dizer o motivo, a alternativa é "Saldo Não Apurado", que também cabe numa linha a 390 px.
  - Na tabela "Pedidos em aberto" (`pedidos_em_aberto`, valores em CAIXA ALTA como "SEM LIMITE" e "CLIENTE EM ATRASO"), o `.upper()` continua certo: "NÃO APURADO".
  - Mudar o texto pede o mesmo ajuste nos testes que citam o valor.

### 🟢 3. "(loja não identificada)": manter como está
- Em minúscula e entre parênteses, o texto se distingue de uma razão social de verdade, que sempre vem em CAIXA ALTA e sem parênteses. Segue o padrão de marcador do próprio núcleo, como "(sem acompanhamento)".
- Cabe na coluna nas duas larguras, e a mensagem é clara: o cliente existe e a loja não foi achada.
- Sem mudança. Só vale garantir a 🟡 1 para que o texto apareça também no título do cartão do celular.

### 🟢 4. Linha âmbar sem o motivo visível no computador
- Os pedidos 000001 e 000005 passaram a ter fundo âmbar (`tons` = "atencao", porque o crédito ≠ "Com Limite"). No computador, a coluna ANÁLISE CRÉDITO é oculta, e o motivo só aparece no pop. O 000006 ("Sem Limite") já era assim no `main`, então não é regressão.
- Proposta para depois (modulo-web): mostrar ANÁLISE CRÉDITO na grade do computador quando o valor for diferente de "Com Limite". Assim a cor deixa de ser a única pista.

### 🟢 5. Filtro RR com linha de UF AM (pergunta ao po, não é de tela)
- Em `depois_pedidos_RR_pc.png`, o pedido 000004 é da filial BOA VISTA e mostra UF AM, porque o código tem uma só loja (AM) e vale a `HERDA_LOJA_UNICA` ([SUPOSIÇÃO] do modulo-farois). Isso já acontecia no `main`.
- O 000001 foi corrigido para RR.
- Vale o po confirmar a suposição com o Alexandre, porque a regra 8 diz "estado = filial da nota".

### Resumo, visão BAP
- O "Resumo gerencial" passa de "1 pedido(s) em aberto com pendência de crédito (R$ 400)" para "3 … (R$ 2.600)", porque os não apurados agora contam como pendência. Está coerente com a RN-GER-019.
- Os cartões do topo não mudam (Pedidos 6, R$ 63.500, Volume 60).
- Sem achado de tela.
