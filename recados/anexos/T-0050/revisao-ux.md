# T-0050 · Revisão de UX, redundância e marca · simulação da tela Usuários com o acesso aos faróis

- **Revisor:** designer-ux (UX e marca) · **Data:** 27/11/2026 (Manaus)
- **Desenho revisado:** `docs/desenho/T-0050.md` na branch `engenheiro-software/T-0050-desenho`, **head SHA `8a91c11cd4f052775fafc58128cade29460434be`** (§8.1, P1 = B; P2 a P4 simuladas com A).
- **Simulação revisada:** `recados/anexos/T-0050/sim/` (ainda sem commit no repositório de recados). Para rastrear: `LEIAME.md` sha256 `226c213dd0f8…`, `proposta/sim-farois.css` `d0eea4415d0a…`, `proposta/gera.js` `db3d79f5e5c5…`. O `estilo.css` é o do `main` (`origin/main` em `ed324ca`, igual ao de `ce7149e`).
- **Referências:** `.coord/contratos/tela-bc3.md` v1 (§1, §4.2, §7.4, §8, §11, §12, §13.4, §15) e `docs/marca/manual.md` (§4 e §5).
- **Como medi:** rodei o `gera.js` de novo numa cópia fora do repositório, com o `estilo.css` e as fontes do `main`. Os números batem com os do designer. Depois medi os casos que não estavam nos PNGs: o painel aberto de cada perfil, a 1920×1080 e a linha de baixo.
- **PNGs desta revisão:** em `ux/`, gerados com os mesmos usuários fictícios.
  - `antes-1-admin-farois-pc.png` × `depois-1-admin-farois-pc.png`.
  - `depois-1-vendas-farois-pc.png`.
  - `depois-2-novo-usuario-pc.png`; o antes é o `sim/4-novo-usuario-pc.png`.
  - `medida-1920-farois-aberto.png`.
  - A folha `ux/sugestao.css` é só uma maquete; quem aplica é o modulo-web.

## Resultado

**Sem 🔴.** A simulação pode ir ao po para aprovação por delegação.
Ficam **5 🟡**, a corrigir na própria proposta ou no PR do código, e **9 🟢**. O 🟡 1 e o 🟡 2 mudam o desenho da tela. Convém o po ver os PNGs `depois-*` junto com a simulação.

## O que está certo

- **Largura:** não há rolagem lateral em nenhum caso. Medi a 1366, a 1920 e a 390, com o painel aberto e fechado, no "Novo usuário" e no erro (`scrollWidth ≤ clientWidth` no documento e em toda caixa).
- **Alvos no celular:** todos têm 44 px ou mais, inclusive a linha inteira de cada caixa de marcar (`.f-item` com `min-height: var(--alvo)`), o "Salvar acesso", o "Criar", os campos e o "Desativar". No PC, os botões têm 36 px, que é o padrão do PC.
- **Regra dos 3 toques:** Faróis → marcar → Salvar acesso, sem confirmação no meio. No celular, o "Salvar acesso" fica fixo no pé da tela, então não é preciso rolar até ele. A confirmação é o `p.ok` de hoje, e os selos da linha se atualizam.
- **Marca:**
  - nenhum hex fora do `:root`, sem azul e sem laranja;
  - só tokens do manual: `--verde-claro`, `--verde-escuro`, `--texto`, `--suave`, `--fundo`, `--borda`, `--cartao`, `--raio`, `--alvo`, `--t-corpo`, `--t-rotulo`;
  - a sombra usa o `--c-0000001f`, o mesmo dos painéis `u-det` de hoje;
  - o logo inteiro na placa preto BAP e "BAP AUTOPARTS" escrito certo;
  - a faixa segue o degradê `--faixa-inicio` → `--faixa-fim`, com texto branco;
  - um só botão principal ("Novo usuário"); "Salvar acesso" e "Criar" são neutros, e o "Desativar" continua como perigo, com confirmação.
- **Contraste dos pares novos** (pela tabela do manual, §4.3):

  | Par | Contraste |
  |---|---|
  | "tirado" e nome riscado: `--suave` sobre `--fundo` | 5,06:1 |
  | `--suave` sobre `--cartao` | 5,59:1 |
  | "liberado": `--texto` sobre `--verde-claro` | 13,31:1 |
  | "Faróis" aberto: `--texto` sobre `--verde-claro` | 13,31:1 |
  | Caixa marcada: `accent-color` `--verde-escuro` | 5,12:1 |

