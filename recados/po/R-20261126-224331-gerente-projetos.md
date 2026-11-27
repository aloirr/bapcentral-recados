---
id: R-20261126-224331-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: normal
tarefa: T-0045
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-26T22:43:31-04:00
---
# T-0045: visitas da Máxima no site — desenho, custo e 5 decisões

# T-0045: visitas da Máxima no site (opção C) — desenho pronto e 5 decisões

O desenho está no ADR 0004, sem código: branch `engenheiro-software/T-0045-visitas-render` 070411c, com cópia em `recados/anexos/T-0045-adr-0004.md`. Pedido: R-20261126-182728-alexandre.

## Resumo
- **Onde roda:** o navegador com a Máxima usa de 420 a 740 MB (estimativa) e não cabe junto do site no plano de 512 MB. Proposta: um serviço agendado à parte no Render, só para as visitas. Esse serviço usa um plano de 2 GB cobrado por minuto, cerca de US$ 1 a 3 por mês (preço a conferir no Render). O site continua no Starter de US$ 7. A senha da Máxima fica só nesse serviço, fora do site que atende a internet.
- **Senha:** entra só como variável secreta no painel do Render, criada por você. O time nunca vê o valor.
- **Quando roda:** às 06h00 (Manaus), baixando o dia anterior, e quando alguém aperta "Atualizar visitas" no site, com o início em até 10 min. Uma rodada por vez. O botão do PC continua.
- **Tempo:** hoje o PC leva cerca de 2 a 2,5 min por dia de visitas. Na nuvem, estimo 5 a 8 min na rodada das 06h e 20 a 40 min no botão com 7 dias, com limite de 45 min.
- **Volta ao PC:** o robô do PC traz as visitas do site na volta de 30 min e só acrescenta (regra 7). Nunca apaga nem sobrescreve o Excel. A montagem, o acompanhamento e a Prospecção continuam no PC. Regras novas propostas: RN-VIS-001 a 005.
- **Falhas:** confirmação, captcha, código por SMS/e-mail ou senha errada pausam as rodadas até o admin clicar em "Retomar". Tela mudada ou Máxima fora aparecem com aviso claro.
- **Maior risco:** a Máxima pedir confirmação ou bloquear o acesso vindo do Render (servidor nos EUA). Só um teste real responde: o primeiro passo depois do código é um diagnóstico no Render.
- **Tamanho:** cerca de 32 h de agente. O `render.yaml` muda, então o PR de governança precisa do seu "autorizo".

## Decisões (recomendo: 1 A, 2 A, 3 A, 4 A, 5 B)
1. **Onde roda:** (A) serviço agendado à parte, ~US$ 1 a 3/mês · (B) dentro do site, subindo o plano do site (cerca de +US$ 18/mês).
2. **Horário automático:** (A) 06h00 · (B) 06h00 e 12h30.
3. **Quem aperta "Atualizar visitas" no site:** (A) admin e gerente · (B) só admin.
4. **Login da Máxima usado pelo site:** (A) um usuário próprio para o robô (recomendado: não usa o seu) · (B) o seu.
5. **Print da tela em caso de erro:** (A) guardado no site, só para o admin (pode conter dado de cliente) · (B) sem print, só o código do erro.

Resposta pronta: **"1 A, 2 A, 3 A, 4 A, 5 B"**.

Previsão: depois das decisões e do seu "autorizo" no PR de governança, o código fica pronto em cerca de 2 dias. O diagnóstico no Render vem antes de ligar a rotina.
