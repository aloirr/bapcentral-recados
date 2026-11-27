---
id: R-20261127-192550-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0058
responde_a: R-20261127-172918-alexandre
encerra: true
contrato: null
criado_em: 2026-11-27T19:25:50-04:00
---
# Entrega T-0058: faturado por estado desconta toda a devolução da filial

No recorte por estado, o Farol de Pedidos e o Saldo passam a descontar toda a devolução da filial, inclusive a de vendedor sem venda no mês (RN-GER-002: faturado = VND − DEV pela data da NF). Só o PA muda: AGO/26 46.799 → 33.834 e SET/26 54.624 → 48.166. Com isso, cada estado bate com o Painel. O TOTAL não muda.

## No main
- #217 (modulo-farois: recorte por filial) → ee987e8
- #224 (modulo-robo: o recorte por estado da web usa o mesmo filtro) → 727af92
- #220 (testes RN-GER-002, inclusive o da web) → 5d1b358
- #221 (simulação aprovada pelo PO, R-20261127-180616-po) → 135e379

Pareceres: revisor-codigo aprovado e corretor-redundancias sem achado em cada PR; CI verde em cada head.

## Instalação
A rotina diária das 06h30 de 28/11 instala sem precisar de "instale". Na web, o número por estado corrige quando o robô novo publicar o pacote de 28/11.

## Como testar em 5 passos
1. Amanhã, depois das 06h30, confira no atualizar_do_github.log que o relatorios_nucleo.py e o bap_automation.py foram instalados.
2. No PC, abra o Farol de Pedidos de AGO/26, recorte PA: faturado R$ 33.834.
3. Abra o Painel do Diretor de AGO/26 e veja o PA: R$ 33.833,74, que é o mesmo número com centavos.
4. Repita em SET/26, PA: R$ 48.166 no farol e R$ 48.166,49 no Painel.
5. Depois do pacote do robô de 28/11, abra o Farol de Pedidos na web, recorte PA de AGO/26: R$ 33.834.