- **Cor nunca sozinha:** o tirado leva o nome riscado mais a palavra "tirado". O liberado leva a palavra "liberado". Os selos da linha têm texto.
- **Faixa:** sem número novo; ficam Ativos · Desativados · Troca pendente (tela-bc3 §4.2).
- **Textos:** são curtos, com o verbo na frente e sem jargão: "Faróis", "Desmarque para tirar.", "Liberar além do perfil", "Salvar acesso", "Alterado em … por …".
  - A frase do "só o Resumo" aparece uma vez só, e não em cada farol.
  - O código do farol (`rid`) não aparece em lugar nenhum.
  - O erro "marque ao menos um farol. Para tirar todo o acesso, use Desativar." diz o que fazer.
- **Dados:** só `admin.ficticio` e `usuario.ficticio.01` a `.08`. Não há CNPJ, nome, telefone nem e-mail, nem nos PNGs nem no `gera.js`.
- **Celular:** os selos descem para uma linha própria, e o login não quebra. O painel entra no fluxo da página, e a §7.4 já aceita que um formulário role no celular.
- **1920×1080:** cabe com folga. O painel de Vendas vai até 710 px (`ux/medida-1920-farois-aberto.png`).

## 🟡 Corrigir antes do merge

### 1. Em 4 dos 8 perfis, o painel "Faróis" passa da tela no PC, e o "Salvar acesso" some
- **Tela:** Usuários, PC 1366×768, com o painel aberto para Admin, Diretor, Gerente ou Analista. Esse caso não foi simulado: os PNGs mostram só o usuário de Vendas.
- **Problema:** esses perfis veem os 15 faróis. Por isso o painel tem só a parte "Do perfil", que fica presa na 1ª coluna da grade (`.f-partes`: `minmax(200px,.8fr) minmax(0,3fr)`), com uns 220 px de largura.
  - Os 5 grupos ficam empilhados numa coluna estreita, com o resto do painel vazio.
  - O painel chega a 695 px de altura, a página a 910 px, e o "Salvar acesso" fica abaixo da dobra (`ux/antes-1-admin-farois-pc.png`).
- **Regra quebrada:** tela-bc3 §1.2 ("cabe numa tela no PC"), e a regra dos 3 toques (é preciso rolar antes de salvar).
- **Correção:** quando não há a parte "Liberar", a parte "Do perfil" ocupa a largura toda, com os grupos em 5 colunas. No celular, fica 1 coluna. O painel cai para 297 px, e a página fica em 768 (`ux/depois-1-admin-farois-pc.png`):
  ```css
  .f-partes:not(:has(.f-lib)){grid-template-columns:minmax(0,1fr)}
  .f-partes:not(:has(.f-lib)) .f-perfil .f-grupos{grid-template-columns:repeat(5,minmax(0,1fr))}
  @media(max-width:700px){.f-partes:not(:has(.f-lib)) .f-perfil .f-grupos{grid-template-columns:1fr}}
  ```
- **No PR do código:** levar um PNG do painel do admin aberto.

### 2. D4: o "Novo usuário" aberto leva a página a 1074 px no PC
- **Tela:** Usuários, PC 1366×768 (`sim/4-novo-usuario-pc.png`).
- **Regra quebrada:** a tela-bc3 §7.4 só aceita formulário rolando **no celular** e diz "Nenhuma outra". Para abrir exceção no PC, o contrato precisa de uma v2, com simulação e o "aprovo" do Alexandre (tela-bc3, cabeçalho). Não dá para aceitar aqui.
- **O que acontece:** o formulário em si cabe, porque termina em 559 px. Quem passa da tela é a lista, empurrada para baixo.
- **Correção:** abrir o formulário **por cima da lista**, como o painel "Faróis" já abre, na largura da lista.
  - A página fica em 768 px, e o "Criar" fica a 560 px (`ux/depois-2-novo-usuario-pc.png`).
  - Os painéis da tela passam a ter um padrão só.
  - O máximo de 1060 px deixa de ser preciso.
  - No celular, nada muda: o formulário segue no fluxo da página, como a §7.4 permite.
  ```css
  @media(min-width:701px){
    .u-novo{position:relative}
    .u-novo[open]>form.u-novo-form{position:absolute;left:0;right:0;top:44px;z-index:26;width:auto;max-width:none;margin:0;
      box-shadow:0 10px 28px var(--c-0000001f);border:1px solid var(--borda)}
  }
  ```

