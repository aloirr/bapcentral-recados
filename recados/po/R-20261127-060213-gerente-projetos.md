---
id: R-20261127-060213-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: pedido
prioridade: normal
tarefa: T-0045
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T06:02:13-04:00
---
# T-0045: o que entrou, previsão corrigida e governança 1 (3 linhas do donos.json) para o Alexandre

T-0045: o que já entrou, a correção da previsão e o que depende do Alexandre agora.

## No main (06h00)
- #149: contrato v1.1 (42c81a1)
- #150: núcleo das visitas, da rota (d58b12f)
- #151: web 0.6.0, com rotas do serviço agendado, fila e tela "Atualizar visitas" (4728880). **No ar:** o /saude dá 0.6.0.
- #152: o botão do PC usa a regra do núcleo (0f3106a)
- #161: testes (núcleo, paridade e plano). Aprovado; entra assim que o CI der verde.

## Correção da previsão do resumo das 05h45
Eu disse "tudo no main até umas 07h". Isso vale só para os itens acima. Pela ADR 0004, §9, ainda faltam:
- **item 6** (modulo-robo): o robô pronto para rodar na nuvem. Começou agora.
- **item 7** (engenheiro-software): o Dockerfile.
- **item 8** (modulo-robo): o código do serviço agendado em `nuvem/visitas/` e a sincronização no robô. A parte do robô começou agora.
- **item 9** (testes): a matriz web nova × robô antigo.
- **item 10:** o render.yaml.

Os itens 7 e 8 dependem da **governança 1**, logo abaixo.

## Governança 1, para o Alexandre (pode ser feita já)
São 3 linhas no `.coord/donos.json`, para dar dono à pasta do serviço agendado:
```json
{ "padrao": "nuvem/visitas/Dockerfile", "dono": "engenheiro-software" },
{ "padrao": ".dockerignore", "dono": "engenheiro-software" },
{ "padrao": "nuvem/**", "dono": "modulo-robo" },
```
- Elas entram antes das regras gerais (a primeira que casa vence). O texto e o porquê estão em `docs/desenho/T-0045-render-yaml.md`, §3, no main.
- **Quem grava:** só o Alexandre. O guardião não deixa nenhum agente (nem o gerente) gravar o `donos.json` nem o `render.yaml`, e o time não contorna isso. É como foi no PR #57: uma sessão do Alexandre cria a branch `alexandre/T-0045-donos-nuvem` com as 3 linhas e abre o PR. Eu confiro o CI e faço o merge depois do "autorizo o merge do PR #N no commit <sha>".
- Na mesma sessão, ele pode corrigir a linha 40 do `.claude/agents/revisor-ux.md`. Ela ainda pede "Dados de … (Manaus)" visível na faixa, contra a decisão R-20261127-054626-po.

## Governança 2 (depois)
O `render.yaml`, num PR próprio do Alexandre (`alexandre/T-0045-render-yaml`), só depois dos itens 5, 7, 8 e 9 no main. O texto exato está em `docs/desenho/T-0045-render-yaml.diff`. Eu aviso quando chegar a hora, e aí seguem os passos 3 a 9 do passo a passo (`recados/anexos/T-0045/passo-a-passo-alexandre.md`).

## Na Máxima (pode ser feito já)
Passos 1 e 2 do passo a passo: o usuário só para o robô, somente leitura no Painel Auditoria. Usuário e senha ficam só com ele.
