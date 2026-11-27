# T-0050 · Revisão de marca · simulação do acesso aos faróis (tela Usuários do site)

- **Revisor:** design-de-marca · **Data:** 27/11/2026 (Manaus)
- **O que foi revisto:** a simulação do designer-ux em `recados/anexos/T-0050/sim/` (os 17 PNGs e o `LEIAME.md`), a folha proposta `sim/proposta/sim-farois.css` e o gerador `sim/proposta/gera.js` (o HTML das telas).
- **Base:** `docs/marca/manual.md` (aprovado em 26/11/2026, R-20261126-182227-alexandre) e o `:root` do `web/app/static/estilo.css` do repositório.
- **Vale para:** os arquivos de `sim/` gravados em 27/11/2026 às 10:23. Ainda não há PR. No PR do modulo-web, o parecer é refeito no head SHA.

## Resultado: liberado com ajustes

**Sem 🔴.** Nada fere o manual a ponto de segurar a simulação: o po pode levar ao Alexandre.
São **5 🟡**, todos de tipografia ou de papel da cor, a corrigir no CSS antes do merge, e **3 🟢**.

## O que está certo

| Item | Situação |
|---|---|
| **Cores** | ✓ A folha proposta usa só variáveis do `:root`, sem nenhum hex solto. Usa `--verde-claro`, `--verde-escuro`, `--cartao`, `--borda`, `--fundo`, `--texto`, `--suave`, `--raio`, `--t-corpo`, `--t-rotulo` e `--alvo`. Nenhum azul, laranja nem cor "quase igual" |
| **"liberado"** | ✓ `--texto` sobre `--verde-claro`: 13,31:1. É o uso que o manual manda (§4.2, "só com `--texto`"). Não usa `--verde-escuro` sobre `--verde-claro` (4,44:1, proibido no §4.4) |
| **"tirado"** | ✓ Nome riscado em `--suave` sobre `--cartao`: 5,59:1. Marca "tirado" em `--suave` sobre `--fundo`: 5,06:1. Selo da linha em `--texto` sobre `--fundo`: 13,91:1. Toda marca tem palavra: a cor nunca é a única pista |
| **Cores de farol** | ✓ Nenhum verde, amarelo ou vermelho de farol como enfeite. O vermelho fica no "Desativar" (`--erro`, o papel do §4.1) e no erro do topo (`--erro` sobre `--fundo`, 5,96:1). O amarelo fica no selo "Troca de senha pendente", que já existe |
| **Botão principal** | ✓ "Novo usuário" é o único botão cheio de verde (`--verde-escuro` com texto branco, 5,12:1). "Salvar acesso" e "Criar" são neutros (`.bt-neutro`), como o "Salvar senha" de hoje. O "Faróis" aberto é o único ponto a ajustar (🟡 MC-0028) |
| **Caixa de marcar** | ✓ `accent-color: --verde-escuro`, com o visto branco: 5,12:1. É controle de formulário, não botão, e não compete com o "Novo usuário" |
| **Letra** | ✓ Inter (a pilha `--fonte`), pesos 400, 600 e 700. Os ajustes de tamanho e de peso estão nos 🟡 |
| **Logo e nome** | ✓ Logo inteiro na placa preto BAP, com "BAP Central" e "BAP AUTOPARTS", no PC e no topo do celular (§3.3). A aba do navegador mostra "Usuários · BAP AUTOPARTS" (§7). A faixa BC3 não muda |
| **Nomes de produto** | ✓ "Painel Executivo", o nome único do §2 (12 A), na lista, no texto do "só o Resumo" e na confirmação |
| **Tom de voz** | ✓ Direto, verbo na frente, sem jargão: "Desmarque para tirar.", "Liberar além do perfil", "Salvar acesso", "marque ao menos um farol. Para tirar todo o acesso, use Desativar." e "Não deu para salvar agora. Tente de novo em 1 minuto." |
| **"BAP AUTOPARTS"** | ✓ Aparece onde o manual pede (placa e aba). A tela não gera PDF, e-mail nem Excel novos, então não há outro lugar onde ele precise entrar |

## 🟡 Corrigir antes do merge (dono: modulo-web, ao aplicar a folha; designer-ux ajusta a proposta)

