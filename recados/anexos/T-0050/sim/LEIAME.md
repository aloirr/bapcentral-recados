# T-0050: simulação da tela Usuários com o acesso aos faróis (designer-ux, v2 de 27/11/2026)

O que está simulado: o desenho do engenheiro-software (§8.1), com P1 = B e as recomendações A de P2, P3 e P4 (o liberado vê só o Resumo; o Painel Executivo está na lista; farol novo do perfil chega marcado).
- A v2 aplica os 🟡 de `../revisao-ux.md` (1 a 4) e de `../revisao-marca.md` (MC-0028 a MC-0032), mais os pedidos do gerente sobre textos e layout.
- Dados 100% fictícios: `admin.ficticio` e `usuario.ficticio.01` a `08`.
- Usa o `estilo.css` do `main` e a folha de proposta `proposta/sim-farois.css` (só tokens do manual), que o modulo-web aplica depois do "aprovo". O gerador é `proposta/gera.js`.
- Os faróis são os do PR #158: Painel + 14, agrupados como no menu. O perfil Trade ainda não tem farol no site.
- PC 1366×768 e celular 390×844, deviceScaleFactor 2, pt-BR, America/Manaus.

**Medição** (todas as telas, pelo gerador):
- No PC, a página fica em **768 px** em todos os estados, inclusive com o painel do Admin aberto e com o "Novo usuário" aberto.
- Nenhuma rolagem lateral, nem a 1366 nem a 390.
- No celular, todo alvo tem 44 px ou mais.
- **Nenhum selo quebra de linha** a 1366 nem a 390. A conferência foi feita com todos os selos à vista, no pior caso.

## Imagens

| Arquivo | O que mostra |
|---|---|
| `antes-depois-pc.png` | Antes (hoje) × depois, a 1366, com o painel Faróis aberto |
| `antes-depois-cel.png` | Antes × depois no celular: a lista com o botão Faróis e os selos |
| `0-antes-usuarios-{pc,cel}.png` | A tela de hoje, com os mesmos usuários fictícios |
| `1-usuarios-lista-{pc,cel}.png` | A lista: botão "Faróis" em toda linha; selos "1 farol liberado" (03) e "1 farol tirado" (05) |
| `2-farois-aberto-pc.png` | Painel do 03 (Vendas). "Do perfil", com Roteirização desmarcada ("tirado"). "Liberar além do perfil", com o Painel Executivo e Pedidos marcados ("liberado"). No pé, "Alterado em … por …" e "Salvar acesso" |
| `2-farois-aberto-cel-{a,b}.png` | O mesmo no celular: (a) o começo; (b) o fim, com "Alterado em" no fluxo e só o "Salvar acesso" fixo no pé |
| `3-salvo-{pc,cel}.png` | A confirmação: "Acesso de usuario.ficticio.03 salvo. Liberado: Painel Executivo. Tirado: Roteirização.", com os selos da linha já atualizados |
| `4-novo-usuario-{pc,cel-a,cel-b}.png` | "Novo usuário" com o perfil Pré-venda. No PC, abre por cima da lista. No celular, entra no fluxo |
| `5-erro-nenhum-farol-{pc,cel-a,cel-b}.png` | O erro de quem desmarca tudo, no lugar das mensagens, com o painel reaberto como ficou |
| `6-farois-admin-{pc,cel-a,cel-b}.png` | Admin, que vê os 15 faróis. Só existe a parte "Do perfil", então ela usa a largura toda, com os 5 grupos em colunas. O mesmo vale para Diretor, Gerente e Analista |
| `7-farois-trade-{pc,cel-a,cel-b}.png` | Trade, perfil sem farol no site: "Do perfil" diz "Este perfil ainda não tem farol no site.", e a parte "Liberar" traz os 15. Pedidos aparece marcado, ainda sem salvar |

## O que mudou da v1 para a v2

