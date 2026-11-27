# T-0045 · PR #137 · Reteste de redundância e excesso (corretor-redundancias)

- **Escopo:** `git diff a6c719c 59864e7` (6 arquivos, +308 −321), lido no estado do head: ADR 0004, contrato `visitas-nuvem.md` v1, `docs/desenho/T-0045-render-yaml.md` e `.diff`, `requirements-visitas.txt` e o diário.
- **Head SHA retestado:** `59864e7fdb1f602847581c497d692a5e34731836` (filho de `a6c719c`).
- **Parecer anterior:** `redundancias-pr137.md` (RD-0072 a RD-0081).
- **Resultado:** **não libera.** Dos 10 achados, 9 estão fechados. O RD-0072 tem 1 resto em aberto. A correção criou 3 repetições novas, do RD-0082 ao RD-0084 (2 médias, 1 baixa). Nenhuma está só em comentário ou título de teste.
- **Dono:** engenheiro-software (os 5 arquivos).

## 1. Situação dos RD-0072 a RD-0081

| RD | Situação | Evidência no head |
|---|---|---|
| RD-0072 | **Aberto (1 resto).** Os itens 1 e 3 a 8 estão fechados: os passos da importação estão só no contrato §4.4 (251-256), e a ADR §5.1 (184) aponta para lá; a tabela de falhas saiu da ADR §6 (216), e o `SITE_FORA` ficou com uma versão só; o diagnóstico aponta para a ADR (contrato:314); o "sem print" saiu da ADR §6; o aviso do PC está só no contrato (272), e a ADR:156 aponta para ele; o plano pelo pico está só na ADR:102 (com o Pro); a retenção está só em `LOTE_GUARDA_DIAS` (ADR:236, contrato:338). **O resto é o item 2:** "Proibido no cron" continua com 2 listas diferentes, e cada uma tem itens que a outra não tem. A ADR:224 lista "trace, vídeo, HAR, `page.on("console")` e print de tela". O contrato:25 lista "`DEBUG` que contenha `pw`, `PWDEBUG` e `PLAYWRIGHT_*` de trace ou vídeo". HAR e `console` só existem na ADR, e quem implementa o `rodar.py` lê o contrato. | ADR:223-224 × contrato:25 |
| RD-0073 | **Fechado.** O desenho não repete o YAML (linha 6: "explica o diff sem repetir o YAML"). As características do Render estão só no desenho §2.1, e a ADR:97 aponta para lá. As linhas do `donos.json` estão só no desenho §3 ("a única cópia"), e a ADR:112 e o item 2 do §9 apontam para lá. A ordem está na ADR §9 ("a única fonte da ordem"), e o contrato §8 e o desenho §4 apontam para ela. | ADR:97, 112, 261; desenho:6, 48, 105; contrato:346 |
| RD-0074 | **Fechado.** O §10 entrou no §0 (com a coluna "Recomendação do time" e o texto literal na linha 36). A numeração D1 a D5 está nos 3 arquivos e nos comentários do `.diff` (o `grep` por "decisão N A" sai vazio). O "40 min" só tem número no §4 (169); o §5.3 e o §10 apontam para ele. | ADR:26-36, 169, 210, 290; contrato:21, 33, 264, 274 |
| RD-0075 | **Fechado.** A ADR:106 e o desenho:4 e :11 dizem "neste PR"; a ADR:265 diz "todos no PR #137". A branch `origin/engenheiro-software/T-0045-render-yaml` continua no remoto, sem PR; cabe ao gerente-projetos decidir o que fazer com ela. | ADR:106, 265 |
| RD-0076 | **Fechado.** Há um índice só, com `fechados_pc` (contrato §4.3, 236-244), `origem` no `indice` (91) e `fechados_pc_em` como condição para ligar a agenda (87). A janela de 30 min que ainda sobra está explicada na ADR:188. | contrato:87, 91, 243-244 |
| RD-0077 | **Fechado.** O laço é o `puxar_fila_web`, que serve às edições e às visitas (contrato:250), e o armazém é a `edicoes.Fila`, parametrizada (contrato:225 e 338). A cobrança fica de fora, com motivo escrito: ela confirma só o `ate_seq`. Isso é `manter` (§3). | contrato:225, 250; ADR:183-184, 269, 272 |
| RD-0078 | **Fechado.** O `fim` leva só o `codigo`, e o status sai do `STATUS_DO_CODIGO` (186). O `pico_mb` está só no topo do `fim` (187), e `medidas` fica com o `fonte_pico` (328). Os indicadores de confirmação e captcha saíram de `medidas` e do log. O 401 está só na regra comum (59). O `/saude` não tem mais `status`. | contrato:181-189, 271, 330 |
| RD-0079 | **Fechado.** Os 5 textos estão como na proposta, e o PC tem um nome só, "o Atualizar visitas do PC" (285-295). Os 2 textos novos (`DADO_PESSOAL` e `TETO_DIA`) seguem o mesmo molde. | contrato:285-298 |
| RD-0080 | **Fechado.** A tela mostra "as 10 últimas rodadas … a mais recente em destaque, no topo", sem a linha "última rodada" à parte. | contrato:263 |
| RD-0081 | **Fechado.** O `GET /api/visitas/estado` saiu; o `/saude.visitas` ganhou `rodada_ativa` e `fase` e é "a única rota de estado". O aviso do PC passou para o §4.5. | contrato:271-272 |

