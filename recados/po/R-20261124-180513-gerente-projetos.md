---
id: R-20261124-180513-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:05:13-04:00
---
# Parecer do designer-ux: simulação do Farol de Inadimplência, head 0b00e43 — 🟡 com 4 bloqueios

> Parecer do designer-ux (subagente do gerente-projetos; gravado pelo gerente sem alteração, pela limitação do --de no coord.mjs).

# Revisão de UX: T-0017, Farol de Inadimplência, simulação PC × site

- Revisor: designer-ux · 24/11/2026
- Branch `origin/modulo-web/T-0017-farois-web`, **head 0b00e43**. O parecer vale só para esse head.
- Prints revisados: sim-pc-tela.png, sim-web-real-pc.png (1366 px), sim-web-real-cel.png (390 px) e sim-web-real-am.png (filtro AM).
- Decisões de base: R-20261124-175008-alexandre e R-20261124-175838-alexandre (2A, 3A, 4A).

## Veredito: 🟡 Ajuste. NÃO mostrar ao Alexandre antes de corrigir os 4 itens 🔴.

---

## 🔴 Bloqueiam a simulação

**R1. Com o filtro de estado, a tela mostra dois números diferentes para a mesma coisa, e o aviso não explica**
- Onde: `web/app/templates/farol.html:16` (aviso), `farol.html:30-34` (resumo) e `web/app/render.py:139` (`AVISO_UF`).
- O que acontece no filtro AM:
  - o cartão mostra "Em atraso R$ 92.893" e "Inadimplência 67%";
  - logo abaixo, o Resumo gerencial diz "Em atraso: R$ 400.388" e "Inadimplência: 65%", que são os números da BAP inteira;
  - o aviso "Cartões por estado; gráficos da BAP inteira" não cita o resumo e não diz qual é o estado.
- Por que bloqueia: o Diretor vê dois valores conflitantes de "Em atraso" na mesma tela. A decisão 4A só cobre cartões × gráficos.
- O que fazer:
  1. Trocar o aviso por texto com o estado e o resumo: **"Cartões: AM. Resumo e gráficos: BAP inteira."**
  2. Com filtro, pôr o selo "· BAP inteira" no título do resumo: "Resumo gerencial · BAP inteira".

