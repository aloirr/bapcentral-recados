# Revisão prévia T-0017, entregas 3 a 5 (Pedidos, Entregas e Visita no site), antes do PR

Revisor: revisor-codigo · 25/11/2026 (Manaus) · base `origin/main` = `ae1d6e2`

| Branch | Head revisado | Veredito |
|---|---|---|
| engenheiro-software/T-0017-abas-tres-farois | d951ffd | 🟡: corrigir antes do merge |
| modulo-farois/T-0017-hoje-fora-du | 11cef9a | 🟡: corrigir antes do merge |
| modulo-robo/T-0017-tres-farois | 3361d6a | 🟡: corrigir antes do merge (o 🔴 do conjunto se resolve na web ou aqui) |
| modulo-web/T-0017-tres-farois | 9e16c70 | 🔴: bloqueia |
| gerente-projetos/T-0017-rn-ger-011 | 730643e | aprovado (só 🟢) |

Observação: a branch local `modulo-robo/T-0017-tres-farois` está em `6d99e22`, atrás da remota. Revisei a remota (`origin/...` = `3361d6a`).

## Como conferi
- Worktree temporário fora do repositório, com o main e as 5 branches juntas na ordem contrato → faróis → RN → web → robô. Os merges não deram conflito.
- `python -m compileall -q` OK. `bap_dados.VERSAO = 27` (sem mudança).
- `pytest tests/`: 278 passaram. `pytest web/tests`: 212 passaram.
- `coord.mjs verificar --por-commit origin/main..<branch>`: OK nas 5 branches. Todos os commits têm o trailer `Agente:` do dono.
- **Ponta a ponta com as bases congeladas:**
  - `bap_automation.simular_pacote_farol([4 faróis], 2026-11, hoje=20/11)` montou o pacote, que passou por `web/app/pacotes.validar` e foi publicado num TestClient. Depois abri todas as abas e sub-abas com os 6 perfis.
  - O pacote real tinha dado de cliente. Ficou só no rascunho e foi apagado no fim.
- Resultado do ponta a ponta:
  - Pacote compacto: 1,76 MB, contra o teto de 20/25 MB.
  - **Pacote do robô recusado pela web: 422** (achado W1 abaixo).
  - Com o ajuste manual de W1, o pacote foi aceito: 76 respostas 200 e 69 respostas 403, como o §10.7.5 manda.
    - O diretor vê só o Resumo.
    - O perfil de um farol leva 403 nos outros.
    - Todas as páginas com tabela têm `no-store` e `noindex`.
    - O HTML tem 0 CPF/CNPJ formatado, 0 CPF/CNPJ com 11/14 dígitos, 0 e-mail e 0 telefone.
    - Toda página abriu em até 0,1 s.
  - Soma dos estados = topo (RN-GER-006):
    - Pedidos: 42+43+28 = 113 pedidos; R$ 33.576 + 59.536 + 19.589 = R$ 112.701.
    - Entregas: 1+2+0 = 3 em aberto; 21+14+19 = 54 entregues; frete R$ 0 + 2.552 + 654 = R$ 3.206.
    - Inadimplência: igual à de antes.
- Listas de colunas, selos, juntas e colunas proibidas: as do robô (`_COLUNAS_TABELAS_WEB`) e as da web (`tabelas.COLUNAS`/`SELOS`/`JUNTAS`) são idênticas entre si e ao §10.7.3.
- Nenhum arquivo de dado digitado nem config `.json` alterado. Nada de segredo: as senhas do `web/simular_farol.py` são fictícias e locais.

---

## 1. engenheiro-software/T-0017-abas-tres-farois (d951ffd): 🟡

🟡 **E1. O contrato não diz o que a web faz com `total` e com as sub-abas, e o código diverge** (`.coord/contratos/relatorio.md:667` e §10.7.6, `:748-760`).
- O §10.7.2 diz `subabas: list[TabelaWeb7]`, e TabelaWeb7 tem `total` e `filtros`. A web aceita na sub-aba só `titulo/colunas/linhas/tons`.
- O §10.6.2 define `total: list[Celula]` (str|int|float|null em qualquer coluna). A web exige que cada célula do total siga o tipo da coluna.
- A web recusa CPF/CNPJ formatado em qualquer célula de texto (`RE_DOC`), regra que não está no §10.7.6.
- **Correção:** escrever no §10.7.2 e no §10.7.6, sem ambiguidade:
  - (a) as chaves da sub-aba (com `total`/`filtros` opcionais, `null`/`[]`);
  - (b) célula do `total` = qualquer Celula (rótulo "TOTAL" em coluna de data e `""` em coluna numérica valem);
  - (c) `""` em coluna numérica de linha;
  - (d) a recusa por CPF/CNPJ formatado em texto, e que o PC confere a mesma coisa e tira **só a aba** antes de mandar.

