---
id: R-20261125-073500-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0018
responde_a: R-20261125-035000-alexandre
encerra: false
contrato: null
criado_em: 2026-11-25T07:35:00-04:00
---
# T-0018: pasta pessoal atualizada (dados + programas do main 71b60ec); T-0017 com o 🟡 do revisor corrigido

## Pedidos do Alexandre (sessão BAPCentral - Cowork, 25/11, manhã; textos literais)
- "Acelere, porque esta parado?"
- "essa é a pasta na nuvem onde está o regionais leandro no one drive pessoal. acelere a atualização dela" (pasta pessoal PMZ\1 - PMZ\2025\IM PMZ\Regionais - Leandro)
- "qual o passo a passo para atualizar o robo na pasta pessoal? e ja ative o timer tambem para ele ficar rodando a cada 30 minutos e atualizando a web"

## Feito
- Cópia da pasta da empresa para a pessoal (rsync, sem apagar nada; o que foi substituído na pessoal foi para SISTEMA BAP\BACKUP_RELATORIOS\ANTES_MIGRACAO_NOV2026): raiz (programas e configs), RELATORIOS (sem EXPORTADOS e _CACHE_RELATORIOS), SISTEMA BAP (sem auth, logs e BACKUP_RELATORIOS), BAP Ajuda 2.0. TABELA_BAP e SOLICITACAO_BAP antigas (ago/26) da raiz movidas para o backup (raiz_antiga), para o pastas_bap não confundir.
- Conferência por SHA-256: 112 arquivos de dado digitado e configuração (_EDICOES_POS_VENDA, _NCC, _GARANTIAS, _AUTORIZACOES, _COBRANCA_WHATSAPP, ACOMPANHAMENTO_*, COORDENADAS_CLIENTES.json, painel_diretor_hist.json e os .py/.bat/.json/.csv/.xlsx da raiz) = 0 diferença.
- Programas: os 75 .py/.bat/requirements da raiz do main 71b60ec instalados na pasta pessoal (pedido explícito do Alexandre de atualizar a pasta), 75/75 byte a byte; os 12 substituídos estão em ANTES_MIGRACAO_NOV2026\programas_antes_do_main.
- Revisão independente do lote T-0017 (#69–#74): sem 🔴; 1 🟡 (telefone/e-mail digitado no nome em Prospecção e Indicação ia ao site) corrigido no #75 `71b60ec` (modulo-robo) e testado no #76 (testes); 4 🟢 ficam para depois (8 dígitos soltos viram "[removido]"; pacote > 20 MB ainda é enviado; D1 A mostra Cliente a cliente de todos ao perfil vendas; 9–10 dígitos no começo do nome).

## Pendente (Alexandre, no notebook do robô)
1. OneDrive pessoal sincronizado e "Sempre manter neste dispositivo" na pasta.
2. Avisar antes do instalar_bap.bat: o gerente faz a cópia delta empresa → pessoal (rodada das 08h e o que as assistentes digitarem).
3. instalar_bap.bat na pasta pessoal; depois o comando do timer de 30 min (tarefa "BAP Tools - Atualizar TABELA_BAP", 07h–21h, sem rodada dupla, só com o usuário logado).
4. Primeira rodada pelo atalho; o gerente confere o /saude e as abas novas no site.
- Ainda não copiados (arquivo morto): RELATORIOS\EXPORTADOS, _CACHE_RELATORIOS, SISTEMA BAP\BACKUP_RELATORIOS da empresa, ARQUIVO MORTO, DOCUMENTOS BAP, Treinamentos.
- Restos de cópia (arquivos temporários de 0 byte) movidos para ANTES_MIGRACAO_NOV2026\temporarios_da_copia (sem permissão de apagar).