### 3. "Do perfil Vendas · 5 faróis" repete o perfil e a contagem
- **Tela:** o painel "Faróis" (PC e celular) e o "Novo usuário".
- **Problema:**
  - O nome do perfil já está na linha, logo acima do painel ("Vendas"), e no campo Perfil do "Novo usuário". No perfil Vendas, o grupo "VENDAS" logo abaixo repete o nome uma terceira vez.
  - O "5 faróis" conta o que a lista mostra logo embaixo.
  - O "5 faróis" sai com 11,7 px de peso 400 (`small` dentro da `legend`). Isso fica abaixo do mínimo de 12 px para texto, e o manual só aceita 11 px para o rótulo de peso 600 em maiúsculas (§5).
- **Regra quebrada:** tela-bc3 §1.1 ("uma informação, um lugar"); o checklist de redundância ("o rótulo não repete o que o filtro já diz"); o manual §5.
- **Correção:** a legenda vira só **"Do perfil"**, com "Desmarque para tirar." embaixo, e o `<small>` com a contagem sai. A separação pedida no P1 B ("do perfil" × "liberado a mais") continua clara.

### 4. A marca "tirado"/"liberado" do painel tem um estilo diferente do selo da linha, e há tamanhos fora da escala
- **Problema:** os dois são o mesmo componente, um selo com texto, mas saem com medidas diferentes:
  - no painel (`.f-tag`): 11 px, peso 600, minúsculas, raio de 9 px;
  - na linha (`.selo`): 0,78 rem, peso 700, raio de 10 px.
- **Tamanhos fora da escala do manual:** o `.f-nota` e o `.f-quando` usam 12,5 px; a escala tem 12 (apoio). O `.f-tag` usa 11 px fora do papel de rótulo.
- **Regra quebrada:** checklist da marca ("um só estilo por componente"); manual §5 ("o mesmo papel usa sempre o mesmo tamanho e o mesmo peso").
- **Correção:**
  - a marca do painel usa as mesmas medidas do `.selo`, ou a própria classe `.selo selo-tirado` / `.selo selo-liberado`;
  - o apoio fica em 12 px.
  - Está em `ux/sugestao.css` e aparece em `ux/depois-1-vendas-farois-pc.png`.

### 5. (PR do código) Perfis sem rótulo: o código do perfil apareceria na tela (D1)
- **Problema:** o `rot_perfil` de `usuarios.html` não tem `analista` nem `trade`. A linha, o campo Perfil e a legenda mostrariam "analista" e "trade" crus.
- **Regra quebrada:** tela-bc3 §13.4 ("o código nunca aparece na tela").
- **Correção:**
  - Concordo com a D1 do designer. Como o PR da T-0050 mexe no mesmo template, ele leva os rótulos "Analista" e "Trade", se o #158 não os trouxer antes.
  - Melhor ainda: o rótulo sai de uma fonte única no `render`, e não de um dicionário dentro do template.

## 🟢 Sugestões

1. **"liberado" quebra de linha a 1366.** As 4 colunas da parte "Liberar" têm uns 190 px. Por isso, "Painel Executivo" leva o selo para a linha de baixo, enquanto em "Pedidos" ele fica na mesma linha. Duas saídas:
   - tirar a marca "liberado" só na parte "Liberar": a caixa marcada, sob o título "Liberar além do perfil", já diz isso, e o selo da linha confirma depois de salvar;
   - ou aceitar a quebra.
   - O "tirado", com o nome riscado, vale manter, porque tirar é o gesto que mais pede atenção.
2. **Celular, pé fixo:** o "Alterado em …" está dentro do pé fixo. Com ele, o pé ocupa uns 90 px e cobre metade do último farol visível (`sim/2-farois-aberto-cel-a.png`, "Pedidos"). Deixar só o botão no pé fixo, e o "Alterado em" no fluxo, no fim do painel.
3. **Celular, divisória:** a borda de cima da 2ª `fieldset` corta a legenda "Liberar além do perfil" pela metade da altura. Pôr a borda num invólucro, ou dar `padding-top` antes da legenda.
4. **Erro depois de recarregar, no celular:** a mensagem fica no topo, e o painel reaberto fica uns 1.300 px abaixo. Redirecionar com âncora para a linha (`#u-<login>`), para o painel aparecer na tela. A mensagem continua num lugar só.
5. **Texto da confirmação:** "Painel Executivo liberado; Roteirização tirado." tropeça no gênero. Sugestão, no mesmo formato dos selos: "Acesso de usuario.ficticio.03 salvo. Liberado: Painel Executivo. Tirado: Roteirização."
6. **Dois selos cinza parecidos:** "Desativado" (`selo-cinza`: `--borda` com `--suave`) e "1 farol tirado" (`selo-tirado`: `--fundo` com borda e `--texto`). O texto separa os dois. Vale alinhar os neutros num só desenho, com o "tirado" diferente só pela borda.
7. **Estados não simulados:**
   - o perfil sem farol (Trade: "Este perfil ainda não tem farol no site.", mais a parte "Liberar");
   - os erros 400 e 503.
   - Os textos do LEIAME estão bons. Basta um PNG do Trade no PR do código.
