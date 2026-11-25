---
id: R-20261124-210623-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T21:06:23-04:00
---
# Parecer do revisor-codigo: PR #56 head d029695 — 9 🟡 (contrato da cobrança)

> Parecer do revisor-codigo, com checagem de redundância (subagente do gerente-projetos; gravado pelo gerente sem alteração).

# Revisão do PR #56 — T-0017: contrato da cobrança no site (§10.2) e Adendo 3 da ADR 0001

- **Head revisado:** `d029695fa16916be69c59adaae71e4bbfc82d80b` (branch `engenheiro-software/T-0017-contrato-cobranca`). Commit novo = revisão nova.
- **Arquivos:** `.coord/contratos/relatorio.md` (+186), `docs/decisoes/0001-bap-central-web-render.md` (+41). Só documentação: sem código, sem teste, sem tela.
- **Revisor:** revisor-codigo, 25/11/2026 (Manaus).

## Parecer: NÃO aprovado. Nenhum 🔴, 9 🟡 e 9 🟢.

As decisões "1 A … 7 A" (R-20261124-192008-alexandre) estão todas no texto, sem mudança a mais. As RN-POS-001 a 004 estão citadas, e a RN-POS-001 do `main` foi conferida. A segurança está bem desenhada: CSRF, corte do perfil no servidor, Bearer só na API, 400/404/409 e confirmação idempotente. CNPJ fica fora, e as colunas batem com `relatorios_nucleo.farol_inadimplencia` (`:6373-6438`) menos TELEFONE. Sem chave nem segredo no texto; nenhum dado digitado foi tocado; `bap_dados.py` não foi alterado. Os 🟡 são ambiguidades. Os três módulos (web, posvenda e robô) vão implementar em paralelo a partir deste texto, então elas precisam fechar antes do merge.

`node scripts/coord.mjs verificar engenheiro-software --base origin/main` (rodado no head, numa worktree temporária): OK, 2 arquivos, nenhuma violação.

## 🟡 Corrigir antes do merge

1. **`.coord/contratos/relatorio.md` §10.2.3, linha `whatsapp`: a regra do contrato está errada.** O texto diz `"55" + DDD + 9 dígitos, ou "" quando não há celular válido`. A RN-POS-001 (`main`, `docs/produto/03-regras.md:40`) e o `cobranca_whatsapp.celular()` (`cobranca_whatsapp.py:63-83`) fazem outra coisa:
   - o número **fixo** sai em `whatsapp` (`"55"` + DDD + 8 dígitos), com o aviso "telefone fixo: pode não ter WhatsApp";
   - o campo só fica vazio quando o número é inválido (curto), repetido (`99 99999999`) ou ausente.

   Alinhar o contrato: o tipo passa a ser `"55"+DDD+8 ou 9 dígitos` ou `""`. O mesmo vale para a validação do §10.2.5 (`telefone`) e do §10.2.4 (telefone corrigido): fixo é aceito, e o 400 só vem quando o `celular()` devolve `""`. Senão a web rejeita o que o PC monta.
2. **Numeração §10.2 em conflito.** "§10.2" já é usado para o **item 2 do §10** ("chaves com `_` são internas"). Exemplo: `web/app/pacotes.py:202`, que diz "internas do contrato (§10.2)"; e a linha 40 do contrato cita "§10.5" no sentido de item 5. Com a subseção nova, a mesma citação aponta para dois lugares. Renumerar (ex.: §10.1 → "10.A"/"10.B", ou chamar os itens de "§10, item 2") ou pedir ao modulo-web que corrija a referência no mesmo lote.
3. **§10.2.3, `ultimo.origem` × `historico()`.** O `historico()` devolve `{cliente: (quando, acao)}`, sem `maquina` (`cobranca_whatsapp.py:202-218`). Então o `origem = "WEB"` não sai dele, e o `situacao()` desempacota a dupla (`:224`). O contrato precisa dizer qual função pública o modulo-posvenda cria ou muda, e com que assinatura. Ex.: `historico(raiz, com_maquina=False)` ou uma função nova `ultimos(raiz)`, mantendo a janela do PC igual.
4. **§10.2.4, `ENVIADO` sem número.** Com `telefone` vazio e `whatsapp` do item `""`, o texto manda usar o `whatsapp` do item, que está vazio. Não diz se o servidor responde 400 ou grava `ENVIADO` com telefone vazio. Definir (sugestão: 400).
5. **§10.2.4, item que saiu da fila ou pacote trocado.** O 404 vale para "cliente fora da fila do pacote ativo". Se o pacote das 08h/14h chega entre abrir a tela e clicar em "Enviado", a mensagem já foi pelo WhatsApp e o registro se perde. Definir o comportamento: por exemplo, aceitar o `cod` da fila do pacote ainda guardado (`pacote_sha` vindo da página), ou 409 com aviso na tela.
6. **§10.2.5, retenção e `seq`: contradição.**
   - O texto diz que "a linha confirmada é apagada 30 dias depois" e também que "o arquivo do mês some quando todas as linhas passaram do prazo". Não diz se a limpeza é por linha (reescreve um jsonl "só acréscimo") ou por arquivo inteiro.
   - Não diz onde ficam o contador de `seq` ("nunca reaproveitado, nem depois da limpeza") e a marca de confirmação, nem como sobrevivem quando todos os arquivos são apagados.

   Fixar: limpeza por arquivo e um arquivo de estado (ex.: `<BAP_WEB_DADOS>/cobranca/estado.json` com `ultimo_seq`, `confirmado_ate` e `confirmado_em`), gravado de forma atômica.
