---
id: R-20261127-172333-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0045
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T17:23:33-04:00
---
# T-0045 lote 2 entregue: visitas na nuvem com janela até 21h59 e sem 2º login no dia (web 0.16.0)

**No main:** #207 (RN-VIS-002 a 008, 960486e), #206 (contrato v1.2 e ADR 0004, e71e992), #210 (web 0.16.0, 9e3404c), #213 (transição, fafda45), #208 (robô da nuvem, 298c7e9), #212 (testes, 4557bfb). Revisor de código e corretor aprovados; UX e marca no #210; CI verde.

**O que muda:** a última busca do dia vai até 21h59 (antes parava 21h50); depois de um login recusado ou interrompido, não há outro login no mesmo dia, nem pelo "Retomar" nem pelo "Pedir diagnóstico" (RN-VIS-005); pedido de dias já fechados sai da fila com o motivo; as RN-VIS-002 a 008 estão no 03-regras.

**Como testar em 5 passos** (depois dos 4 passos do Render, com o serviço rodando):
1. No site, Visitas: conferir a agenda e o diagnóstico na tela do admin.
2. "Pedir diagnóstico": uma tentativa só; o resultado aparece na tela.
3. Se a Máxima pedir confirmação/captcha, a nuvem pausa e não tenta de novo no mesmo dia (nem com "Retomar").
4. Pedir um dia já fechado: o pedido sai da fila com o motivo (sem ficar parado).
5. No dia seguinte, o "Retomar" volta a permitir o login.

**Fica pendente:** painel_farol.py no buildFilter do render.yaml (governança do Alexandre; o build funciona sem isso).
