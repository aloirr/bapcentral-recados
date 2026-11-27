---
id: R-20261127-131554-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: alta
tarefa: T-0056
responde_a: R-20261127-104041-gerente-projetos
encerra: false
contrato: null
criado_em: 2026-11-27T13:15:54-04:00
---
# T-0056 no main: texto do "instale" para o Alexandre

**No main:** #193 (testes, c34e0b0) e #187 (código, 8ce110632261ecbcba981c34e07fd0dd0a57e23a). Revisor de código e corretor aprovados; CI verde.

**O que muda no PC:** a rotina das 06h30 passa a instalar o commit mais novo do main que já tem 2 h, em vez de desistir do dia quando o último commit é recente. As outras travas continuam (CI verde, versão do site, janela 06h00–07h30 com o robô parado, "instalado por fora", pausa). O arquivo que muda é o `atualizar_do_github.py`, que só entra no PC com o "instale" (ADR 0002).

**Texto exato para o Alexandre mandar (se concordar):**
> instale o PR #187 no commit 8ce110632261ecbcba981c34e07fd0dd0a57e23a

**Como instalar, no notebook do robô (depois da frase):**
1. Parar o robô.
2. Na MESMA pasta de onde o robô roda, dar dois cliques em ATUALIZAR_DO_GITHUB.bat (modo manual: baixa o main, faz o backup e troca os .py/.bat, inclusive o atualizar_do_github.py novo).
3. Se aparecer aviso ("instalado por fora" ou outro), mandar só a frase do aviso.
4. Mandar as 3 últimas linhas de SISTEMA BAP\LOGS\atualizacao_diaria.log.
5. Religar o robô; na rodada seguinte o /saude deve mostrar mais de 5 faróis.

## Decisões que o Alexandre precisa tomar
- O "instale" acima. Recomendação: sim; é o que destrava o robô do notebook (faróis novos e a edição de Entregas no site). Sem efeito no prazo das outras tarefas.
