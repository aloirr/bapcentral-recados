---
id: R-20261126-175814-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: normal
tarefa: T-0033
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-26T17:58:14-04:00
---
# Migração completa PC → site: inventário, 16 tarefas com prazo, o que fica no PC e 8 decisões

# Migração completa PC → site: inventário, tarefas, prazos e decisões (resposta ao R-20261126-174334-alexandre)

Anexos (sem dado pessoal), em `recados/anexos/T-0033/`:
- `inventario-pc-site.md`: os 79 itens do PC, um por linha;
- `revisao-ux-geral.md` e `revisao-marca-geral.md`: revisão geral de todos os faróis.

A revisão de redundâncias ainda está rodando e entra na T-0033.

## 1. Inventário PC × site (79 itens do BAP Central do PC)
| Estado | Itens |
|---|---|
| Já no site | 19 |
| Em PR aberto (T-0023, T-0024, T-0025, #82) | 15 |
| Falta | 25 |
| Fica no PC (motivo no item 5) | 15 |
| Não migrar (sem uso) | 5 |

## 2. Revisão geral (corretor, marca, design): primeira tarefa
- **Marca: 3 🔴.**
  - No BC3, o logo virou um quadrado verde e "BAP AUTOPARTS" sumiu da tela.
  - A mensagem do "Cobrar no WhatsApp" diz "BAP Auto Parts".
  - O PDF exportado pelo site sai sem o nome da empresa e com um verde fora da paleta.
  - Também há 7 verdes soltos, 3 famílias de fonte e contraste baixo na faixa verde.
- **UX: 5 🔴.**
  - Dois visuais no site: Painel, página inicial, Usuários, Login, Senha e Parcial ainda fora do BC3.
  - Rolagem para o lado dentro da tabela em quase todo farol (só o Pedidos tem grade × popup).
  - No celular, só o Pedidos tem o M3.
  - Páginas de 100 linhas em vez da rolagem por dentro.
  - Usuários com 3 botões verdes e "Desativar" sem confirmação.
- **Feito hoje:** o #124 (T-0032) entrou no ar antes da simulação e cortava o Exportar no celular. A correção está no PR #126 (uma linha de CSS), em revisão, e entra hoje.

## 3. Tarefas na ordem, com prazo (Manaus)
Tamanho em horas de agente (P ≤ 3, M 4–8, G > 8). "Simulação" é a data em que o PNG chega para aprovar; o merge vem depois do seu "ok".

| # | Tarefa | Donos | Tam. | Prazo |
|---|---|---|---|---|
| 1 | T-0033 Revisão geral: correções de marca, UX e redundância; grade × popup por farol; contrato visual BC3 | modulo-web, engenheiro-software, testes | M | simulação 27/11 03h |
| 2 | T-0034 Página inicial = Painel Executivo no BC3/M3, mais Usuários e Senha no BC3 | modulo-web, testes | M | simulação 27/11 08h |
| 3 | T-0035 Um pacote por farol, lido do disco sob demanda (ADR 0003). Sem tela; necessário para o Render de 512 MB aguentar a migração | engenheiro-software, modulo-robo, modulo-web, testes | G | PRs 27/11 14h |
| 4 | T-0024 Lote 2: Indicadores, Clientes, Roteirização, Giro, Estoque FRW. Simulação refeita com as colunas reais; a primeira tinha colunas inventadas e não foi mandada | modulo-web, modulo-robo, testes | M | simulação 26/11 22h; merge depois da T-0035 |
| 5 | T-0023 v2 Garantias, Devoluções, NCC, refeitos sobre o main (os 4 PRs antigos serão fechados) | modulo-web, modulo-robo, modulo-farois, testes | M | simulação 28/11 10h |
| 6 | T-0025 v2 DDR, Campanhas, Expositores; TOTAL A PAGAR só admin/gerente/diretor; parâmetros das campanhas pela web (só admin) | web, robô, faróis, pós-venda, testes | G | simulação 28/11 20h |
| 7 | #82 (T-0026) testes das parciais | testes | P | merge hoje 20h |
| 8 | T-0036 Faróis do Analista (Saldo, Markup, Preço, Divergências) e perfis analista e trade | robô, web, testes | M | simulação 29/11 12h |
| 9 | T-0037 Farol de Fretes com edição | web, robô, faróis, pós-venda, testes | M | simulação 29/11 18h |
| 10 | T-0038 Parcial BAP, Exportar para o RH e o PDF de cada pessoa para baixar | robô, faróis, rota, web, testes | M | simulação 30/11 12h |
| 11 | T-0039 Painel Executivo completo: Excel, filtro por supervisor, mês anterior fechado | robô, web, testes | M | simulação 30/11 18h |
| 12 | T-0040 Trocar loja de coleta pela web (só admin, gravado pelo robô) | web, robô, testes | M | simulação 01/12 10h |
| 13 | T-0041 Cadastros do Analista em leitura (Planner, Metas/RV, Kits, Meta de saldo, Transportadoras, rotina DDR) | rota, metas, pós-venda, robô, web, testes | G | simulação 02/12 12h |
| 14 | T-0042 Os mesmos cadastros com edição pela web (gravada pelo robô) | idem | G | simulação 03/12 18h |
| 15 | T-0043 Página "Dados e robô": hora de cada fonte, última rodada, erros | engenheiro-software, robô, web, testes | M | simulação 04/12 12h |
| 16 | T-0044 Desligar no PC o que ficou 2 semanas igual ao site | faróis, engenheiro-software, testes | P | a partir de 18/12, farol a farol, com o seu "ok" |

São cerca de 126 h de agente, com 3 a 4 frentes em paralelo. A migração termina em 04/12 se as aprovações vierem no mesmo dia.

## 4. Página inicial
`/` abre o Painel Executivo no formato dos faróis: BC3 no PC (barra lateral, faixa verde com os números, abas curtas sem rolagem) e M3 no celular. Vale para admin, diretor e gerente. O menu lateral é por área (Diretoria, Pré-venda, Pós-venda, Vendas, Conta). Simulação na T-0034.

## 5. O que fica no PC, e por quê
1. **Robô e downloads do ERP.** O BAP Tools fica na rede interna, que o Render não alcança, e a senha está no cofre do Windows (regra 5). No site vão a hora dos dados e a última rodada (T-0043).
2. **"Atualizar dados".** A conta usa os arquivos locais; o site não calcula (ADR 0001).
3. **"Atualizar visitas".** Usa o login da Máxima (segredo, regra 5) e o Excel do Forms pelo OneDrive. Ler isso do Render exigiria o Graph (regra 9).
4. **Envio de e-mail** (Parcial, Inadimplência, Rota). Sai pelo Outlook do computador; mandar do Render exigiria Graph/SMTP (regras 9 e 5). O PDF de cada pessoa vai ao site para baixar (T-0038).
5. **Exportar campanha (premiação).** Leva CPF, CNPJ e e-mail (regra 6). No site vai o fechamento sem documento.
6. **"Abrir no Excel".** Abre a planilha da pasta. No site já existe o Exportar Excel.
7. **A gravação das edições.** A tela vai ao site, mas quem grava é o robô no PC, só acrescentando linha (regra 7).
8. **Coordenadas dos clientes.** As chaves do Google e do TomTom ficam só na pasta de produção (regra 5).
9. **Cálculos pesados** (Recalcular Planner, Gerar DDR, dividir meta de saldo, Gerador de Meta). Você pede no site e o robô executa (T-0042).
10. **Sincronização do BAP Ajuda, instaladores e rotina diária.** São a infraestrutura do PC.
11. **Não migrar:** `conta_email.py` (usa o Graph, regra 9, e ninguém usa), Painel do Diretor antigo, IDs do LEGADO, `bap_acesso.json` (trocado pelo perfil do site) e "Relatórios do time" (vira o menu do site).

## Decisões que você precisa tomar (recomendo A em todas)
1. **Ordem das tarefas:** (A) como na tabela acima · (B) outra prioridade (diga qual).
2. **Perfis que não veem o Painel** (pré-venda, pós-venda, vendas) abrem em: (A) o primeiro farol da área · (B) um resumo da área.
3. **Perfis novos "analista" e "trade":** (A) criar os dois na T-0036 · (B) por enquanto, usar admin e gerente.
4. **Meta RH no site:** (A) só no Exportar para o RH, para admin e gerente · (B) só admin.
5. **"Pedir rodada do robô" pelo site:** (A) sim, só admin, atendido na volta de 30 min (T-0043) · (B) não.
6. **Configs editadas pela web** (transportadoras, metas, Planner, kits): (A) um "autorizo" seu por arquivo, como no champions · (B) uma autorização geral agora.
7. **Botão verde "Cobrar no WhatsApp"** (entrou no #124 sem pedido e repete a aba de mesmo nome): (A) tirar o botão; fica a aba · (B) manter.
8. **Manual da marca:** não existe no repositório. (A) o design-de-marca monta o rascunho com o logo e as cores que você já viu (visual C e BC3), para você aprovar · (B) você manda o manual.

Resposta pronta: **"1 A, 2 A, 3 A, 4 A, 5 A, 6 A, 7 A, 8 A"**
