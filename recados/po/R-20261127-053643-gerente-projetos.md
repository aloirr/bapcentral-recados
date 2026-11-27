---
id: R-20261127-053643-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: aviso
prioridade: normal
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T05:36:43-04:00
---
# Resumo da madrugada (00h às 05h45) para levar ao Alexandre às 06h

Resumo da madrugada (00h às 05h45, Manaus) para você levar ao Alexandre às 06h.

## 1. O que entrou no main (20 PRs)
- **T-0024 concluída:** faróis do lote 2 no site (Indicadores, Clientes, Roteirização, Giro e Estoque FRW), com o robô e os testes (#89, #91, #97).
- **T-0033 concluída** (#127, #135, #138 a #140, #143 a #145):
  - marca BAP AUTOPARTS no PC, no robô, no Planner e nos e-mails da rota e da cobrança;
  - cor da Aderência (RN-VIS-001, 80/50);
  - revisão geral da web.
- **T-0034 concluída:**
  - página inicial = Painel Executivo, com Login, Senha, Usuários e Parcial no visual novo (#146);
  - testes das comparações do Diretor: 57 comparações batem com o PC (#148);
  - **site no ar na 0.5.0**, com o /saude ok.
- **T-0023/T-0025:** regras (RN-GER-014 a 016, RN-POS-005 e 006) e contrato da edição pela web (#141, #142).
- **T-0045 (visitas da Máxima no site):** desenho (ADR 0004), contrato v1.1 e núcleo da rota (#137, #149, #150).
  - O núcleo foi provado nos 1.622 Espelhos reais: 13.571 linhas iguais, zero diferença.
- Quadro às 00h30 e às 04h15 (#136, #147).
- SHAs: #89 a178af2 · #91 8dab048 · #97 0bb251b · #127 a81c2e4 · #135 2613cf7 · #137 e8b5912 · #138 958cf8f · #139 0ab3942 · #140 891d6fd · #141 89d93bd · #142 e39dad3 · #143 8f0600e · #144 2aa5ba7 · #145 f3c4569 · #146 3a453d1 · #147 30ae65d · #148 98f87db · #149 42c81a1 · #150 d58b12f · #136 a32b610.
- **/saude às 05h36:** ok, versão 0.5.0, fuso de Manaus ok. O último pacote do robô é de ontem às 21h06, com 5 faróis. Os faróis da T-0024 só chegam ao site quando o robô novo estiver instalado no PC (rotina das 06h30, regra 11).

## 2. Previsões (manhã de hoje)
- **T-0045:**
  - a web 0.6.0 (#151) está no CI e entra assim que der verde;
  - em seguida entram o robô do PC (PR #152, aberto) e os testes (último ajuste de redundância);
  - previsão: tudo no main até umas 07h;
  - depois disso, o site só liga a busca na Máxima com os passos do Alexandre (item 4).
- **T-0023** (Garantias, Devoluções e NCC no site, web 0.7.0):
  - aprovada por você;
  - os PRs saem depois da última revisão de código da web, na ordem web → núcleo → robô → contrato → testes;
  - previsão: manhã de hoje.
- **T-0037** (Farol de Fretes, web 0.8.0):
  - correções da última revisão aplicadas: contrato renumerado para a §10.12, Resumo do Fretes com 2 frases aprovadas pelo designer-ux e totais iguais nas 3 tabelas;
  - falta a trava dos testes (CI verde em qualquer ordem de PR);
  - depois vai a você a simulação final para aprovar, e então os PRs.
- **T-0036** (faróis do Analista e perfis analista/trade, web 0.9.0):
  - pronta;
  - pedi a aprovação da simulação em R-20261127-052537;
  - os PRs saem em seguida.
- **Depois:** T-0025 v2 (código, depois da T-0023), T-0046, T-0047 e T-0048 (nova, abaixo).

## 3. Informes ao Alexandre (padrão adotado; ele pode mudar)
- **T-0023, mudança de processo:** a edição de garantias e NCC passa a ser só pelo site e só pelo admin. O PC fica só leitura nessa parte, menos o contato da garantia. Se ele quiser manter a edição no PC, é só dizer.
- **T-0036:** P1 A (o analista vê os outros faróis como o gerente) · P2 A (cliente só pelo código) · P3 A (o analista não vê o TOTAL A PAGAR das Campanhas).
- **T-0037:**
  - P1 A, P2 A (sem o frete real na edição) e P4 A;
  - P3 B: % sobre o faturado líquido, o que leva a BAP de 54,76% para 57,46% em NOV.
- **T-0025:** P4 A (pontos visíveis para vendas).
- **T-0045, custo:** no pior caso, cerca de US$ 7 por mês no Render (serviço agendado de 2 GB, cobrado por minuto); o normal é US$ 1 a 3.
- **T-0048 (nova):**
  - defeito antigo: o Painel do Diretor mostra o desconto comercial total como 15,0% em vez de 15,1%, porque relê o número já arredondado do cartão;
  - a correção vai com simulação antes (regra 10).
- **Pergunta (com recomendação):** a faixa "Dados de dd/mm/aaaa hh:mm" no topo dos faróis contraria a §4.1 da tela-bc3.md. Recomendação: **manter a faixa**, que já está em todos os faróis no ar, e corrigir o documento.

## 4. Fila do Alexandre
1. **T-0045, já pode fazer:** passos 1 e 2 da Máxima (usuário só para o robô, só leitura no Painel Auditoria). O passo a passo está em `recados/anexos/T-0045/passo-a-passo-alexandre.md`. Usuário e senha ficam só com ele.
2. **T-0045, depois do aviso do time:** o "autorizo" do PR de governança (render.yaml e donos.json `nuvem/**`). Esse PR ainda não foi aberto; sai hoje de manhã, logo depois da web e do robô, e eu mando o número e o SHA. Depois disso: variáveis no Render, diagnóstico e "Ligar a agenda" (passos 3 a 9).
3. **Guardião:** numa worktree de subagente, o guardião não barrou uma mudança no render.yaml. A mudança da T-0045 ficou só como proposta em `docs/desenho/T-0045-render-yaml.diff`, e o render.yaml do main não mudou. Fechar essa brecha é mudança de governança e precisa do autorizo dele.

## 5. Limite de uso
O limite semanal continua em alerta. Mantive a frente larga ("Acelere tudo"), mas com agentes curtos e retestes só no que mudou.
