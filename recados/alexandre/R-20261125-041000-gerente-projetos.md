---
id: R-20261125-041000-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0017
responde_a: R-20261125-035000-alexandre
encerra: false
contrato: null
criado_em: 2026-11-25T04:10:00-04:00
---
# T-0017: abas de Pedidos, Entregas e Visita no site — merges feitos e site v0.3.0 no ar

## Merges (CI verde em cada head; sessão BAPCentral - Cowork)
- #69 `21bc292` contrato (engenheiro-software) · #70 `1f5e473` RN-GER-011 (gerente-projetos) · #71 `659d06a` núcleo dos faróis (modulo-farois) · #72 `8669f1a` robô (modulo-robo) · #73 `31429f1` site v0.3.0 (modulo-web) · #74 `52162a9` testes (testes).
- Antes dos PRs, os 6 branches juntos na nuvem: pytest 460/460, web 222/222, smoke_processos só com a falha conhecida, `verificar` sem violação em cada branch.
- Pareceres do revisor-codigo e do corretor-redundancias por PR NÃO foram feitos nesta sessão (pendência para a próxima rodada do time; o código veio pronto dos branches da outra conta).

## Site
- /saude às 04:07 (Manaus): status ok, versão 0.3.0, tz_ok true; último pacote ainda o de 24/11 18:07 (robô antigo).
- As abas novas só ganham número quando o robô novo rodar na pasta de produção (rotina diária, T-0018).

## Decisões aplicadas (R-20261125-035000-alexandre)
- 1 A; D1–D6 A. Nada voltou na pasta "Regionais - Leandro". T-0018: 1 A a 5 A. Sem ronda nesta sessão.

## Como testar em 5 passos
1. Abrir https://bap-central.onrender.com/saude e ver "versao":"0.3.0".
2. Entrar como admin e abrir Pedidos, Entregas e Visita: as abas aparecem (sem número até o robô novo rodar).
3. Depois da migração (T-0018) e da 1ª rodada do robô novo, conferir o número de cada aba com o farol do PC.
4. Escolher um estado em Pedidos e Entregas e ver as linhas filtradas.
5. Entrar como diretor e ver só o Resumo.
