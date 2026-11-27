# Parecer do revisor-codigo — PR #137 (T-0045, ADR 0004 e contrato visitas-nuvem v1)

- **Head SHA revisado:** `a6c719c4e226d1b3894fc4dabed8ae8728f3ef76` (branch `engenheiro-software/T-0045-visitas-render`). Commit novo = revisão nova.
- **Base:** `origin/main` a32b610. Diff lido com `git diff origin/main...origin/engenheiro-software/T-0045-visitas-render`, sem trocar de branch.
- **Decisões conferidas:** R-20261127-005437-alexandre, itens 2 a 6 (2 A, 3 A, 4 A, 5 A, 6 B).
- **Data:** 27/11/2026 (Manaus).

## Resultado: **não aprovado** — nenhum 🔴, 4 🟡 a corrigir antes do merge

## O que confere

- **Decisões fiéis** (ADR §0 e §10, contrato):
  - 2 A: cron job à parte, Standard por minuto, ~US$ 1 a 3/mês; o site continua no Starter;
  - 3 A: 06h00 de Manaus, baixando ontem;
  - 4 A: admin e gerente no botão;
  - 5 A: usuário próprio do robô, só como variável secreta;
  - 6 B: sem print, só o código e a fase.
- **Segredos:**
  - nenhum valor secreto no diff (busca por padrões de chave, senha e token);
  - `BAP_MAXIMA_USUARIO` e `BAP_MAXIMA_SENHA` têm `sync: false` e ficam só no `bap-visitas-maxima`. O `bap-central` não as recebe (conferido aplicando o diff sobre o `render.yaml` do main e lendo o YAML);
  - a chave da API do Render foi recusada com o motivo certo (ADR §3.3);
  - leitura com `os.environ.pop`, `DEBUG=pw:*` e trace proibidos, filtro de máscara no log.
- **Token com escopo mínimo:**
  - o `BAP_VISITAS_TOKEN` (`generateValue`) só abre `/api/visitas/trabalho` e `/rodada*` (contrato §3);
  - os testes de não abrir `/api/pacote*`, `/api/edicoes` e `/api/visitas/lotes` estão previstos (ADR §8);
  - a comparação é em tempo constante.
- **Sem print:**
  - contrato §5: "a nuvem não tira print em nenhum caso";
  - `foto=False` na nuvem e o teste "nenhum `screenshot`".
- **Regra 9:** a Prospecção fica no PC justamente para não usar o Graph (ADR §1 e §7).
- **`render.yaml` proposto** (`docs/desenho/T-0045-render-yaml.diff`):
  - aplica limpo sobre o a32b610 (`git apply --check` numa cópia fora do clone);
  - o site continua `plan: starter`, com uma variável a mais;
  - o cron é `standard`, na mesma região (oregon);
  - o `schedule` em UTC `*/10 10-23,0-1` dá as 06h00 às 21h50 de Manaus, coerente com a `JANELA`;
  - a conta de ~1.900 min/mês × ~US$ 0,00058 dá ~US$ 1,10: coerente com "~US$ 1 a 3/mês" [SUPOSIÇÃO de preço, marcada no texto].
- **Donos:**
  - `requirements-visitas.txt` casa com `requirements*.txt` (`.coord/donos.json`, linha 491), dono engenheiro-software;
  - `docs/desenho/**` (linha 163), `docs/decisoes/**` e `.coord/contratos/**` também são do engenheiro-software;
  - `nuvem/**` continua "sem-dono", e a ADR leva isso corretamente à governança 1.
- **Governança escondida:**
  - nenhuma. O diff não toca `.claude/**`, `.coord/donos.json`, `scripts/coord*.mjs`, `.github/**`, `render.yaml`, `.gitignore` nem os `.json` da raiz;
  - o `render.yaml` vai como proposta em texto;
  - `verificar --por-commit origin/main..a6c719c`: OK, 3 commits, nenhuma violação (o a6c719c é um merge, ignorado; o squash resolve).
- **Fora do escopo, intocados:**
  - os dados digitados e as 3 configs;
  - o `planner_config.json`;
  - o `bap_dados.py` (VERSAO 27);
  - nenhum número do Diretor.
- **Redundância:**
  - `depois_de_baixar` é uma função só, usada pelo PC e pela importação;
  - `dias_a_baixar` sai do `plano`/`dia_fechado`, que já existem;
  - `arquivo_analitico` e `nome_limpo` são reusados.
- **Divisão por dono e ordem** (ADR §9; desenho §4; contrato §8):
  - governança 1 → web → robô e Dockerfile → testes → governança 2 → diagnóstico;
  - web antes do robô, e o `render.yaml` só depois do código no main. Coerente.
- **Testes e CI:**
  - é só desenho: sem código, sem `compileall` aplicável;
  - no head SHA, o check `conferir` ainda estava `in_progress` (GitGuardian `neutral`). O merge segue a regra de CI verde no head.

## 🟡 Corrigir antes do merge

