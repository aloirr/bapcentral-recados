---
id: R-20261127-101045-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0050
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:10:45-04:00
---
# T-0050 entregue: acesso aos faróis por usuário (web 0.10.0 no ar)

**T-0050 entregue: acesso aos faróis por usuário, na tela Usuários.** O site está no ar na versão 0.10.0: o /saude dá ok e mostra 0.10.0.

**O que entrou no main:**
- #173: RN-GER-018 (d0588e6);
- #174: o desenho (4c6155f);
- #175: a web 0.10.0 (57cf6fa).

**O que faz:**
- O perfil continua dando o padrão.
- Na tela Usuários, o admin pode **tirar** um farol de um usuário ou **liberar** um farol além do perfil (P1 B).
- Liberar um farol libera o menu e a tela. As restrições de dado continuam pelo perfil: meta do RH, total a pagar, edição só do admin, dados pessoais.
- Quem tenta abrir um farol sem acesso recebe 403 no servidor, não só no menu.
- Toda mudança de acesso fica registrada, só acrescentando linha.

**Como testar em 5 passos:**
1. Entre no site como admin e abra **Usuários**.
2. Escolha um usuário de teste (perfil vendas, por exemplo) e abra os faróis dele. A tela separa o que vem do perfil e o que foi liberado a mais.
3. **Tire** um farol que o perfil dá (ex.: Clientes) e **libere** um que o perfil não dá (ex.: Giro de produtos). Salve.
4. Entre com esse usuário em outra janela anônima. O menu não mostra Clientes e mostra Giro de produtos. Ao digitar o endereço de Clientes direto, a página dá "sem acesso".
5. Volte como admin e clique em restaurar o padrão do perfil. O usuário volta a ver os faróis do perfil.

**Revisões no head 8586ab7:**
- revisor-codigo aprovado, com 8 perfis × 692 pontos comparados e 0 diferenças fora do que foi pedido;
- revisor-ux e design-de-marca aprovados;
- corretor sem achado aberto;
- simulação aprovada por você (R-092425).

**Observação:** o corretor viu um teste da web instável na suíte inteira (`test_T0045_visitas.py::test_lote_ok_idempotente...`), que passa quando roda sozinho. O revisor da T-0052 está conferindo se ele já falhava antes. Não afeta a T-0050.
