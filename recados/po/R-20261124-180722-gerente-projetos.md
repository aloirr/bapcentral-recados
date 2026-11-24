---
id: R-20261124-180722-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: alta
tarefa: T-0017
responde_a: R-20261124-175008-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T18:07:22-04:00
---
# T-0017: simulação do Farol de Inadimplência pronta (PC × site) e 3 decisões

## Simulação (PNG, "Simule" = mostrar antes)
Anexos em `recados/anexos/T-0017/` (repositório de recados):
- `inadimplencia_pc_x_site.png` — PC (tela real do BAP Central) à esquerda × site à direita, mesmas bases, NOV/2026.
- `inadimplencia_site_computador.png` (1366 px), `inadimplencia_site_celular.png` (390 px), `inadimplencia_site_filtro_AM.png` (filtro AM).
- `inadimplencia_pc_tela.png` — a tela do PC sozinha.
Nos prints os vendedores aparecem como "Vendedor 01..08" e as frases de cliente do PC estão cobertas (regra 6: sem nome em print de recado). No site de verdade, com o "2 A", aparece o nome do vendedor; nome de cliente e CNPJ nunca.

## Número bate com o PC (testes, valor × regra)
| Cartão | PC | Site |
|---|---|---|
| Em atraso | R$ 400.388 (329 títulos · 136 clientes) | igual |
| Inadimplência | 65% de R$ 619.706 | igual |
| A vencer em 7 dias | R$ 54.410 (44) | igual |
| Acima de 90 dias | R$ 269.327 (67%) | igual |
| Atraso médio | 133 dias | igual |
| Recuperado no mês | R$ 65.988 | igual |
| AM (5 cartões) | R$ 92.893; 67% de R$ 139.502; R$ 9.522; R$ 83.225; 124 dias | iguais |
Soma dos estados = total (R$ 400.387,79; a diferença de R$ 1 era arredondamento). Todos os títulos caem num estado.

## Achado corrigido de carona (regra 8)
O Farol de Inadimplência do PC não tirava CNPJs internos nem a conta 000040 (RN-GER-004/005). Hoje não muda número (0 títulos assim), mas foi corrigido (modulo-farois, branch modulo-farois/T-0017-inadimplencia-internos) e entra no mesmo lote.

## Como fica no site
Cartões com as barrinhas por estado, Resumo gerencial e os gráficos; filtro por estado muda só os cartões, com o aviso "Cartões: AM. Resumo e gráficos: BAP inteira."; "Recuperado no mês" mostra "só na BAP inteira" no filtro. Nada grava no site (sem e-mail, WhatsApp ou edição). Revisões: designer-ux 🟢 (head 9211d8b), números conferidos pelo testes.

## Decisões para o Alexandre (resposta pronta "N X")
1. Simulação do Farol de Inadimplência: (A) aprovada, abrir os PRs (robô, site, contrato, testes e o ajuste dos internos); (B) ajustar antes (diga o quê). Recomendo A. Resposta: "1 A".
2. Formato dos cartões no site: (A) manter como na simulação (cartões com tamanhos diferentes: os 2 com barrinhas ocupam mais espaço); (B) cartões todos do mesmo tamanho, como no Painel já no ar, com as barrinhas embaixo. Recomendo A agora e B numa entrega de acabamento. Resposta: "2 A".
3. Registro dos pareceres: os revisores rodam dentro da sessão do gerente e o coord.mjs só aceita o remetente da sessão; hoje o gerente grava o parecer deles com a nota de origem. (A) seguir assim; (B) abrir tarefa de governança para o coord.mjs aceitar o papel do subagente (precisa do "autorizo" no PR). Recomendo A por ora. Resposta: "3 A".

## Depois do "1 A"
PRs na ordem: contrato → site (deploy da web antes do robô) → robô → testes (2º PR) → internos. Merge com CI verde e pareceres. Depois: "aprovo deploy v0.2.0" (site) e "instale" do bap_automation.py (robô no notebook). Em seguida, Farol de Pedidos (previsão 26/11).
