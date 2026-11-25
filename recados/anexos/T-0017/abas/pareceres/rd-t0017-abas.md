# T-0017, entregas 3 a 5: auditoria de redundâncias antes do PR (corretor-redundancias, 25/11/2026)

Os seis branches foram comparados com `git diff origin/main...<branch>`. Heads: engenheiro-software d951ffd · modulo-farois 11cef9a · modulo-robo 3361d6a · modulo-web 9e16c70 · testes 48d8b10 (em andamento) · gerente-projetos 730643e.
Também li os 31 PNGs do `sim6/`, com atenção a: 01, 03, 04, 05, 06, 07, 08, 12, 13 e 14.
Numeração: o último RD usado é o RD-0016, citado nos recados de 24/11. Aqui começa no **RD-0017**.

## Resumo

| ID | Tipo | Sev. | Dono | Bloqueia? |
|---|---|---|---|---|
| RD-0017 | código (regra) | alta | modulo-farois · modulo-posvenda | sim, a parte do modulo-farois · a do modulo-posvenda vira tarefa à parte |
| RD-0018 | código (regra) | média | modulo-robo | sim |
| RD-0019 | código (regra) + teste | alta | modulo-robo · testes | sim |
| RD-0020 | código (regra) | média | modulo-robo · modulo-farois | sim, a parte do modulo-robo · a do modulo-farois vira tarefa à parte |
| RD-0021 | código (regra) | média | modulo-robo · modulo-web | sim |
| RD-0022 | código + layout | média | modulo-web | sim |
| RD-0023 | texto (aviso) | média | modulo-web · modulo-robo | sim |
| RD-0024 | texto + código morto + teste | média | modulo-web · engenheiro-software | sim; os títulos de teste não seguram o lote |
| RD-0025 | texto (estado vazio) | baixa | modulo-web | sim |
| RD-0026 | layout (filtro inútil) | baixa | modulo-robo · engenheiro-software | sim |
| RD-0027 | texto (aviso) | média | modulo-robo · engenheiro-software | sim |
| RD-0028 | código | baixa | modulo-web | sim |
| RD-0029 | doc | baixa | engenheiro-software | sim |
| RD-0030 | código (regra de filtro) | média | modulo-farois | não: tarefa à parte (o teste de igualdade protege) |
| RD-0031 | código (fuso) | baixa | modulo-robo | não: tarefa à parte (depende do merge do modulo-farois) |

**Parecer:** o lote **não sai** enquanto os itens marcados "sim" estiverem abertos.

---

## RD-0017 · A limpeza de documento está em duas funções que dão resultados diferentes
- **Onde:**
  - `relatorios_nucleo.sem_documento` / `cliente_sem_documento` (modulo-farois, 11cef9a, RN-GER-011);
  - `cobranca_whatsapp.nome_sem_documento` (`cobranca_whatsapp.py:99`, RN-POS-004), que continua sendo usada pela Inadimplência no site (`bap_automation.py:7042-7047`).
- **O que se repete:** a mesma regra ("nome de cliente vai ao site sem CPF/CNPJ") tem 2 funções e 2 RNs. Os resultados divergem (conferido rodando as duas regex):
  - `"12.345.678 FULANO"` (o caso MEI da RN-POS-004): `sem_documento` → `"12.345.678 FULANO"` (o pedaço do CNPJ fica); `nome_sem_documento` → `"FULANO"`;
  - `"FULANO 12345678900"`: `sem_documento` → `"FULANO"`; `nome_sem_documento` → o CPF fica;
  - `"001234 - NOME"`: `sem_documento` mantém o código; `nome_sem_documento` apaga.
