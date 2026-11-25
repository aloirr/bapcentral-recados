---
id: R-20261124-212002-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T21:20:02-04:00
---
# Parecer do designer-ux: entrega 2 head 5e07a32 — 6 🔴 (inclui dado pessoal na simulação, já apagada)

> Parecer do designer-ux (subagente do gerente-projetos; gravado pelo gerente; trecho com dado pessoal ocultado pela regra 6).

# Revisão de UX: T-0017, entrega 2 (Títulos, Por cliente, Cobrar no WhatsApp)

- Revisor: designer-ux · 25/11/2026
- Branch `origin/modulo-web/T-0017-cobranca-web`, **head 5e07a32**. O parecer vale só para este head.
- Conferi as 8 imagens inteiras, em trechos:
  - sim3-titulos, sim3-cliente e sim3-gerente: pc 2732×11036 e cel 780×~11500;
  - sim3-cobranca-pc 2732×50092 e sim3-cobranca-cel 780×143432.
- Conferi também o código: `_fila.html`, `_tabela.html`, `cobranca.js`, `estilo.css:102-128` e `cobranca.py:271-284` e `:522-537`.

## Veredito: 🔴 Não mostrar ao Alexandre ainda. São 6 bloqueios: 2 na simulação e 4 na tela.

---

## 🔴 Antes de mostrar

### 🔴 1. Dado pessoal real nas imagens (regra 6)
- A anonimização trocou `nome` e `nome_msg`, mas **não trocou o texto da `mensagem`**.
- Por isso as 139 caixas de mensagem trazem o nome real do cliente: "Olá, Bruno Furtado Costa!", "Olá, Mariana de Campos!", "Olá, Jhones B Gomes!", "Olá, Matheus Alves Pendra!"…
- Um deles traz o que parece o começo de um CPF ou CNPJ: "Olá, **[CPF/CNPJ e nome ocultados] Ca!" (sim3-cobranca-pc, card Cliente 071).
- O que fazer: a simulação deve remontar a `mensagem` a partir do `modelo` com o `nome_msg` fictício. As imagens atuais não podem sair da sessão.
- Achado de produto, para o dono do robô (`cobranca_whatsapp`), registrado aqui: a saudação usa a razão social crua.
  - Em MEI, a razão social leva o CPF, e ele vai na mensagem ao cliente.
  - O nome tem de sair sem dígitos de documento. Encaminhar como 🔴 de produto ao dono.

### 🔴 2. As imagens da fila estão quebradas
- Há uma falha de captura: a página tem 25 mil px no PC e 72 mil px no celular. A partir do 2º terço da página:
  - cartões cortados ao meio;
  - textareas em branco;
  - botões pela metade (ex.: "IADO" no Cliente 102, "Abrir WhatsApp" cortado no Cliente 005);
  - blocos soltos fora dos cartões.
- O Alexandre vai achar que é a tela.
- O que fazer: capturar só a dobra mais 2 ou 3 telas, com cartões nos estados do 🔴 6, e mais um recorte do fim da fila.

### 🔴 3. Títulos e Por cliente: o valor não aparece sem rolar de lado
- Títulos (`cobranca.py` `_T`): VALOR e SALDO são as **duas últimas** das 18 colunas visíveis.
  - A 1366 px a tabela acaba em "VENDEDOR / S…";
  - no celular só se veem SITUAÇÃO, FAIXA, FILIAL, NF e PARC.;
  - nem o cliente nem o saldo aparecem.
- Por cliente: a 390 px só se veem SITUAÇÃO, FAIXA, CLIENTE e NOME. EM ATRASO (o número que ordena a lista) fica fora.
- Nada indica que a tabela rola de lado (`estilo.css:53` `.rolagem{overflow-x:auto}`).
- Ordem pedida, com a mesma regra no PC e no celular:
  - **Títulos:** CLIENTE · NOME · SALDO · DIAS ATRASO · VENCIMENTO · SITUAÇÃO · FAIXA e o resto depois;
  - **Por cliente:** CLIENTE · NOME · EM ATRASO · MAIOR ATRASO · TÍTULOS VENCIDOS · FAIXA e o resto depois.
  - Fixar a 1ª coluna (CLIENTE+NOME) com `position:sticky;left:0`.
- Se a ordem tiver de ser a do PC (Tkinter), basta fixar CLIENTE e trazer SALDO/EM ATRASO logo depois de NOME só no site. Decisão do dono, mas o valor tem de estar à vista.

