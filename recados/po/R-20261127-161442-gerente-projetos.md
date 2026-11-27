---
id: R-20261127-161442-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0036
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T16:14:42-04:00
---
# T-0036 entregue: faróis do Analista no site (Saldo, Markup, Preço e Divergências)

**No main:** #177 (testes tolerantes, cb54182), #159 (robô, f8e7940), #211 (testes sem tolerância). Revisor de código e corretor aprovados em cada head; CI verde. Regras, desenho e faróis já estavam no main (#156, #160, #157; RN-GER-017).

**O que muda:** o robô leva ao site os faróis do Analista Comercial (Saldo, Markup, Preço e Divergências). Veem: admin, gerente e analista; o diretor vê só o Resumo (RN-GER-014); o Excel de correção das Divergências é só do admin. Números iguais aos do PC (valor × regra: Divergências n1 = "Vendedor diferente", n2 = Sem vendedor + Fora da base + Código duplicado).

**Como testar em 5 passos** (depois de o robô novo rodar no notebook; o .bat já foi rodado às 16h):
1. Abrir o /saude: o pacote novo traz mais de 5 faróis.
2. Entrar como analista ou gerente: aparecem Saldo, Markup, Preço e Divergências no menu.
3. Comparar os cartões de cada um com o farol do PC no mesmo horário de dados: os números batem.
4. Entrar como diretor: nesses faróis, só o Resumo.
5. Entrar como admin: o Excel de correção das Divergências aparece só para ele.

**Para depois (🟢):** 2 ajustes pequenos nos testes (filtro sobrando e um comentário), para um lote futuro.