- **Impacto:** o mesmo cliente aparece limpo de um jeito na Inadimplência e de outro em Pedidos, Entregas e Visita. Manutenção em dobro.
- **Proposta:**
  - **modulo-farois (bloqueia):** `sem_documento` passa a cobrir também a regra do começo da RN-POS-004, ou seja, vira a soma das duas regras:
    - antes: `s = _DOC_QUALQUER.sub(" ", str(texto))`;
    - depois: `s = _DOC_INICIAL.sub("", str(texto)); s = _DOC_QUALQUER.sub(" ", s)`, com `_DOC_INICIAL = re.compile(r"^\s*(?=(?:[.\-/\s]*\d){6})[\d.\-/\s]+")` vindo para o núcleo;
    - em `cliente_sem_documento`, aplicar só depois de separar o código, como hoje;
    - teste `test_RN_POS_004_...` com os casos MEI chamando `rn.sem_documento`.
  - **modulo-posvenda (tarefa à parte, fora deste lote):** a função passa a delegar ao núcleo. Antes: `return _DOC_INICIAL.sub("", texto(nome)).strip()`. Depois: `return rn.sem_documento(nome)`.
  - **gerente-projetos (junto com a tarefa à parte):** RN-POS-004 em `03-regras.md` passa a dizer "caso da Inadimplência da RN-GER-011".
- **Ao testes (valor, não catalogado aqui):** o MEI `"12.345.678 NOME"` sai com o pedaço do CNPJ nas tabelas novas.

## RD-0018 · A regra da UF por linha (RN-GER-006) e outros trechos aparecem duas ou três vezes no `bap_automation`
- **Onde e o que se repete:** em `bap_automation.py` (3361d6a):
  - **Qual coluna dá a UF:** em 2 tabelas de configuração. `_TABELA_RECORTE_WEB` (:6616) com `_COLUNA_UF_RECORTE_WEB` (:6625) servem os recortes dos cartões; `_UF_LINHAS_WEB` (:7140) serve o `uf_linhas` das tabelas. As duas dizem "Entregas = UF do cliente; Pedidos = FILIAL".
  - **A validação "UF de 2 letras":** 2 vezes, em `_uf_valida_web` (:7378) e no `uf_de=lambda` (:7778).
  - **A busca do filtro padrão `MÊS`:** 3 cópias, em :7453, :7671 e :7812.
  - **`_sem_acento_maiusculo` (:7304):** igual a `bap_dados.sem_acento`, que o robô já importa (:6564).
  - **`_avisos_curtos_visita_web`:** chamada 2 vezes no mesmo `selecionar_farol_web` (:6960 e :6990).
- **Impacto:** manutenção. Uma mudança na RN-GER-006 precisa ser feita em 2 lugares.
- **Proposta:**
  - **Uma tabela só:** `_UF_LINHAS_WEB` passa a ser a fonte. `_recortes_do_farol_web_bruto` lê dela: a coluna e a conversão `"filial"`/`"uf"` saem de lá. Apagar `_COLUNA_UF_RECORTE_WEB` e o `lambda` (usar `uf_de=_uf_valida_web`).
  - **Uma função** `_mes_padrao(t) -> str | None`, usada nos 3 lugares.
  - **Acento:** antes `_sem_acento_maiusculo(nome)`; depois `_bd.sem_acento(nome)`.
  - **Avisos curtos:** chamar `_avisos_curtos_visita_web` uma vez só, no fim (`if rid == "vc_visitas": val["avisos"] = _avisos_curtos_visita_web(val.get("avisos") or [])`), e apagar a chamada de :6960.

## RD-0019 · "Pendências anteriores" por estado é resolvida de dois jeitos que se contradizem
- **Onde:**
  - **modulo-farois:** `entregas.cartoes_mes(ls, filtro=None)` e `rn.chamar_kpis_de(f, linhas, filtro)` já calculam o cartão por estado, pela UF do cliente.
  - **modulo-robo:** `_KPIS_SO_BAP_WEB` (:6624), o comentário de :6621-6623 ("o kpis_de ignora as linhas filtradas") e `_recortes_do_farol_web` (:7757) tiram o cartão do recorte. Além disso, `recortes_farol_por_uf` chama `kpis_de(por_uf[uf])` (:7829) **sem** o filtro.
  - **testes:** `test_RN_GER_006_entregas_pendencias_anteriores_so_na_BAP_no_site` e o achado 2 do `docs/testes/T-0017.md` registram o atalho do robô.