### 🔴 4. A aba "Cobrar no WhatsApp" aparece cortada no celular
- A 390 px a aba aparece como "Cobrar r…" (`estilo.css:18-19`, `.abas` com `overflow-x:auto` e sem dica).
- É a aba que mais se usa no celular, porque o WhatsApp está nele.
- O que fazer:
  - quebrar as abas em 2 linhas (`flex-wrap:wrap`), ou
  - encurtar o rótulo para **"Cobrar"** (o título da página já diz "Cobrar no WhatsApp").

### 🔴 5. Risco de clique errado em ENVIADO/PULADO
- O `cobranca.js:26-48` grava no primeiro toque, sem confirmar e sem desfazer.
- ENVIADO é um botão cheio azul, encostado no "Abrir WhatsApp" verde e do mesmo tamanho. No celular, os dois dividem a linha meio a meio (`estilo.css:126`).
- Resultado:
  - **dois botões principais** por cartão;
  - um toque escorregado registra ENVIADO sem ter enviado;
  - ENVIADO fica ativo antes de abrir o WhatsApp;
  - depois de 60 s os botões voltam a funcionar e dá para gravar PULADO por cima.
- O que fazer:
  - **um só principal:** "Abrir WhatsApp" (verde);
  - ENVIADO aparece como secundário (contorno) e só fica ativo depois do toque em "Abrir WhatsApp";
  - PULADO vira neutro (texto/link), separado na outra ponta da linha;
  - depois de gravar, o cartão mostra "ENVIADO HOJE · Desfazer" por ~10 s, ou até sair da tela;
  - o desfazer grava um registro novo no diário (só acréscimo, regra 7).
- No cartão sem número (`_fila.html:17` esconde o link), ENVIADO fica como **primeiro botão cheio**, sem nada que se possa ter enviado. Ele só deve aparecer quando o telefone digitado for válido.

### 🔴 6. A simulação não mostra a situação do cliente
- Todos os 139 cartões estão em "a cobrar".
- Os `ultimo` do pacote são de 09 e 17/11, fora dos 7 dias (`cobranca.py:271-284`). Por isso o Alexandre não vê:
  - ENVIADO HOJE;
  - ENVIADO dd/mm;
  - PULADO HOJE;
  - o cartão depois do toque (borda verde, `.feito`);
  - a mensagem de erro.
- O que fazer: incluir na simulação 1 cartão de cada estado (RN-POS-002) e 1 com erro.
- Junto, decidir o que acontece com o cartão já ENVIADO HOJE: vai para o fim da fila, fica apagado ou some.
  - Hoje ele continua no meio da lista, com os mesmos botões, e a pessoa perde o lugar.
  - Recomendo: ir para o fim, numa seção "Já cobrados hoje".

---

## 🟡 Pode ir junto, se der; senão, logo depois

1. **Selos**
   - A Faixa sai toda em amarelo: "1–15" e "+180" iguais. O `chip` é suposição da simulação (`modweb_sim3.py`).
   - Pedir ao PC uma escala da faixa: amarelo claro → laranja → vermelho.
   - "FORA DO PLANNER" amarelo, ao lado de "ATIVO" verde, está bom. Os contrastes medidos passam: vermelho 5,7:1, verde 4,55:1, amarelo 5,7:1.
   - "a cobrar" sai em minúsculas e cinza (`estilo.css:117`), diferente dos selos em MAIÚSCULAS das tabelas. Usar **A COBRAR** no mesmo `.selo`.
2. **Botão verde:** branco sobre #25a244 dá **3,3:1**. Passa só como texto grande ou negrito ≥ 14 pt; o rótulo é negrito de ~16 px, então fica no limite. Escurecer para #1e8e3e (≥ 4,5:1).
3. **Textos que explicam o sistema** (cortar):
   - "Mensagem (pode editar; o texto editado não é guardado)" → **"Mensagem"**;
   - "Telefone só para este envio (opcional)" → **"Outro telefone (só neste envio)"**;
   - o rodapé "Sem exportação nesta tela. Os dados são os do PC, na hora do pacote." (`_tabela.html:30`) → sai;
   - "139 clientes, do maior atraso ao menor" → **"139 clientes"**: a ordem se vê.
