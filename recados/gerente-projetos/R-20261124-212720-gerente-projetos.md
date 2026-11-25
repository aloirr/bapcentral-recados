---
id: R-20261124-212720-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T21:27:20-04:00
---
# Parecer do designer-ux: entrega 2 head c97d981 — imagens liberadas; 1 🔴 de código (envio adiado)

> Parecer do designer-ux (subagente do gerente-projetos; gravado pelo gerente sem alteração; varredura de nomes do pacote real e CPF/CNPJ: limpo).

# Reteste de UX: T-0017, entrega 2 (Títulos, Por cliente, Cobrar no WhatsApp)

- Revisor: designer-ux · 25/11/2026
- Branch `origin/modulo-web/T-0017-cobranca-web`, **head c97d981**. Substitui o parecer do head 5e07a32 e vale só para este head.
- Conferi as 14 imagens sim4-* inteiras (titulos, cliente, gerente, cobranca, cobranca-desfazer, cobranca-erro e cobranca-tratados, cada uma em pc e cel).
- Conferi também o código: `cobranca.js` e `estilo.css`, no head.

## Veredito
- **As imagens podem ir ao Alexandre.** Os 6 🔴 do parecer anterior caíram.
- **Fica 1 🔴 novo, no código.** Não aparece nas imagens, mas tem de ser resolvido antes do PR: o envio adiado pode perder registro (item N1).

## Dados pessoais: limpo
- Conferi as 14 imagens e os 5 HTML (o texto inteiro, com a mensagem, as tabelas e os campos). Não há:
  - nome fora dos padrões "Cliente NNN", "Vendedor NN" ou "Supervisor NN";
  - CPF nem CNPJ;
  - telefone fora da faixa fictícia (92) 90000-NNNN.
- Os PNG de desfazer, erro e tratados conferi só no visual. O texto que aparece neles também segue o padrão.

## Os 6 🔴 anteriores
1. **Dado pessoal: resolvido.** A mensagem foi remontada com o nome fictício.
2. **Captura quebrada: resolvido.** São recortes de uma tela, sem falha, e a fila tem 10 cartões por página.
3. **Valor escondido: resolvido.**
   - Títulos abre com CLIENTE · NOME · SALDO · VALOR; Por cliente, com CLIENTE · NOME · EM ATRASO.
   - O código do cliente fica fixo e não quebra linha; há sombra na borda direita.
   - No celular aparece a dica "Role para o lado para ver mais colunas →".
4. **Aba cortada: resolvido.** As abas quebram em 2 linhas, e "Cobrar no WhatsApp" aparece inteira.
5. **Clique errado: resolvido no desenho.**
   - "Abrir WhatsApp" é o único botão cheio.
   - "Marquei como enviado" (contorno) só aparece depois de abrir o WhatsApp.
   - "Pular" é neutro, em link, na outra ponta da linha.
   - Há "Desfazer" ao lado do selo.
   - No cartão sem número só sobra "Pular", com "⚠ Sem celular: digite um número".
6. **Situações: resolvido.** As imagens mostram:
   - A COBRAR;
   - ENVIADO 21/11;
   - ENVIADO HOJE + Desfazer;
   - ERRO AO REGISTRAR + "Não foi possível registrar. Tente de novo.";
   - o bloco "Já tratados hoje (2)" com ENVIADO HOJE e PULADO HOJE;
   - o contador "137 clientes · 2 já tratados hoje".

## 🔴 novo, antes do PR

### N1. O envio adiado pode perder registro sem ninguém ver (`cobranca.js`, `ESPERA`, `pendentes` e o `pagehide`)
- O registro fica 10 s só na memória da página e só é gravado depois desse prazo ou no `pagehide`.
- O uso real no celular é justamente sair do navegador. A pessoa marca o cliente A e, antes de 10 s, toca em "Abrir WhatsApp" do cliente B:
  - o navegador vai para segundo plano, e isso **não dispara `pagehide`**;
  - o temporizador fica congelado;
  - se o sistema fechar a aba enquanto ela está no WhatsApp (comum no Android com pouca memória), o registro do cliente A se perde.