- **O que se repete:** a mesma regra (cartão por estado) tem 2 mecanismos. O do robô ficou obsoleto quando o núcleo passou a aceitar `filtro`.
- **Impacto:** alto. O PC mostra "Pendências anteriores" de AM; o site, no estado AM, não mostra o cartão. Os mesmos números, contados de jeitos diferentes, confundem.
- **Proposta:**
  - **modulo-robo:**
    - antes: `ks = kpis_de(por_uf[uf])`;
    - depois: `ks = _rn.chamar_kpis_de(kpis_de, por_uf[uf], {ix: uf_bruta})`, com o valor da coluna como a tela do PC filtra, ou seja, o valor de `ln[ix]` da UF;
    - apagar `_KPIS_SO_BAP_WEB`, `_recortes_do_farol_web` (o `_bruto` vira o nome) e o comentário :6621-6623.
  - **testes:**
    - trocar `..._so_na_BAP_no_site` por `test_RN_GER_006_entregas_pendencias_anteriores_por_estado_no_site` (o recorte AM do pacote = `chamar_kpis_de` com `{iu: "AM"}`);
    - atualizar o achado 2 do `docs/testes/T-0017.md`.

## RD-0020 · `tipos_solicitacao_web` copia a regra da tela
- **Onde:**
  - `bap_automation.tipos_solicitacao_web` (:7545). A docstring admite: "Replica a regra porque o bap_relatorios importa Tk; o teste compara as duas";
  - `bap_relatorios.AbaSolicitacaoBap.carregar` (`bap_relatorios.py:2093-2099`).
- **O que se repete:** a mesma lista `QUANTIDADE, DEMANDA_PEDIDO, JA_SOLICITADO, SALDO_A_SOLICITAR, ESTOQUE_NA_ORIGEM` (`_COLUNAS_NUM_SOLICITACAO_WEB`) e a regra "DATA vira data quando toda célula é data". São 2 cópias, mais a do contrato (§10.7.3).
- **Proposta:** uma função pura no `solicitacao_bap.py`, que é do modulo-robo e não importa Tk: `solicitacao_bap.tipos_colunas(colunas, linhas) -> list[str]`.
  - **modulo-robo (bloqueia):** `tipos_solicitacao_web` some. `solicitacao_web` chama `_sb.tipos_colunas(cols, d["linhas"])`.
  - **modulo-farois (tarefa à parte):** em `carregar`, `cols = [{"nome": c, "tipo": t} for c, t in zip(d["colunas"], sb.tipos_colunas(d["colunas"], d["linhas"]))]`. Até lá, fica o teste de igualdade.

## RD-0021 · "Coluna que não vai ao site": 4 listas diferentes e a mesma validação feita duas vezes na web
- **Onde:**
  - **robô:**
    - `_COLUNAS_FORA_WEB` (:7125) vale para as abas: igualdade, sem acento;
    - `_COLUNAS_PESSOA_TABELA_WEB` (:6629) vale para o bloco tabela: trecho do nome, com `"telefone"`, `"e-mail"`, `"email"`, `"contato"`, `"cnpj"` e `"cpf"` repetidos da outra lista.
  - **web:**
    - `tabelas.COLUNAS_FORA` (:159) tem CONTATO, FOTO e ENDERECO;
    - `render._PROIBIDA` (:297) não tem CONTATO, FOTO nem ENDERECO, mas tem "fone" e "whats";
    - a mesma conferência do bloco tabela (até 20 colunas, coluna proibida) roda em `pacotes._tabela_ok` (:109) e de novo em `render._bloco_tabela`.
