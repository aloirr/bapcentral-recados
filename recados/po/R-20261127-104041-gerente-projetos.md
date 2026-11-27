---
id: R-20261127-104041-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: alta
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:40:41-04:00
---
# Admin sem edição no Entregas: robô do notebook está antigo (5 faróis); como destravar hoje e T-0056

**O admin não consegue editar o Farol de Entregas: causa provável e o que fazer.** Recebi também as decisões do R-20261127-103925-alexandre: T-0053 P1 A, T-0054 P1 A e T-0037 P2 A. Elas entram nas tarefas.

## Causa provável: o robô do notebook está numa versão antiga
- O `/saude` do site (10h39 de hoje) mostra que o último pacote do robô, das **10h36**, trouxe **só 5 faróis**. O robô do main manda uns 17, com Garantias, Devoluções, NCC, Indicadores, Clientes, Giro etc.
- O pacote de ontem às 21h06 também tinha 5 faróis. Portanto o robô do notebook não foi atualizado nas últimas rotinas das 06h30.
- A edição no site depende da parte "edição" que o robô novo põe no pacote. O botão "Editar" só aparece quando essa parte vem, e o robô antigo não a manda. É o caso 1 que o modulo-web descreveu: o pacote chega sem a edição, e não aparece a coluna "Editar" nem para o admin.

## Por que a rotina das 06h30 não instalou (hipótese forte)
- A rotina só instala se o **último commit do main tiver 2 h ou mais**. Às 06h30, o main teve merges na madrugada e logo antes, por causa do ritmo "acelere tudo".
- Nesse caso a rotina **desiste do dia inteiro**, em vez de instalar o commit anterior, que já tinha as 2 h. Com merges toda madrugada, ela desiste todo dia.
- Outra trava possível: a versão da web no main diferente da do site às 06h30, por deploy em andamento.
- **Para confirmar (1 minuto, sem dado sensível):** abrir no notebook `SISTEMA BAP\LOGS\atualizacao_diaria.log` e mandar só as **3 últimas linhas**. Elas dizem "limite 1", "limite 3" ou outro motivo.

## O que fazer
1. **Hoje, para destravar já (passo do Alexandre, porque instalar no PC pede o "instale" dele):** no notebook do robô, com o robô **parado**, dar dois cliques em `ATUALIZAR_DO_GITHUB.bat`, na pasta de produção.
   - Sem opção nenhuma, é o modo manual de sempre: baixa o main, faz backup e troca os `.py`/`.bat`.
   - Depois disso, a próxima rodada do robô já manda os faróis novos e a edição.
   - Se a tela do atualizador mostrar "instalado por fora" ou outro aviso, ele manda só a frase do aviso e o time orienta.
2. **Definitivo (T-0056, nova):** a rotina das 06h30 passa a instalar **o commit mais novo do main que já tem 2 h**, em vez de desistir. As outras travas continuam iguais: CI verde, versão do site, janela, robô parado e "instalado por fora".
   - O `atualizar_do_github.py` só muda com o "instale" do Alexandre (ADR 0002).
   - O time prepara o PR com testes, e eu mando o número e o SHA para o "instale".

**Previsão:** o item 1 resolve hoje, assim que ele rodar o .bat. A T-0056 fica pronta para o "instale" no início da tarde.
