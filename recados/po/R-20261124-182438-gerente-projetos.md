---
id: R-20261124-182438-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: alta
tarefa: T-0017
responde_a: R-20261124-181913-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T18:24:38-04:00
---
# T-0017 (2ª entrega): desenho do WhatsApp, Títulos e Por cliente no site — 6 decisões

## Resumo (gerente-projetos)
- No PC, o "Cobrar no WhatsApp" já é feito por funções puras (cobranca_whatsapp.py, modulo-posvenda): fila de quem está inadimplente, telefone normalizado, mensagem pronta, link wa.me e um diário por máquina que só acrescenta. Achado: as abas do PC não têm coluna CNPJ; o cliente aparece pelo código-loja.
- No site: abas Títulos e Por cliente (sem telefone na tabela) e a fila de cobrança com o WhatsApp normalizado e a mensagem pronta (~40 KB a mais por rodada, compactado). Hoje: 136 clientes na fila, 17 sem WhatsApp.
- A volta ao PC sem perder nada: o site grava um diário só de acréscimo; na rodada do robô (08h e 14h), ele puxa o diário, acrescenta a um arquivo próprio "COBRANCA_WEB.csv" (sem repetir registro) e só então confirma. Os diários das assistentes no PC ficam intocados (regra 7) e o PC passa a ver o que foi cobrado pelo site.
- Segurança: filtro por perfil no servidor, registro de acesso sem dado de cliente, páginas sem cache; nenhum segredo novo (usa o token do robô que já existe).
- Muda a ADR 0001 (adendo 3): só neste farol, nome/código/telefone de cliente vão ao Render e o site grava o diário da cobrança.

## Previsão (Manaus), com as decisões hoje
- Simulação PNG (abas + fila do WhatsApp, computador e celular): 30/11.
- Entrega completa (PRs, revisões): 02/12. Depois: "aprovo deploy" do site e "instale" do robô.
- Farol de Pedidos segue previsto para 26/11 (em paralelo).

## Decisões para o Alexandre (resposta pronta "N X")
1. Quem vê e quem cobra: (A) admin e pós-venda veem as tabelas e cobram; gerente vê as tabelas sem telefone e sem botão; diretor só cartões e gráficos; (B) diretor também vê as tabelas; (C) só admin e pós-venda veem as tabelas. Recomendo A. Resposta: "1 A".
2. CNPJ: (A) não vai; vai o código do cliente, como nas abas do PC; (B) acrescentar a coluna CNPJ (muda também o PC). Recomendo A. Resposta: "2 A".
3. Quanto tempo o dado fica no Render: (A) últimos 7 pacotes; diário do site apagado 30 dias depois de confirmado no PC; (B) 15 pacotes e 90 dias. Recomendo A. Resposta: "3 A".
4. Atraso entre PC e site: (A) as 2 rodadas de hoje (08h e 14h), com o aviso "situação do PC até hh:mm" na tela; (B) rodada extra de hora em hora só da cobrança (mais carga no PC do robô). Recomendo A. Resposta: "4 A".
5. Telefone corrigido no site: (A) vale só para aquele envio e fica no diário, como no PC; (B) o site não deixa editar. Recomendo A. Resposta: "5 A".
6. Exportar as tabelas no site: (A) não nesta entrega; (B) sim, Excel por perfil. Recomendo A. Resposta: "6 A".

## Desenho técnico completo (engenheiro-software)

