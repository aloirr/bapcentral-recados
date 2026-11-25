---
id: R-20261124-221903-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T22:19:03-04:00
---
# Parecer do designer-ux: Pedidos, Entregas e Visita (head f27e0a3) — 3 🔴 (datas UTC, segundos nos gráficos, aviso longo)

> Parecer do designer-ux (subagente do gerente-projetos; gravado pelo gerente sem alteração; varredura: limpo).

# Revisão de UX: T-0017, entregas 3 a 5 (Faróis de Pedidos, Entregas e Visita no site)

- Revisor: designer-ux · 25/11/2026
- Branch `origin/modulo-web/T-0017-tres-farois`, **head f27e0a3**. O parecer vale só para este head.
- O que conferi:
  - as 6 imagens sim5-* (pedidos, entregas e visita, em pc e cel);
  - as páginas **inteiras**, renderizadas por mim a partir do sim5-*.html, a 1366 px e a 390 px.
- As 6 PNG mostram só a primeira tela. Gráficos, a tabela de frete no celular e o fim das páginas só aparecem na renderização completa.

## Dados pessoais: limpo
- Nas 6 imagens e nos 3 HTML só há "Vendedor NN", nomes de cidade e de estado, e nenhum CPF ou CNPJ.

## Veredito: 🔴 Ainda não mostrar ao Alexandre. São 3 bloqueios.

### 🔴 1. Datas fora do fuso de Manaus na simulação (regra 4)
- Os dados são de 24/11 22:15, horário de Manaus. Ainda assim a tela mostra:
  - em Visita: "Sem o arquivo de 4 dia(s) útil(eis): …, **24/11, 25/11**";
  - em Pedidos: "… em NOV **até 25/11** …" (3 linhas do Resumo).
- 25/11 ainda não tinha chegado, e hoje (24/11) não entra no DU. É o dia em UTC: a simulação rodou com o relógio em UTC, e às 02:15 UTC já é 25/11.
- O que fazer:
  - refazer a simulação com `TZ=America/Manaus`;
  - o dono confirma que a função de "hoje" usa `America/Manaus` explicitamente, e não o relógio da máquina. Teste para o `testes`.

### 🔴 2. Visita: os gráficos mês a mês de horário mostram segundos
- Cinco gráficos mês a mês ("do dia 1 ao dia 19 de cada mês") rotulam as barras em **segundos brutos**, com 4 a 5 dígitos:
  - Início do 1º cliente;
  - Último cliente;
  - Jornada;
  - TMD;
  - TMA.
- Os cartões, logo acima, mostram hh:mm ou hh:mm:ss.
- Número com unidade errada não pode ir ao Alexandre. Formatar o rótulo como hh:mm (TMA e TMD: mm:ss), igual ao cartão.

### 🔴 3. Visita: o aviso amarelo ocupa a primeira tela do celular e explica o sistema
- Na primeira tela do celular, o aviso amarelo de 4 parágrafos toma tudo antes do 1º cartão. Ele traz:
  - os nomes técnicos dos arquivos de rota ("ROTA_PROTHEUS …", "A_PARTIR_… ");
  - a fórmula da aderência.
- Isso não ajuda a agir e empurra os cartões para baixo da dobra.
- Deixar só 2 linhas:
  - **"Faltam os arquivos de N dia(s) útil(eis): dd/mm, dd/mm. Hoje é parcial."**
  - **"Sem cartões por estado: vale só o total da BAP."**
- A regra da aderência pode ir para a dica do cartão "Aderência ao Planner", ou sair.

## 🟡 Pode ir junto, se der; senão, logo depois
1. **Visita, cartão Visitas:** a barra de RR aparece sem barra e sem número. Mostrar "0", ou tirar RR quando for zero.
   - [SUPOSIÇÃO] As barras por estado dentro do cartão valem mesmo com o aviso "vale só o total". Se não valerem, saem também.
2. **Visita:** os cartões da 1ª linha esticam até o mais alto ("Vendedores em campo" e "Visitas por dia" ficam com meia altura em branco). Usar `align-items:start` na grade, como no Inadimplência.
3. **Entregas, tabela "Frete por estado" a 390 px:**
   - a 1ª coluna fica fixa e a linha TOTAL aparece;
   - mas a tela mostra UF · REGIÃO · NOTAS · VALOR NF, e **FRETE R$** e **% S/ NOTA**, que são o assunto da tabela, ficam fora;
   - pôr FRETE R$ e % S/ NOTA logo depois de UF, com REGIÃO no fim;
   - pôr a dica "Role para o lado para ver mais colunas →", como nas tabelas do Inadimplência.
4. **Entregas:**
   - o rótulo "TRANS. TERCERIZADA" está com erro de grafia; o certo é "TERCEIRIZADA";
   - o gráfico "Frete estimado · mês a mês (R$ e % sobre a nota)" mostra só R$: acrescentar o % ou tirar "e % sobre a nota" do título.
5. **Pedidos e Entregas:** o Resumo gerencial repete números dos cartões (Faturado no prazo, Pedidos devolvidos, Em aberto, Excluídos). Fica para o corretor-redundancias decidir junto com o padrão do Inadimplência.
6. **Cartões no celular:** valores quebram no meio ("devoluções R$ / 5.552", "1 / s/ transp."). Usar `white-space:nowrap` no valor dentro do detalhe.
7. **Cores dos gráficos:** Pedidos ("Por filial: SLA médio") e Visita (horários) usam um azul forte que não aparece no Inadimplência nem no Painel. Validar com o design-de-marca.
8. **Gráficos dia a dia de Visita** não têm rótulo de valor. A leitura é só pela altura. Aceitável como tendência; se der, mostrar o valor do maior e do último dia.

## 🟢 Ok
- **Consistência com o Inadimplência aprovado:**
  - o mesmo cabeçalho com "Baixado do ERP em dd/mm/aaaa hh:mm" ao lado do título (abaixo dele, no celular);
  - os mesmos chips "Estado" (BAP inteira / UF);
  - cartões com a barra de cor à esquerda e o texto do estado;
  - o mesmo "Resumo gerencial" com a barra de tom.
- **Pedidos:** os 8 cartões ficam numa faixa só a 1366 px, como no PC; no celular, 2 por linha, legíveis.
- **Entregas a 1366 px:** a tabela tem a 1ª coluna fixa, cabeçalho e TOTAL, e está legível.
- **Visita:** sem chips de estado e com o aviso de que vale só o total. O texto precisa encurtar (🔴 3).
- **Gráficos no celular:** cabem em 1 coluna a 390 px, com o título inteiro e o eixo legível. Os rótulos verticais dos gráficos mês a mês se leem (a unidade está errada, 🔴 2).
- **3 toques:** trocar de estado é 1 toque, e cada farol abre já com o que importa.

## Pronto para mostrar quando
- 🔴 1 a 3 resolvidos;
- simulação refeita com `TZ=America/Manaus`;
- PNGs da **página inteira**, ou da 1ª tela mais os gráficos e a tabela de frete no celular;
- reteste meu no head novo.