**Proposta para o resto do RD-0072:** uma lista só, no contrato.
- Contrato:25, **antes:** "**Proibido no cron:** `DEBUG` que contenha `pw`, `PWDEBUG` e `PLAYWRIGHT_*` de trace ou vídeo. Com qualquer um deles, o `rodar.py` sai com `CONFIG_INSEGURA` antes de abrir o navegador." → **depois:** "**Proibido no cron:** (a) no ambiente: `DEBUG` que contenha `pw`, `PWDEBUG` e `PLAYWRIGHT_*` de trace ou vídeo; com qualquer um, o `rodar.py` sai com `CONFIG_INSEGURA` antes de abrir o navegador; (b) no código: trace, vídeo, HAR, `page.on("console")` e print de tela (D5). Os testes conferem os dois."
- ADR:224 sai. A ADR:223 já aponta para o contrato §1.

## 2. Repetições novas, criadas pela correção

### RD-0082 · Diagnóstico com dado pessoal: os `achados` vão 2 vezes no mesmo `fim`
- **Onde:** contrato §3.5, no topo do `fim` (183 e 188: "`achados`: só com `DADO_PESSOAL`") × §6, em `medidas.espelho.achados` (325 e 329). Quando o diagnóstico acha dado pessoal, o mesmo `fim` leva a mesma lista em 2 chaves. É o padrão do `pico_mb` que o RD-0078 fechou.
- **Tipo:** código (contrato). **Impacto:** manutenção (2 chaves que podem divergir; o site precisa saber qual vale).
- **Severidade:** média.
- **Proposta:** a lista fica só no topo do `fim`, que vale para toda rodada.
  - Contrato:325, **depois:** `"espelho": {"colunas_fora": ["KM DIST", "BONIF", "OBSERVACAO"]}}`.
  - Contrato:329, **depois:** "`espelho.colunas_fora`: as colunas que o `filtrar_espelho` (§3.6) tirou nos 2 Excel. Os achados vão no `achados` do `fim` (§3.5), e com eles o `codigo` é `DADO_PESSOAL`."

### RD-0083 · A RN-VIS-006 está escrita 3 vezes na ADR
- **Onde:** a regra está na RN-VIS-006 (ADR:200) e é repetida na própria ADR:
  - §0:42: "um achado de CNPJ, CPF, telefone ou e-mail trava tudo até a decisão do Alexandre";
  - §7:234: "CNPJ, CPF, telefone, e-mail ou valor fora do formato nas colunas permitidas travam o dia e pausam tudo (RN-VIS-006)";
  - §6:218: "O admin só retoma com o id do recado da decisão", que é a última frase da RN-VIS-006 de novo, e que também está no contrato:266 e :288.
