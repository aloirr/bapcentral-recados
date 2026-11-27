---
id: R-20261127-052537-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: pergunta
prioridade: normal
tarefa: T-0036
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T05:25:37-04:00
---
# Simulação da T-0036 (faróis do Analista e perfis analista/trade) para aprovar por delegação

A T-0036 (faróis do Analista Comercial no site e perfis "analista" e "trade") está pronta para os PRs. Falta só a aprovação da simulação. Peço que você aprove por delegação, como na R-20261127-013010-alexandre.

**Simulação** (dados fictícios; 1366 px e 390 px): `recados/anexos/T-0036/sim/`
- `saldo`, `markup`, `preco`, `divergencias`: os 4 faróis, com o cliente só pelo código;
- `menu-analista`: o menu do analista, com o grupo "Analista Comercial";
- `trade-inicio`: o perfil trade vê só a frase "Os faróis do Trade Marketing ainda não estão no site.";
- `MEDICAO.md`: as medidas.

**Critérios da delegação, conferidos:**
- só dados fictícios ("CIDADE FICTICIA", "VENDEDOR FICTICIO", códigos 900000+), sem documento nem contato;
- revisor-ux aprovado e design-de-marca aprovado (só 🟢, já aplicados);
- revisor-codigo aprovado, sem 🔴 nem 🟡 (`recados/anexos/T-0036/revisao-codigo.md`);
- corretor-redundancias sem achado aberto (RD-0001 a RD-0008 da sessão, fechados);
- número bate: o "desconto comercial" de cada estado é igual no Saldo, no Por UF, no cartão e na barra do RRM (RN-GER-006).

**Perguntas ao Alexandre, com o padrão adotado (nenhuma bloqueia):**
- P1: o analista vê os outros faróis? **A: sim, como o gerente** · B: só os 4 do Analista e o Painel.
- P2: como o cliente aparece nos 4 faróis? **A: só o código** · B: o nome sem CPF/CNPJ, com adendo à ADR 0001.
- P3: o analista vê o TOTAL A PAGAR das Campanhas? **A: não (RN-GER-015 como está)** · B: sim.

**Ajustes do gerente antes dos PRs:**
- web passa a ser a 0.9.0 (0.6.0 = T-0045, 0.7.0 = T-0023, 0.8.0 = T-0037);
- a §10.11 do contrato fica com a T-0036; a T-0037 passa para a §10.12;
- PNGs e relato da sessão saem do repositório e ficam nos anexos.

**Fora da T-0036 (viram tarefas novas):**
- T-0048: o Painel do Diretor mostra o desconto comercial total com 1 casa a partir do "15%" arredondado (15,0% em vez de 15,1%). A correção vai ao modulo-farois, com simulação antes (regra 10).
- Pergunta para você levar ao Alexandre: a faixa "Dados de dd/mm/aaaa hh:mm" no topo dos faróis contraria a §4.1 da `tela-bc3.md`. Vale a faixa (como está no site) ou a §4.1? **Recomendação: manter a faixa** e corrigir a §4.1, porque ela já está em todos os faróis no ar.

**Ordem dos PRs depois da sua aprovação:** regras → desenho (contrato §10.11) → faróis → web 0.9.0 → robô → testes.
