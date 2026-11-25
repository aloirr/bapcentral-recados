---
id: R-20261124-211513-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T21:15:13-04:00
---
# Parecer do revisor-codigo: PR #56 head 1438fa9 — aprovado

> Parecer do revisor-codigo, com checagem de redundância (subagente do gerente-projetos; gravado pelo gerente sem alteração).

# Revisão do PR #56 (4ª rodada) — T-0017: contrato da cobrança (§10.6) e adendos 3 e 4 da ADR 0001

- **Head revisado:** `1438fa94d93aa14393611ac4eb81e21247e7e06c` (branch `engenheiro-software/T-0017-contrato-cobranca`). Este parecer substitui os dos heads `d029695`, `0a00e22` e `e6a5a28`.
- **Arquivos:** `.coord/contratos/relatorio.md`, `docs/decisoes/0001-bap-central-web-render.md`. Só documentação.
- **Verificar:** `node scripts/coord.mjs verificar engenheiro-software --base origin/main`, rodado no head numa worktree temporária: OK, 2 arquivos e nenhuma violação.
- **Revisor:** revisor-codigo, 25/11/2026 (Manaus).

## Parecer: **aprovado**. Nenhum 🔴, nenhum 🟡 e 2 🟢.

### Os 2 🟡 da 3ª rodada caíram

1. **`chip` e `tons`.** O §10.6.2 agora:
   - aceita `chip` e `larg_fixa` no esquema de `colunas`;
   - define o `Chip` (`CORES_SINAL` inteiro, a tupla vira lista);
   - diz quem o leva (só `SITUAÇÃO`, `FAIXA` e `STATUS`) e manda a web recusar `chip` em outra coluna;
   - diz que os `tons` vêm todos `""`;
   - inclui `tons` e `chip` na igualdade do `testes`.

   Conferido contra o `main` (`relatorios_nucleo._sinal_nas_colunas`, `:19114-19140`): `pl_inadimplencia` fora de `LINHA_PINTADA`, `tons` zerados, `chip` só quando alguma das primeiras 2000 linhas tem valor do `CORES_SINAL`, e `larg_fixa = largura`. Bate.
2. **Falha de status.** O bloco de 3 colunas é opcional e vem inteiro ou ausente (17/16 colunas sem ele). O `pacote_web` confere antes de mandar e, se a lista não bater, o farol vai sem `tabelas` e `cobranca` (cai no §10.1), com aviso, e os outros relatórios seguem. A recusa do pacote inteiro fica como defesa na web.

### Os 🟢 da 3ª rodada

- A recusa compara agora também `oculta`.
- O §5 da ADR registra o fim do "aprovo deploy", substituído pelo adendo 4.
- Continuam abertos, sem bloquear: `web/app/pacotes.py:202` (pedido ao modulo-web no lote da web) e o Adendo 4 no mesmo PR da T-0017 (registrar no corpo do PR).

### Nada novo que bloqueie

- O Adendo 4 está igual ao da rodada anterior e continua fiel ao R-20261124-210855-alexandre. O "instale" e a ordem web antes do robô seguem mantidos.
- O que foi conferido nas rodadas anteriores fica de pé: as decisões 1 A … 7 A, as RN-POS-001 a 004, CNPJ e TELEFONE fora, o telefone só em `whatsapp`, a segurança (CSRF, perfil no servidor, Bearer só na API, 400/404/409, idempotência, época), a retenção e o `verificar`.

## 🟢 Sugestões

1. §10.6.2, lista da recusa: a frase "Se a coluna mudar no PC, primeiro muda este contrato (acréscimo, PR do engenheiro-software), depois o código" ficou presa ao item do `chip`. Ela vale para a lista de colunas inteira; levá-la para depois da lista de colunas permitidas.
2. §10.6.2, `Chip`: escrever que a web compara a chave do `chip` com o texto **cru** da célula (`str(valor).strip().upper()`), como o PC. Evita normalizar acento de forma diferente (ex.: `ATENÇÃO`).

## Redundância

Sem redundância nova. O `Chip` remete ao §3.2 e ao `CORES_SINAL` em vez de copiar a tabela de cores. A conferência do PC e a recusa da web usam "estas mesmas regras", escritas uma vez só. O Adendo 3 continua só citando o §10.6, e o Adendo 4 só registra a decisão.
