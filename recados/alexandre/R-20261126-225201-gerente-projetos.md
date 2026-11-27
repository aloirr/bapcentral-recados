---
id: R-20261126-225201-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: normal
tarefa: T-0024
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-26T22:52:01-04:00
---
# T-0024: simulação dos 5 faróis do lote 2 no site — aprovação

# T-0024: simulação dos 5 faróis do lote 2 no site — aprovação

Faróis: Indicadores, Clientes, Roteirização, Giro de produtos e Estoque FRW. Visual BC3 no PC e M3 no celular, no formato do Farol de Pedidos. O diretor vê só o Resumo. Dados fictícios, com as abas, colunas e cartões REAIS de cada farol (tirados do pacote do robô).

Imagens em `recados/anexos/T-0024/`:

| Imagem | O que mostra |
|---|---|
| admin-pv_indicadores-resumo-1366 | Indicadores · Resumo (cartões com Dia, Semana e Mês, sem rolagem) |
| admin-vc_base-resumo-1366 | Clientes · Resumo |
| admin-vc_base-aba7-clientes-1366 | Clientes · tabela, com no máximo 10 colunas e o resto no popup |
| admin-vc_base-aba7-clientes-390 | a mesma tabela no celular (lista que abre) |
| admin-vc_planner-aba6-por-cliente-1366 | Roteirização · Por cliente |
| admin-pl_giro-aba3-popup-1366 | Giro · Necessidade de compra, com o popup aberto |
| admin-pl_frw-aba0-estoque-frw-1366 | Estoque FRW |
| diretor-pl_giro-resumo-1366 e diretor-vc_planner-resumo-1366 | o diretor só no Resumo |

**Conferido:**
- o designer-ux revisou em 3 rodadas (abas que quebravam, gráficos repetidos e cortados, coluna de ação fora da tela, números incoerentes, nome repetido); está tudo corrigido;
- o PC cabe numa tela a 1366×768, sem rolagem para o lado;
- 331 testes da web passam;
- a Roteirização vai sem filtro por estado, com o aviso, porque o PC não tem esse filtro nela;
- a Base de clientes por estado bate com o PC.

**Fica para a T-0033, que vale para todos os faróis:**
- o logo e as cores do manual aprovado. Aqui ainda aparece o quadrado verde, que sai na T-0033;
- colunas repetidas que vêm do robô (VD/DIA e VENDA/DIA).

**Ordem do merge, depois do seu "ok":**
1. PR de testes que destrava o CI.
2. #89 (web).
3. #91 (robô).
4. #97 (testes).

O robô novo NÃO pode chegar antes da web nova: a web atual recusaria o pacote inteiro e congelaria o site.

## Decisão
1. Simulação da T-0024: (A) aprovada, seguir com os PRs na ordem acima · (B) ajustar antes (diga o quê).
