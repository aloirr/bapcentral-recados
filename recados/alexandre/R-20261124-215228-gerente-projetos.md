---
id: R-20261124-215228-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: alta
tarefa: T-0018
responde_a: R-20261124-214958-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T21:52:28-04:00
---
# T-0018: plano de migração do robô para a pasta pessoal — 5 decisões

## Resumo (gerente-projetos)
- Migrar = copiar os dados para a pasta pessoal, trazer os programas do main e rodar o instalar_bap.bat lá (a tarefa 08h/14h é recriada na pasta nova; o Windows pede a senha da conta). Não precisa mudar o código do robô.
- O cofre do Windows (BAP_TOOLS, BAP_WEB) é por usuário, não por pasta: com o mesmo usuário, nada muda. O login do site BAP Tools é refeito pelo robô (a pasta de sessão não é copiada).
- Dado digitado (pós-venda, NCC, garantias, autorizações, acompanhamentos, coordenadas manuais, configs digitados) é copiado byte a byte e conferido por hash, em 2 passadas, com as edições congeladas durante a cópia (regra 7).
- Tempo ativo ~2h30 a 3h30 numa noite (entre a rodada das 14h e a das 08h) + 1 a 3 dias de observação; o robô perde no máximo uma rodada; voltar atrás leva ~45 min.
- A rotina das 06h30 (T-0018) só liga depois da virada, já na pasta nova.
- Pode quebrar: o Power BI não lê OneDrive pessoal pelo gateway da empresa sem credencial própria; atalhos e links antigos das assistentes; quem não tiver conta pessoal.

## Decisões para o Alexandre (resposta pronta "N X")
1. Janela da virada: (A) uma noite de dia útil · (B) fim de semana. Recomendo A. Resposta: "1 A".
2. Pasta da empresa depois: (A) somente leitura por 30 dias e depois arquivar · (B) apagar logo. Recomendo A. Resposta: "2 A".
3. As assistentes: (A) trabalham direto na pasta pessoal compartilhada (testar antes com 1) · (B) editam a cópia e o time sincroniza. Recomendo A. Resposta: "3 A".
4. Power BI: (A) reconectar à pasta pessoal pelo Power BI Desktop e republicar com credencial própria (conferindo totais com o farol) · (B) manter a pasta da empresa só para o Power BI. Recomendo A. Resposta: "4 A".
5. O robô segue com o mesmo usuário do Windows (cofre intacto): (A) sim · (B) usuário novo (refaz o cofre). Recomendo A. Resposta: "5 A".

## Plano completo (modulo-robo)
Fato-chave: o robô usa a pasta onde o bap_automation.py está (PASTA_LOCAL = pasta do arquivo; LOCAL_DA_PLANILHA="mesma_pasta"). Não há caminho fixo: mudar de pasta = reinstalar lá, sem editar código. O venv fica em %LOCALAPPDATA%\BAP_TOOLS, fora da pasta.