| ID | Onde | Tipo | Fere | Correção (antes → depois) |
|---|---|---|---|---|
| MC-0028 | `sim-farois.css:4` · botão "Faróis" aberto (`2-farois-aberto-pc.png`, `5-erro-nenhum-farol-pc.png`) | cor | §4.2 (papel do `--verde-claro`) e a regra da tela: um só botão verde | Aberto, o "Faróis" vira um segundo botão verde, com fundo `--verde-claro` e borda `--verde-escuro`. Fica na mesma linha e com o mesmo fundo do selo "1 farol liberado": o verde-claro passa a dizer duas coisas na mesma tela. `.u-farois[open]>summary{background:var(--verde-claro);border-color:var(--verde-escuro)}` → `.u-farois[open]>summary{background:var(--fundo);border-color:var(--suave)}` (borda `--suave` sobre `--cartao`: 5,59:1). Com isso, o verde-claro fica só no "liberado" |
| MC-0029 | `sim-farois.css:29` e `:51` · "Salvar acesso" e "Criar" (`2-farois-aberto-pc.png`, `4-novo-usuario-pc.png`) | tipografia | §5: botão com 14 px e peso 600, e o mesmo papel com o mesmo tamanho | Os dois saem com 16 px: o `button` herda o corpo, e o `.bt-neutro` não fixa o tamanho. Os outros botões da linha ("Faróis", "Trocar senha") têm 14 px. `.f-rodape button{min-height:36px}` → `.f-rodape button{min-height:36px;font-size:var(--t-corpo)}` |
| MC-0030 | `sim-farois.css:14` · títulos "Do perfil Vendas" e "Liberar além do perfil" | tipografia | §5: o título de bloco tem 16 px e peso 600. A escala não tem a combinação 14 px com 700 | `.f-parte>legend{…font-size:var(--t-corpo);font-weight:700…}` → `.f-parte>legend{…font-size:16px;font-weight:600…}` |
| MC-0031 | `sim-farois.css:16` e `:28` · nota "Desmarque para tirar." e "Alterado em … por …" | tipografia | §5: apoio, data e rodapé têm 12 px. O 12,5 px não existe na escala | `.f-nota{…font-size:12.5px…}` → `font-size:12px`; `.f-quando{…font-size:12.5px…}` → `font-size:12px` |
| MC-0032 | `sim-farois.css:33` · selos da linha (`3-salvo-pc.png`: "1 farol tirado" ao lado de "2 faróis liberados") | tipografia | §5: o mesmo papel tem sempre o mesmo peso | O `.selo-tirado` baixa o peso para 600, e o `.selo-liberado` fica com o 700 do `.selo`, como o "Desativado" e o "Troca de senha pendente". Lado a lado, os dois selos ficam com pesos diferentes. `.selo-tirado{…color:var(--texto);font-weight:600}` → `.selo-tirado{…color:var(--texto)}` (tira o `font-weight:600`) |

## 🟢 Observações (não seguram)

| ID | Onde | Tipo | Observação |
|---|---|---|---|
| MC-0033 | `sim-farois.css:19` · títulos de grupo do painel ("VENDAS", "DIRETORIA") | tipografia | O manual (§5) pede +4% de espaço entre letras no rótulo de 11 px: `letter-spacing:.07em` → `.04em`. A proposta copia o título de grupo do menu (`estilo.css:370`, `.bc3-grupo small`, também com `.07em`), e é bom que os dois fiquem iguais. O certo é trocar os dois juntos, numa limpeza do modulo-web; não precisa ser nesta tarefa |
| — | `sim-farois.css:8` · sombra do painel | cor | Usa `--c-0000001f`, um dos tokens de "demais cores" que ainda esperam a consolidação do MC-0006. É a mesma sombra dos outros painéis da tela. Sem ação aqui |
| — | `.selo` (`estilo.css:245`) | tipografia | O selo base tem `.78rem` (12,48 px), fora da escala do §5. É dívida anterior a este PR e vale para todos os selos do site. Fica para a limpeza do MC-0006, não para a T-0050 |

## Fora do escopo da marca (para o gerente-projetos encaminhar; não catalogado aqui)