🟡 **E2. D1 a D6 ainda em aberto** (`:633`, §10.7.9 `:788`; ADR 0001 adendo 5 `:428` "D1 a D6 em aberto").
- O próprio §10.7.10, item 1, exige o contrato "com as decisões D1 a D6 respondidas" antes do núcleo, da web e do robô.
- O R-20261125-025823-gerente-projetos ainda não tem resposta.
- **Correção:** depois do "1 A; D1 A … D6 A", tirar as marcas [Dn] (ou registrar a resposta) e mudar o status do adendo 5.

🟢 **E3.** O §10.7.4 (`:727`) diz que `sem_documento` tira "formatado no meio". A RN-GER-011 e o código tiram também o CPF/CNPJ de 11/14 dígitos no meio. Alinhar o texto.

🟢 **E4.** Texto do aviso dos cartões: o contrato diz "Com filtro, os cartões seguem só no PC." (`:668`), e a web mostra "Cartões só para a BAP inteira, sem recorte nem filtro. Os números do estado estão no Resumo." (texto vindo do parecer de UX). Atualizar o contrato com o texto final.

🟢 **E5.** O §10.7.9 traz a "regra nova proposta" com texto diferente da RN-GER-011 aprovada (a proposta cita contato e foto). Trocar pelo número e pelo texto aprovados.

## 2. modulo-farois/T-0017-hoje-fora-du (11cef9a): 🟡

🟡 **F1. Caminho do `filtro` sem uso: as "Pendências anteriores" por UF nunca disparam** (`relatorios_nucleo.py:7165-7170`, `chamar_kpis_de` `:772`, `bap_relatorios.py:2654 filtros_colunas`).
- A tabela "Entregas" filtra por `MÊS, SITUAÇÃO, ETAPA, PRAZO, FILIAL`. Não há filtro UF nem filtro geral UF (o `_filtros_gerais` só sobe filtro que a aba declara). Por isso `filtro.get(E_UF)` nunca chega no PC.
- O robô também não passa `filtro`: ele usa `_KPIS_SO_BAP_WEB` para tirar o cartão do estado.
- Resultado: código novo (3 funções/assinaturas) que nenhum caminho usa. O comentário do robô (`bap_automation.py:6619-6623`, "usa `pend` global") ficou velho.
- **Correção (escolher uma, combinada com o modulo-robo):**
  - (a) o robô passa `filtro={i_UF: uf}` no `recortes_farol_por_uf` via `chamar_kpis_de` e apaga `_KPIS_SO_BAP_WEB`. Recomendada: o cartão do estado conta a mesma história da junta "Pendências" que a web já filtra por UF;
  - (b) tirar `filtro`/`filtros_colunas`/`chamar_kpis_de` e manter o `cartoes_mes(ls)` de antes.

🟡 **F2. RN-GER-011: CPF/CNPJ com máscara parcial passa** (`relatorios_nucleo.py:788-796`).
- Ficam no texto: `"LOJA 123456789-00"`, `"LOJA 12345678/0001-90"` e `"cpf 123456789-00"` no `texto_sem_contato`.
- `"cnpj 12345678/0001-90"` vira `"cnpj [removido]/0001-90"`.
- **Correção:** separadores opcionais (`\d{3}\.?\d{3}\.?\d{3}-?\d{2}`, `\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}`), com `(?<![\w])` à esquerda. **Só** nas colunas "limpa" e de texto livre: o `ID_PRODUTO` da Solicitação BAP tem a forma `A999999999-99A` (137 células) e não pode virar "[removido]". Mais um teste `test_RN_GER_011_mascara_parcial` (pedido ao testes).

🟢 **F3.** Código morto: `tons_b` (`:878`) não é usado em `linhas_padrao`, e `idx = []` (`:944`) é sobrescrito em `recortes_em_linhas`.

