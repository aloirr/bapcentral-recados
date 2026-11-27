---
id: R-20261127-041434-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0033
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T04:14:34-04:00
---
# Entrega: T-0024 (lote 2), T-0033 (revisão geral) e T-0034 (página inicial) no ar, web 0.5.0

Entrega de três tarefas, todas no main e no ar. O site está na versão 0.5.0 e o /saude responde ok.

## T-0024: faróis do lote 2 no site
PRs: #89 web, #91 robô, #97 testes.
- Faróis novos: Painel de indicadores, Farol de Clientes, Roteirização, Giro de Produtos e Estoque FRW.
- Cada perfil vê os faróis do seu quadrado do PC. O diretor vê só o Resumo.
- Os dados aparecem no site no primeiro pacote do robô depois que a rotina diária instalar o robô novo (a próxima é às 06h30; ela pede o commit com 2 h no main).

## T-0033: revisão geral de todos os faróis
PRs: #127, #138, #139, #140, #135, #143, #144, #145.
- Todos os faróis no visual BC3 (PC) e M3 (celular), com a marca do manual: logo inteiro, "BAP AUTOPARTS", cores e fonte Inter.
- Grade de até 10 colunas, com o resto da linha num popup. Páginas de 500 linhas.
- Com filtro ou estado, os cartões da aba saem e entra o aviso "Cartões sem filtro…".
- Cor da Aderência pela RN-VIS-001: verde a partir de 80%, amarelo de 50% a menos de 80%, vermelho abaixo de 50%.
- Saiu o botão verde "Cobrar no WhatsApp". A aba continua.

## T-0034: página inicial
PR: #146, web 0.5.0.
- Ao entrar, admin, diretor e gerente abrem no Painel Executivo. Pré-venda, pós-venda e vendas abrem no 1º farol da área.
- Login, Trocar senha, Usuários (Desativar com confirmação) e Parcial passam ao novo visual.

## Como testar em 5 passos
1. Entre como diretor: abre o Painel Executivo. A faixa mostra a data, "13 de 19 DU" e os 3 números principais. Os outros cartões trazem o valor e a comparação de out, set e jul.
2. Entre como pré-venda: abre direto o Farol de Pedidos.
3. No Farol de Pedidos a 1366, a grade não rola para o lado. Clique numa linha para ver o popup com todas as colunas.
4. Escolha o estado PA: os cartões da aba saem e aparece "Cartões sem filtro. Com filtro, veja as linhas na tabela.".
5. No celular, o Farol de Visita mostra 3 abas mais "Mais ▾". Em Aderência dia a dia, as cores seguem 80/50.

## Ficou para depois
- **T-0046:** limpeza interna da web, o texto do aviso de cartões e a faixa vazia em 2 abas do Visita. Esta última já acontecia antes.
- **T-0047:** cores das faixas do PC, do robô e do site no manual, com as decisões de cor já tomadas (R-20261127-010314).