- **O que se repete:** a lista do §10.7.4 do contrato está escrita 4 vezes, com conteúdos diferentes.
- **Impacto:** um telefone com o nome "CONTATO" passa no bloco do painel da web, mas é recusado na aba.
- **Proposta:** a fonte é o §10.7.4.
  - **robô:**
    - `_COLUNAS_PESSOA_TABELA_WEB = ("cliente", "razão", "razao", "fantasia", "nome")`, só o que é próprio do bloco;
    - o teste do bloco passa a ser `_coluna_proibida_web(n) or any(t in n.lower() for t in _COLUNAS_PESSOA_TABELA_WEB)`.
  - **web:**
    - `COLUNAS_FORA` e `coluna_fora` mudam para o `render.py`; o `tabelas` importa do `render`, que já é a direção atual do import;
    - `render.coluna_proibida(nome) = coluna_fora(nome) or bool(re.search(r"cliente|raz[aã]o|fantasia", nome, re.I))`;
    - em `render._bloco_tabela`, sai a reconferência das colunas: o pacote já foi validado em `pacotes._tabela_ok`. Se o modulo-web quiser manter a defesa, que seja uma linha que chama `pacotes._tabela_ok(b)`, sem uma segunda regra.

## RD-0022 · A web formata número de três jeitos e tem duas grades de tabela
- **Onde:**
  - **formatação:**
    - `tabelas.fmt_celula` (:485): pct sem casa decimal;
    - `render.fmt_cel` (:314): pct com 1 casa; o `dia` vira número com 1 casa;
    - `render.fmt_valor` (:167): os cartões.
  - **grade:**
    - `farol.html:58-66` (bloco tabela do painel) redesenha a tabela com classes próprias (`tab tb`, `n`, `dica-rolar`);
    - `_grade.html` (`grade`) faz a mesma coisa para as abas (`tab tab-dados`, `num`, `dica-rolagem`).
  - **texto:** "Role para o lado para ver mais colunas →" está escrito 2 vezes (`_tabela.html:48`, `farol.html:60`).
- **Impacto:** a moeda e o % mudam conforme o lugar da tela, e um ajuste de estilo precisa ser feito em 2 grades.
- **Proposta:**
  - **formatação:**
    - `render.fmt_cel` some;
    - `_bloco_tabela` usa `tabelas.fmt_celula`, mudado para `render`, porque o `tabelas` importa o `render`: `fmt_celula(v, tipo, centavos=False)` passa a ficar no `render`, e o `tabelas` reexporta;
    - teste único `test_formatos_do_contrato`, apagando `test_fmt_cel`.
  - **grade:**
    - o bloco tabela do painel chama o macro: `{% elif b.tipo == "tabela" %}{{ grade(b, "", "", "Sem linhas neste pacote.") }}`;
    - `_bloco_tabela` devolve a forma de `tabela_para_tela`: `cols` com `num`/`i`, `linhas[].cel[].t`;
    - a dica de rolagem fica só no macro `grade`.

## RD-0023 · O aviso de "sem filtro por estado" tem dois textos e aparece onde não há o que escolher
- **Onde:**
  - **web:**
    - `main.py:303`: `if rid == "vc_visitas" or (uf and not t.get("uf_linhas")): aviso_uf = tabelas.AVISO_SEM_ESTADO`, que põe "Sem filtro por estado: esta tabela mostra a BAP inteira." nas 7 abas do Visita (PNG 08 e 12);
    - `render.py:409-410` separa os avisos com `startswith("Sem filtro por estado")`, ou seja, depende do texto do robô.
  - **robô:** o aviso "Sem filtro por estado: os cartões mostram a BAP inteira." vai no resumo (PNG 13).
- **O que se repete:** o mesmo fato com 2 textos, que aparece em 8 páginas do Visita.
- **Impacto:** nas abas do Visita não há seletor de estado (a página não mostra a barra Estado). O aviso explica um controle que não está na tela: é texto que o usuário não usa para agir (regra 3).
- **Proposta:**
  - **web:**
    - antes: `if rid == "vc_visitas" or (uf and not t.get("uf_linhas")):`;
    - depois: `if uf and not t.get("uf_linhas"):`. O aviso só aparece quando a pessoa escolheu um estado que a tabela não filtra;
    - o texto vira `AVISO_SEM_ESTADO = "Esta tabela não filtra por estado: mostra a BAP inteira."`.
  - **web e robô:** em vez de comparar o texto, a separação passa a usar uma chave. O robô manda `"sem_estado": true` no farol, já que o contrato aceita chave nova compatível pelo §10.1. Se a chave nova não for aceita, a constante `AVISO_SEM_ESTADO_FAROL` fica no robô e é citada no teste da web.
  - Sem a chave, o texto atual continua no resumo.