🟢 **F4.** `hoje_manaus()` (`:761`) é a 3ª cópia: já existem `atualizar_do_github.hoje_manaus` e `bap_automation._agora_manaus`. Fica o do núcleo; o robô pode passar a usá-lo em outra tarefa.

🟢 **F5.** `sem_documento` (núcleo) e `cobranca_whatsapp.nome_sem_documento` são duas funções para a RN-GER-011. Hoje a Inadimplência do pacote real sai com 0 documento, mas o certo é uma função só (recado ao modulo-posvenda, fora do lote).

🟢 **F6 (fora do diff).** `farol_visitas`, `:13638-13641`: `du_adm` conta DU até `data_ate`, que pode ser hoje (regra 4). Vale conferir numa tarefa própria. O aviso "O dia de hoje é parcial" continua no pacote.

## 3. modulo-robo/T-0017-tres-farois (3361d6a): 🟡

🟡 **R1. A conferência do PC (§10.7.6) não espelha a defesa da web, e o pacote real foi recusado inteiro** (`bap_automation.py:7601` e `_tabela_web7`).
- Os 3 motivos de 422 no pacote real: `subabas` com `total`/`filtros`; total do "Por supervisor" com `""` em `REPRES.` (int); total do "Dia a dia" com `"TOTAL"` em `DATA` (data).
- Os 3 cabem no contrato (ver W1). Mas com a web como está, o robô derruba o pacote inteiro: `vc_painel` e Inadimplência param de atualizar.
- **Correção:**
  - (a) não mandar `total`/`filtros` nas sub-abas (são sempre `None`/`[]`);
  - (b) antes de mandar, rodar por aba a mesma checagem da web (tipo de célula, `RE_DOC` em texto, chaves de filtro em `{"coluna","padrao","multi","oculto"}`, `:7480`) e tirar **só a aba** que falhar;
  - (c) pedir ao testes um teste de contrato robô→web: `montar_pacote_web` → `web.app.pacotes.validar == []`, com fixture fictícia que tenha linha de total, sub-aba e `""` numérico.

🟡 **R2. Redundância:** `_sem_acento_maiusculo` (`:7304`) repete `bap_dados.sem_acento` (mesma normalização NFKD + upper + strip). **Correção:** usar `bap_dados.sem_acento`.

🟡 **R3. Ligado ao F1:** `_KPIS_SO_BAP_WEB` (`:6624`) e o comentário de `:6619-6623`. Com a opção (a) do F1, sai `_KPIS_SO_BAP_WEB` e o cartão "Pendências anteriores" aparece por estado, igual à junta da web.

🟢 **R4.** `_TABELA_RECORTE_WEB["vc_visitas"] = "Por vendedor"` (`:6616`) nunca é usado (`_COLUNA_UF_RECORTE_WEB["vc_visitas"] = None`). Tirar a entrada e o comentário.

🟢 **R5.** O lambda `uf_de` (`:7778`) repete `_uf_valida_web` (`:7378`), sem o `isalpha`. Usar `_uf_valida_web`.

🟢 **R6.** `tipos_solicitacao_web` (`:7545`) copia a regra de `bap_relatorios.AbaSolicitacaoBap.carregar`, que mora numa classe Tk. Levar a regra para uma função pura (ex.: `solicitacao_bap.tipos_colunas`) e as duas telas usarem.

🟢 **R7.** `_cortar_pacote_web` (`:7750`): depois do passo 3, o pacote pode continuar acima do teto, e o docstring diz "nunca manda". Também passa de 2 avisos no Visita. Registrar no log e aplicar `_avisos_curtos_visita_web` depois do corte.

🟢 **R8. Compatibilidade.** Robô novo com web velha = 422 no pacote inteiro. A ordem (web antes) e o limite 3 da rotina diária (`/saude` = main) protegem, mas um rollback da web no Render derruba tudo. Sugestão: se o envio der 422, tentar de novo uma vez sem as `tabelas` dos 3 faróis.

## 4. modulo-web/T-0017-tres-farois (9e16c70): 🔴

🔴 **W1. O validador recusa um pacote válido pelo contrato, e o pacote real do robô leva 422** (`web/app/tabelas.py:332`, `:360-362`, `:223-233`).
- Com 422, nada é publicado (nem `vc_painel` nem Inadimplência).
- Motivos encontrados no ponta a ponta:
  - `pv_pedidos: tabela Solicitação BAP: chave não aceita: filtros` (sub-aba com `total: null` e `filtros: []`; `subabas` = `list[TabelaWeb7]` no §10.7.2);
  - `vc_visitas: tabela Por supervisor: total inválido` (`""` em `REPRES.` int);
  - no "Dia a dia", `"TOTAL"` em `DATA` (data).
