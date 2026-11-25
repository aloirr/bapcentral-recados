---
id: R-20261124-211913-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: alta
tarefa: T-0017
responde_a: R-20261124-211805-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T21:19:13-04:00
---
# Atualizar a pasta Regionais - Leandro: o próprio ATUALIZAR_DO_GITHUB.bat faz isso (T-0003) — roteiro para o Alexandre

## Situação
- /saude em 0.2.0 desde 21:15 (pré-condição cumprida).
- Esta sessão do gerente NÃO alcança a pasta: o conector Microsoft 365 não está carregado aqui e nenhuma pasta foi compartilhada pelo Remote Control (R-20261124-211535-gerente-projetos).
- O pedido ("atualize ele com os arquivos necessários") é exatamente o que a ferramenta da T-0003 faz, no próprio PC, sem conector: baixa o main do GitHub, pega só os .py/.bat da raiz, NUNCA lê nem toca .json, bases (RELATORIOS/, SISTEMA BAP/, BAP Ajuda 2.0/), dados digitados nem segredos, faz o backup em SISTEMA BAP\BACKUP_RELATORIOS\ANTES_ATUALIZACAO_NOV2026, troca cada arquivo conferindo SHA-256 e, se algo falhar, restaura sozinho. Nada é apagado.
- Manifesto do main 9edfee9 (75 programas com SHA-256) para conferência: recados/anexos/T-0017/manifesto_regionais_leandro_main_9edfee9.csv.

## Decisão para o Alexandre (resposta pronta "N X")
1. Como atualizar: (A) o Alexandre roda o ATUALIZAR_DO_GITHUB.bat na pasta, primeiro simulando (roteiro abaixo; ~5 min); (B) compartilha a pasta pelo Remote Control e o gerente roda o mesmo processo; (C) o po faz pelo conector, arquivo a arquivo (75 programas; lento e só se o conector grava). Recomendo A. Resposta: "1 A".

## Roteiro do 1 A (no PC, na pasta PMZ/1 - PMZ/2025/IM PMZ/Regionais - Leandro — NÃO a "- Copia")
1. Se a pasta não tiver atualizar_do_github.py e ATUALIZAR_DO_GITHUB.bat, baixar os dois de https://github.com/aloirr/bapcentral (main) para a raiz da pasta.
2. Abrir o Prompt de Comando na pasta e rodar: ATUALIZAR_DO_GITHUB.bat --simular
3. Mandar ao po a saída (lista de novos / alterados / iguais; só nomes de programa e hashes curtos). Se sair o código 2 ("instalado por fora"), parar e mandar a saída: algum arquivo da pasta é mais novo que o main e eu confiro antes.
4. Com o ok do gerente sobre a lista, rodar: ATUALIZAR_DO_GITHUB.bat
5. Mandar ao po a saída final (código 0 = ok). Eu confiro os SHA contra o manifesto e aviso. Depois o robô roda no notebook (a pasta sincroniza pelo OneDrive) e o Farol de Inadimplência aparece no site.
