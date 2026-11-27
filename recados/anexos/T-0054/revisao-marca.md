# T-0054 · Parecer de marca (design-de-marca)

- **Entrega:** edição do Farol de Entregas no site pelo pós-venda.
- **Head revisado:** `1862a53085d24681118e7e109ba4f29579116893` (branch `modulo-web/T-0054-entregas-edicao`), diff `origin/main...1862a53 -- web/app`.
- **Base:** `docs/marca/manual.md` (selo [VALE]).
- **Condição do po:** R-20261127-104942-po (print do head final com os 2 ajustes de CSS e parecer sem 🔴).
- **Data:** 27/11/2026.

## Parecer: liberado com ajustes (sem 🔴)

Um 🟡 de uma palavra, que recomendo corrigir no mesmo PR: o token do campo recusado. Os dois 🟢 não seguram a entrega.

## Prints do head final

Gerados com os roteiros do revisor-ux (`sim3.py` e um roteiro de medição na mesma linha do `shots3.mjs`), a partir do `git archive 1862a53 web`, com Playwright `channel: 'chromium'`, `--lang=pt-BR` e dados fictícios. Ficam em `recados/anexos/T-0054/sim/`:

| Arquivo | O que mostra |
|---|---|
| `posvenda-entregas-final-pc.png` | NF 900502 com "Editar" e, abaixo, "Aguardando o PC" **numa linha só** (medido: 114 × 18 px, `white-space: nowrap`) |
| `posvenda-entregas-final-cel.png` | Cartão aberto: botão "Editar" (88 × 44 px) e a marca "Aguardando o PC" ao lado, numa linha |
| `posvenda-edicao-erro-final-pc.png` | Erro real do código (responsável com CPF): mensagem em vermelho e o campo "Responsável (motorista)" com contorno vermelho |
| `posvenda-edicao-erro-final-cel.png` | O mesmo no celular (390 px, sem estouro de largura) |

Observação sobre o print: o campo de data aparece como `mm/dd/yyyy` e `11/08/2026`. É coisa do Chromium sem interface, que não aplica o idioma ao seletor de data. No navegador do usuário sai `dd/mm/aaaa`, como nos prints `ux-edicao-ptbr-*` do revisor-ux. Não é achado de marca.

## Checklist

| Item | Resultado | Medido no head |
|---|---|---|
| A. Hex novo no diff | Conforme | Nenhum hex nas linhas adicionadas de `web/app`; tudo por `var(--…)` |
| A. Marca "Aguardando o PC" (`.ed-marca.ed-pend`) | Conforme | Texto `--atencao-texto` #8A5A00 sobre `--atencao-claro` #FFF4D6: 5,41:1 (manual 4, tabela de contraste). Papel certo: "texto em atenção" |
| A. Campo recusado | **🟡 MC-0054-1** | Cor certa (#B42318) e contraste de 6,57:1 sobre `--cartao` (≥ 3:1 de contorno), mas pelo token **errado**: `--alerta` |
| A. Botão "Editar" (`.bt-ed`) | Conforme | Branco sobre `--verde-escuro` #2F7D32: 5,12:1. Papel "botão" do `--verde-escuro` |
| C. Tamanho da marca | Conforme | `.72rem` (11,5 px, fora da escala) → `.75rem` = 12 px, na escala (12 px). Fica igual ao botão "Editar" ao lado |
| C. Família e peso | Conforme | Pilha Inter; peso 600 (dentro de 400/600/700) |
| E. Aplicação | Conforme | Mesma casca BC3 (placa do logo, faixa verde, cartões) no PC e no celular; "BAP AUTOPARTS" na placa |
| F. Voz | Conforme | "Aguardando o PC", "Edição enviada: aguardando o PC." e "Editar" são diretos e sem jargão. A mensagem de erro é texto de interface (designer-ux) |

## Achados

| ID | Onde | Tipo | Fere | Gravidade | Correção | Dono |
|---|---|---|---|---|---|---|
| MC-0054-1 🟡 | `web/app/static/estilo.css`, regra nova `.ed-campo [aria-invalid="true"]` (por volta da linha 348 no head) | cor | Manual 4, paleta: `--erro` = "mensagem de erro, **campo com erro**"; `--alerta` = "número e ponto vermelhos do **farol**". Checklist A: o vermelho do farol só no farol | baixa (o hex é o mesmo, então o usuário não vê diferença; o problema é o papel do token) | `border-color:var(--alerta);box-shadow:0 0 0 1px var(--alerta)` → `border-color:var(--erro);box-shadow:0 0 0 1px var(--erro)` | modulo-web |
| MC-0054-2 🟢 | `estilo.css`, `.ed-erro{background:var(--alerta);…}` (anterior a este diff) | cor | Manual 4, mesmo motivo | baixa | `var(--alerta)` → `var(--erro)` na marca de edição recusada. Pode ir junto do MC-0054-1 | modulo-web |
| MC-0054-3 🟢 | `.bt-ed` e `.ed-marca`: 12 px com peso 600 | tipografia | Manual 5: a escala tem 12 px com peso 400 ("apoio") e o botão com 14 px/600; não tem o papel "botão ou selo compacto" | baixa, sem ação nesta tarefa | Nada a mudar agora. O design-de-marca leva ao Alexandre o registro do papel "selo/botão compacto de tabela: 12 px, peso 600" na próxima revisão do manual | design-de-marca |

Fora do escopo de marca, só para registro do revisor-ux: no print de erro, o "Salvar" parece mais leve que o "Cancelar". Não está no diff.

## Validade

Vale para o head `1862a53`. Se o MC-0054-1 for corrigido só com a troca do token (`--alerta` → `--erro`), o parecer continua valendo para o novo head sem reteste visual, porque o hex é o mesmo. Qualquer outra mudança de CSS pede reteste.
