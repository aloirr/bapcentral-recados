---
id: R-20261120-100338-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: alta
tarefa: T-0001
responde_a: R-20261120-080000-alexandre
encerra: true
contrato: null
criado_em: 2026-11-20T10:03:38-04:00
---
# T-0001 concluída: a montagem do time na nuvem está conferida

## Entregue
- Crit. 1 ✅ `node --test` da CLI e dos guardiões: 139/139.
- Crit. 2 ✅ leitura pela CLI (`caixa`, `pendencias`, `ler`, `fio`); gravação por git no `main` dos recados (R-20261120-092924-alexandre); o token não aparece em nenhuma saída.
- Crit. 3 ✅ ida e volta po ↔ gerente: R-20261120-091217-po, respondido com `encerra` no R-20261120-091442-gerente-projetos.
- Crit. 4 ✅ o guardião barra o po em `relatorios_nucleo.py` e libera o modulo-farois.
- Crit. 5 ✅ a issue aloirr/bapcentral-recados#2 virou o recado R-20261120-095950-alexandre, que chegou na caixa do gerente. O formulário aceita a conta aloirr desde o merge `de3f2ec`.
- Crit. 6 ✅ `verificar --por-dono` limpo.
- Também no main do código:
  - correção do ci.yml (PR #3, `8cd54cb`);
  - fluxo po ↔ gerente no doc 07 (PR #1, `4a2d351`);
  - desenho da T-0007 (PR #2, `c96a153`).

## Em andamento
- T-0007: código do coord.mjs, na sessão de governança.
- T-0008: po.md, gerente-projetos.md e donos.json, na sessão de governança.
- T-0004: falta o `smoke_processos` no CI.

## O que o time pede a você
- T-0009 (guardião aceita `de: alexandre` do po no clone dos recados): sim ou não.
- As frases de merge da T-0007 e da T-0008, quando os PRs ficarem prontos.

## Próximo passo
- Seguir o quadro: T-0002, T-0003, T-0005 e T-0006, como pede o R-20261120-080000-alexandre.

## Como testar em 5 passos
1. `node scripts/coord.mjs caixa gerente-projetos`: o R-20261120-095950-alexandre aparece lido.
2. `node scripts/coord.mjs fio R-20261120-091217-po`: aparece a resposta com `encerra`.
3. Abra uma issue pelo formulário "Recado" na conta aloirr: em menos de 1 min vira recado e a issue fecha.
4. Veja o CI de um PR qualquer no aloirr/bapcentral: o job `conferir` roda os 8 passos.
5. `git log origin/main --oneline -4` no aloirr/bapcentral: aparecem `c96a153`, `4a2d351` e `8cd54cb`.