4. **Aviso "situação do PC até hh:mm"** (`_fila.html:2`)
   - Está no topo e é claro. Mas repete a faixa "Dados de 24/11/2026 21:12", com a mesma hora, logo acima.
   - Proposta: um aviso só: **"Situação do PC até 21:12. O que você marcar aqui chega ao PC às 08h ou 14h."**
   - A segunda frase fica, porque explica por que o PC ainda não mostra o que a pessoa marcou.
   - Sem data, "até 21:12" engana quando o pacote é de outro dia. Usar "até 24/11 21:12" quando não for hoje.
5. **Avisos no cartão:** "sem telefone no cadastro", "telefone fixo: pode não ter WhatsApp" e "telefone inválido (repetido)".
   - São do próprio cliente, e ficar no cartão é aceitável aqui: é o estado do item, e não um alerta da tela.
   - Mas o amarelo em bloco pesa mais que o selo de situação. Usar uma linha com ícone ⚠ e texto escuro, colada ao campo de telefone, porque é dele que fala.
   - Dar um nome curto e de ação: **"Sem celular: digite um número"** / **"Fixo: confira se tem WhatsApp"** / **"Número repetido em outro cliente: digite o certo"**.
6. **Cabeçalho do cartão:** quando a cidade é longa, o valor quebra para a esquerda numa linha própria (Clientes 057, 069, 031, 015, 093). Usar `flex-wrap:nowrap` e o nome com reticências, para manter o valor sempre à direita.
7. **Fila de 139 cartões numa página só:**
   - sem filtro (vendedor, UF);
   - sem contador "12 de 139 feitos hoje";
   - sem "próximo a cobrar".
   - Paginar de 20 em 20, ou ter o filtro "só a cobrar". Sem isso, a 3ª tarefa do dia exige rolar muito.
8. **Borda do cartão** (`estilo.css:112`): 2 px #8f9c93 (2,86:1) cinza-esverdeado, mais pesado que os cartões do Resumo (entrega 1). Usar a borda/sombra dos `.kpi`.
9. **Tabelas**
   - O código "900058-01" quebra em 2 linhas: `white-space:nowrap` em CLIENTE.
   - O rótulo do filtro "Uf" deve ser **"UF"** (`_tabela.html:6`, `|capitalize`).
   - As opções de Faixa saem em ordem alfabética ("+180, 16–30, 1–15…", `cobranca.py:535`). Usar a ordem das faixas.
   - "Limpar" e "Próxima »" estão em azul padrão sublinhado; usar o link do site.
   - O total da tabela ("539 linhas") não diz o valor: acrescentar a soma do SALDO filtrado, que é o que o usuário quer saber ao filtrar.
10. **Rótulos "ENVIADO"/"PULADO" como verbo de botão:** usar **"Marquei como enviado"** / **"Pular"**. O rótulo em MAIÚSCULAS fica para o selo do resultado.

## 🟢 Ok

- **Visão do gerente** (sim3-gerente):
  - só Resumo · Títulos · Por cliente;
  - sem a aba de cobrança, sem telefone, sem botão;
  - o resto é igual ao admin: pixel a pixel, só muda o topo e as abas.
  - Cumpre RN-POS-004 (1 A). O cabeçalho "ger.sim · gerente" está claro.
- **CNPJ fora:** o cliente sai pelo código, como no PC (2 A).
- **Consistência com a entrega 1:** mesmas abas em pílula, mesma faixa "Dados de…", mesmo título "Farol · Aba", mesma fonte. Depois do 🟡 8, fica igual.
- **Filtros:** quebram bem no celular (2 por linha) e "Por cliente" abre já em INADIMPLENTE.
- **Ordenação:** a fila vai do maior valor ao menor; Títulos, do maior atraso ao menor; Por cliente, do maior EM ATRASO. Faz sentido para cobrar.
- **Alvos de toque:** os botões têm 44 px (`estilo.css:121`).
- **Estados vazios:** "Nenhuma linha neste filtro." e "Nenhum cliente na fila." têm uma frase só.

## Regra dos 3 toques
- **Cobrar um cliente:**
  - hoje: 1 Abrir WhatsApp → (envia no WhatsApp) → 2 voltar → 3 ENVIADO. **Ok.**
  - Depois do 🔴 5, continua em 3 toques.
- **Achar um cliente na fila:** não há busca nem filtro. Para um cliente do meio da lista, ❌ (🟡 7).
- **Ver quanto um cliente deve, no celular:** em Por cliente, ❌ hoje (rolagem lateral); ✅ depois do 🔴 3.

## Pronto para mostrar quando
- 🔴 1 a 6 resolvidos;
- simulação nova com dado 100% fictício, sem falha de captura, com os estados da fila;
- reteste meu no head novo.
