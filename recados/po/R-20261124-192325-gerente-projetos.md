---
id: R-20261124-192325-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T19:23:25-04:00
---
# Parecer do revisor-codigo: PR #55 head f9149ce — aprovado

> Parecer do revisor-codigo (subagente do gerente-projetos; gravado pelo gerente sem alteração).

# Revisão PR #55 — T-0017 — head f9149ce68babbf9d22477d26b2d3a61c8513bfa0

Branch `gerente-projetos/T-0017-regras-cobranca`. Diff contra origin/main: só `docs/produto/03-regras.md` (+5 −1). Os 2 commits trazem `Agente: gerente-projetos`. Desde o 8266aa2 só mudou a linha 40 (RN-POS-001).

Parecer: **aprovado** (0 🔴, 0 🟡). Os 🟢 ficam a critério do autor.

## O 🟡 anterior caiu
- `03-regras.md:40` (RN-POS-001) agora diz: "celular: 55 + DDD + 9 dígitos; fixo sai com aviso; número repetido ou ausente fica vazio, com aviso". Isso bate com `cobranca_whatsapp.celular()`, que devolve o fixo com "telefone fixo: pode não ter WhatsApp" e o vazio com "telefone inválido (repetido)" ou "sem telefone no cadastro".

## 🟢 (sugestões, não bloqueiam)
- `03-regras.md:40` — o texto não diz que o celular de 8 dígitos (começando com 6 a 9) ganha o 9, como faz `celular()`. "Com títulos VENCIDOS" pode ser lido como filtro, mas `fila()` inclui todo cliente INADIMPLENTE. Falta "do maior para o menor" na ordenação.
- `03-regras.md:42` (RN-POS-003) — "(dado digitado, regra 7)": o diário da cobrança não está na lista nominal da regra 7 do CLAUDE.md. Cite a fonte ou peça a inclusão ao dono.
- `03-regras.md:42` — retenção no Render e nome de arquivo são infraestrutura. Quando o Adendo 3 da ADR 0001 sair, deixe na RN só a referência a ele.
- `03-regras.md:37–43` — as RN numeradas estão misturadas com bullets sem número. Um subtítulo "Cobrança no WhatsApp" ajudaria.

## Redundância
Nenhuma regra foi reescrita: nada no doc 03 nem em `docs/decisoes/` trata de cobrança, e a RN-GER-005 só ganhou a distinção (fiel à decisão 7 A, como em `bap_dados.titulos_sem_internos` e `email_inadimplencia.COD_TESTE`). Risco futuro: RN-POS-003/004 × Adendo 3 da ADR 0001.

## Checklist
- Fiel às decisões 1 a 7 A do R-20261124-192008-alexandre: sim.
- Escopo: o PR mexe só no doc 03, sem mudança a mais.
- Dado pessoal: nenhum. Segredos: nenhum. Dados digitados, `.json` da raiz e `bap_dados.VERSAO` ficam intocados.
- Testes e tela: não se aplicam (só doc).
- `verificar gerente-projetos --base origin/main` no head f9149ce (worktree): OK, sem violação.
