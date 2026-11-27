# T-0036 — relato da sessão de tarefa ao gerente fixo

Sessão de tarefa: https://claude.ai/code/session_01QvB2SU9Wtp5KdywcGtq7PR. O `send_message` para a sessão fixa falhou ("só sessões do mesmo canal"), por isso o relato fica aqui.

## Estado final (27/11/2026, Manaus): pronto para os PRs

Todas as branches têm o `origin/main` 30ae65d. Nenhum PR foi aberto e nenhum merge foi feito.

| Ordem do PR | Branch | Head | O que leva |
|---|---|---|---|
| 1 | `gerente-projetos/T-0036-regras` | este commit | RN-GER-017 (perfis analista e trade) e este relato |
| 2 | `engenheiro-software/T-0036-desenho` | 845ff4a | contrato §10.11 (o §10.9 e o §10.10 do main são da T-0023/T-0025) e `docs/desenho/T-0036.md` |
| 3 | `modulo-farois/T-0036-correcao-codigo` | f4d197d | `codigo_do_cliente`, `correcao_linhas`, `CAB_CORRIGIR`/`CAB_ANALISAR` |
| 4 | `modulo-robo/T-0036-pacotes` | 4de2cb1 | os 4 rid no pacote web, lista positiva, anexo `correcao`, cortes do Markup |
| 5 | `modulo-web/T-0036-analista` | a214659 | 4 faróis no BC3, perfis, menu, Excel de correção (só admin), `/saude` 0.6.0, PNGs |
| 6 | `testes/T-0036-testes` | 6c33a72 | testes valor × regra, travas de escopo |
| — | `revisor-codigo/T-0036-revisao` | 79c7b36 | parecer `docs/revisao/T-0036.md` |

O `verificar` do robô e do testes acusa só os arquivos que chegam por merge dos donos (faróis e robô). A acusação some se os PRs entrarem na ordem da tabela.

## Pareceres (todos no head final)

- revisor-codigo: **aprovado**, sem 🔴 nem 🟡 (79c7b36). O 🔴 da 1ª volta (o Diretor mudava sem simulação) fechou com o revert.
- corretor-redundancias: RD-0001 a RD-0008 **fechados**, sem achado novo.
- revisor-ux: **aprovado** em ae6b1ea; depois disso entrou só o merge do main (`.coord/quadro.md`).
- design-de-marca: **aprovado** em 5c033d9 (só 🟢, já aplicados). O parecer não foi gravado em `docs/marca/pareceres/T-0036.md`.
- Testes: `web/tests` 448 passed; `tests/test_T0036_analista_robo.py` 29 passed e 2 xfail esperados (o Diretor, abaixo, e a lista de colunas da web, que vira teste real quando a web estiver no main); travas T0013/T0017/T0024: 334 passed. `test_T0021_edicao_web_robo.py` não carrega neste Linux (falta tkinter). Smokes não rodados (economia).

## Valor × regra

| Critério | Regra | Resultado |
|---|---|---|
| Cliente só pelo código | RN-GER-011 | ✅ |
| Pesquisa sem contato ("[removido]") e sem 000040 | RN-GER-011, RN-GER-005 | ✅ (robô e web) |
| UF pela filial (Saldo, Markup, Reajustes) e pelo cliente (Pesquisa, Divergências) | RN-GER-006 | ✅ |
| Cortes do Markup e lista positiva de colunas | §10.11.3 e §10.11.5 | ✅ |
| "Desconto comercial" de cada estado: Saldo = Por UF = cartão = barra do RRM | RN-GER-006 | ✅ |
| Total do Diretor com 1 casa | regra dá 15,1%, o Diretor mostra 15,0% | ❌ defeito antigo do `painel_diretor.py`, fora da T-0036 (xfail strict) |

## Para abrir como tarefa (não bloqueiam a T-0036)

1. **Diretor, desconto comercial com 1 casa** (modulo-farois): ele relê o "15%" arredondado do cartão do Saldo e mostra "15,0%". Corrigir com o número cheio, com simulação antes (regra 10).
2. **Faixa do BC3 em todos os faróis** (modulo-web e designer-ux): o "Dados de dd/mm/aaaa hh:mm" contraria a §4.1 do `tela-bc3.md`, e o checklist do designer-ux diz outra coisa. O po confirma com o Alexandre qual vale. O corte em 6 números e o rótulo curto no celular hoje valem só para os 4 faróis do Analista.
3. 🟢 Fonte uniforme no grupo de números da faixa quando um valor passa de 9 caracteres (revisor-ux).
4. Quando a T-0023 v2 e a T-0025 v2 entrarem, conferir que o analista entra nos faróis do §10.10 pelo `LEITURA_GERAL` e **não** vê o TOTAL A PAGAR (RN-GER-015).

## Perguntas ao Alexandre (padrão adotado entre parênteses; nenhuma bloqueia)

- **P1:** o analista vê os outros faróis? A: sim, como o gerente · B: só os 4 do Analista e o Painel. (A)
- **P2:** como o cliente aparece nos 4 faróis? A: só o código · B: o nome sem CPF/CNPJ, com adendo à ADR 0001. (A)
- **P3:** o analista vê o TOTAL A PAGAR das Campanhas? A: não (RN-GER-015 como está) · B: sim, e o analista entra na RN-GER-015. (A)

## PNGs (dados fictícios, 1366 e 390, deviceScaleFactor 2)

Em `web/docs/simulacoes/T-0036/`, na branch da web: `saldo`, `markup`, `preco`, `divergencias`, `menu-analista` e `trade-inicio`, cada um em `-pc.png` e `-cel.png`, com o `MEDICAO.md`.

## Como testar em 5 passos (para o recado de entrega)

1. Entrar no site com um usuário `analista`: abre no Farol de Saldo, e o grupo "Analista Comercial" aparece no menu.
2. Abrir Saldo, Markup, Preço e Divergências: o cliente aparece só pelo código.
3. Entrar como `diretor`: nos 4 faróis aparece só o Resumo.
4. Entrar como `admin` nas Divergências: baixar o Excel de correção (sem a coluna do cliente). Com outro perfil, o link dá 403.
5. Entrar como `trade`: aparece só a frase "Os faróis do Trade Marketing ainda não estão no site."
