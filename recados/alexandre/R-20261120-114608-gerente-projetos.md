---
id: R-20261120-114608-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: alta
tarefa: T-0006
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-20T11:46:08-04:00
---
# BAP Central na web: o passo seguinte da ADR 0001 (ondas 0 a 2) e as decisões dele

## Onde estamos
- A T-0006 entregou o PLANO (ADR 0001, no main desde 10:43). A construção da web ainda não começou, porque é backlog novo e precisa da autorização dele.

## Onda 0 (fundação): recomendação SIM, começar agora
- O que é: o serviço vazio no Render, com login próprio, perfis, tela de usuários, página de saúde, disco montado e deploy manual. Nenhum dado de cliente.
- Dono: modulo-web (pasta web/). A proposta do render.yaml, com o fuso de Manaus, é governança, com o merge pela delegação.
- Depende de: nada do que está em andamento (T-0003 e T-0010 são independentes). Para pôr no ar, depende dele: criar os segredos no Render (só ele cria) e dar o "aprovo deploy v0.1.0".
- Previsão [SUPOSIÇÃO, estimativa]: desenho às 13:30; PR com o serviço e os testes às 16:30 de hoje; no ar no mesmo dia, se ele criar os segredos e aprovar o deploy.

## Onda 1 (Painel do Diretor e Farol de Inadimplência, só leitura)
- Precisa de:
  - o modo leitura no modulo-farois;
  - a lista do pacote no engenheiro-dados (hoje TRAVADO: nenhuma sessão roda como engenheiro-dados, ver a decisão 7);
  - o passo 4f do robô no modulo-robo. Esse passo roda no PC e só vai para lá com o "instale";
  - os blocos do renderizador, no modulo-web.
- Previsão [SUPOSIÇÃO]: o código pronto em 24/11, o "instale" do passo 4f no PC em 25/11 e os 5 dias úteis batendo com o PC de 25/11 a 01/12. Entrega da onda 1 em 01/12/2026, se nenhum dia divergir. Cada divergência zera a contagem.

## Onda 2 (os outros faróis, em lotes por área)
- Previsão [SUPOSIÇÃO]: um lote por semana, cada um com 5 dias úteis batendo. São 4 lotes: Vendas e CRM; Pós-venda; Analista; Trade. Fim em 23/12/2026, sem contar feriados.

## Decisões que ele precisa tomar (cada uma com a recomendação do gerente)
1. Autorizar a ONDA 0 no backlog (T-0013, modulo-web).
   - Recomendação: SIM. É a base de tudo, não tem dado de cliente e não depende de nada aberto.
   - Prazo: sem efeito nas outras tarefas.
2. Dado de cliente (CNPJ e nome) e cópia do dado digitado (edições do pós-venda, autorizações, transportadoras) no Render, no disco, atrás do login, nunca no GitHub.
   - Recomendação: SIM, como o BAP Ajuda já faz.
   - Prazo: sem isso a onda 1 não começa. A onda 0 não depende disso.
3. Login próprio, com perfis.
   - Recomendação: SIM. A regra 9 proíbe depender de registro no Microsoft 365.
   - Prazo: nenhum.
4. Disco persistente nas ondas 1 e 2, e Postgres só na onda 3 (edições, com ADR 0002 antes).
   - Recomendação: SIM. Não reescreve nada e roda o mesmo cálculo do PC, então o número é o mesmo.
   - Prazo: é o caminho mais curto.
5. Primeira entrega = Painel do Diretor + Farol de Inadimplência, batendo com o PC por 5 dias úteis.
   - Recomendação: SIM. São as duas telas que ele mais usa, e os 5 dias provam o número.
   - Prazo: a onda 1 dura no mínimo 5 dias úteis depois do código.
6. Custo [SUPOSIÇÃO, tabela pública do Render, a conferir no painel da conta]: cerca de US$ 26/mês nas ondas 0 a 2 (serviço Standard de 2 GB + 5 GB de disco), e cerca de US$ 45/mês a partir da onda 3 (com Postgres).
   - Recomendação: SIM, confirmando o valor no painel do Render, onde o BAP Ajuda já roda.
   - Prazo: a confirmação é preciso antes do deploy da onda 0.
7. Ambiente para o engenheiro-dados (BapCentral-Dados, BAP_AGENTE=engenheiro-dados, sem segredo).
   - Recomendação: SIM. Sem ele, a lista do pacote da onda 1 e a pasta de cache não andam.
   - Prazo: não atrasa a onda 0, mas a onda 1 depende dele.