## (a) O que o robô precisa na pasta nova
- Programas: toda a raiz (.py e .bat), em especial bap_automation.py, base_cliente.py, solicitacao_bap.py, conferir_solicitacao.py, aviso_arquivo.py, visitas_maxima.py, prospeccao_forms.py, respostas_bap_ajuda.py, cnae_bap.py, bap_dados.py, executar_bap.bat, atualizar_visitas.bat, instalar_bap.bat, tarefa_bap.xml, requirements.txt. Via código do main (ATUALIZAR_DO_GITHUB.bat), não por cópia da empresa.
- Bases (cópia): TABELA_BAP.xlsx e SOLICITACAO_BAP.xlsx na raiz; RELATORIOS/ inteiro; SISTEMA BAP/ (BACKUP_RELATORIOS, PLANNER_MESES, cache, recursos, Consulta CNAE); BAP Ajuda 2.0/; COORDENADAS_CIDADES_BAIRRO_BAP.xlsx, SEGMENTACAO_BAP.xlsx, CATEGORIAS_PRODUTO.csv.
- Dado digitado (regra 7, copiar byte a byte, nunca reescrever): RELATORIOS/_EDICOES_POS_VENDA, _NCC, _GARANTIAS, _AUTORIZACOES, _COBRANCA_WHATSAPP; ACOMPANHAMENTO_*.xlsx; COORDENADAS_CLIENTES.json (inclui o MANUAL); Visitas; painel_diretor_hist.json; champions_config.json, transportadoras_config.json, painel_diretor_config.json.
- .json de config da raiz (copiar do que está em produção): meta_config, meta_saldo_config, oportunidade_config, planner_config, expositores_config, farol_ddr_config, planner_pastas (chaves: tabela_bap, base_cliente, saida; os caminhos dentro dela precisam apontar para a pasta nova, conferir após a cópia). Configs de mapas/visitas e SISTEMA BAP/auth: não abri e não vão em texto; copiar sem ler.
- SISTEMA BAP/auth (sessão do navegador): NÃO copiar. O robô faz login de novo (garantir_login); evita levar sessão velha.
- Cofre do Windows: guarda por usuário do Windows, não por pasta. Se o robô seguir no mesmo usuário do notebook, BAP_TOOLS (senha do ERP) e BAP_WEB (url/token da web) já estão lá: nada a mover. Conferir por existência, sem mostrar valor. Se o usuário mudar, rodar de novo --salvar-senha e o cadastro de BAP_WEB.
- Tarefa agendada 08h/14h ("BAP Tools - Atualizar TABELA_BAP"): o tarefa_bap.xml traz __PASTA__; instalar_bap.bat grava a tarefa com o caminho de onde ele roda e pede a senha do Windows. Logo, rodar o instalar_bap.bat DENTRO da pasta nova.

## (b) O notebook precisa sincronizar a conta pessoal?
Sim: o robô lê e grava arquivo local; o OneDrive é só o transporte. Precisa de uma pasta sincronizada no notebook (a empresa e a pessoal convivem, são contas separadas).
1. Configurações do OneDrive > Conta > Adicionar uma conta, entrar com a conta pessoal (~5 min).
2. Escolher uma pasta local da conta pessoal; ativar "Sempre manter neste dispositivo" em "Regionais - Leandro" (botão direito > Sempre manter neste dispositivo). Sem isso, arquivos sob demanda travam o Excel. Espaço: confirmar o tamanho total antes (~10 min + download).
3. Se a pasta só está compartilhada com a conta pessoal: abrir no OneDrive web > "Adicionar atalho ao Meu OneDrive".
4. Conferir que o caminho local termina em PMZ\1 - PMZ\2025\IM PMZ\Regionais - Leandro e que o ícone é verde.
5. Excluir da proteção "Backup de pastas" do OneDrive o venv (já fica em LOCALAPPDATA).

## (c) Ordem segura (robô não para; nada digitado se perde)
Hoje (sem nenhuma alteração): robô segue na pasta da empresa.
1. Simulação ao Alexandre (imagem antes/depois da estrutura) e aprovação: 1 dia.
2. Sincronizar a conta pessoal no notebook e preparar a pasta nova vazia (b): 30 min.
3. Congelar edições: avisar assistentes (2 min) e escolher a janela entre 14h30 e 07h30 do dia seguinte, sem rodada; Excel fechado; pausar OneDrive da empresa: 5 min.
4. Cópia 1 (a quente, só leitura da origem): robocopy de tudo, exceto auth e logs: 20–60 min conforme o tamanho.
5. Conferência: hash (SHA-256) dos dados digitados e das bases, tamanho+data do restante, lista de faltantes/extras, zero diferença: 15 min. Falhou = repetir só o diferente.
6. Cópia 2 (delta, na janela congelada, dados digitados primeiro) + nova conferência: 15 min.
7. Instalar o robô na pasta nova: rodar instalar_bap.bat lá e deixar a tarefa 08h/14h criada, mas DESABILITADA; login do ERP novo: 20 min.
8. Rodada de teste manual na pasta nova (rápida ~530 s; primeiro --simular com imagem, se travar por arquivo antigo: --primeira-vez com backup total, decisão 5 A): 15–30 min. Critério: 7 de 7 relatórios, TABELA_BAP e BASE_CLIENTE atualizadas, dados digitados iguais (hash).
9. Virada: desabilitar a tarefa da pasta antiga (não apagar) e habilitar a nova; assistentes e Power BI passam para a pasta nova (d): 15 min. Volta ao ar na próxima 08h.
10. Primeira rodada 08h/14h na pasta nova acompanhada; 3 dias de observação: 1–3 dias.
11. Pasta da empresa vira cópia: marcar somente leitura/renomear com sufixo, sem apagar, por 30 dias; depois decisão do Alexandre.
Total ativo ~2h30 a 3h30 em uma noite; o robô perde no máximo uma rodada.

