---
id: R-20261125-025823-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-25T02:58:23-04:00
---
# T-0017: simulação das abas de Pedidos, Entregas e Visita no site — aprovação

# T-0017: simulação das abas de Pedidos, Entregas e Visita no site — aprovação

Pedido: R-20261124-223741-alexandre (Pedidos) e R-20261124-223958-alexandre ("1 B", Entregas e Visita). Feito com a recomendação A nas 6 decisões do R-20261125-021827-gerente-projetos (ainda sem resposta).

**Imagens** (dados fictícios; PC 1366 px e celular 390 px) em `recados/anexos/T-0017/abas/`:

| Imagem | O que mostra | Perfil |
|---|---|---|
| sim6-01-pedidos-pedidos-admin-pc-inteira | aba Pedidos inteira: cartões, tabela com as linhas pintadas e as 3 juntas (separação CD, reversa, analítico) | admin |
| sim6-01-pedidos-pedidos-admin-cel | a mesma aba no celular (tabela rola para o lado, 1ª coluna fixa) | admin |
| sim6-03-pedidos-solicitacao-cd-pre_venda-pc | Solicitação BAP com as 7 sub-abas (sem estado nem cartões) | pré-venda (D1 A) |
| sim6-04-pedidos-resumo-diretor-cel | diretor vê só o Resumo, sem abas | diretor |
| sim6-05-entregas-entregas-pos_venda-pc-inteira | aba Entregas com a junta "Pendências dos meses anteriores" | pós-venda (D1 A) |
| sim6-06-entregas-entregas-PA-admin-pc | Entregas com o estado PA escolhido (linhas só do PA; D5 A) | admin |
| sim6-08-visita-por-vendedor-gerente-cel | Visita · Por vendedor no celular | gerente |
| sim6-09-visita-dia-a-dia-sem-visita-vendas-pc | Visita · Dia a dia com o recorte "Sem visita em dia útil" (cartões somem com recorte) | vendas (D1 A) |

**Regras aplicadas:** sem CNPJ, sem telefone, sem e-mail; nome de cliente sem documento (RN-GER-011 nova); sem exportar; nada que grava (autorização de venda, edição de entrega, "Atualizar visitas", parciais) vai ao site. Visita sem filtro por estado, com aviso.

**Conferido:** designer-ux revisou as 28 telas (3 🔴 corrigidos, reteste sem 🔴); gerente abriu as 8 acima. Com o pacote real (bases congeladas, só no PC/nuvem, nada publicado): 124.733 células, 0 CPF/CNPJ, 0 e-mail; fora as colunas limpas, igual ao PC; pacote de 1,46 MB (limite 25 MB).

**Limite:** o "antes" do PC (tela Tkinter) não dá para gerar na nuvem; as telas do PC são as que ele já usa.

## Decisão
1. Simulação: (A) aprovada — abrir os PRs (contrato, faróis, testes, web v0.3.0, robô) · (B) ajustar antes (dizer o quê).
2. As 6 decisões D1–D6 (R-20261125-021827): resposta pronta "D1 A, D2 A, D3 A, D4 A, D5 A, D6 A".

Resposta pronta: **"1 A; D1 A, D2 A, D3 A, D4 A, D5 A, D6 A"**

Depois do "1 A": revisor-codigo e corretor-redundancias em cada PR; merge na ordem contrato → faróis → testes → web → robô (a web v0.3.0 vai ao ar sozinha no merge); o robô novo só chega à produção pela rotina diária (T-0018).
