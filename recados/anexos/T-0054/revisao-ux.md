# T-0054: revisão de tela (designer-ux)

- Branch `modulo-web/T-0054-entregas-edicao`, head **ce626345f33fd0f6391b806da1079f21cf349188**.
- Simulação regerada do head SHA (git archive) com o `sim.py` do gerente e a fixture fictícia (`CLIENTE TESTE`, `MOTORISTA TESTE`, `FILIAL FICTICIA`, logins `sim.*`). Também gerei as telas "gerente e admin depois de salvar".
- PNGs gerados no Chromium completo do Playwright com `--lang=pt-BR` e `LANG=pt_BR.UTF-8`, em 1366 px e 390 px.
- Largura: 1366 e 390 px em todas as telas; nada estoura.
- O diff de tela é só `.py`: nenhum template ou CSS mudou e não entra hex novo.

**Resultado: não aprovado ainda. Nenhum 🔴, três 🟡.**

## Respostas aos pontos

1. **Datas "mm/dd/yyyy" e "11/08/2026": vêm do navegador da simulação, não do código.**
   - O `base.html` já fixa `<html lang="pt-BR">`. O valor enviado também está certo: `value="2026-11-08"`, ou seja, 8 de novembro.
   - Para o Chromium, o `locale: 'pt-BR'` do contexto não basta: o campo de data segue o idioma do processo. Com só o `locale` do contexto, a tela continua "11/08/2026" e "mm/dd/yyyy". Testei no Chromium 158.
   - Com `chromium.launch({ channel: 'chromium', args: ['--lang=pt-BR'], env: { LANG: 'pt_BR.UTF-8', LANGUAGE: 'pt_BR' } })` sai "08/11/2026" e "dd/mm/aaaa". O headless shell sem `LANG` ainda mostra "dd/mm/yyyy".
   - No Chrome/Edge em pt-BR das assistentes sai "dd/mm/aaaa". **Não é achado.**
   - Sugestão para o `web/simular_png.mjs`: lançar o Chromium assim de agora em diante.
   - PNGs: `ux-edicao-ptbr-pc.png`, `ux-edicao-ptbr-cel.png`.
2. **A linha de contexto não diz qual nota está sendo editada.** Ver o 🟡 1.
3. **Coluna "Editar" e "Aguardando o PC".**
   - Funcionam nas Entregas e nas Pendências, no PC e no celular. No celular, as 24 linhas (18 + 6) têm o botão dentro do cartão.
   - Há defeitos de acabamento no celular e na largura da coluna no PC: ver o 🟡 3 e o 🟢 1 e 2.
4. **Perfis.**
   - O gerente não tem a coluna nem o botão. Depois de uma edição, vê só a coluna "Edição" com a marca, sem botão (`ux-gerente-com-marca-pc.png` e `-cel.png`).
   - O admin vê igual ao pós-venda (`ux-admin-pc.png`). Correto.
5. **Erro de validação.**
   - A mensagem está boa: no topo, em `--alerta`, com `role="alert"`, contraste 6,6:1.
   - Mas o formulário volta com os valores do pacote e não com o que a pessoa digitou: ver o 🟡 2.
6. **Marca.**
   - Só tokens: `--verde-escuro`, `--atencao-claro`/`--atencao-texto`, `--alerta`, `--suave`.
   - Nenhum hex novo no diff.
   - Contraste AA: botão 5,1:1; "Aguardando o PC" 5,4:1; resumo 7,7:1.
   - A marca sempre tem texto junto, não só cor. **OK.**

## 🟡 Corrigir antes do merge

### 1. Formulário de edição: a linha de contexto não diz a nota
- O topo mostra "PENDENTE · 3 · 03/11/2026 · 04/11/2026 · 08/11/2026 · MA": situação, SLA e três datas sem rótulo. Não diz NF nem cliente, e o pós-venda não tem como conferir se abriu a nota certa.
- **Causa:** `resumo_da_linha` (`web/app/main.py`) só usa a GRADE (chave + nome) quando `rid in SEM_ESTADO_AVISO`, e `pl_entregas` não está nessa lista. Por isso cai nas "6 primeiras colunas" do pacote.
- **Correção:** usar a GRADE também para `pl_entregas`. A GRADE já tem `chave: "NF"` e `cel[1]: "CLIENTE"`.
  - Faça isso com uma tupla própria (ex.: `RESUMO_PELA_GRADE = SEM_ESTADO_AVISO + ("pl_entregas",)`), para não mexer no aviso de estado.
  - Fica **"NF 900502 · CLIENTE TESTE 02 · MA"**. Conferi que `cod_e_nome("900502")` devolve a NF inteira.
  - Sugiro também o resumo em `--texto` e 600, porque é a identificação da nota e não um detalhe.
