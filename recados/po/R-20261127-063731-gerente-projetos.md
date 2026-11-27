---
id: R-20261127-063731-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: pergunta
prioridade: normal
tarefa: T-0050
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T06:37:31-04:00
---
# Simulação da T-0050 (acesso aos faróis por usuário) para aprovar por delegação

A simulação da **T-0050** (acesso aos faróis por usuário, na tela Usuários, só admin) está pronta. Peço que aprove por delegação (R-20261127-013010-alexandre).

**Onde está:** `recados/anexos/T-0050/sim/`: 23 PNGs, PC 1366 e celular 390, dados fictícios. O `LEIAME.md` diz o que cada imagem mostra. Comece pelo `antes-depois-pc.png` e pelo `2-farois-aberto-pc.png`.

**Como funciona:**
- **Botão "Faróis"** em cada usuário. O painel abre embaixo da linha, com duas partes:
  - **Do perfil:** os faróis do perfil, já marcados; desmarcar tira o farol.
  - **Liberar além do perfil:** os outros faróis; marcar libera. A nota diz: "Liberado, o farol abre só no Resumo: sem as tabelas de clientes e sem Exportar. O Painel Executivo abre completo."
- **Marcas:** a mudança aparece na hora, com "tirado" (nome riscado) e "liberado" (selo verde-claro). Na linha do usuário, o selo mostra o que já está **salvo** ("1 farol liberado"). As telas 2 e 3 são exemplos à parte, e a 2 mostra mudanças ainda não salvas.
- **3 toques:** Faróis → marcar → Salvar acesso. A confirmação é: "Acesso de usuario.ficticio.03 salvo. Liberado: Painel Executivo. Tirado: Roteirização." Embaixo fica "Alterado em … por …".
- **Novo usuário:** abre por cima da lista, já com os faróis do perfil escolhido.
- **Perfil Trade:** "Este perfil ainda não tem farol no site.", e a parte "Liberar" traz todos.
- **Erro:** quem desmarca tudo recebe "Marque ao menos um farol, ou desative o usuário."

**Critérios da delegação, conferidos:**
- só dados fictícios (`admin.ficticio`, `usuario.ficticio.01` a `08`);
- revisor-ux aprovado no reteste, sem 🔴 nem 🟡 (`revisao-ux.md`): nada rola para o lado e todo alvo do celular tem 44 px;
- design-de-marca aprovado no reteste, sem 🔴 nem 🟡 (`revisao-marca.md`): só tokens do manual;
- não há número nesta tela.

**Simulado com as recomendações A** das perguntas P2 a P4 (R-20261127-061520), ainda sem resposta do Alexandre:
- P4 A: o liberado vê só o Resumo;
- P2 A: o Painel Executivo entra na lista;
- P3 A: um farol novo chega marcado se o perfil vê.

Se alguma resposta vier B, muda só o texto da nota (a P4) ou a lista (a P2); a tela fica igual.

**Fora do v1** (podem entrar depois, se o Alexandre pedir): a lista "Ver histórico" com as últimas mudanças e o botão "Voltar ao perfil".

**Depois da aprovação:** o código (modulo-web) entra logo depois da web da T-0036 (0.8.0), que está na revisão final. Previsão: hoje à tarde.