- **O que se repete:** os 5 tipos de achado aparecem 3 vezes na ADR, e o "só retoma com a decisão do Alexandre" aparece 2 vezes na ADR e 2 no contrato.
- **Tipo:** doc. **Impacto:** manutenção. Quando o po passar a RN para o `03-regras.md`, sobram 3 cópias a manter iguais.
- **Severidade:** média.
- **Proposta:**
  - ADR:42, **depois:** "**o lote leva só as colunas permitidas do Espelho**, com varredura de dado pessoal (§7, RN-VIS-006);"
  - ADR:234, **depois:** "**varredura do que fica** (RN-VIS-006): é melhor parar a nuvem e usar o PC por uns dias do que guardar dado pessoal no Render;"
  - ADR:218: a última frase ("O admin só retoma com o id do recado da decisão.") sai; ela continua na RN-VIS-006 e no contrato §4.5.
  - A ADR:233 ("lista de permitidas, não de proibidas") fica, porque é o porquê.

### RD-0084 · Um ponteiro duplicado, uma frase repetida e um número fixo no lugar da constante
- **Onde:**
  1. **O contrato aponta 2 vezes para a ordem:** na linha 4 ("A ordem de publicação está na ADR 0004, §9") e de novo no §8 (344-346: "ADR 0004, §9.").
  2. **A mesma frase na ADR e no desenho:** "Se o `render.yaml` entrar antes do código, o build do cron fica vermelho no painel até o código chegar; o site não cai." está igual na ADR:279 e no desenho:105.
  3. **"40" fixo na ADR:** a ADR:187 diz "os dias fechados dos últimos 40 dias", e o contrato usa a constante `FECHADOS_PC_DIAS` (46, 91, 243).
- **Tipo:** doc. **Impacto:** manutenção. Se a constante mudar, a ADR fica errada.
- **Severidade:** baixa.
- **Proposta:**
  1. O §8 do contrato (344-346) sai, porque a linha 4 já aponta para a ordem.
  2. Desenho:105, **depois:** "ADR 0004, §9 (itens 2, 7, 8, 10 e 11)." A frase fica só na ADR:279.
  3. ADR:187, **antes:** "os dias fechados dos últimos 40 dias (`fechados_pc`, contrato §4.3)" → **depois:** "os dias que ele fechou (`fechados_pc`, contrato §4.3)".

## 3. O que foi conferido e não é repetição (manter)
- **`puxar_fila_web`:** a definição está no contrato:250; a ADR (184, 250, 272) só cita. A cobrança fica com o seu laço porque confirma de outro jeito (só o `ate_seq`). Manter.
- **`fechados_pc`:** o como está no contrato (§3.1, §4.3); o porquê e a janela de 30 min estão na ADR:185-188. Fora o "40" do RD-0084, não há cópia.
- **Ordem do merge:** a fonte é só a ADR §9. Sobram só ponteiros (e os 2 do RD-0084).
- **RN-VIS-007:** os números (8 no total; 4, 3, 1 e 2 por motivo) aparecem na ADR:123-125 e nas constantes do contrato (36-37). Na ADR, eles justificam a escolha do 8 e a conta de custo; a ADR:6 diz que, se os dois divergirem, vale o contrato. Manter.
- **`.dockerignore` × a lista fechada do `COPY`:** manter. O desenho:85 diz que é defesa em camadas e que encurta o envio do contexto de build.
- **`tentativas_hoje.por_motivo.codigo` × `rodadas.jsonl`:** manter. Um é o estado do dia; o outro é o histórico, só com acréscimo.
- **`MAXIMA_CAPTCHA` × `MAXIMA_CONFIRMACAO`:** continua `manter?`, como no parecer anterior.

## 4. Pendências
- O catálogo `docs/redundancias/catalogo.md` e os recados ao dono não foram feitos, por instrução de quem chamou (só o relatório, sem commit). [SUPOSIÇÃO] Quem chamou leva o resto do RD-0072 e os RD-0082 a RD-0084 ao engenheiro-software.
- Reteste no próximo head SHA.