7. **§10.2.6/§10.2.7, perda do disco do Render.** O Adendo 3 (Consequências) admite que o disco se perca. Se acontecer, o `seq` recomeça em 1 e o robô continua pedindo `desde=<último confirmado>` (ex.: 41). Os registros novos com `seq ≤ 41` **nunca** são puxados, e a web ainda os esconde como "já no PC" (`seq ≤ web_ate_seq`). O `id` não resolve, porque o `desde` pula as linhas antes de comparar. Incluir uma época do diário: por exemplo, `diario_id` no GET e no pacote, com o robô voltando a `desde=0` quando ele muda. Outra saída: o GET devolve `ultimo_seq`, e o robô reinicia quando o `desde` passa dele.
8. **Retenção dos pacotes ("3 A") só no ADR.** Hoje a web guarda 15 pacotes (`web/app/pacotes.py:18`, `GUARDAR = 15`). O §10.2 não diz que o valor passa a 7 nem se vale para todos os `rid`. O modulo-web implementa pelo contrato, então pôr no §10.2 (ou no §10.1) "GUARDAR = 7, todos os pacotes".
9. **§10.2.3 × §10.2.7, a definição de `web_ate_seq` diverge.** Em um lugar é "o maior `seq` que já estava no `COBRANCA_WEB.csv`"; no outro, "o `ate_seq` **confirmado**". Os dois diferem quando o robô importa e o `POST /confirmar` falha. Escolher uma definição; a primeira é a mais segura para a tela.

## 🟢 Sugestões

1. §10.2.4, resposta do clique duplo: dizer se `{"ok": true, "repetido": true}` traz também `seq`, `id` e `situacao` do registro original. A tela precisa da `situacao`.
2. §10.2.3, `modelo`: dizer se a web usa o campo (refazer a mensagem) ou só mostra a `mensagem` pronta. Se ela refizer, os `venc` em ISO sairiam como "2026-10-20" no texto, e não como `dd/mm/aaaa` (`_venc`, `:136`). Se não usa, tirar do pacote (é redundante).
3. §10.2.4: o PC aceita o número digitado sem passar pelo `celular()` (`janela.numero()`, `:384-389`). Registrar que o site é mais estrito, ou tirar o "como no PC".
4. §10.2.6: dizer o que o robô faz com 401 e 5xx no GET e no confirmar. Hoje o texto só fala de 404 e "falha de rede".
5. §10.2.4/§10.2.6: escrever que a API **não** aceita cookie de sessão e que a rota do site **não** aceita Bearer.
6. §10.2.7, o parâmetro `nomes` de `importar_web` (`{cod-loja: NOME}`) tem o mesmo nome e outro sentido do `nomes` de `fila()` (`{cod6: fantasia}`). Renomear (ex.: `nomes_por_cod`).
7. §10.2.7: se uma máquina se chamar `WEB` (`maquina()`), ela grava no mesmo `COBRANCA_WEB.csv`. Reservar o nome ou citar o caso.
8. ADR item 6, "registro de acesso": dizer onde fica e por quanto tempo, porque o §10.2 não cita.
9. §10.2.7, "função pura sobre o disco" é contraditório. Trocar por "função sem tela, testável com `tmp_path`".

## Redundância

O Adendo 3 repete o §10.2: a tabela de perfis, a retenção, a ordem de publicação e "sem exportar". O texto diz que "o formato exato está no contrato", o que aceito; sugiro que o adendo cite as seções em vez de reescrever as regras. Não há regra de DU, projeção ou positivação reescrita, e o §10.2 reusa a autenticação do `/api/pacote`, o CSRF da sessão e o filtro do §10.1 sem duplicar código.
