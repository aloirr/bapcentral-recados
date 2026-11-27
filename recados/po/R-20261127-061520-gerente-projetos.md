---
id: R-20261127-061520-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: pergunta
prioridade: normal
tarefa: T-0050
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T06:15:20-04:00
---
# T-0050: o que muda com a ampliação e as perguntas P2, P3 e P4 (com recomendação)

O desenho da T-0050 está pronto (o engenheiro conferiu farol a farol). Você pediu para ver antes do código o que muda com a ampliação (P1 = B). Abaixo está, com três perguntas, cada uma com recomendação clara.

## O que muda com a ampliação
- **Nenhum farol mostra coluna ou aba a mais** para quem foi liberado. O pacote do site é um só por farol, e todos os cortes de dado são listas por perfil: abas com cliente, Cobrar, edição, colunas restritas e Excel de correção. Quem vem de fora do perfil fica fora de cada uma.
  - O TOTAL A PAGAR continua só para admin, gerente e diretor (RN-GER-015).
  - Nunca aparece documento nem telefone.
- **Ponto 1 (vira a P4):** pela sua leitura, liberar um farol que tem tabelas com cliente dá **só o Resumo**, como o diretor. As abas e o Exportar respondem 403. Se o Alexandre espera ver as tabelas, entram nome e código do cliente linha a linha (sem telefone e sem documento).
- **Ponto 2:** o Painel Executivo, se liberado, vem inteiro, sem corte por perfil dentro: Markup, Preço e Inadimplência da BAP inteira (vira a P2).
- **Ponto 3:** os faróis do Analista, se liberados, mostram desconto, markup e preço agregados no Resumo (números, sem cliente).
- **Ponto 4:** a parcial de Pedidos e a de Visita seguem a tela (quem vê o farol tira a parcial; nelas não há cliente nem meta RH). A de Entregas, que lista cliente, continua pelo perfil.

## Perguntas ao Alexandre
- **P4:** quem foi liberado além do perfil vê:
  - **A: só o Resumo** do farol (recomendado: não abre cliente linha a linha a quem o perfil não dá);
  - B: o farol completo, com as tabelas (nome e código do cliente, sem telefone nem documento).
- **P2:** o Painel Executivo entra na lista de faróis liberáveis?
  - **A: sim** (recomendado; ele mostra só números agregados da BAP);
  - B: não, só pelo perfil.
- **P3:** um farol novo que entrar no site chega, para quem tem acesso personalizado:
  - **A: marcado, se o perfil dele vê** (recomendado: segue o perfil, sem o admin ter de lembrar);
  - B: desmarcado até o admin liberar.

## Como fica a tela
Na tela Usuários, ao criar ou editar um usuário, aparecem dois grupos:
- **"Do perfil":** os faróis que o perfil dá, marcados; o admin pode desmarcar.
- **"Liberar além do perfil":** os outros faróis, desmarcados; o admin pode marcar.

A tela Usuários e Trocar senha ficam fora da lista, para o admin não tirar a tela Usuários de si mesmo. Toda mudança fica registrada com quem, quando, de quem e qual farol, sem dado de cliente.

## Próximos passos
- Com as respostas (ou com A nas três, se vier "siga a recomendação"), o designer-ux faz a simulação: PC e celular, dados fictícios.
- O código entra depois da T-0036.
- Previsão: a simulação vai a você hoje até umas 08h30.
