---
id: R-20261126-182050-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: normal
tarefa: T-0035
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-26T18:20:50-04:00
---
# T-0035: simulação do selo Desatualizado e um ponto de governança (recado de subagente)

# T-0035: simulação do selo "Desatualizado" e um ponto de governança

## Simulação (única mudança de tela da T-0035)
Imagens com dados fictícios, em `recados/anexos/T-0035/`:
- `selo-pc.png` (1366);
- `selo-cel.png` (390).

Quando o envio de um farol falha e os dados têm mais de 26 h, o cabeçalho do farol mostra o selo amarelo "DESATUALIZADO", ao lado da data dos dados. Isso segue a opção A da decisão pendente (R-20261126-181202).

O resto da T-0035 não tem tela:
- o robô manda um arquivo por farol (gzip): os 6 faróis de hoje somam 1,8 MB, contra o teto de 8 MB por farol;
- a web guarda só o índice e lê o farol do disco, com cache de 96 MB;
- o `/saude` mostra a memória.

Branches prontas: contrato e97761f, web 527004f (v0.4.0), robô 5231f19. O testes está fazendo a prova ponta a ponta das 4 combinações robô × web. Depois vêm revisor e PRs (previsão 27/11 14h, mantida).

## Decisão
1. Selo "Desatualizado" e farol herdado até 26 h: (A) aprovado, como na imagem · (B) ajustar.

## Ponto de governança (para você saber)
- Um subagente (modulo-robo) gravou recados em nome próprio: R-20261126-181930-modulo-robo e R-20261126-181933-modulo-robo. Até aqui o `coord.mjs` só aceitava `--de` igual ao agente da sessão (gerente-projetos), e os pareceres de subagente iam com `--de gerente-projetos` e nota de origem (decisão 3 A).
- O conteúdo está correto. O provável é que ele tenha trocado o `BAP_AGENTE` só no comando.
- Os subagentes passam a usar só a regra 3 A. Se o Alexandre quiser que cada subagente grave em nome próprio, é mudança de governança, em `scripts/coord.mjs` e nos guardiões.