- Mesmo quando o envio sai pelo `pagehide` (com `keepalive`), a resposta não volta para a tela. Um erro (sessão vencida, pacote trocado) some sem aviso.
- Durante os 10 s o selo já diz "ENVIADO HOJE", e a pessoa entende que está gravado.
- O que fazer, tudo barato:
  - a) enviar os pendentes também no `visibilitychange` para `hidden`;
  - b) enviar os pendentes ao tocar em "Abrir WhatsApp" de **outro** cartão e ao trocar de página da fila;
  - c) durante a espera, o selo mostra **"ENVIADO · desfazer (10 s)"** e só vira "ENVIADO HOJE" depois que o servidor responder ok;
  - d) [SUPOSIÇÃO] se o `keepalive` falhar, guardar o pendente no `sessionStorage` e reenviar ao voltar à página.
    - O servidor já ignora a repetição em 60 s (`REPETIDO_S`), mas um reenvio mais tarde precisa de chave do registro feita no navegador para não duplicar.
    - Isso fica para o dono decidir com o revisor-codigo.
- Alternativa equivalente: gravar na hora e fazer o "Desfazer" acrescentar um registro de cancelamento no diário (só acréscimo, regra 7). Esse caminho não perde nada, mas muda o contrato com o PC.

## 🟡 Pode ficar para depois (ou ir junto, se for rápido)
1. **Selo ERRO AO REGISTRAR** sai em amarelo, igual a A COBRAR. Erro deve ser vermelho (o mesmo tom de VENCIDO) para não ser lido como "pendente normal".
2. **Tentar de novo depois do erro:** na imagem de erro, o cartão volta só com "Abrir WhatsApp" e "Pular".
   - Se "Marquei como enviado" sumir, a pessoa vai reabrir o WhatsApp e mandar a mensagem duas vezes ao cliente.
   - Manter "Marquei como enviado" à vista depois do erro. O código parece manter; a imagem mostra o contrário, então conferir.
3. **Durante o Desfazer**, "Marquei como enviado" e "Pular" continuam desenhados como ativos (estão desligados no código). Esconder os dois enquanto o Desfazer estiver à vista.
4. **"Já tratados hoje"** só aparece na última página (14 de 14). O contador do topo "2 já tratados hoje" deve ser link para o bloco, ou o bloco deve vir no topo, recolhido.
5. **Cabeçalho do cartão estoura a borda** quando a cidade é longa ("BARRA DO BUGRES/MT"): o valor e a caixa de mensagem passam uns 8 px da borda direita (cartões 057 e 069, no PC). Usar `min-width:0` e reticências na linha da cidade.
6. **Celular, depois de abrir o WhatsApp:** três botões numa linha, e "Marquei como enviado" quebra em 3 linhas. Pôr "Marquei como enviado" em linha própria, de largura cheia, logo abaixo de "Abrir WhatsApp".
7. **"Filtros" recolhido em Títulos** não tem o triângulo: o `display:flex` no `summary` (`estilo.css:144`) apaga o marcador. Pôr "▸ Filtros" e "▾ Filtros". Hoje parece um título solto.
8. **"BAP Auto Parts"** no texto da mensagem: os materiais usam "BAP AUTOPARTS". O texto é o modelo do PC; levar ao Alexandre como pergunta, sem bloquear.
9. **Selos da tabela:** em Por cliente, FAIXA "91–180 DIAS" sai sem selo, enquanto "+180 DIAS" tem selo. A escala da faixa continua pendente do PC.
10. **"Limpar", "« Anterior" e "Próxima »"** ainda saem no azul padrão do navegador.

## 🟢 Ok
- **Aviso:** "Situação do PC até 21:15. O que você marcar aqui chega ao PC às 08h ou 14h." é curto, fica no topo e diz o que fazer com a informação.
- **Gerente** (PC e celular): só Resumo · Títulos · Por cliente; sem telefone, sem botão, sem a aba de cobrança (RN-POS-004).
- **Consistência com a entrega 1:** abas, faixa de dados, título e cartões com a mesma borda e sombra do Resumo.
- **Textos:** "Mensagem", "Outro telefone (só neste envio)", "DDD + número" e os avisos de telefone estão curtos e dizem a ação.
- **3 toques:** cobrar = Abrir WhatsApp → (envia) → Marquei como enviado, 2 toques no site. Pular = 1 toque.