- **Texto de interface, do designer-ux e do corretor-redundancias:** a confirmação "Painel Executivo liberado; Roteirização tirado." faz a concordância pelo farol, e não pelo nome. Lida em voz alta, "Roteirização tirado" soa errado. Uma opção é "Painel Executivo: liberado; Roteirização: tirado.". A voz da marca não é afetada.
- **Layout, do designer-ux:** no PC, a marca "liberado" do Painel Executivo quebra para a linha de baixo (`2-farois-aberto-pc.png`), e a do Pedidos fica na mesma linha. Não é marca.

## Reteste

Ao aplicar, mande os PNGs do PC e do celular nos estados 2 (painel aberto), 3 (salvo) e 4 (novo usuário), já com os 5 🟡 corrigidos, no head SHA do PR do modulo-web. Confiro no print e fecho os MC-0028 a MC-0032.

---

## Reteste da v2 (27/11/2026, arquivos de `sim/` gravados às 10:34)

**Resultado: aprovado.** Não sobra nenhum 🔴 nem 🟡. Os MC-0028 a MC-0032 estão fechados, e ficam abertos só os 🟢, que não seguram nada.

Conferi a `proposta/sim-farois.css` v2, o `proposta/gera.js` e os PNGs: `2-farois-aberto-pc`, `2-farois-aberto-cel-b`, `3-salvo-pc`, `4-novo-usuario-pc` e `7-farois-trade-pc`.

| ID | Situação | Evidência |
|---|---|---|
| MC-0028 | ✓ fechado | `.u-farois[open]>summary{background:var(--fundo);border-color:var(--suave)}`. No `2-farois-aberto-pc.png`, o "Faróis" aberto fica cinza-gelo com borda `--suave`. O verde-claro fica só no "liberado", e "Novo usuário" é o único botão verde da tela |
| MC-0029 | ✓ fechado | `.f-rodape button{min-height:36px;font-size:var(--t-corpo)}`. Nos prints, "Salvar acesso" e "Criar" ficam com o mesmo tamanho de "Faróis" e "Trocar senha" |
| MC-0030 | ✓ fechado | `.f-parte>legend{…font-size:16px;font-weight:600…}`: "Do perfil" e "Liberar além do perfil" seguem o título de bloco do §5 |
| MC-0031 | ✓ fechado | `.f-nota` e `.f-quando` com 12 px |
| MC-0032 | ✓ fechado | O `.selo-tirado` ficou sem `font-weight`. No `3-salvo-pc.png`, "1 farol tirado" e "2 faróis liberados" têm o mesmo peso dos outros selos da linha |

**O que mudou além dos achados, conferido na marca:**
- **Marca no painel:** o "tirado" e o "liberado" do painel passaram a usar o próprio `.selo selo-tirado` / `.selo selo-liberado`, o mesmo selo da linha (mesmo papel, mesmo tamanho e mesmo peso). Cores: "liberado" em `--texto` sobre `--verde-claro`, 13,31:1; "tirado" em `--texto` sobre `--fundo`, com borda `--borda`, 13,91:1. O nome riscado continua em `--suave`, 5,59:1.
- **Tokens:** a folha continua só com tokens. Nenhum hex novo. A sombra do "Novo usuário", que agora abre por cima da lista, é a mesma `--c-0000001f` dos outros painéis.
- **Confirmação:** "Acesso de … salvo. Liberado: Painel Executivo. Tirado: Roteirização." O texto ficou neutro, direto e sem problema de concordância. Está no `p.ok`, `--verde-escuro` sobre `--fundo`: 4,64:1.
- **Perfil sem farol:** "Este perfil ainda não tem farol no site." (`7-farois-trade-pc.png`), no tom do §6.
- **Marca e nomes:** a placa do logo, "BAP AUTOPARTS" e "Painel Executivo" não mudaram.

**🟢 que continuam abertos (não seguram):**
- **MC-0033:** o título de grupo usa `letter-spacing:.07em`; o manual pede `.04em`. Trocar junto com o `.bc3-grupo small`, numa limpeza futura.
- A sombra usa `--c-0000001f` e o `.selo` base tem 12,48 px. As duas são dívidas anteriores, para a limpeza do MC-0006.

**Vale para:** a simulação v2. No PR do modulo-web, confiro de novo no head SHA, com os prints do navegador, que o CSS aplicado é igual a esta proposta.
