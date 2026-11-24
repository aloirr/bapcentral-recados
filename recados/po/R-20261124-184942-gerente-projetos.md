---
id: R-20261124-184942-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: alta
tarefa: T-0017
responde_a: R-20261124-181912-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T18:49:42-04:00
---
# T-0017: Farol de Inadimplência no main — pedir "aprovo deploy v0.2.0", "instale" e a decisão do 000040

## O que entrou no main (73a8b4a)
#47 contrato · #48 site · #49 robô · #51 fotos sem CNPJs internos · #50 títulos sem CNPJs internos · #52 web v0.2.0. Todos com CI verde e pareceres do revisor-codigo e do corretor-redundancias limpos (designer-ux 🟢 no site). Falta só o 2º PR do testes (testes novos; não muda o que vai à produção), em correção de um teste repetido.

## Decisões para o Alexandre (resposta pronta "N X")
1. Deploy do site: (A) "aprovo deploy v0.2.0" agora (o site passa a mostrar o Farol de Inadimplência e o menu dos 4 faróis; o Painel no ar continua igual, conferido pelo revisor); (B) esperar. Recomendo A. Resposta: "1 A" ou a frase "aprovo deploy v0.2.0".
2. Instalar no PC, DEPOIS do deploy (o site tem de aceitar o farol antes de o robô mandar): (A) "instale" de bap_automation.py, bap_dados.py e relatorios_nucleo.py do main 73a8b4a na pasta do Leandro, com backup SISTEMA BAP\BACKUP_RELATORIOS\ANTES_T0017_NOV2026 e conferência byte a byte (SHA-256 começa com: bap_automation 2d12edcd283a6dad · bap_dados 52f764ff4d6e0d80 · relatorios_nucleo 7fc7ca395c9147b7); (B) esperar. Recomendo A. Resposta: "2 A".
3. Conta 000040 no Farol de Inadimplência: o CLAUDE.md diz "a conta 000040 fora", mas a RN-GER-005 diz que 000040 é a conta de TESTES (fora de prospecção, indicação, pesquisa e e-mails), e o revisor achou um CLIENTE real com código 000040, cuja dívida sumiria se tirássemos. (A) no farol, o 000040 de cliente continua (como está no main); (B) tirar também o cliente 000040. Recomendo A. Resposta: "3 A".

## Como testar em 5 passos (depois do 1 e do 2)
1. Rode o robô no notebook (ou espere a rodada das 14h de amanhã); no site, Farol de Inadimplência deve mostrar "Baixado do ERP em ..." com a data do relatório de títulos.
2. No PC, abra o Farol de Inadimplência (NOV/2026); compare os 6 cartões com o site: Em atraso, Inadimplência, A vencer em 7 dias, Acima de 90 dias, Atraso médio, Recuperado no mês — devem ser iguais.
3. No site, toque em AM; no PC, filtre UF = AM: os 5 cartões do estado devem bater (Recuperado mostra "só na BAP inteira").
4. Confira que o site não tem botão de e-mail, WhatsApp ou edição, e que nenhum nome de cliente ou CNPJ aparece (vendedor aparece, decisão 2 A).
5. Abra no celular: cartões com as barrinhas por estado, Resumo e gráficos sem texto cortado. Responda ao po só com "bate" ou os números que não bateram.
