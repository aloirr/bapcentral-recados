---
id: R-20261127-101503-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: normal
tarefa: T-0054
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:15:03-04:00
---
# T-0054: a edição já existe para o admin; qual login foi usado no print? (+ P1 e P2)

T-0054: o desenho está pronto (PRs #178, a regra RN-POS-011, e #179, o desenho). O modulo-web já está na simulação.

**Achado principal:** a edição do Farol de Entregas no site já existe desde a T-0021 v4, mas só para o **admin**. O PC está só leitura desde 25/11. Resultado: hoje o pós-venda não edita em lugar nenhum. A T-0054 abre a mesma edição para o **pós-venda** (e mantém o admin):
- abas Entregas e Pendências;
- as 6 edições do PC: ETAPA, TRANSPORTADORA, DT. PREVISTA, DT. REAL, RESPONSÁVEL e VLR FRETE (REAL);
- o robô grava só acrescentando (regra 7).

**Pergunta para fechar o diagnóstico (não trava nada):** com qual login o Alexandre tirou o print do Farol de Entregas?
- **Se foi com um login que não é admin:** é o caso acima, e a T-0054 resolve.
- **Se foi com o admin:** ele já deveria ver a edição. Então o pacote chegou ao site sem a parte de edição (por exemplo, o robô do notebook em versão antiga). Nesse caso, investigo isso à parte e com prioridade.

**Perguntas ao Alexandre, com recomendação (o padrão adotado vale até a resposta):**
- **P1:** o gerente também edita o Farol de Entregas? **Recomendação e padrão: não**; só admin e pós-venda.
- **P2:** o pós-venda também edita "Notas com frete", no Fretes (T-0037)? **Recomendação: sim**, porque é a mesma linha da aba ENTREGAS. **Padrão até o "sim": só admin.**

Previsão: a de antes continua valendo. Simulação para você até umas 14h.
