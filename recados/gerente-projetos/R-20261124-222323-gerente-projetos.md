---
id: R-20261124-222323-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T22:23:23-04:00
---
# Parecer do designer-ux: Pedidos, Entregas e Visita (site 1d488f5, robô 071b4cb) — pode mostrar ao Alexandre

> Pareceres do designer-ux (subagente do gerente-projetos; gravados pelo gerente sem alteração).

---
# Reteste de UX: T-0017, entregas 3 a 5 (Faróis de Pedidos, Entregas e Visita no site)

- Revisor: designer-ux · 25/11/2026
- Heads conferidos:
  - site: `origin/modulo-web/T-0017-tres-farois` **6ed0cf8**;
  - robô: **071b4cb**.
- Substitui o parecer do head f27e0a3.
- Conferi as 12 imagens: sim5-{pedidos,entregas,visita}-{pc,cel}.png e as versões -inteira.png, todas por inteiro.

## Dados pessoais: limpo
- Só aparecem "Vendedor NN", cidades e estados.
- Nenhum nome de pessoa, CPF ou CNPJ.

## Veredito: 🔴 Falta 1 bloqueio (novo) antes de mostrar ao Alexandre
- Os 3 🔴 anteriores caíram.
- O novo bloqueio é a página do Visita, que vaza para o lado no celular.

## Os 3 🔴 anteriores
1. **Datas em Manaus: resolvido.**
   - "Sem o arquivo de 3 dia(s) útil(eis): 20/11, 23/11, 24/11", sem dia futuro.
   - Pedidos diz "em NOV até 24/11".
   - [SUPOSIÇÃO] O dia 24/11 aparece como sem arquivo porque é o dia da simulação. Pela regra 4, hoje fica fora do DU. Se 24/11 for "hoje" no pacote, ele não deveria estar na lista de faltas. O dono confere.
2. **Gráficos do Visita: resolvido.**
   - Os rótulos de horário vêm em hh:mm (ex.: início 10:20 / 09:53 / 09:02).
   - TMD e TMA vêm em "N min".
   - Os valores batem com os cartões.
3. **Aviso do Visita: resolvido.** São 2 linhas curtas, sem nome técnico de arquivo e sem a fórmula.

## 🔴 novo

### N1. Visita no celular: a página é mais larga que a tela
- O `sim5-visita-cel-inteira.png` tem 856 px de largura (428 px de tela), contra os 780 px (390 px) dos outros dois faróis.
- No `sim5-visita-cel.png`:
  - o cartão "Visitas" passa da borda direita;
  - os valores da coluna da direita aparecem cortados: Ating. do mês, Meta, Projeção e Nec./dia (ex.: "1.458 (90…");
  - o cartão "Visitas por dia" também é cortado.
- Pedidos e Entregas não têm o problema.
- Causa provável: as barras por estado (PA/MA/AM) dentro do cartão Visitas, ou um rótulo sem quebra, forçam uma largura mínima.
- O que fazer: limitar a largura das barras dentro do cartão (`min-width:0` no cartão e na grade das barras) e conferir a 390 px sem rolagem lateral.

## 🟡 Pode ficar para depois
1. **Entregas:** a grafia "TRANS. TERCERIZADA" continua; o certo é "TERCEIRIZADA". Vem do dado do PC: pedir ao dono do robô.
2. **Entregas:** o título "Frete estimado · mês a mês (R$ e % sobre a nota)" ainda mostra só R$.
3. **Visita:** os cartões da 1ª linha esticam até o mais alto, com espaço em branco em "Vendedores em campo" e "Visitas por dia".
4. **Cartões no celular:** valores quebram no meio ("devoluções R$ / 5.552", "1 / s/ transp.").
5. **Resumo gerencial:** repete números dos cartões. Fica com o corretor-redundancias.
6. **Azul forte** nos gráficos de horário (Visita) e de SLA por filial (Pedidos): validar com o design-de-marca.

## 🟢 Ok
- **Entregas, tabela de frete:** UF fixa, com FRETE R$ logo depois de VALOR NF e REGIÃO no fim.
  - A 390 px aparecem UF · NOTAS · VALOR NF · FRETE R$.
  - A dica "Role para o lado para ver mais colunas →" e o TOTAL estão à vista.
- **Visita:** a barra RR sem dado saiu.
- **Consistência com o Inadimplência:**
  - "Baixado do ERP em";
  - os chips de estado;
  - os cartões com barra de cor e texto;
  - o Resumo gerencial.
- **Pedidos:** os 8 cartões ficam numa faixa só no PC e 2 por linha no celular.
- **Gráficos:** legíveis no celular, em 1 coluna.

## Pronto para mostrar quando
- N1 resolvido;
- nova `sim5-visita-cel(-inteira).png` com 780 px de largura e os valores do cartão Visitas inteiros.
- O resto pode ir como está.

---
# Reteste de UX: T-0017, Farol de Visita (largura no celular)

- Revisor: designer-ux · 25/11/2026
- Heads conferidos:
  - site: `origin/modulo-web/T-0017-tres-farois` **1d488f5**;
  - robô: **071b4cb**.
- Substitui o parecer do head 6ed0cf8.

## Veredito: 🟢 Pode mostrar ao Alexandre, com o texto do aviso trocado (🟡 abaixo)

## O 🔴 N1, da largura: resolvido
- As 3 imagens -cel e as 3 -cel-inteira têm 780 px de largura (390 px de tela). Antes o Visita tinha 856 px.
- No `sim5-visita-cel.png`, o cartão Visitas cabe inteiro. Ating. do mês, Meta, Ating. até 19/11, Projeção "1.458 (90%)" e Nec./dia aparecem completos.
- Os dois cartões de baixo ficam lado a lado, sem corte.
- Dados pessoais: continua limpo (só estados e números fictícios).

## O aviso "Cartões por estado indisponíveis" com as barras PA/MA/AM: 🟡 confunde
- Quem lê o aviso entende que não há número por estado. Logo abaixo, o primeiro cartão mostra visitas por estado.
- O aviso quer dizer outra coisa: não há **filtro** por estado (os chips) e os cartões são da BAP inteira.
- As barras são só a divisão das visitas, dentro do total.
- Texto proposto para a 2ª linha do aviso:
  - **"Sem filtro por estado: os cartões mostram a BAP inteira."**
- Assim o aviso não nega as barras e continua com 2 linhas.
- [SUPOSIÇÃO] As barras PA/MA/AM vêm de um dado confiável no pacote. Se não vierem, elas é que devem sair, e o aviso fica como está.
- É troca de texto, sem impacto de layout. Pode ir junto antes de mostrar, ou ser citada ao Alexandre como ajuste já previsto.

## Os demais
- Os 🟡 do parecer anterior (ux-tres-farois-b.md) seguem para depois. Nenhum bloqueia.
