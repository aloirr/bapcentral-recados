# T-0023 v2 e T-0025 v2 · Reteste final de redundância do desenho (corretor-redundancias)

- **Escopo:**
  - `git diff 97ccba7 origin/engenheiro-software/T-0023-T-0025-contrato`, nos 6 arquivos: contrato, ADR 0001, ADR 0005, os dois desenhos e o diário;
  - `git diff 58760c0 origin/gerente-projetos/T-0023-regras`, no `docs/produto/03-regras.md`.
- **Heads revisados:** desenho `970e625a6d19b9c9b7cb9bde312bee3d5c8f1467`; regras `c8f445a89f5200952f02908bbbd341d667e9a7c4`.
- **Resultado:** **não libera por 1 resto.**
  - Fecharam 7 dos 8 achados: o RD-0093, o RD-0095 e do RD-0105 ao RD-0109.
  - O RD-0104 tem 1 resto em aberto, de dono gerente-projetos: a RN-GER-012 traz só uma das 2 garantias da edição no lugar.
  - A correção não criou repetição nova. Não há RD novo.

## Os 8 achados

| ID | Situação | Evidência no head |
|---|---|---|
| RD-0093 (resto) | fechado | T-0023 §4 e T-0025 §4 só apontam para o §10.9.6. O resumo que não tinha o passo 1 saiu, e o "Antes" e o "lote B só depois do A" ficaram só no contrato (1271). A T-0025:41 saiu |
| RD-0095 (resto) | fechado | Os desenhos só citam as RNs ("RNs: … (`03-regras.md`, fonte da verdade)"). A RN-GER-015 do `03-regras.md` já tem a P4 A, e a RN-GER-016 tem um texto só |
| RD-0104 | **resto em aberto** | abaixo |
| RD-0105 | fechado | O contrato saiu do bloco "O que `vendas` vê" e só aponta para a RN-GER-015 e para a T-0025 §7. O "vendas refaz" fica só no contrato:1189. A T-0025 §7 e o risco 3 apontam para o §10.9.4 |
| RD-0106 | fechado | ADR 0001, adendo 6, itens 2 e 3, como proposto |
| RD-0107 | fechado | T-0023:36 e :128 apontam para o §7, e os campos do contato ficam só no §7 |
| RD-0108 | fechado | contrato §10.9.2, "A web não calcula número": o robô regrava com o `garantias.novo_ticket` da hora. O `edicoes.py` saiu da lista do modulo-web, e o critério 5 foi ajustado |
| RD-0109 | fechado | o ADR:55 não repete o "um teste por passo", e o contrato:1240 não repete o "só ao admin" |

### RD-0104 (resto) · A RN-GER-012 traz só uma das 2 garantias da edição no lugar
- **Onde:**
  - No `03-regras.md` (`c8f445a`), a RN-GER-012 diz: "o que a tela troca no lugar (DDR, Expositores e arquivo de configuração, RN-GER-016), o robô troca e guarda antes o valor anterior (`antes`), para dar para desfazer".
  - A cópia do arquivo saiu da RN-GER-016, mas não entrou na RN-GER-012. Hoje nenhuma RN tem a cópia.
  - O contrato §10.9.3 (1145-1150) dá **as 2 garantias** aos 3 arquivos: o `antes` e a cópia do dia. A ADR 0005 §3.5 e o risco 1 da T-0025 mandam para elas.
- **O que mudou desde o reteste anterior:** a regra está agora numa RN só, com o escopo certo (DDR, Expositores e config). Falta a 2ª garantia, e o texto ainda cita o nome do campo (`antes`), que é mecanismo do contrato.
- **Tipo:** doc. **Impacto:** decisão. O `testes` testa pela RN (`test_RN_GER_012_*`), e a cópia antes só aparece no contrato.
- **Severidade:** média.
- **Dono:** gerente-projetos.
- **Proposta:** no `03-regras.md`, RN-GER-012, **antes:** "o robô troca e guarda antes o valor anterior (`antes`), para dar para desfazer." → **depois:** "o robô troca, guarda o valor anterior de cada troca e faz uma cópia do arquivo no dia, antes da 1ª gravação, para dar para desfazer."

## Repetição nova
Nenhuma. O que entrou nesta correção cita a fonte e não reescreve a regra:
- **contrato:** as Fontes citam as RNs (1032); o §10.9.3 aponta "menos o contato da garantia, RN-GER-012"; o §10.9.4 aponta para a RN-GER-015;
- **ADR 0005 §3.6:** aponta para a RN-GER-016;
- **RN-GER-012 e RN-GER-016:** uma aponta para a outra;
- **T-0023, modulo-robo:** a linha do ticket cita o §10.9.2;
- **T-0023, critérios 3 e 5:** são casos de teste novos, não repetição.

## Liberação
**Não libera** até o resto do RD-0104 no `03-regras.md`. O desenho (`970e625`) não tem achado em aberto.

[SUPOSIÇÃO] Por instrução de quem chamou, ficaram de fora o catálogo, os recados aos donos, o commit e qualquer alteração no clone de código.
