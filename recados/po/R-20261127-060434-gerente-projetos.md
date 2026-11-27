---
id: R-20261127-060434-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: resposta
prioridade: normal
tarefa: T-0050
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T06:04:34-04:00
---
# T-0050 aberta: acesso aos faróis por usuário (plano, P1 e prazo)

**T-0050 aberta:** escolher o acesso aos faróis por usuário, na tela Usuários (só admin). O pedido é do Alexandre (R-20261127-060328-alexandre).

## Plano
1. **Desenho** (engenheiro-software, começou agora):
   - o modelo: o perfil dá o padrão e o admin marca ou desmarca;
   - uma só regra `pode_ver(usuario, rid)`, usada pelo menu e pelo servidor;
   - o registro de quem mudou;
   - as restrições de perfil continuam por cima;
   - o texto da RN-GER-018.
2. **Simulação** (designer-ux): a tela Usuários com a lista de faróis marcáveis, no PC e no celular, com dados fictícios. Vai a você para aprovar por delegação.
3. **Código** (modulo-web): entra logo depois da web da T-0036, como você pediu. Os perfis analista e trade chegam com ela.
4. **Testes** (testes): 403 por perfil × usuário, o menu e o registro.

## Pergunta que deve ir ao Alexandre (com recomendação)
- **P1:** o admin pode dar a um usuário um farol que o perfil dele não vê?
  - **A: não, no v1 só restringe** (recomendado: ampliar pode abrir dado restrito ao perfil, como o TOTAL A PAGAR ou a tabela com cliente);
  - B: pode ampliar.

O desenho pode trazer outra pergunta; mando junto com a simulação.

## Prazo (Manaus)
- Desenho e simulação para você: hoje, até umas 08h.
- Código e testes: hoje à tarde, depois que a T-0036 entrar.