- PNGs: antes `ux-edicao-ptbr-pc.png`; depois `ux-depois-resumo-pc.png` e `ux-depois-resumo-cel.png`.

### 2. Erro de validação apaga o que a pessoa digitou
- No `editar_post`, quando há `erro`, a página volta com `form_ctx(...)`, que lê os valores do pacote. Tudo o que foi mudado se perde: etapa, datas, frete.
- Na simulação, o campo do motorista recusado voltou como "MOTORISTA TESTE 3" (`ux-erro-cel.png`). Para o pós-venda, que muda 3 ou 4 campos de uma vez, isso obriga a refazer tudo.
- O caminho da linha nova (`novo_ctx`) já devolve os valores (`c_`). Este caminho deveria fazer igual:
  - repor os `c_` digitados;
  - deixar vazio só o campo recusado, para não ecoar CPF ou telefone;
  - marcar esse campo com `aria-invalid="true"` e a mensagem logo abaixo dele.
- É herança da T-0021, mas agora pega o usuário principal desta tela.

### 3. Celular: o botão "Editar" fica torto no cartão
- `.bc3-ed a.bt-ed` ganha `min-height: 44px` mas continua `inline-block`. O texto fica grudado no topo de um bloco verde de 50 × 44 px, e a marca "Aguardando o PC" (18 px de altura) não alinha com ele.
- **Correção** só com tokens, no `@media` do celular:

  ```css
  .bc3-ed{display:flex;align-items:center;gap:.5rem}
  .bc3-ed a.bt-ed{display:inline-flex;align-items:center;justify-content:center;min-width:88px;padding:0 1rem;font-size:.9rem}
  .bc3-ed .ed-marca{margin-left:0}
  ```
- PNGs: antes `ux-antes-cel-cartao.png`; depois `ux-depois-cel-cartao.png`.

## 🟢 Sugestões para depois

1. **PC: a marca alarga a coluna "Editar".** Com uma linha "Aguardando o PC", a coluna vai de 60 para 175 px e a TRANSPORTADORA passa a cortar ("TRANSPORTADORA TEST…", `ux-posvenda-salvo-pc.png`). Ponha a marca embaixo do botão (`.ed-col .ed-marca{display:block;margin:.2rem 0 0}`). No gerente, a coluna "Edição" ocupa 125 px por uma marca só.
2. **Celular: a nota pendente só aparece com o cartão aberto.** Um ponto âmbar com texto acessível no `summary` do cartão deixaria ver as notas "Aguardando o PC" sem abrir uma por uma.
3. **"—" sem explicação no celular.** O motivo ("Nota concluída…") está só no `title`, que não aparece no toque. No cartão, troque por um texto curto "Sem edição: nota anterior ao controle" (`ux-depois-cel-cartao.png`) ou não mostre nada.
   - Na fixture, a nota sem chave é de 03/11/2026, e o texto fixo "anterior a 01/10/2026" fica contraditório.
   - Vale o texto vir do motivo real.
4. **A dica "Apague a data para voltar à calculada pelo PC" repete em todos os campos de data,** inclusive na DT. REAL (ENTREGA), que está vazia e não é calculada. Mostre a dica uma vez, só nos campos que têm valor calculado.
5. **`.ed-marca` usa 0,72 rem (11,5 px),** abaixo dos 12 px do checklist. Suba para 0,75 rem. É herança da T-0021.

## Arquivos nesta pasta
- `ux-edicao-ptbr-pc.png` e `ux-edicao-ptbr-cel.png`: o formulário com o navegador em pt-BR.
- `ux-erro-cel.png`: o erro de validação.
- `ux-depois-resumo-pc.png` e `ux-depois-resumo-cel.png`: o resumo proposto.
- `ux-posvenda-salvo-pc.png`: o PC depois de salvar.
- `ux-antes-cel-cartao.png` e `ux-depois-cel-cartao.png`: o botão no celular.
- `ux-posvenda-pendencias-cel.png`: as Pendências no celular.
- `ux-gerente-antes-pc.png`, `ux-gerente-com-marca-pc.png` e `ux-gerente-com-marca-cel.png`: o gerente.
- `ux-admin-pc.png`: o admin.

Os "depois" são maquetes (HTML do head SHA com CSS/texto trocado na mão), não código do PR.

---

# Reteste: head 69d6fcfc2b7fce14cb9a4f1b21b9eab35e7bd35c (delta desde ce62634)