1. **O lote pode levar CNPJ, telefone e e-mail de cliente.**
   - Onde:
     - `.coord/contratos/visitas-nuvem.md:131-132` (o Excel cru em `b64`);
     - `.coord/contratos/visitas-nuvem.md:274` (`espelho_colunas` só tem `cnpj`, `telefone` e `endereco`, **sem `email`**);
     - `docs/decisoes/0004-visitas-maxima-no-render.md:255-257`.
   - O problema:
     - o lote é o Excel do Espelho sem filtro, e a ADR mesmo diz que não sabe se ele tem CNPJ ou telefone;
     - "se tiver, o lote continua só em trânsito, e isso vai ao Alexandre" quer dizer que o dado sobe assim mesmo;
     - isso não garante "o lote não leva CNPJ, telefone nem e-mail".
   - Correção:
     - pôr `email` no `espelho_colunas`;
     - tratar `cnpj`, `telefone` ou `email` verdadeiro no diagnóstico como o captcha: a agenda **não liga** e o botão do site não roda até a decisão do Alexandre. As saídas são tirar as colunas no contêiner antes do envio, com o efeito no `montar_dia` medido, ou aceitar;
     - pôr o teste disso no ADR §8.
2. **As novas tentativas não têm limite, e o `deve_rodar` não tem o dado para limitá-las.**
   - Onde:
     - `.coord/contratos/visitas-nuvem.md:62-71` e `:74-82` (o corpo do `trabalho`);
     - `:90-91` (passos 6 e 7);
     - `:33` (`RETENTATIVAS_AGENDA`);
     - `:241`, `:244` e `:247` (`NAVEGADOR_FALHOU`, `RODADA_INTERROMPIDA` e `ERRO_INTERNO` = "volta seguinte").
   - O problema:
     - o `trabalho` não traz a última tentativa da agenda nem quantas houve no dia;
     - com "ontem fora do `indice`", o passo 6 dispara **a cada 10 min até 21h50**;
     - o `RETENTATIVAS_AGENDA` (06h30, 07h00, 07h30) não dá para implementar com `deve_rodar(agora, trabalho)`;
     - o mesmo vale para o passo 7: se a nova tentativa cair, o `refeito` continua `false`.
   - Efeito:
     - até ~96 logins por dia na Máxima, com risco de bloqueio da conta (RN-VIS-004);
     - um custo que sai do "~US$ 1 a 3/mês" (96 × 3 a 8 min/dia).
   - Correção:
     - pôr no `trabalho` um campo como `tentativas_hoje: {motivo: {n, ultima_em}}`, mantido pelo site no `fim` e no `RODADA_INTERROMPIDA`;
     - um teto diário por motivo (agenda: 1 + 3; retentativa: 1);
     - marcar `refeito: true` também quando a nova tentativa falha;
     - testes no `deve_rodar` (ADR §8: "teto de tentativas no dia").
3. **O desenho permite pôr o `render.yaml` "no mesmo PR".**
   - Onde: `docs/desenho/T-0045-render-yaml.md:13`.
   - O problema: o texto contradiz:
     - o §4 do mesmo arquivo ("governança 2 só depois do código no main", senão o build do cron falha);
     - o ADR §9, item 10;
     - "um PR por dono e por lote" (CLAUDE.md, Git e PR).
   - Correção: "num PR próprio do Alexandre (`alexandre/T-0045-...`), só depois dos itens 5, 7 e 8 no main".
4. **A ADR aponta para uma branch que deixou de ser a da proposta.**
   - Onde: `docs/decisoes/0004-visitas-maxima-no-render.md:101`, `:103` e `:282` (item 1 do §9).
   - O problema: citam a `engenheiro-software/T-0045-render-yaml`, mas o a6c719c juntou a proposta a esta branch, e o desenho já diz isso (`T-0045-render-yaml.md:4`). Depois do squash, a referência fica sem destino.
   - Correção: "em `docs/desenho/T-0045-render-yaml.md` e `.diff` (neste PR)".

## 🟢 Sugestões

- **Cobrança:** a ADR §2.2 diz "por segundo", e o comentário do diff diz "cobrado por minuto".
  - Escolher um dos dois.
  - Medir no diagnóstico a duração de uma volta **sem trabalho** (a ADR §3.3 supõe 30 s). Ela é o maior item da conta: 1.440 dos ~1.900 min.
- **`CONFIG_FALTANDO` sai com 1** (contrato `:245` e `:250`). Entre o merge do `render.yaml` e os 2 segredos, cada volta fica vermelha no painel, com até 96 avisos por dia.
  - Opção 1: sair com 0 nesse código, mantendo o registro no site.
  - Opção 2: o Alexandre preenche os segredos no mesmo sync do Blueprint, que já pede os `sync: false`.
- **Plano B do token** (`T-0045-render-yaml.md`, §2.1): "qualquer texto longo" é fraco. Trocar por "um valor de 32 bytes aleatórios, gerado no PC do Alexandre (ex.: `secrets.token_urlsafe(32)`), colado nos dois serviços e nunca em recado".
- **`dockerContext: .`:** um `.dockerignore` (`RELATORIOS/`, `SISTEMA BAP/`, `BAP Ajuda 2.0/`, `.coord/`, `docs/`) tira as bases do contexto de build e encurta a imagem. A lista fechada de `COPY` já protege a imagem.
- **D3:** "Baixar de novo", "Retomar", "Diagnóstico" e "Ligar a agenda" só para o admin é uma escolha técnica, não está na decisão 4 A. Deixar isso explícito na simulação do designer-ux (item 4) para o Alexandre ver.

## Observação de processo

- Por instrução de quem pediu ("não altere nada"), este parecer ficou só neste arquivo, sem commit.
- Ficaram de fora: o recado `revisao` ao gerente-projetos e o `docs/revisao/T-0045.md`. O gerente-projetos encaminha ou pede o registro.