**R2. "A vencer em 7 dias" sai azul no site e neutro no PC**
- Onde: `web/app/static/estilo.css:69` (`.kpi.c-info` → `--info` azul). O pacote manda `cor: "info"`.
- No PC, o tom `info` não tem bolinha no cartão, e o item do "O que o farol diz" leva bolinha cinza.
- No site, o cartão e os 3 últimos itens do resumo ficam azuis (`estilo.css:77`, `.ins.t-info`).
- Por que bloqueia: o Alexandre pediu cor igual à do PC, e é a primeira diferença que aparece lado a lado.
- O que fazer: no farol, `info` usa o cinza do neutro (#8f9c93) no cartão e no resumo. Vermelho (Em atraso, Inadimplência, Acima de 90) e verde (Recuperado) já batem com o PC.

**R3. Gráficos "dia a dia": as barras descem até a linha dos dias, e o eixo fica torto**
- Onde: `farol.html:45` junto com `estilo.css:83` e `:107` (`.gb-denso`).
- O que acontece: nas colunas sem rótulo (dias pares), `.gb-rot` fica vazio e com altura 0. A barra desce até o rodapé e cobre os números 3, 5, 11, 13, 17...
- Afeta os 3 gráficos dia a dia (Em atraso, Recebido e Vencido), no PC e no celular.
- Por que bloqueia: o gráfico parece quebrado, e a base das barras deixa de servir de referência.
- O que fazer: dar altura fixa a `.gb-rot`, ou gravar `&nbsp;` na coluna sem rótulo, para que toda coluna tenha a mesma base.

**R4. Celular: os nomes das filiais saem cortados no "Por filial: em atraso e a vencer"**
- Onde: `estilo.css:106` (`.gb-rotv .gb-rot`, altura 74 px) e o bloco `gb-largo`.
- O que acontece a 390 px: aparecem só pedaços como "IS", "ROSSO", "STA", "RÉM" e "Á". Não dá para saber qual filial é qual.
- Por que bloqueia: é exatamente o ponto pedido, legibilidade dos rótulos no celular.
- O que fazer (uma das duas):
  - no celular, trocar este gráfico por barras horizontais (o componente `hbarras` do "Em atraso por vendedor" já está pronto, com uma linha por filial e as duas barras);
  - ou dar altura suficiente ao rótulo e deixar o gráfico rolar na horizontal sem cortar o texto.

---

## 🟡 Pode ficar para depois (registrar no backlog da T-0017)

**A1. Rótulo "sem recorte por estado" no Recuperado (filtro AM)**
- Onde: `render.py:140`.
- "Recorte" é palavra do time, não do usuário.
- Sugestão: "—" com a legenda **"só na BAP inteira"**.
- Melhor ainda: esconder o cartão quando há filtro, porque o aviso do R1 já explica.
- É uma constante só; se der, entra junto com o R1.

**A2. O cartão não é o mesmo componente do Painel no ar nem do PC**
- No Painel web (`.rc`) e no farol do PC, o cartão tem faixa verde-clara no topo (#e8f0e4) e filete verde (#62bb47). O estado aparece pela bolinha colorida ao lado do rótulo.
- O farol web usa cartão branco com borda esquerda colorida (`estilo.css:67-69`).
- Ação: reaproveitar o visual `.rc-topo`/`.rc-filete`, com bolinha + rótulo, para os 4 faróis e o Painel ficarem iguais.
- Validar com o design-de-marca.

**A3. Grade dos cartões com buracos**
- Onde: `estilo.css:67` e `:96`.
- A 1366 px, a BAP inteira fica com 2 cartões largos + 1 na primeira linha e 3 cartões na segunda, com sobra à direita. No AM ficam 5 cartões + 1 sozinho.
- Ação: grade fixa (6 colunas no PC; 2 no celular), com os cartões de mini-barras ocupando 3.

**A4. "Carteira em aberto por faixa de atraso": a barra "A VENCER" sai vermelha**
- Ela não está em atraso.
- Ação: usar o mesmo azul de "a vencer" do gráfico por filial, ou cinza. Conferir antes como o PC pinta essa barra.

**A5. Acentos e espaços nos nomes das filiais**
- Aparecem "BELEM", "SANTAREM", "MACAPA" e "MATOGROSSO".
- Vêm do pacote do PC. Pedir ao dono do farol no PC, se for ajustar.

**A6. Uma informação, um lugar**
- O resumo repete os cartões em Em atraso, Inadimplência e Acima de 90 dias. É paridade com o PC: avaliar nos dois juntos.
- A data também aparece duas vezes: "Dados de 24/11/2026 18:00" e "Baixado em 24/11/2026 18:00". O Painel tem o mesmo padrão, então vale decidir para o site inteiro.

**A7. Página longa no celular (~5.600 px, 19 gráficos)**
- Ação: agrupar por assunto (Em atraso, Recebido, Vencido, Carteira) com sumário ou abas, como o PC faz com as abas.
- Valores girados 90° (mês a mês): no celular, mostrar só o último mês ou usar o título da barra.

**A8. Mini-barras por estado em ordens diferentes**
- "Em atraso" mostra PA MA AM RR MT AP; "Inadimplência" mostra PA MA AM RR AP MT.
- É igual ao PC, mas o ideal é uma ordem fixa nos dois.

---

## 🟢 Ok

- **Hierarquia:** cartões no topo, visíveis sem rolar a 1366 px e a 390 px. Depois vêm o resumo e os gráficos, a mesma ordem do PC.
- **Cores:** vermelho nos cartões de alerta e verde no "Recuperado no mês", iguais ao PC (fora o R2).
  - Não há âmbar neste farol, nem no PC nem no site.
  - O âmbar do CSS (#b7791f) passa em borda e ícone (≥ 3:1). Não usar em texto pequeno.
- **3 toques:** menu → farol → estado = 2 toques.
- **Chips de estado:** 44 px no celular (`estilo.css`, media 600px), filtro ativo em verde com texto. É o mesmo componente `.filtros` do Painel.
- **Mini-barras nos cartões:** legíveis no celular, com estado e valor.
- **Texto e formatos:** R$ com milhar, datas dd/mm/aaaa no horário de Manaus, "BAP AUTOPARTS" no rodapé.
- **Dados pessoais:** nenhum cliente ou CNPJ. Os vendedores aparecem como fictícios ("Vendedor 01..."), conforme a decisão 2A.
- **Topo e rodapé:** mesmo cabeçalho e rodapé do Painel.

## Reteste

Depois de corrigidos R1 a R4, novos prints no mesmo head:
- 1366 px na BAP inteira;
- 1366 px com o filtro AM;
- 390 px, rolando até o "Por filial".