- **Correção:**
  - (a) na sub-aba, aceitar também `total` (`null` ou lista) e `filtros` (`[]`);
  - (b) no total, aceitar qualquer Celula (str ≤ 2000 sem `RE_DOC`, número ou `null`), como o §10.6.2;
  - (c) aceitar `""` em coluna numérica de linha (Celula `str`);
  - (d) teste com o formato real (linha de total com rótulo, sub-aba com `total`/`filtros`).
- O `test_pacote_dos_tres_farois_aceito...` passa porque a fixture não tem esses casos.

🟡 **W2. `RE_DOC` em qualquer texto derruba o pacote inteiro** (`tabelas.py:184`, `:233`, `:241`).
- Um CNPJ formatado em `TRANSPORTADORA`, `ANÁLISE CRÉDITO`, `MOTIVO` etc. (colunas que o PC não limpa) faz a web recusar tudo. A defesa é boa, mas a consequência é desproporcional, e a regra não está no contrato.
- **Correção:** manter a defesa, combinada com R1 (b) (o PC tira a aba antes) e E1 (d) (fica no contrato).

🟡 **W3. Redundância: dois formatadores de célula novos no mesmo PR, com saída diferente** (`render.py:314 fmt_cel`, para o bloco tabela do painel, e `tabelas.py fmt_celula`).
- Exemplos: pct com 1 casa contra 0 casa; vazio vira "—" num e "" no outro.
- **Correção:** o `_bloco_tabela` usa `tabelas.fmt_celula`, ou o contrário. Uma regra só, igual ao `bap_visual.formatar` do PC.

🟢 **W4.** `render._PROIBIDA` (`render.py:297`), `tabelas.COLUNAS_FORA` e `bap_automation._COLUNAS_PESSOA_TABELA_WEB` são três listas de "coluna de pessoa" com critérios diferentes (substring contra nome exato). Documentar no contrato qual vale para o bloco `tabela` do painel.

🟢 **W5.** `web/tests/golden_inadimplencia.json` tem 7.565 linhas. Os dados são fictícios ("Cliente 001", "Vendedor 02"; 0 CPF/CNPJ), mas `json.dumps(..., indent=None)` reduz o arquivo e o diff.

Segurança conferida, sem achado:
- Jinja com autoescape. Cores de `style=` validadas por `RE_COR`/`PALETA_TOM`. `tom-` validado em `TONS`.
- Parâmetros `uf`/`rec`/`sub`/`pag`/`ord` convertidos e limitados.
- Valores de filtro com `urlencode` e cortados em 80 caracteres.
- 403 por perfil e por aba no servidor (`main.py:256-266`). Aba da Inadimplência pedida em outro farol = 403.
- Nenhuma rota que grava nos 3 faróis.
- Página com tabela tem `no-store` e `noindex`, e o acesso é registrado sem cliente.

## 5. gerente-projetos/T-0017-rn-ger-011 (730643e): aprovado

🟢 **G1.** A RN-GER-011 (`docs/produto/03-regras.md:16`) está coerente com o código. Sugestões:
- citar as colunas que nunca vão (telefone, e-mail, contato, foto, CPF/CNPJ), hoje só no contrato;
- trazer a máscara parcial (F2);
- deixar explícito na RN-GER-006 o recorte de cada farol (Pedidos = filial da nota; Entregas = UF do cliente; Visita = sem recorte, falta a UF na tabela), hoje só no §10.7.3/§10.7.7.

---

## Ordem de merge (confere com o §10.7.10)
1. Contrato, com E1 e E2.
2. Faróis, com F1 e F2.
3. Testes (a branch `testes/T-0017-testes-tres-farois`), com o teste de contrato robô→web.
4. Web v0.3.0, com W1 a W3 (sobe sozinha no merge).
5. Robô, com R1 a R3, por último. Só chega à produção pela rotina diária, com `/saude` = 0.3.0.

O F1 (a) e o R3 vão juntos: núcleo e robô na mesma rodada.

Revisão nova obrigatória em cada head novo.