## RD-0024 · O aviso dos cartões da aba explica o sistema, existe em 3 versões, e `kpis_sem_numero` é código morto
- **Onde:**
  - **contrato** §10.7.2, linha 668: cartões com "—" e o aviso "Com filtro, os cartões seguem só no PC.";
  - **web, texto:** `tabelas.AVISO_CARTOES` (:46): "Cartões só para a BAP inteira, sem recorte nem filtro. Os números do estado estão no Resumo." (PNG 06);
  - **web, código morto:**
    - `main.py:311` calcula `render.kpis_sem_numero(...)`;
    - mas `_tabela.html:16` só desenha cartão `if kpis and not aviso_kpis`. O traço nunca aparece, e `kpis_sem_numero` (`render.py:227`) não chega à tela;
  - **títulos de teste desatualizados:** `test_estado_filtra_linhas_pelo_uf_linhas_e_cartoes_da_aba_viram_traco` e `test_cartoes_da_aba_sem_numero_com_recorte_ou_filtro`.
- **Impacto:** a primeira frase do aviso explica o funcionamento (regras 3 e 4), e o contrato descreve uma tela diferente da desenhada.
- **Proposta:** a versão enxuta é a que já está desenhada (cartões fora + uma frase).
  - **web:**
    - apagar `render.kpis_sem_numero` e, em `main.py:311`, trocar por `kpis, aviso_kpis = [], tabelas.AVISO_CARTOES`;
    - texto com o problema e a ação, em 2 constantes:
      - `AVISO_CARTOES_ESTADO = "Cartões de {uf}: veja no Resumo."` (com estado);
      - `AVISO_CARTOES_FILTRO = "Cartões com filtro: só no PC."` (com filtro ou recorte).
  - **contrato (engenheiro-software):** na linha 668, trocar "com outro filtro, os cartões da aba mostram "—" e o aviso …" por "com outro filtro, recorte ou estado, os cartões da aba saem e fica um aviso: com estado, "Cartões de <UF>: veja no Resumo."; com filtro ou recorte, "Cartões com filtro: só no PC."". Ajustar também o §10.7.7 ("mostram "—", como com filtro").
  - **Títulos de teste (baixa, não segura o lote):** `..._cartoes_da_aba_saem_com_aviso` e `test_cartoes_da_aba_saem_com_recorte_ou_filtro`.

## RD-0025 · O estado vazio aparece duas vezes, com controles sobre uma tabela sem linhas
- **Onde:** `_tabela.html:7`, `:48` e `:49`. Exemplo: o PNG 12 (Indicação vazia).
- **O que se repete:** "0 linhas" no cabeçalho e "Nenhuma linha neste mês." na grade. A mesma tela ainda mostra "▸ Filtros" e "Role para o lado para ver mais colunas →" sobre uma tabela vazia.
- **Proposta:** com `tabela.total_linhas == 0`:
  - o cabeçalho fica sem a contagem: antes `<span>0 linhas</span>`, depois nada;
  - o bloco Filtros só aparece se `not tabela.padrao` (a pessoa precisa conseguir limpar o filtro);
  - a dica de rolagem não aparece;
  - fica uma frase só: "Nenhuma linha neste mês." (ou "… neste filtro.").

## RD-0026 · No Entregas, o filtro MÊS tem uma opção só
- **Onde:**
  - **PNG 06:** a caixa "MÊS" mostra só "NOV/26";
  - **contrato** §10.7.3, linha 706: "Filtros: `MÊS` (padrão = mês do pacote), …";
  - **robô:** `_tabela_web7` passa o filtro do PC como está.
- **Por quê:** com a D2 A, o pacote só leva as linhas do mês. A caixa não tem escolha: é excesso (regra 3). O Pedidos já resolve isso com `"oculto": true`.
- **Proposta:**
  - **robô:** nas `_TABELAS_SO_MES_WEB`, o filtro `MÊS` vai com `"oculto": True` (`f = dict(f, oculto=True)`);
  - **contrato:** "Filtros: `MÊS` (padrão = mês do pacote, oculto), `SITUAÇÃO`, …".