## (d) Compartilhamentos a refazer
- Assistentes: compartilhar a pasta pessoal com cada uma (e-mail pessoal ou link com edição) e o atalho em "Meu OneDrive" delas. Muda o caminho local e a conta (pessoal, não corporativa). Pode quebrar: planilhas abertas ou atalhos do Excel ligados ao caminho antigo, links de _EDICOES_POS_VENDA/_NCC/_GARANTIAS, quem não tiver conta pessoal; edição simultânea na pasta velha e na nova (corrompe a verdade): bloquear a antiga como somente leitura.
- Power BI: trocar as fontes (OneDrive/SharePoint) de TABELA_BAP, BASE_CLIENTE, ESTOQUE_BAP etc. para a pasta nova. Pode quebrar: Power BI Service não lê OneDrive pessoal pelo gateway corporativo sem credencial; atualização agendada falha com "credencial inválida"; caminhos em Parâmetros; medidas que dependem do nome da consulta. Fazer no Desktop, atualizar, comparar os totais com o farol e só então republicar.
- Lista de links a levantar antes (chaves: tabela_bap, base_cliente, saida do planner_pastas.json).

## (e) Rotina das 06h30 (engenheiro-software)
Janela 06h00–07h30 sem robô; as rodadas ficam 08h/14h. Ordem: 1) a rotina 06h30 só passa a rodar depois do passo 9 e é configurada já apontando para a pasta nova; 2) durante a migração (passos 3–9), a rotina fica desligada ou na pasta da empresa em modo só-leitura; 3) a 1ª rotina 06h30 só roda depois da cópia conferida, nunca no meio; 4) o "instale" automático não mexe em .bat, tarefa_bap.xml e configs (pedem "instale"). O robô não pode estar rodando na hora (a janela garante).

## (f) Riscos e como voltar atrás
- Perda/divergência de dado digitado: mitiga hash + cópia 2 + pasta antiga intocada. Volta: manter só a pasta antiga.
- OneDrive pessoal com arquivo sob demanda ou cota cheia: confirmar espaço e "sempre manter".
- Sincronização lenta/conflito de cópia (arquivo "-NomeMaquina"): congelar edições e pausar o sync durante a cópia.
- Login do ERP, pop-up de arquivo aberto, 1ª rodada travada: --simular antes.
- Tarefa agendada duplicada (duas pastas gravando): desabilitar a antiga no passo 9.
- Power BI/assistentes sem acesso: avisar antes; Power BI mantém o relatório antigo até a troca.
- Volta atrás (até 30 dias): desabilitar a tarefa nova, habilitar a antiga, copiar de volta só os dados digitados alterados (por data/hash) e repontar Power BI/assistentes: ~45 min.

## (g) Decisões que faltam ao Alexandre
- 1 A/B: janela da virada. A) uma noite de dia útil (entre as rodadas 14h e 08h). B) fim de semana. Recomendo A, com o fim de semana se o tamanho exigir.
- 2 A/B: pasta da empresa depois. A) somente leitura por 30 dias e depois arquivar. B) apagar logo. Recomendo A.
- 3 A/B: o que a assistente faz. A) trabalha direto na pasta pessoal compartilhada. B) edita a cópia e o time sincroniza. Recomendo A, depois de testar com 1 assistente.
- 4 A/B: Power BI. A) conectar à pasta pessoal pelo Desktop e republicar com credencial própria. B) manter a empresa só para o Power BI. Recomendo A, comparando totais com o farol.
- 5 A/B: confirmar que o robô segue com o mesmo usuário do Windows (cofre intacto). A) sim. B) usuário novo (refaz o cofre). Recomendo A.
