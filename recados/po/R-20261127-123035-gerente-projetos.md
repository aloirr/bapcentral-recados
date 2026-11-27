---
id: R-20261127-123035-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: alta
tarefa: T-0055
responde_a: R-20261127-110732-alexandre
encerra: false
contrato: null
criado_em: 2026-11-27T12:30:35-04:00
---
# T-0055 entregue: porta só de leitura do site no ar (web 0.13.0)

**No main:** #183 (RN-GER-020, f6c4b00), #184 (desenho, 3f9e681), #185 (web 0.13.0, e06bff1), #189 (testes, cd9faf2). O /saude mostra 0.13.0. Revisor de código e corretor aprovados; simulação aprovada pelo po (R-20261127-121844-po).

**O que é:** GET /api/leitura/painel e GET /api/leitura/resumo/{rid}, com "Authorization: Bearer <BAP_WEB_LEITURA_TOKEN>". Sai só o que o diretor vê (Painel Executivo, cartões do Resumo e carimbo do pacote), com os números do site. Nunca sai tabela, nome, documento, telefone, e-mail, meta RH, TOTAL A PAGAR nem gravação.

**Como testar em 5 passos:**
1. No Render, bap-central > Environment, criar BAP_WEB_LEITURA_TOKEN com uma senha de 32 caracteres ou mais, diferente das outras, e salvar.
2. Esperar o deploy curto do site e abrir /saude: versão 0.13.0.
3. Sem token, chamar /api/leitura/painel: resposta 401.
4. Com o token, chamar /api/leitura/painel: os mesmos valores do Painel Executivo do site, no mesmo horário dos dados.
5. Conferir que não aparece nome de cliente, documento, telefone, e-mail, meta RH nem TOTAL A PAGAR.

**Fora:** o estoque de Belém (não está no pacote). **Atenção:** o pacote de hoje ainda vem do robô antigo do notebook (5 faróis); a porta mostra o que o pacote tiver.

## Decisões que o Alexandre precisa tomar
- Só o passo 1 (a variável no Render). A sessão de análise pede a senha pelo formulário seguro dela.