## RD-0027 · O aviso de "aba fora" explica o motivo interno, e o mesmo texto está escrito 3 vezes
- **Onde:**
  - **robô:**
    - "…: as colunas do PC não batem com o contrato." aparece em `bap_automation.py:6976`, `:6984` e `:7689`, sem constante;
    - "Bloco {titulo} fica so no PC (traz cliente)." (:6927) também traz o motivo, e o "so" está sem acento;
  - **contrato:** §10.7.6, linha 750.
- **Impacto:** "as colunas do PC não batem com o contrato" e "(traz cliente)" explicam o funcionamento por trás. O usuário só precisa saber o que falta e onde ver (regras 3 e 4).
- **Proposta:** constantes no robô.
  - `_AVISO_ABA_FORA_WEB = "A aba {titulo} não veio nesta atualização. Veja no PC."`
  - Com várias abas: `"As abas {lista} não vieram nesta atualização. Veja no PC."`
  - Bloco: `"O quadro {titulo} fica só no PC."`
  - O motivo técnico fica só no log, que já o registra.
  - **Contrato,** linha 750: o mesmo texto.

## RD-0028 · A rota da web repete o caminho da rota original e monta o resumo duas vezes
- **Onde:**
  - `main.farol_abas` (`main.py:254-317`) repete da rota `farol`:
    - o registro de acesso;
    - o `rel_do`;
    - a página "sem pacote";
    - o `ctx`;
    - a leitura de `consulta`.
  - Em cada página de aba, `render.farol_para_tela` roda 2 vezes: uma em `main.py:283` (`topo`, só para `ufs`) e outra no `else` dos cartões.
  - `render.py:406`: `"faixa": bool(rel.get("kpis_faixa")) or rid == "pv_pedidos"`. A mesma decisão vem de 2 fontes: a chave do robô e o `rid` fixo.
- **Proposta:**
  - **`consulta`:** `def _consulta(request) -> dict` usada pelas 2 rotas.
  - **Resumo:** `topo = render.farol_para_tela(rel, uf or None, rid)` calculado uma vez, com `ufs = topo["ufs"]` e `kpis = topo["kpis"]`.
  - **Faixa:** antes `bool(rel.get("kpis_faixa")) or rid == "pv_pedidos"`; depois `bool(rel.get("kpis_faixa"))`.

## RD-0029 · O contrato e a ADR repetem regra e números
- **Onde e o que se repete:**
  - **RN-GER-011 em dois textos:** o contrato, linha 799 ("Regra nova proposta … com o número que ele der: "RN-GER-011 · Tabela no site: sem CPF/CNPJ, telefone, e-mail, contato e foto…"") e o texto aprovado em `docs/produto/03-regras.md` (730643e), que é diferente. A linha 726 ainda diz "regra proposta RN-GER-011, §10.7.9".
  - **ADR 0001, adendo 5, linhas 438-439:** repete os números do §10.7.4 ("84 nomes de 2.216") e do §10.7.8 ("0,3 → 2,2 MB"), embora o próprio adendo diga que "as regras e os formatos ficam só no contrato".
  - **§10.7.10, linha 808:** "Web nova com robô antigo: só a aba Resumo (§10.1)" repete a linha 648 ("Sem a chave, o farol se comporta como no §10.1 (robô antigo)").
- **Proposta:**
  - **Linha 799:** sai o texto proposto. Fica "Regra: RN-GER-011 (`docs/produto/03-regras.md`). Os testes citam `test_RN_GER_011_...`."
  - **Linha 726:** "(RN-GER-011)".
  - **ADR:** antes, os números; depois, "A limpeza de documento do núcleo vale para as tabelas desses faróis (contrato §10.7.4), e o pacote cresce para o tamanho do §10.7.8, dentro do teto do `render.yaml`."
  - **Linha 808:** sai a frase. O §10.7.1 já diz isso.

