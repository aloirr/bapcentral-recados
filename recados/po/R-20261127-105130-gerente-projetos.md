---
id: R-20261127-105130-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: alta
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:51:30-04:00
---
# RETOMADA — estado na pausa (27/11, 10h55)

# RETOMADA — estado na pausa (27/11, ~10h55 Manaus)

O limite semanal está em 93% e volta em 03/12 às 17h. A partir de agora não começo trabalho longo novo. Os agentes que já estão rodando terminam o que estão fazendo. Main: **7f8d980**. Web no ar: **0.10.0** (T-0050).

## Entrou no main hoje (depois das 09h)
- #173: RN-GER-018 (T-0050)
- #163: contrato §10.9 e §10.10 (T-0023)
- #166: testes da nuvem (T-0045)
- #174 e #175: desenho e web 0.10.0 (T-0050). Entregue.
- #176: governança única (T-0045)
- #181: testes do Painel (T-0052)
- #178: RN-POS-011 (T-0054)

## Frentes abertas: branch, SHA e próximo passo
| Tarefa | Situação | Branch · SHA | Próximo passo |
|---|---|---|---|
| **T-0052** Painel Executivo | aprovada pelo po; revisor de código sem 🔴; UX reconfirmando no head final | PR #182 `modulo-web/T-0052-painel-cartoes` · 73dbbbe · CI verde | UX "ok no 73dbbbe" → merge do #182 → /saude 0.10.1 → entrega |
| **T-0053** Farol de Pedidos (cliente da loja certa) | aprovada com condições, já cumpridas (UX e marca ok); o revisor de código barrou o b56f121 | regras PR #180 · e2364d5; código `modulo-farois/T-0053-cadastro-do-pedido` · b56f121, com o commit novo em curso; testes `testes/T-0053-cadastro-do-pedido`, em curso | modulo-farois limita o escopo à família do Farol de Pedidos e aplica os 🟡 → testes → revisor de código e corretor no head final → PRs (#180 → testes → faróis) |
| **T-0054** Entregas com edição (pós-venda) | aprovada com 2 condições (print final e marca, em curso) | desenho PR #179 · ccc2e70, com o merge do main em curso; web `modulo-web/T-0054-entregas-edicao` · 1862a53; robô `modulo-robo/T-0054-entregas-edicao` · f0b895b; testes, em curso | marca e print → revisor de código e corretor (em curso) → PRs: #179 → web 0.12.0 → robô → testes |
| **T-0056** rotina das 06h30 instala o commit maduro | código pronto | `engenheiro-software/T-0056-commit-maduro` · 9b2b35c, CI vermelho até o testes ajustar 1 teste | testes (16 casos em `docs/desenho/T-0056.md`) → revisor → PR → **"instale" do Alexandre** |
| **Robô do notebook antigo** (por isso o admin não edita) | o site recebe só 5 faróis | — | **Alexandre:** rodar `ATUALIZAR_DO_GITHUB.bat` no notebook, com o robô parado, e mandar as 3 últimas linhas de `SISTEMA BAP\LOGS\atualizacao_diaria.log`. Depois, conferir no /saude se aparecem mais de 5 faróis |
| **T-0045** visitas pela nuvem | governança no main (#176) | — | **Alexandre:** colar a frase do R-20261127-102456 numa sessão BapCentral-Governanca. Depois, merge do PR dele → 4 passos do Render → modulo-robo `nuvem/visitas/` → Dockerfile → testes → diagnóstico |
| **T-0036** faróis do Analista | testes v2 com o merge do main e o pacote medido como o robô (em curso) | PR #177 `testes/T-0036-testes-v2` · 102d879; robô PR #159 · c8209a1 (colunas duplicadas corrigidas) | CI do #177 → merge → revisor do delta do robô → update do #159 → merge → entrega |
| **T-0023** PC só leitura (Garantias, Devoluções, NCC) | revisor de código no 327a294: 0 🔴, 2 🟡 (testes; corpo de gravação apagado, que aceitei) | `modulo-farois/T-0023-pc-so-leitura` · 327a294; testes em curso | testes → adendo do desenho (engenheiro) → corretor → PRs → fechar o #105 → entrega |
| **T-0037** Farol de Fretes | aprovada; web e testes finais prontos | #169 testes · ccb7950; #170 contrato · bcb5582; web `modulo-web/T-0037-fretes` · 0f941d5 (0.11.0); faróis · 94c6391; robô · 5d13276 | merge do main no robô e nos faróis → revisor de código e corretor nos heads finais → #169 → #170 → web → faróis → robô |
| **T-0055** porta só de leitura | plano enviado (R-100915) | — | desenho depois da T-0052, T-0053 e T-0054 |
| **T-0025 v2** | não começou | PRs antigos #93, #98, #100 e #107 | rever na retomada |

## Decisões de hoje já aplicadas
- T-0045: opção B (nuvem), com o mesmo login da Máxima do notebook.
- T-0052: faixa do topo sem os 3 números.
- T-0053: P1 A ("Saldo Não Apurado", que entra em crédito a analisar). Escopo limitado à família do Farol de Pedidos.
- T-0054: P1 A (o gerente não edita) e P2 A (o pós-venda também edita "Notas com frete").
- T-0036: o teste mede o pacote como o robô mede (15,0 MiB, dentro da margem).
- T-0037: COR_PC pela opção (C) do design-de-marca.

## Pendências do Alexandre
1. `ATUALIZAR_DO_GITHUB.bat` no notebook e as 3 linhas do log. É o que destrava a edição no site.
2. A frase da governança T-0045 e os 4 passos do Render.
3. O "instale" da T-0056, quando o PR sair.
4. Governança futura: a lista de falhas conhecidas do agente testes ganha "Farol DDR (3x)" e "recorte de vendedor do Clientes", que já falham no main.

## Na retomada
Ler este recado, `node scripts/coord.mjs caixa gerente-projetos` e os PRs abertos; seguir a coluna "Próximo passo".
