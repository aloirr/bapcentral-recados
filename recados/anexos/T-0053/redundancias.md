# T-0053: auditoria de redundância (curta)

- Código: `modulo-farois/T-0053-cadastro-do-pedido`, head **b4006e7** (só `relatorios_nucleo.py`).
- Regra: `gerente-projetos/T-0053-regras`, head **3874b3a** (RN-GER-019).
- Faixa: RD-0256 a RD-0261 (usados de RD-0256 a RD-0260).

## O que está limpo
- A loja é escolhida só em `cadastro_do_pedido()`. As telas do escopo (detalhe, em aberto, excluídos, `farol_pedidos`, parcial) passam por `ctx.cliente_do_pedido`, `ctx.credito_do_pedido` ou `nome_cliente(cod, filial)`, e nenhuma reimplementa a escolha.
- A volta de Fretes, Entregas e dos outros ao main (b56f121 → b4006e7) não deixou sobra: `HERDA_LOJA_UNICA` saiu, e não ficou nenhuma chamada nem constante órfã.
- RN-GER-019: o texto não se repete dentro da RN.

## Achados

| ID | Onde | Tipo | O que se repete | Impacto | Sev. | Proposta (antes → depois) | Dono |
|---|---|---|---|---|---|---|---|
| RD-0256 | `relatorios_nucleo.py` `pedidos_em_aberto` (~l.1559) e `analise_credito` (~l.1868) | código | A regra "sem crédito apurado não se analisa" (RN-GER-019) está escrita 2 vezes: `cred.get("credito_apurado") is not False` em `pedidos_em_aberto` e `cli.get("credito_apurado") is False` em `analise_credito`. | manutenção: se a regra mudar num lugar só, as duas telas passam a divergir | média | antes: `apurado = cred.get("credito_apurado") is not False` → depois: `apurado = analise_credito(cred, valor) != CREDITO_NAO_APURADO`. A regra fica só em `analise_credito`. | modulo-farois |
| RD-0257 | `Contexto.cadastro_do_pedido` (~l.1115), chamado por `cliente_do_pedido`, `credito_do_pedido` e `nome_cliente(cod, filial)` | código | O mesmo (filial, cod) é recalculado de 3 a 3+N vezes por pedido: em `pedidos_em_aberto` (cliente + crédito + nome na linha + nome em cada falta), em `farol_pedidos` (`linha()` + `analise_credito(ctx.credito_do_pedido(...))`) e em `detalhe_pedido` (cliente + nome 2 vezes). | desempenho e consulta repetida | baixa | depois: guardar o resultado no próprio método: `memo = self.__dict__.setdefault("_memo_cad_ped", {}); k = (uf_da_filial(filial), cod); if k not in memo: memo[k] = ...; return memo[k]` (é o padrão `_memo_*` que o arquivo já usa). | modulo-farois |
| RD-0258 | `cadastro_do_pedido()` (~l.786 e ~l.796), no retorno | código | As chaves `"identificada"` e `"cod"` são devolvidas, mas nenhum chamador nem teste as lê. `identificada` repete o que `credito_apurado` e `nome == LOJA_NAO_IDENTIFICADA` já dizem. | manutenção: campo morto | baixa | Tirar `"cod"` e `"identificada"` do retorno e da docstring. `manter?` só se o teste da RN-GER-019 for usá-las; nesse caso, o teste cita a chave. | modulo-farois |
| RD-0259 | `Contexto.lojas_do_codigo` (~l.1097 e ~l.1108) | código | O mesmo dict de 8 chaves (`loja, nome, fantasia, cidade, uf, limite, saldo, atraso_valor`) é montado 2 vezes: no índice do `protheus_lojas` e no caso de quem só está em `tabela['clientes']`. | manutenção | baixa | depois: uma função local `_ficha(d, saldo, atraso)` que devolve o dict, usada nos 2 lugares. | modulo-farois |
| RD-0260 | docstrings de `cadastro_do_pedido()` (~l.751-770) e de `analise_credito` (~l.1864-1867) | doc | As docstrings repetem a RN-GER-019 em cerca de 20 linhas e com texto diferente (RN: "o nome (e a fantasia) fica se for igual…"; docstring: "a fantasia e igual ao nome"). | manutenção: 2 textos para a mesma regra | baixa (só comentário, não segura o lote) | depois: `"""RN-GER-019 (fonte: docs/produto/03-regras.md). Entrada: lojas_do_codigo = [{uf, nome, fantasia, cidade, limite, saldo, atraso_valor}]; saldo None = não conhecido. Saída: {nome, fantasia, uf, cidade, limite, saldo, atraso_valor, credito_apurado}."""` e, em `analise_credito`, uma linha: `RN-GER-019: credito_apurado False -> CREDITO_NAO_APURADO.` | modulo-farois |

Fora do escopo (vai para o `testes`, não está catalogado): a RN diz "a loja que não é a de maior limite", e o código usa "a loja que `tabela['clientes']` guarda por código". Conferir se é a mesma loja.

## Parecer
**Não liberado** no head b4006e7: estão em aberto RD-0256 (média), RD-0257, RD-0258 e RD-0259 (baixas, em código). RD-0260 é só comentário, não segura o lote e entra no próximo. A RN (3874b3a) está sem achado.
