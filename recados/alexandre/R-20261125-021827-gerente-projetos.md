---
id: R-20261125-021827-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-25T02:18:27-04:00
---
# T-0017: 6 decisões das abas de Pedidos, Entregas e Visita (recomendo A em todas)

# T-0017: 6 decisões para as abas de Pedidos, Entregas e Visita no site

Desenho pronto (engenheiro-software, branch engenheiro-software/T-0017-abas-tres-farois `d951ffd`, sem PR; parecer gravado pelo gerente, decisão 3 A).

## O que vai ao site (todas as abas do PC)
- **Pedidos:** Resumo · Pedidos (33 colunas, ~119 linhas no mês) com as 3 juntas (separação CD, reversa, analítico) · Solicitação BAP (7 sub-abas, ~4.370 linhas).
- **Entregas:** Resumo · Entregas (22 colunas, ~59 linhas no mês) com a junta "Pendências dos meses anteriores".
- **Visita:** Resumo · Por supervisor · Por vendedor · Dia a dia · Aderência dia a dia · Cliente a cliente (~1.441) · Prospecção · Indicação. Sem filtro por estado (aviso).
- **Saem do site:** CNPJ, CONTATO, TELEFONE e FOTO (o nome da foto traz o CNPJ) na Prospecção e na Indicação. Em Pedidos e Entregas não sai coluna.
- **Fica só no PC:** autorização de venda, edição de entrega, troca de loja de coleta, "Atualizar visitas", parciais.
- **Tamanho:** ~2,2 MB no fim do mês (hoje 0,33 MB; teto 25 MB). Trava nova no robô em 20 MB.
- **Achado:** em 84 razões sociais de Pedidos, 30 do Cliente a cliente e 4 de Entregas há CPF/CNPJ grudado no fim do nome. Regra nova RN-GER-011: nome de cliente vai ao site sem documento (o código fica), com teste.

## Perfis (1 A): admin e gerente veem tudo; diretor só o Resumo.

## Decisões (recomendo A em todas)
- **D1 — o perfil de cada farol vê as tabelas?** (pré-venda no Pedidos, pós-venda no Entregas, vendas no Visita) (A) sim, como o pós-venda na Inadimplência · (B) só admin e gerente · (C) A, mas vendas sem Cliente a cliente, Prospecção e Indicação.
- **D2 — quantos meses de linhas?** (A) só o mês do pacote, como o PC abre · (B) 12 meses com filtro de mês (+1 MB).
- **D3 — Solicitação BAP:** (A) as 7 abas inteiras · (B) só pedido EM ABERTO · (C) só no PC.
- **D4 — "Ver pedido" (duplo clique):** (A) fica no PC nesta entrega · (B) detalhe só leitura no site.
- **D5 — o estado de cima filtra as linhas?** (A) sim, pela regra dos cartões (Pedidos: filial da nota; Entregas: UF do cliente; Visita e Solicitação com aviso) · (B) não, tabelas da BAP inteira.
- **D6 — texto livre (justificativa, observação, resultado) e nome do motorista:** (A) vão, com telefone, e-mail e CPF/CNPJ trocados por "[removido]" · (B) ficam só no PC.

Resposta pronta (com as recomendações): **"D1 A, D2 A, D3 A, D4 A, D5 A, D6 A"**

## Enquanto isso
O time começa já pelo que não depende da resposta (funções de limpeza, tabelas genéricas no site, dados fictícios) e a simulação sai com as recomendações. Se vier B ou C em algum item, ajusto antes da simulação final. Nenhum PR antes da aprovação da simulação. Previsão da simulação dos 3 faróis: 07h30 (Manaus) — mudou de 06h30 porque agora são 14 telas (PC e celular, por perfil).