8. **Anterior à T-0050, fora do escopo:**
   - a 1366×768, a lateral do admin, com o grupo Analista Comercial do #158, corta em "Saldo / M…", e "Usuários" fica abaixo da dobra (vale para o modulo-web e o #158);
   - a linha do desativado (07) desalinha as colunas, porque o botão "Ativar" é mais estreito que o "Desativar" (já está no `sim/0-antes-usuarios-pc.png`).
9. **Anterior à T-0050, para o engenheiro-software (tela-bc3 v2):** a tela Usuários só cabe em 768 px com até uns 8 usuários. Acima disso, a lista empurra a página. Também o painel aberto numa linha de baixo (07) leva a página a 949 px. O contrato precisa dizer se a lista de Usuários rola por dentro (`flex: 1`, como a tabela dos faróis) ou se entra na §7.4. Isso é independente desta tarefa.

## Dúvidas do designer (LEIAME)

- **D2, "Ver histórico":** **não na T-0050.**
  - O "Alterado em … por …" responde à pergunta do dia a dia: quem mexeu por último.
  - O registro completo existe no `usuarios_acesso.jsonl` e pode ser auditado.
  - Uma lista de 10 mudanças no rodapé seria o 3º elemento do pé (no celular, do pé fixo), com mais texto na tela. O desenho, §8.2, já diz "só se o Alexandre pedir".
  - Se ele pedir, a melhor forma é um link "Ver histórico" que abre uma lista curta ("27/11 06:30 · admin.ficticio · Painel Executivo liberado"), sem tela nova.
- **D3, "Voltar ao perfil":** **dispensável agora.**
  - Os selos já mostram quem está personalizado, e o caso típico é de 1 ou 2 faróis, que se remarcam em 1 ou 2 toques.
  - Se entrar, o botão só **remarca as caixas** pelo perfil, no `usuarios.js` que já existe, e não grava nada. O admin confere e toca em "Salvar acesso". Assim os 3 toques ficam e não é preciso confirmação de perigo.
  - Não pode ser um botão que grave direto: seria uma ação de várias mudanças sem passar pela tela.
- **D4, o "Novo usuário" passa de 768 px no PC:** **não aceitar como exceção da §7.4.**
  - Exceção no PC é uma v2 do contrato, com o "aprovo" do Alexandre, e o próprio caso mostra que não precisa dela.
  - O formulário termina a 559 px. Basta abri-lo por cima da lista, como o painel "Faróis" (🟡 2, `ux/depois-2-novo-usuario-pc.png`), e a página fica em 768.
  - O problema da lista longa é anterior à T-0050 e vai separado (🟢 9).

## Resumo para o gerente-projetos

| Sev. | # | Tela | Elemento | Correção | Onde |
|---|---|---|---|---|---|
| 🟡 | 1 | Faróis, PC | Painel de Admin, Diretor, Gerente e Analista com 695 px | Grupos em 5 colunas quando só há "Do perfil" | proposta + PR |
| 🟡 | 2 | Novo usuário, PC | Página com 1074 px (D4) | Formulário por cima da lista | proposta + PR |
| 🟡 | 3 | Faróis e Novo usuário | "Do perfil Vendas · 5 faróis" | "Do perfil", sem contagem | proposta + PR |
| 🟡 | 4 | Faróis | `.f-tag` 11 px; apoio 12,5 px | Medidas do `.selo`; apoio 12 px | proposta + PR |
| 🟡 | 5 | Linha e Perfil | `analista`/`trade` sem rótulo (D1) | Rótulos de uma fonte única | PR do código |
| 🟢 | 1–9 | várias | ver acima | — | backlog / PR |

---

## Reteste · simulação v2 (27/11/2026, Manaus)

- **O que revisei:** `sim/` v2, com `LEIAME.md` sha256 `bdf19ad30a5e…`, `proposta/sim-farois.css` `38be875903a6…` e `proposta/gera.js` `b40c1dcd404a…`, sobre o mesmo desenho (`8a91c11`) e o `estilo.css` do `main` (`ed324ca`).
- **Como medi:** rodei de novo o `proposta/gera.js` com a `proposta/sim-farois.css` numa cópia fora do repositório, com as fontes e o logo do `main`. Depois abri o painel em **cada uma das 8 linhas**, a 1366×768, 1920×1080 e 390×844.

