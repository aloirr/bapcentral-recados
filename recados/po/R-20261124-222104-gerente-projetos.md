---
id: R-20261124-222104-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T22:21:04-04:00
---
# Pareceres do revisor-codigo: #62 c24df7a, #63 e8c9f1e, #64 62779ba, #65 2f50def — aprovados

> Pareceres do revisor-codigo, com checagem de redundância (subagente do gerente-projetos; gravados pelo gerente sem alteração; varredura: limpo).

# Re-revisão T-0017, entrega 2: PRs #62, #63 e #64 e o PR do contrato

Conferência comum aos quatro PRs:
- merge temporário (já descartado) dos 4 heads com `origin/testes/T-0017-testes-cobranca` (56ae5db), sem conflito: `compileall` OK, `pytest tests/` 214 passed, `web/` 114 passed;
- testes de dono (pós-venda e robô, versão atual): 31 passed;
- o `verificar <agente> --base origin/main` sai OK nos 5 branches, e os commits trazem o trailer `Agente` do dono;
- pacote simulado com as bases congeladas: "Títulos" com 20 colunas, "Por cliente" com 19 e fila com 136 itens. Nenhum NOME começa por CPF/CNPJ, nem nas tabelas, nem em `fila.nome`, nem em `nome_msg` (antes eram 8 linhas e 1 item). O `pacotes.validar` da web devolve 0 erros.

**🟡 de fora dos 4 PRs, para o dono `testes`:** o branch de testes ainda está em 56ae5db e não tem teste para o NOME sem documento. Os testes de dono que cobrem o caso (`nome_sem_documento` nas tabelas e na fila, com `test_RN_POS_004_...`) passam, mas precisam entrar no branch `testes/T-0017-testes-cobranca` antes do merge.

## PR #62 · modulo-posvenda · head `c24df7a`
**Aprovado.**
- O 🟡 caiu. O `nome_sem_documento` (RN-POS-004) é usado no `nome` da fila (`pacote_web`) e na saudação. O `nome_msg` e a mensagem continuam sem documento.
- O 🟢 1 caiu: o `historico()` agora deriva do `historico_origem()`, com o mesmo comportamento (`v[:2]`).
- 🟢 Ficou aberta a do `_gerado_em`, com deslocamento fixo `-4`. Ela não pesa: o robô sempre passa o `gerado_em`.

**Redundância:** nenhuma em aberto. O `nome_saudacao` virou um apelido de uma linha do `nome_sem_documento`; pode ficar, para quem já chama.

## PR #63 · modulo-web · head `e8c9f1e`
**Aprovado.**
- O 🟡 caiu: `web/app/cobranca.py:296` agora mostra "Número com dígitos repetidos: digite o certo".
- 🟢 que caíram:
  - 1: o `celular()` do JS espelha a regra do PC, e o link e o registro passam a usar o mesmo número;
  - 2: o selo compara o texto com `strip().upper()`;
  - 3: a limpeza usa `>=` 30 dias;
  - 4: `isascii() and isdigit()`;
  - 5: o trinco da thread é solto quando o `flock` falha;
  - 7: o `_MEMO_SHA` só guarda os pacotes ainda guardados;
  - 8: as citações do contrato foram corrigidas para §10.6. Também há testes novos.
- 🟢 que ficaram:
  - 6: a trava de clique repetido vale só para um worker. Está correta com o `startCommand` de hoje;
  - a troca do `autoDeploy` no `RENDER.md` foge do lote, mas é texto de apoio.

**Redundância:** a regra do `celular()` existe em três lugares: PC, servidor e JS. É aceitável porque a web não importa os módulos da raiz e há teste de paridade no servidor. A cópia do JS não tem teste de paridade (🟢: incluir no `test_celular_mesma_regra_do_pc`).

## PR #64 · modulo-robo · head `62779ba`
**Aprovado.**
- O 🟡 caiu. O `tabelas_cobranca_web` passa a coluna NOME pelo `cobranca_whatsapp.nome_sem_documento`. Se a função não existir, as tabelas não vão, e o farol cai no §10.1. O `COBRANCA_WEB.csv` do PC continua com o NOME do PC: o `nomes_por_cliente_web` lê o `rel` cru, como o §10.6.7 pede.
- 🟢 que caíram:
  - 1: o `enviar_pacote_web` reusa o `_base_web`;
  - 2: o `_pasta_cobranca` reusa o `cw.pasta`.
- 🟢 que ficaram:
  - 3: o `_fantasias_clientes` continua copiado do `bap_relatorios.py:926`;
  - 4: o `seq` de linha sem `id` entra na conta, um caso teórico;
  - 5: o cofre é consultado a cada log;
  - novo: `preparar_cobranca_web` (por volta de `:7428`) ainda faz o `sys.path.insert` antes de chamar o `_cobranca_whatsapp(raiz)`, que já faz o mesmo. São 2 linhas sobrando.

**Redundância:** sobram o `_fantasias_clientes`, cópia do `cobrar_whatsapp` do PC (🟢 3), e o `sys.path.insert` repetido (🟢 novo).

## PR do contrato · engenheiro-software/T-0017-nome-sem-documento · head `2f50def`
**Aprovado.**
- O texto do §10.6.2 (NOME sem documento só no site, com a "igualdade" valendo com essa troca) e o do §10.6.3 (`nome`) batem com o código dos PRs #62 e #64. É um acréscimo compatível, e a versão do contrato continua 1.
- O `kpis_faixa` no §10.1 é uma chave opcional, de desenho, com fonte citada. 🟢: o assunto não é a T-0017 entrega 2 (é o Farol de Pedidos). Funciona como acréscimo, mas o ideal seria um PR próprio, ou pelo menos citar no PR qual tarefa pede essa chave. Nenhum código destes PRs a usa ainda.

**Redundância:** nenhuma. O contrato aponta para uma única função, `cobranca_whatsapp.nome_sem_documento`, e não redefine a regra.