- Simulação regerada do head (git archive), com a mesma fixture fictícia.
- Acrescentei um caso de erro com **todos** os campos mudados: etapa, transportadora, as duas datas e o frete, mais o motorista com CPF.
- PNGs no Chromium completo em pt-BR, 1366 e 390 px. Nada estoura a largura.
- Diff de tela: CSS só com tokens, nenhum hex novo.

**Resultado: aprovado com 2 🟡 pequenos (uma linha de CSS cada).** Pode entrar já corrigido, sem nova rodada minha, se a correção for exatamente a abaixo.

## Os 3 🟡 da primeira revisão
1. **Resumo: resolvido.** Mostra "NF 900502 · CLIENTE TESTE 02 · MA" (`sim/posvenda-edicao-aberta-*.png`).
2. **Erro devolve o digitado: resolvido.**
   - Etapa, transportadora, DT. PREVISTA 10/11/2026, DT. REAL 09/11/2026 e frete 260,00 voltam como digitados.
   - Só o motorista volta vazio, com `aria-invalid="true"` (`sim/posvenda-edicao-erro-varios-*.png`).
   - Falta a pista visual: ver o 🟡 B.
3. **Botão do celular: resolvido.** Tem 88 × 44 px, texto centrado e "Aguardando o PC" alinhado ao lado (`sim/posvenda-entregas-salvo-cel-cartao.png`).

## Os 🟢 aplicados
- **`.ed-marca` com 0,75 rem (12 px): ok.**
- **A dica "Apague a data…" só na DT. PREVISTA: ok.** A DT. REAL ficou sem ela.
- **A marca embaixo do botão no PC: a coluna caiu de 175 para 94 px,** mas o chip quebra em duas linhas ("Aguardando / o PC") e a linha fica quase o dobro da altura. Ver o 🟡 A.
- **Simulação em pt-BR: o `web/simular_png.mjs` ainda usa o headless shell.** O placeholder sai "dd/mm/**yyyy**" (`sim/simular_png-sem-channel-yyyy.png`). Com `channel: 'chromium'` no `launch` sai "dd/mm/aaaa". 🟢: não afeta o usuário, só o PNG.

## Novo: "Notas com frete" do Fretes para o pós-venda
- É só a entrada em `EDITA_LUGAR`. Hoje `pl_fretes` não está em `render.FAROIS` nem em `LUGARES`, e nenhuma tela muda.
- Nada a revisar agora. A tela de edição do Fretes passa por mim quando o lugar entrar em `LUGARES` (T-0037).

## 🟡 Falta
- **A. O chip "Aguardando o PC" quebra em duas linhas na coluna "Editar" ou "Edição" do PC** (`sim/posvenda-entregas-salvo-pc.png`, `sim/gerente-entregas-depois-pc.png`).
  - Correção em `web/app/static/estilo.css`: trocar o `white-space:normal` da regra `.ed-col .ed-marca` por `white-space:nowrap`.
  - A coluna fica com 124 px, ainda menor que os 175 px de antes, e o chip numa linha só (`sim/sugestao-marca-sem-quebra-pc.png`).
- **B. O campo recusado volta vazio sem nenhum destaque.** O `aria-invalid` só serve para o leitor de tela; quem enxerga vê um campo em branco e pode achar que o sistema apagou o que digitou.
  - Correção, uma linha em `estilo.css`: `.ed-campo [aria-invalid="true"]{border-color:var(--alerta);box-shadow:0 0 0 1px var(--alerta)}`.
  - Com isso há borda vermelha mais a mensagem com o nome do campo, então a cor não é a única pista (`sim/sugestao-campo-recusado-cel.png`).

## PNGs finais (`sim/`)
- `posvenda-edicao-aberta-pc.png` e `-cel.png`: o formulário.
- `posvenda-edicao-erro-varios-pc.png` e `-cel.png`: o erro com vários campos mudados.
- `posvenda-entregas-pc.png` e `posvenda-entregas-salvo-pc.png`: o farol do pós-venda, antes e depois de salvar.
- `posvenda-entregas-salvo-cel-cartao.png` e `-cel-pendencias.png`: o celular, nas Entregas e nas Pendências.
- `gerente-entregas-pc.png` (sem coluna), `gerente-entregas-depois-pc.png` e `gerente-entregas-depois-cel-cartao.png` (só a marca, sem botão): o gerente.
- `admin-entregas-depois-pc.png`: o admin.
- `sugestao-marca-sem-quebra-pc.png` e `sugestao-campo-recusado-cel.png`: maquetes dos 🟡 A e B, com CSS injetado no HTML do head.
- `simular_png-sem-channel-yyyy.png`: o placeholder "yyyy" do `simular_png.mjs`.