### Medição

| Item | v2 |
|---|---|
| Rolagem lateral | nenhuma, nos 8 estados × 2 telas e nos 8 painéis × 3 tamanhos; nenhuma caixa com `scrollWidth > clientWidth` |
| Alvos < 44 px no celular | nenhum (o `gera.js` e a minha medição concordam) |
| Painel do Admin, Diretor e Analista a 1366 | 303 px; "Salvar acesso" a 505 a 567 px no Admin e no Diretor; página com 768 |
| Painel do Trade a 1366 | 385 px; "Salvar acesso" a 711 px; página com 768 |
| Painel de Vendas e Pré-venda a 1366 | 303 px; página com 768 |
| "Novo usuário" aberto a 1366 | página com **768** (era 1074); "Criar" à vista |
| Selo "liberado" quebrando de linha | 0, a 1366, 1920 e 390 |
| Tamanhos no painel | legenda 16/600 · apoio 12/400 · rótulo de grupo 11/600 em maiúsculas · nome 14/400 · selo 12,5/700 · botão 14/600, todos na escala do manual §5 |
| Selo do painel × selo da linha | idênticos (12,48 px, 700, raio 10 px, mesmo padding): é a própria classe `.selo selo-tirado` / `.selo selo-liberado` |
| Hex fora do `:root` | nenhum |
| Pé fixo no celular | 60 px, só o botão. "Alterado em" fica no fluxo |

### Os 🟡 da v1

| # | Situação |
|---|---|
| 🟡 1 · painel de 695 px | **Resolvido.** Sem a parte "Liberar", os grupos ficam em 5 colunas na largura toda (`6-farois-admin-pc.png`). Painel com 303 px |
| 🟡 2 · D4 | **Resolvido.** O "Novo usuário" abre por cima da lista no PC (`4-novo-usuario-pc.png`); página com 768. Não precisa de exceção à §7.4. No celular, segue no fluxo |
| 🟡 3 · "Do perfil Vendas · 5 faróis" | **Resolvido.** A legenda é só "Do perfil", sem o nome do perfil e sem a contagem |
| 🟡 4 · selo e tamanhos | **Resolvido.** O painel usa o `.selo` da linha; o apoio fica em 12 px. Também entram MC-0028 a MC-0032: o "Faróis" aberto sem verde, o botão com 14 px, a legenda com 16/600 e o `.selo-tirado` com o peso do `.selo` |
| 🟡 5 · D1, rótulos `analista`/`trade` | **Fora da simulação, por decisão do gerente:** vai no código da T-0036. A v2 já mostra "Analista" e "Trade". Fica como item de conferência no PR do código da T-0050: nenhum código de perfil na tela (tela-bc3 §13.4) |

### Os 🟢 da v1

- **Resolvidos na v2:**
  - 1: o "liberado" não quebra mais, com 3 colunas equilibradas (`columns`);
  - 2: o pé fixo tem só o botão;
  - 3: a divisória no celular fica na legenda, sem cortar o título;
  - 5: a confirmação agora diz "Liberado: Painel Executivo. Tirado: Roteirização.";
  - 7: o estado Trade foi simulado (`7-*`), com "Este perfil ainda não tem farol no site." e a parte "Liberar" ativa.
- **Seguem como sugestão** (não bloqueiam):
  - 4: a âncora `#u-<login>` no retorno de erro, para o celular abrir já no painel;
  - 6: os dois selos neutros parecidos ("Desativado" × "tirado");
  - 8 e 9, anteriores à T-0050:
    - a lateral do admin corta a 768 px;
    - a linha 07 fica desalinhada;
    - a lista longa de Usuários não cabe em 768. O painel aberto nas 3 últimas linhas leva a página a 828, 890 e 955 px. É o mesmo caso do 🟢 9, para a tela-bc3 v2.
- **🟢 novo (10):** a `sim-farois.css` usa `font-size:12px` (apoio) e `16px` (título de bloco) em número, porque o `:root` ainda não tem `--t-apoio` nem `--t-bloco`. Os valores são os do manual. Ao aplicar, o modulo-web cria os dois tokens no `:root` (tela-bc3 §12.2) e usa os nomes, em vez dos números.

### Resultado do reteste

**Aprovado: sem 🔴 e sem 🟡 na simulação v2.** Ela pode ir ao po para aprovação por delegação.

No PR do código, conferir três coisas:
- o D1 (rótulos);
- o 🟢 10 (os tokens de tamanho);
- os PNGs no head SHA do PR, com o painel do Admin e o do Trade.