## (a) Onde o PC faz hoje
- Botão: `bap_relatorios.py` `cobrar_whatsapp()` (~l. 918): monta `nomes` {cod: fantasia} de `ctx.base["clientes"]` e abre `cobranca_whatsapp.janela(self, self.rel, AQUI, nomes)`.
- `cobranca_whatsapp.py` (modulo-posvenda), funções puras, sem Tk no topo:
  - `fila(farol, nomes)`: cruza as tabelas "Por cliente" (SITUAÇÃO = INADIMPLENTE) e "Títulos" (VENCIDO); ordena por EM ATRASO; devolve cod, nome, nome_msg, cidade, uf, vendedor, supervisor, em_atraso, maior, telefone_cad, whatsapp, aviso, titulos[].
  - `celular()` normaliza o número (55+DDD+9 dígitos; fixo/repetido/sem número dão aviso); `mensagem(cli, MODELO)`; `link()` (whatsapp:// ou wa.me).
  - Diário: `registrar()` grava `RELATORIOS/_COBRANCA_WHATSAPP/COBRANCA_<MAQUINA>.csv` (só acrescenta, `;`, `CAMPOS_CSV` = quando, maquina, usuario, cliente, nome, telefone, em_atraso, titulos, acao ENVIADO/PULADO).
  - `historico()` lê **todos** os `COBRANCA_*.csv` e guarda o último registro por cliente; `situacao()` dá ENVIADO HOJE / ENVIADO dd/mm (< 7 dias, `DIAS_RECENTE`) / PULADO HOJE.
- Um arquivo por máquina: hoje existem 2. Isso resolve o retorno sem conflito (c).
- As tabelas nascem em `relatorios_nucleo.farol_inadimplencia` (~l. 6229, cols ~l. 6370 e 6426). **Não há coluna CNPJ**: CLIENTE é o código-loja.

## (b) O que o pacote leva a mais (só em `relatorios["pl_inadimplencia"]`)
- `tabelas`: "Títulos" e "Por cliente", só `titulo, colunas, linhas, tons, total, filtros`. Sem `edicao`, `detalhe`, `kpis_de`, `recortes`.
  - Títulos (539 linhas hoje): SITUAÇÃO, FAIXA, FILIAL, NF, PARC., EMISSÃO, VENCIMENTO, DIAS ATRASO, CLIENTE, NOME, CIDADE, UF, VENDEDOR, SUPERVISOR, CONDIÇÃO, VALOR, SALDO. **Sem TELEFONE.**
  - Por cliente (193 linhas): as 16 colunas do PC **menos TELEFONE**.
- `cobranca` (bloco novo): `{modelo, gerado_em, dias_recente: 7, fila: [{cod, nome, nome_msg, cidade, uf, vendedor, supervisor, em_atraso, maior, whatsapp, aviso, titulos[{nf, parc, venc, dias, saldo}], mensagem, ultimo: {quando, acao, origem}}]}`.
  - Hoje: 136 clientes na fila, 17 sem WhatsApp. O telefone vai **só aqui**, já normalizado (`whatsapp`).
  - A `mensagem` vai pronta do PC (M2: o PC monta, a web só desenha). A pessoa pode editar na tela.
- Tamanho medido: Títulos ~152 KB em JSON (15 KB gzip); Por cliente ~51 KB (9 KB). Fila com mensagens: ~80 KB [SUPOSIÇÃO].
  - Total: ~280 KB por rodada (~40 KB no zip). O disco de 1 GB comporta.
- Os cartões e `insights` continuam sem nome de cliente (Adendo 2). O nome aparece só nas tabelas e na fila.

## (c) Volta ao PC sem perder nada
- **Web grava** `/var/data/cobranca/COBRANCA_WEB_<AAAA-MM>.jsonl`: só acrescenta, com fsync, um JSON por linha.
  - Campos: `{seq, id (uuid4 do servidor), quando "AAAA-MM-DD HH:MM:SS" Manaus, usuario (login), cliente, telefone, em_atraso, titulos, acao ENVIADO|PULADO, pacote_sha}`.
  - Rota `POST /r/pl_inadimplencia/cobranca`: CSRF + perfil. A web nunca altera nem apaga uma linha antes da confirmação.
- **Robô, no 4f, antes de montar o pacote:**
  1. `GET /api/cobranca?desde=<seq>` (Bearer `BAP_WEB_TOKEN`, só saída HTTPS).
  2. `cobranca_whatsapp.importar_web(raiz, linhas) -> int`: acrescenta a `COBRANCA_WEB.csv`, com `CAMPOS_CSV` + `id`, maquina = "WEB" e o nome vindo da base. Pula `id` já presente: idempotente.
  3. `POST /api/cobranca/confirmar {ate_seq}`, só depois de gravar.
  4. Monta a fila com `historico()`: o `COBRANCA_WEB.csv` entra pelo glob, sem mudar o PC.
- Escritor único: o PC do robô. Os CSV das assistentes ficam intocados (regra 7).
- **Conflitos possíveis:**
  1. Mesmo cliente cobrado no PC e na web entre rodadas (08h e 14h): a defasagem chega a ~6h de dia e à noite inteira. A web junta `ultimo` do pacote + o log local e avisa "situação do PC até hh:mm".
  2. Reenvio ou queda no meio: a chave `id` impede duplicar. Sem confirmação, a web reenvia na rodada seguinte.
  3. CSV aberto no Excel ou travado pelo OneDrive: o robô não confirma e tenta de novo na próxima rodada.
  4. Fila velha (cliente pagou depois das 08h): igual ao PC de hoje. O `baixado_em` fica à vista.
  5. Clique duplo: a web ignora o mesmo usuário+cliente+ação em menos de 60 s.
  6. Hora: o formato é igual ao do PC (`historico` compara texto) e o `TZ=America/Manaus` é obrigatório.
  7. Perda do disco antes do GET: perde-se no máximo uma rodada [SUPOSIÇÃO: snapshot diário do Render].

## (d) Segurança e LGPD
- **Perfis:** tabelas + "Cobrar" para `admin` e `pos_venda`; `gerente` vê as tabelas sem o botão e sem telefone; `diretor` vê só cartões e gráficos. O filtro é no servidor: 403 + teste por perfil. Proposta na decisão 1.
- **Registro de acesso:** login, rid, aba, ação e hora, em `/var/data/acessos/`. Sem cliente nem telefone. O log da app continua sem dado pessoal (§4.5).
- **Na tela:** HTTPS; `Cache-Control: no-store` e `noindex` nas páginas com tabela; sem exportar CSV/Excel nesta entrega.
- **No disco do Render:**
  - JSON dos últimos 7 pacotes (nome, código-loja, cidade, telefone na fila);
  - o jsonl da cobrança, apagado 30 dias depois de confirmado pelo robô (o PC é a fonte da verdade);
  - `usuarios/` e `acessos/` (90 dias).
  - Nada no GitHub. Fixtures de teste sintéticas (regra 6).
- **Segredos:** nada novo. Usa o `BAP_WEB_TOKEN` existente (env ou cofre `BAP_WEB`).

## (e) Adendo 3 à ADR 0001 (texto curto)
> **Adendo 3 (AAAA-MM-DD): Títulos, Por cliente e "Cobrar no WhatsApp" no Farol de Inadimplência (T-0017).** Vale sobre o Adendo 2 só no `pl_inadimplencia`. Fonte: R-20261124-181913-alexandre. (1) O pacote passa a levar as tabelas "Títulos" e "Por cliente" (sem TELEFONE e sem as chaves de ação) e o bloco `cobranca` (fila, mensagem pronta e o número de WhatsApp). Assim, nome de cliente, código e telefone vão ao Render, só para os perfis da decisão 1. CNPJ não vai. (2) A web deixa de ser só leitura **num ponto**: ela acrescenta registros ao diário da cobrança no disco, num jsonl só de acréscimo. O robô puxa o diário, grava `RELATORIOS/_COBRANCA_WHATSAPP/COBRANCA_WEB.csv` com chave idempotente e confirma. O PC continua a fonte da verdade, e os CSV das máquinas ficam intocados. (3) Retenção: 7 pacotes; o diário web fica 30 dias depois de confirmado. (4) Contrato v1: acréscimo compatível (§10.2). A web publica antes e o robô depois. (5) Continua: M2, sem API de WhatsApp nem disparo automático, e o resto do Adendo 2 (cartões, insights e outros faróis sem cliente).

## (f) Donos, ordem, tamanho e prazo (DU)
1. **engenheiro-software:** Adendo 3 + contrato §10.2 (`tabelas` do farol, bloco `cobranca`, API `/api/cobranca`). **P, 1 DU**, depois das decisões.
2. **gerente-projetos:** RN-POS nova em `docs/produto/03-regras.md` (fila, 7 dias, só acrescenta, idempotência). **P, 0,5 DU.**
3. **modulo-posvenda:** em `cobranca_whatsapp.py`, as funções puras `pacote_web(farol, nomes, hist, hoje)` e `importar_web(raiz, linhas)`, com `test_RN_POS_...`. **M, 1,5 DU.**
4. **modulo-web:** validador (libera `tabelas` só no `pl_inadimplencia`, com lista de colunas), abas com filtros, fila + wa.me, POST, jsonl, GET/confirmar, retenção, perfis e simulação PNG antes do PR. **G, 3–4 DU** (em paralelo com 3).
5. **modulo-robo:** 4f (puxa, importa, monta, envia, confirma). **M, 1,5 DU**, depois de 3.
6. **testes:** ida e volta, idempotência, 403 por perfil, tabela da web = tabela do PC célula a célula. **M, 1,5 DU.** Depois: revisor, corretor, designer-ux.
- Liberação: "aprovo deploy" da web, depois o "instale" do robô.
- **Previsão: ~6 DU** de calendário com paralelismo (~9 DU de esforço), mais a espera das aprovações.

## (g) Decisões para o Alexandre
1. **Quem vê e quem cobra.** A (rec.): admin e pos_venda veem e cobram; gerente vê as tabelas sem telefone e sem botão; diretor só cartões. B: diretor também vê as tabelas. C: só admin e pos_venda veem as tabelas.
2. **CNPJ.** A (rec.): não vai; vai o código do cliente, como nas abas do PC. B: acrescentar a coluna CNPJ (muda também o PC, modulo-farois).
3. **Retenção no Render.** A (rec.): 7 pacotes; diário web por 30 dias depois de confirmado. B: 15 pacotes e 90 dias.
4. **Atraso entre PC e site.** A (rec.): as 2 rodadas de hoje (08h e 14h) e o aviso "situação do PC até hh:mm". B: uma rodada curta de hora em hora só da cobrança (mais carga no PC do robô).
5. **Telefone editado no site.** A (rec.): vale só para aquele envio e fica no diário, como no PC. B: o site não deixa editar.
6. **Exportar tabelas no site.** A (rec.): não nesta entrega. B: sim, Excel por perfil.