## RD-0030 · A regra de filtro da tela está em dois lugares (tarefa à parte)
- **Onde:**
  - `relatorios_nucleo.linhas_padrao` e `_texto_filtro`. A docstring diz: "Mesma regra de `bap_relatorios.VistaTabela._filtradas`";
  - `bap_relatorios.py:2662-2707`.
- **Proteção:** `test_T0017_linhas_padrao_igual_a_tela` (testes) evita que as duas versões se afastem.
- **Proposta:** extrair `rn.linha_passa_filtros(linha, filtros, colunas) -> bool` (o laço de :2676-2686, com `_texto_filtro`). `_filtradas` e `linhas_padrao` passam a chamar essa função.
- **Por que fica para depois:** a troca mexe no filtro de todas as tabelas do PC.

## RD-0031 · O fuso de Manaus está em três funções no código do PC (tarefa à parte)
- **Onde:**
  - `relatorios_nucleo.hoje_manaus` (nova, 11cef9a);
  - `bap_automation._agora_manaus` (:6695);
  - `atualizar_do_github.hoje_manaus`;
  - `bap_automation.py:8189`: `_rn.Contexto(Path(raiz), date.today(), …)`, que ignora o padrão novo do `Contexto`.
- **Proposta:** depois do merge do modulo-farois:
  - `_agora_manaus().date()` vira `_rn.hoje_manaus()`;
  - em :8189, `date.today()` vira `None`, e passa a valer o padrão do `Contexto`;
  - o `atualizar_do_github.py` fica como está (`manter?`): é o instalador, isolado de propósito (ADR 0002), e mudá-lo exige o "instale".

---

## Redundância útil: `manter?` (não conta como achado aberto)
- **A lista de colunas do §10.7.3 em três lugares** (contrato, `bap_automation._COLUNAS_TABELAS_WEB` e `web/app/tabelas.COLUNAS`, além de `JUNTAS`/`SELOS`/`ABAS`):
  - é defesa em profundidade pelo contrato (o PC confere, a web recusa);
  - a web roda com `rootDir: web` e não importa a raiz.
  - **Pedido ao testes:** um teste que compare as listas do robô e da web (nome, tipo, oculta, selo, juntas e ordem das abas). Hoje nenhum teste faz isso.
- **`cobranca.tabela_para_tela` × a tabela genérica:** resolvido no 9e16c70. A da cobrança agora só chama `tabelas.tabela_para_tela`, e o golden `test_inadimplencia_igual_ao_golden_gerado_com_o_codigo_anterior` protege. Não há achado.
- **`web/app/tabelas.RE_DOC`:** a web recusa CPF/CNPJ formatado. É a segunda barreira da RN-GER-011, então fica.
- **Abas do Visita (PNG 08 e 12):** os 5 cartões do Resumo se repetem nas 7 abas. Em "Por supervisor", repetem também a linha TOTAL (45 / 60 / 75%).
  - É paridade com o PC: lá, os cartões ficam no topo da janela.
  - **Pergunta ao po/designer-ux:** nas abas sem `kpis_padrao`, os cartões devem sair? Se a resposta for "sim", vira RD.
- **"21 linhas" no cabeçalho × cartão "Pedidos 21"** (PNG 01): com filtro, os dois números mudam de forma diferente. Fica.
- **"Dados de … (horário de Manaus)" × "Baixado do ERP em …"** (PNG 13): são fatos diferentes (o pacote e a base). Fica.

## Testes duplicados
Não achei teste do mesmo caso com outro nome. O que existe é teste que **segue** um RD:
- `test_fmt_cel` (RD-0022);
- `test_tabela_recusa_coluna_de_cliente_cnpj_telefone` com `test_render_descarta_tabela_com_coluna_de_cliente_mesmo_sem_validador` (RD-0021);
- `..._so_na_BAP_no_site` (RD-0019);
- os títulos com "traço" (RD-0024).

## Pendências do corretor
- Recados aos donos e o catálogo `docs/redundancias/` **não foram feitos** nesta rodada. [SUPOSIÇÃO: o gerente distribui a partir deste relatório; se pedir, eu mando um recado por dono.]
- O reteste fica por evidência (PNG novo e teste) no head SHA de cada PR.
