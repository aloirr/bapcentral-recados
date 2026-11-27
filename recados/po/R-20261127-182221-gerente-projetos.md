---
id: R-20261127-182221-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0057
responde_a: R-20261127-162233-alexandre
encerra: true
contrato: null
criado_em: 2026-11-27T18:22:21-04:00
---
# Entrega T-0057: a janela do robô mostra o andamento

A janela preta do robô passa a mostrar as mesmas linhas que vão para o agendador.log: o início, os passos 1 a 4, "Pacote web enviado", "Rodada concluída" e o FIM com o código de saída. O log continua igual (só acréscimo), e o código de saída do robô é preservado.

## No main
- #214 (robô: bap_automation.py e executar_bap.bat) → 9003d98
- #216 (simulação aprovada pelo PO, R-20261127-175938-po) → ba2f2a8
- #215 (testes: espelho tela × log, código de saída, falha ao iniciar) → dd22600

Pareceres: revisor-codigo aprovado; corretor-redundancias sem achado; CI verde em cada head.

## Instalação
Pela rotina diária das 06h30 de 28/11 (os commits terão mais de 2 h no main). Não precisa de "instale".

## Como testar em 5 passos
1. Amanhã, depois das 06h30, abra o atualizar_do_github.log e confira que o bap_automation.py e o executar_bap.bat foram instalados.
2. Na próxima rodada agendada do robô, olhe a janela preta: as linhas aparecem enquanto o robô trabalha, e a janela não fica mais vazia.
3. Abra o agendador.log e confira que tem as mesmas linhas da janela, na mesma ordem.
4. No fim, confira que a janela mostra "FIM" com o código de saída (0 = tudo certo).
5. Se algo falhar, a janela e o log mostram a mesma mensagem de erro. Mande um print da janela ao PO.
