---
id: R-20261127-101105-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0050
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:11:05-04:00
---
# T-0050: correção do 'como testar' (sem botão de restaurar; liberado abre só no Resumo)

Corrijo 3 pontos do meu R-20261127-101045 (entrega da T-0050). Conferi na tela que está no main.

1. **Não existe o botão "restaurar o padrão do perfil".** Para voltar ao padrão, o admin marca de novo o farol tirado (em "Do perfil"), desmarca o liberado (em "Liberar além do perfil") e salva.
2. **O farol liberado além do perfil abre só no Resumo**, sem as tabelas de clientes e sem Exportar (P4 A). O Painel Executivo, quando liberado, abre completo. A tela Usuários avisa isso.
3. **A mensagem de quem abre um farol sem acesso** é "Você não tem acesso a esta página.", e não "sem acesso".

**Como testar em 5 passos (versão certa):**
1. Entre como admin e abra **Usuários**.
2. Escolha um usuário de teste (ex.: perfil vendas). Os faróis aparecem em duas partes: "Do perfil" (desmarque para tirar) e "Liberar além do perfil".
3. Desmarque um farol do perfil (ex.: Clientes) e marque um para liberar (ex.: Giro de produtos). Salve. Na lista aparecem os selos "1 farol tirado" e "1 farol liberado".
4. Entre com esse usuário numa janela anônima. O menu não mostra Clientes e mostra Giro de produtos, que abre só no Resumo. Digitando o endereço de Clientes direto, aparece "Você não tem acesso a esta página."
5. Volte como admin, remarque Clientes, desmarque Giro de produtos e salve. O usuário volta ao padrão do perfil.

Desculpe a imprecisão.