| Origem | Mudança |
|---|---|
| UX 1 | Sem a parte "Liberar", os grupos de "Do perfil" ficam em 5 colunas na largura toda (no celular, 1). O painel do Admin cabe em 768 px, com o "Salvar acesso" à vista (`6-*`) |
| UX 2 | O "Novo usuário" abre por cima da lista no PC, como o painel Faróis, e a página fica em 768 px. A D4 sai: não há exceção à §7.4 |
| UX 3 | A legenda é só "Do perfil": saíram o nome do perfil e a contagem |
| UX 4 / MC-0031 | As marcas "tirado" e "liberado" do painel são o próprio `.selo selo-tirado` / `.selo selo-liberado` da linha. O apoio ("Desmarque para tirar.", a nota do Resumo, "Alterado em") fica em 12 px |
| MC-0028 | Aberto, o "Faróis" fica com `--fundo` e borda `--suave`, sem verde. O verde-claro fica só no "liberado" |
| MC-0029 | "Salvar acesso" e "Criar" com `--t-corpo` (14 px), como os outros botões |
| MC-0030 | Títulos "Do perfil" e "Liberar além do perfil" com 16 px e peso 600 |
| MC-0032 | `.selo-tirado` sem `font-weight:600`: fica com o peso do `.selo` |
| Texto | A confirmação não depende mais do gênero do farol: "Acesso de <login> salvo. Liberado: Painel Executivo. Tirado: Roteirização." Com vários: "Liberado: Pedidos, Painel Executivo." |
| Layout | Na parte "Liberar", os grupos se distribuem em 3 colunas equilibradas (CSS `columns`, o grupo não se parte). O "liberado" cabe ao lado do nome a 1366 |
| Layout | Celular: o pé fixo tem só o "Salvar acesso" (~60 px), com uma linha fina em cima. O "Alterado em" vai para o fluxo, acima do pé. O último farol fica à vista |
| Layout | Celular: a divisória entre as partes passou para a legenda, e "Liberar além do perfil" não fica mais cortada |
| Layout | PC: uma linha só separa as caixas do pé ("Alterado em" e "Salvar acesso" na mesma altura) |
| Novo estado | Trade (perfil sem farol no site) e Admin (15 faróis do perfil) simulados |

## Decisões de UX (valem na v2)

1. **Um botão "Faróis" por linha**, antes de "Trocar senha", em todos os usuários. O admin pode tirar faróis de si; Usuários e Trocar senha não estão na lista.
   - O painel abre embaixo da linha, na largura da lista, por cima das linhas seguintes. No celular, entra no fluxo.
   - Fluxo em 3 toques: Faróis → marcar → Salvar acesso.
2. **Duas partes:** "Do perfil" ("Desmarque para tirar.") e "Liberar além do perfil".
   - Os grupos seguem a ordem do menu: Diretoria, Pré-venda, Pós-venda, Vendas, Analista Comercial e Trade, quando entrar. Grupo vazio não aparece.
   - Quem vê tudo pelo perfil só tem "Do perfil".
3. **A marca do que difere do perfil é sempre um selo com texto:**
   - tirado: nome riscado + selo "tirado";
   - liberado: selo "liberado".
   - Aparece e some na hora, só com CSS `:has`.
4. **O "só o Resumo" é dito uma vez**, embaixo de "Liberar além do perfil": "Liberado, o farol abre só no Resumo: sem as tabelas de clientes e sem Exportar. O Painel Executivo abre completo."
   - Se a P4 sair B: "Liberado, o farol abre completo, menos Cobrar, edição e TOTAL A PAGAR.".
5. **Selos na linha:** "n farol tirado / n faróis tirados" e "n farol liberado / n faróis liberados". Sem selo, o usuário segue o perfil. No celular, os selos descem para uma linha própria.
6. **"Alterado em dd/mm/aaaa hh:mm por <admin>"** no pé do painel, só quando há registro.
7. **Confirmação = a mensagem de retorno** (`p.ok` de hoje, no topo), sem passo extra antes de salvar. O painel fecha e os selos mostram o novo estado.
8. **Botões:**
   - "Novo usuário" é o único principal (verde);
   - "Salvar acesso" e "Criar" são neutros;
   - no celular, "Salvar acesso" fica fixo no pé enquanto o painel está aberto.
9. **Faixa sem número novo:** Ativos · Desativados · Troca pendente (tela-bc3 §4.2).
10. **Novo usuário:**
    - Usuário, Perfil e Senha numa linha no PC, e as duas partes embaixo.
    - Ao trocar o perfil, as partes se refazem (`usuarios.js` do desenho).
    - Sem JS, vale o texto do §8.1: "Os faróis do perfil entram sempre; marque só os liberados a mais."
11. **Erros** (no `p.erro` de hoje, no topo, com o painel reaberto):
    - nenhum farol: "<login>: marque ao menos um farol. Para tirar todo o acesso, use Desativar.";
    - farol desconhecido (400): "A lista de faróis mudou. Abra a tela de novo e salve outra vez.";
    - falha de gravação (503): "Não deu para salvar agora. Tente de novo em 1 minuto.".
12. **Movimento:** o painel aparece em 160 ms, sem animação com "reduzir movimento". O farol liberado aparece no menu do usuário como os outros, sem marca.

## Fora da v1 (decisão do gerente)

- **D2:** histórico completo e **D3:** "Voltar ao perfil": não entram.
- **D1:** os rótulos "Analista" e "Trade" vão no código da T-0036. A simulação já os usa.
- **D4:** resolvida pelo UX 2.
