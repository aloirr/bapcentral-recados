---
id: R-20261123-192521-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre, gerente-projetos]
tipo: entrega
prioridade: alta
tarefa: T-0010
responde_a: R-20261123-191448-alexandre
encerra: false
contrato: null
criado_em: 2026-11-23T19:25:21-04:00
---
# T-0010 instalada na pasta de produção (7 arquivos, backup e conferência byte a byte)

Sessão BAPCentral - Cowork, 23/11/2026, 19:25 (Manaus), com o "instale" do R-20261123-191448-alexandre. O instalador `.bat` não foi usado: o shell do Cowork no PC estava indisponível (atualização do Windows), então os arquivos foram gravados pela ponte de arquivos do app, com a mesma regra (backup antes, trava de data, conferência depois).

## Antes
- Os 5 arquivos da produção eram idênticos ao `99fc41c` do repositório (nada instalado por fora).
- Backup em `SISTEMA BAP\BACKUP_RELATORIOS\ANTES_T0010_NOV2026`: bap_dados.py, relatorios_nucleo.py, planner_nucleo.py, bap_planner.py, smoke_relatorios.py — conferido byte a byte contra a produção.
- Uma primeira tentativa de gravação caiu (o PC desligou da sessão); conferido depois: nada tinha sido gravado. Gravado de novo em 3 lotes, cada arquivo travado na data de antes (não sobrescreve se mudou).

## Instalado (versão do main 249380a; conferência byte a byte: 7/7 iguais)
| Arquivo | sha256 (12) |
|---|---|
| bap_dados.py | b33af935e460 |
| relatorios_nucleo.py | 50599f14a2ee |
| planner_nucleo.py | 99700b47934d |
| bap_planner.py | b3279f59c29f |
| smoke_relatorios.py | ea9cc663db5b |
| atualizar_do_github.py (novo) | f1bc8bc65c16 |
| ATUALIZAR_DO_GITHUB.bat (novo, CRLF) | a3aaecf4efae |

Os 7 compilam (Python 3.12). Fora, como decidido: os 13 `.bat` (final de linha) e o `bap_automation.py` (senha do robô no cofre antes).

## Como testar em 5 passos
1. No PC, abra o Planner (abrir_planner.bat) e gere a rota de um supervisor como sempre.
2. Exporte o JSON da rota da Máxima e confira, num cliente de visita semanal, que a frequência do JSON é a mesma do Planner (RN-ROT-001).
3. Abra a BAP Central e o Farol de Roteirização: a VISITA_SEMANAL aparece nas visitas (o cache da base refaz uma vez, marca b5; é normal demorar um pouco mais na primeira abertura).
4. Rode RODAR_TESTE_BAP.bat (smoke dos relatórios): só as falhas conhecidas.
5. Se algo der errado: copie os 5 arquivos de `SISTEMA BAP\BACKUP_RELATORIOS\ANTES_T0010_NOV2026` de volta para a pasta e avise.
