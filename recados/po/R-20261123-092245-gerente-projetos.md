---
id: R-20261123-092245-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: aviso
prioridade: alta
tarefa: T-0010
responde_a: R-20261123-091302-alexandre
encerra: false
contrato: null
criado_em: 2026-11-23T09:22:45-04:00
---
# T-0010/T-0003: simulação na pasta de produção — 21 arquivos mudariam, 13 só por final de linha e 1 com risco para o robô

## Como foi feito
- Sessão BAPCentral - Cowork, 23/11/2026, ~09:20 (Manaus). Pasta de produção ligada à sessão com a aprovação do Alexandre: `C:\Users\<usuário>\OneDrive - PMZ DISTRIBUIDORA SA\1 - PMZ\2025\IM PMZ\Regionais - Leandro` (desktop-prukjf6).
- `atualizar_do_github.py` do main d32a454 (hash conferido), com `planejar` + `executar(simular=True)`. Origem: os 74 `.py`/`.bat` da raiz do main d32a454 baixados um a um (o zip do main tem ~53 MB e não baixa no tempo do shell do Cowork); conjunto conferido por hash contra o main. Data de cada arquivo = último commit dele (como no modo `--origem` com git).
- Nada foi gravado na produção. Nenhum arquivo de segredo ou dado digitado foi lido (as exclusões vêm antes da leitura).

## Resultado
- 74 conferidos: 53 iguais, 19 alterados, 2 novos; trava "instalado por fora": não disparou; backup previsto `SISTEMA BAP\BACKUP_RELATORIOS\ANTES_T0010_NOV2026` (19 arquivos).
- 13 `.bat` alterados SÓ por final de linha (produção CRLF, main LF): `abrir_bap_analista`, `abrir_bap_central`, `abrir_gerador_de_meta`, `abrir_oportunidade`, `abrir_planner`, `atualizar_coordenadas`, `atualizar_coordenadas_google`, `atualizar_coordenadas_tomtom`, `atualizar_visitas`, `gerar_farol_ddr`, `INSTALAR_PDF`, `REPARAR_PYTHON_BAP`, `RODAR_TESTE_BAP` (🟢 1 do R-20261123-063245-revisor-codigo confirmado).
- 5 da T-0010, como esperado: `bap_dados.py` (+5 −1), `relatorios_nucleo.py` (+9 −1), `planner_nucleo.py` (+132 −6), `bap_planner.py` (+47 −1), `smoke_relatorios.py` (+35 −8).
- 1 fora da T-0010, com risco: `bap_automation.py` (+3 −1). Na produção a senha do robô tem um valor padrão escrito no código; no main (migração de 10/11) o padrão saiu e a senha vem só do cofre do Windows (`--salvar-senha`) ou da variável `BAP_SENHA`. Se o PC do robô (DT-AMADMBAP-03) não tiver a senha no cofre, o robô para com "Senha do BAP Tools não encontrada". O valor não é repetido aqui.
- 2 novos: `ATUALIZAR_DO_GITHUB.bat`, `atualizar_do_github.py`.

## Recomendação do gerente (decisão do Alexandre)
- Instalar agora só os 5 da T-0010 + os 2 novos, com backup e conferência byte a byte (mesmas funções do instalador, plano filtrado).
- Deixar de fora, por enquanto: os 13 `.bat` (corrigir o final de linha no repositório antes, para o instalador não trocar `.bat` CRLF por LF) e o `bap_automation.py` (só depois de confirmar a senha no cofre do PC do robô).
