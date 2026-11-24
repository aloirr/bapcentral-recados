---
id: R-20261124-182144-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0017
responde_a: R-20261124-181913-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T18:21:44-04:00
---
# T-0017: 4 PRs abertos; plano do WhatsApp no site; conferência T-0013/T-0014 precisa do Alexandre

## 1. Simulação aprovada: PRs abertos (18:25)
#47 contrato (engenheiro-software) · #48 site (modulo-web) · #49 robô (modulo-robo) · #50 internos RN-GER-004/005 (modulo-farois). Revisor-codigo e corretor-redundancias rodando nos 4. Depois do merge, o 2º PR do testes (testes novos do robô e dos internos). Previsão: os 4 no main hoje, 24/11, até as 21h, se as revisões não trouxerem 🔴. Em seguida peço ao Alexandre "aprovo deploy v0.2.0" (site primeiro) e depois o "instale" do bap_automation.py no notebook.

## 2. Pedido novo: WhatsApp, Títulos e Por cliente no site
Entra como 2ª entrega do Farol de Inadimplência na T-0017 (mesmo farol, autorização R-20261124-181913-alexandre). Muda duas regras de base da ADR 0001: dado pessoal de cliente (nome, CNPJ, telefone) passa a ir ao Render, e o site passa a GRAVAR (o registro da cobrança tem de voltar ao PC sem perder o diário de lá; regra 7). O engenheiro-software está fazendo o desenho técnico agora (como o registro volta ao PC, quem vê o quê por perfil, o que fica no disco do Render, adendo 3 da ADR). Previsão: desenho e decisões para o Alexandre hoje até as 20h; com as decisões, simulação PNG em cerca de 2 dias úteis (27/11); o Farol de Pedidos continua previsto para 26/11.

## 3. Robô no notebook: conferir T-0013/T-0014
Não tenho login no site (usuário e senha são só do Alexandre; nenhum segredo vem para o time), e o PC dele tem dados mais novos que as bases do repositório. Por isso a conferência é dele, em 5 passos:
1. No PC, abra BAP Central > Painel · resultado (BAP inteira) e anote o faturado do mês e a positivação.
2. No site (https://bap-central.onrender.com), entre e abra Painel · resultado: os mesmos 2 números devem ser iguais (o site mostra "Dados de 24/11/2026 18:07").
3. No site, escolha o estado AM; no PC, filtre UF = AM: os mesmos 2 números devem bater.
4. Repita o passo 1 e 2 em Painel · produtividade (um número qualquer).
5. Responda ao po só com os números (sem print com nome de cliente ou vendedor): PC × site, BAP inteira e AM. Se baterem, fecho T-0013 e T-0014; se não, o testes investiga com o mesmo pacote.
