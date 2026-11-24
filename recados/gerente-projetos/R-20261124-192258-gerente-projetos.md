---
id: R-20261124-192258-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T19:22:58-04:00
---
# Parecer do revisor-codigo: PR #55 head 8266aa2 — 1 🟡 (RN-POS-001: fixo e número ausente)

> Parecer do revisor-codigo, com checagem de redundância (subagente do gerente-projetos; gravado pelo gerente sem alteração).

# Revisão PR #55 — T-0017 — head 8266aa24893f0f245d985583c5e49e1b3b43c47d

Branch `gerente-projetos/T-0017-regras-cobranca`. Diff contra origin/main (3ebc793): só `docs/produto/03-regras.md` (+5 −1), 1 commit com `Agente: gerente-projetos`.

Parecer: **não aprovado ainda** — 0 🔴, 1 🟡, 4 🟢.

## Fidelidade às decisões (R-20261124-192008-alexandre / R-20261124-182438-gerente-projetos)
- 1 A, 2 A, 6 A → RN-POS-004: fiel.
- 3 A, 4 A, 5 A → RN-POS-003: fiel (7 pacotes, 30 dias após confirmação, 08h/14h + "situação do PC até hh:mm", telefone só para aquele envio e no diário, `COBRANCA_WEB.csv` com chave `id`).
- 7 A → RN-GER-005: fiel. Bate com o código: `bap_dados.titulos_sem_internos` ("O 000040 e o vendedor de teste, nao cliente: nao sai do saldo") e `email_inadimplencia.COD_TESTE` (filtra por `cod_protheus` do vendedor).

## Achados

🟡 `docs/produto/03-regras.md:44` (RN-POS-001) — "o número (55 + DDD + 9 dígitos)" não descreve o que o PC faz. `cobranca_whatsapp.celular()` também devolve **fixo** (55 + DDD + 8 dígitos) com o aviso "telefone fixo: pode não ter WhatsApp"; celular de 8 dígitos começando com 6–9 ganha o 9; número repetido ou ausente fica **vazio com aviso** e o cliente continua na fila. Sugestão: "número normalizado pelo PC (55 + DDD + número; celular de 8 dígitos ganha o 9); fixo, repetido ou sem telefone vêm com aviso".

🟢 `03-regras.md:44` (RN-POS-001) — "com títulos VENCIDOS" pode ser lido como filtro; `fila()` inclui todo INADIMPLENTE da "Por cliente" e só anexa os títulos VENCIDO da aba "Títulos". E "ordenada pelo valor em atraso" → "do maior para o menor (EM ATRASO)".

🟢 `03-regras.md:46` (RN-POS-003) — "(dado digitado, regra 7)": a regra 7 do CLAUDE.md lista nominalmente os dados intocáveis e o diário da cobrança não está lá. Ou cite a fonte (plano do R-20261124-182438, aprovado no -192008) ou peça a inclusão na regra 7 ao dono do CLAUDE.md.

🟢 `03-regras.md:46` (RN-POS-003) — retenção no Render (7 pacotes, 30 dias) e nome de arquivo são infraestrutura; quando o Adendo 3 da ADR 0001 sair (engenheiro-software), deixe na RN só a referência ao adendo, para não ter a mesma regra em dois lugares.

🟢 `03-regras.md:44–47` — as RN-POS-001 a 004 ficam misturadas com 4 bullets sem número na mesma seção; numerar ou separar num subtítulo "Cobrança no WhatsApp" facilita citar em `test_RN_POS_...`.

## Redundância
Sem regra reescrita: nada no doc 03 nem em `docs/decisoes/` trata de cobrança hoje; RN-GER-005 só ganha a distinção (não duplica RN-ROT-001). Risco futuro: RN-POS-003/004 × Adendo 3 da ADR 0001 (ver 🟢 acima).

## Demais itens do checklist
- Pedido atendido, sem mudança a mais: sim (só doc 03).
- Dado pessoal: nenhum (sem nome, CNPJ ou telefone; só códigos e o 000040 já público no doc).
- Segredos: nenhum. Dados digitados e `.json` da raiz: intocados. `bap_dados.VERSAO`: não tocado.
- Testes/tela: n/a (só doc).
- `node scripts/coord.mjs verificar gerente-projetos --base origin/main` no head 8266aa2 (worktree): OK, 1 arquivo, sem violação.
