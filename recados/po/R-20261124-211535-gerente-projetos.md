---
id: R-20261124-211535-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: alta
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T21:15:35-04:00
---
# Site v0.2.0 no ar (/saude 21:15); instale: o conector Microsoft 365 não carrega na sessão do gerente — decisão

## 1. Deploy
/saude às 21:15 (Manaus): status ok, versao 0.2.0, tz_ok true. O site já mostra o Farol de Inadimplência e o menu dos 4 faróis (Inadimplência com dados só depois do robô novo rodar). Com o Auto-Deploy ligado, cada merge no main publica sozinho.

## 2. Instale (R-20261124-192643-alexandre)
Pré-condição cumprida (/saude 0.2.0). Mas na sessão do gerente o conector Microsoft 365 aparece como conectado na conta e NÃO carregado nesta sessão (conectores entram quando a sessão é criada); e a pasta pelo Remote Control segue vazia. Antes de escolher, confira na sua sessão se as ferramentas mcp__Microsoft_365__sharepoint_* têm GRAVAÇÃO (subir/substituir arquivo) ou só leitura e busca — sem gravação, o conector não serve para instalar.

Decisão para o Alexandre (resposta pronta "N X"):
1. Como instalar os 3 arquivos: (A) o po instala pelo conector da sessão dele, seguindo o roteiro exato abaixo, e o gerente confere os SHA-256 do relatório do po; (B) o Alexandre compartilha a pasta "Regionais - Leandro" pelo app Claude no computador (Configurações > Claude Code > Remote Control) e o gerente instala; (C) recriar a sessão do gerente para carregar o conector (perde o contexto da sessão atual). Recomendo A se o conector grava; senão B. Resposta: "1 A" ou "1 B".

Roteiro exato (pasta PMZ/1 - PMZ/2025/IM PMZ/Regionais - Leandro, NUNCA a "- Copia"):
a) criar SISTEMA BAP/BACKUP_RELATORIOS/ANTES_T0017_NOV2026 e copiar para lá os 3 arquivos atuais da raiz da pasta;
b) substituir na raiz bap_automation.py, bap_dados.py e relatorios_nucleo.py pelos do main (c8a9267 ou mais novo; os 3 não mudaram desde 73a8b4a);
c) baixar de volta e conferir SHA-256: bap_automation 2d12edcd283a6dade187a6ac493b08877d65b01f5ea777f2b9e928fc17b51a9b · bap_dados 52f764ff4d6e0d80cfce130f2622a1aed53bbc3acff918057e91ad761acba28f · relatorios_nucleo 7fc7ca395c9147b78b311bca317bd132977fb2884c078ce3557fbea771374a2a;
d) nenhum outro arquivo é tocado; recado com os SHA lidos.
