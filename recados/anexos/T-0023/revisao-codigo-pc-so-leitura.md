# Revisão de código — T-0023, PC só leitura (PR 2 de faróis)

- **Branch:** `modulo-farois/T-0023-pc-so-leitura` (ainda sem PR)
- **Head revisado:** `327a294db0406307e5409bf382f6c61d43b553c5` (commit novo = revisão nova)
- **Base:** `origin/main` `57cf6fa` (o main andou 5 commits, nenhum no `bap_relatorios.py`)
- **Escopo:** só `bap_relatorios.py` (+39/−108)
- **Parecer:** sem 🔴. Há **2 🟡** para fechar antes do merge.

## O que foi conferido

| Item | Resultado |
|---|---|
| Nenhum caminho do PC grava NCC, Devolução ou Garantia, fora o contato | ok. `EDICAO_SO_WEB` (`:4427`) ganhou `("pl_ncc", "NCC pendentes")`, `("pl_devolucoes", "Devoluções")` e `("pl_garantias", "Garantias")`. Os ids e os títulos batem com o `relatorios_nucleo` (`:6909`/`:7065`, `:7856`/`:7968`, `:7647`/`:7772`). Só essas 3 tabelas têm `edicao` com `_NCC`, `ABA_DEV` e `_GARANTIAS`. Os caminhos do PC que chegam ao `Edicao` → `anotar` → `salvar` (duplo clique, juntas e `novo`) passam pelo `editar`, que barra, ou pelo `edicao.novo`, que nenhuma das 3 tem. O "Nova garantia" vira aviso (`:2478`). O `bap_central._garantias_abertas` só lê. O "Editar no Excel" do `pl_devolucoes` continua: é o risco 5 do desenho, já pendente na T-0044 |
| "Salvar contato" grava só `contato_nome` e `contato_fone` | ok, com uma exceção 🟢 abaixo. Simulei em pasta temporária com diário fictício. Status, observação e ticket mexidos na tela não gravaram (+1 linha, só `contato_fone`), e os outros campos de `garantias.ler` ficaram iguais. O `gravar` só acrescenta (regra 7). Contato apagado à mão grava `""`, o que é edição legítima do contato |
| `PADRAO_NOVA_GARANTIA` e `campos_garantia_a_gravar` | têm uso: `relatorios_nucleo.edicao_garantia` (`:1864`), o robô `bap_automation.py:9872` e `:9889` e os testes `test_T0023_nucleo_rd.py` e `test_T0023_robo.py`. Ficam |
| RD-0139 | ok. O prazo exibido vem de `rn.prazo_padrao_txt` (`:4336`). Saíram a cópia `_prazo_padrao`, os padrões ABERTO/PENDENTE e a origem copiados na janela |
| Segredos e dados pessoais | ok. Nada no diff. Os PNGs usam dados fictícios |
| `bap_dados.VERSAO` | 27 |
| Dado digitado e configs | intocados. O smoke suja `RELATORIOS/painel_diretor_hist.json` nos worktrees de teste; foi restaurado, e o clone principal está limpo |
| `compileall` | ok |
| `coord verificar --base origin/main` | OK, 1 arquivo, sem violação |
| Commit | `T-0023: ...` com `Agente: modulo-farois` |

## Testes (xvfb, venv 3.12)

- `pytest tests/ -q` no head: **798 passed, 10 skipped, 2 xpassed**.
- `smoke_relatorios.py`: head e `origin/main` (worktree separado) dão **o mesmo resultado**, 291 ok cada um, e param os dois no `contatos_vcf`. Falharam nos dois:
  - Farol DDR (3x);
  - Farol de Clientes, recorte de um vendedor (check `:214` no main, `:218` no head);
  - Farol de Visita;
  - Farol de NCC.
- **Farol DDR e o recorte do Clientes já falham no main**: não são defeito novo, mas faltam na lista de falhas conhecidas do agente `testes`. Avisar o `testes`.
- Nas 2 primeiras rodadas, o smoke do main morreu por falta de memória (`Killed`), porque havia outros pytest na máquina. A 3ª rodada chegou ao fim.

## 🟡 Corrigir antes do merge

1. **Não há check novo para a mudança, e 2 checks antigos passam descrevendo o que saiu.**
   - Falta o critério 6 do `docs/desenho/T-0023.md`: os 3 lugares no `EDICAO_SO_WEB`; "Nova garantia" e Editar mostram `MSG_EDICAO_SO_WEB`; o `DialogoGarantia.salvar` grava só `CAMPOS_PC`; o sha do diário é igual fora as linhas do contato.
   - O `smoke_relatorios.py:4187` ("ticket editável") e o `:4200` ("cadastro do cliente editável", que só sobrevive pelo `hasattr(..., "_trocou_cliente")`) ficaram falsos para o PC.
   - O `tests/test_T0021_edicao_web_robo.py:299` diz "NCC segue editando no PC" e usa o título `"NCC"`, não `"NCC pendentes"`.
   - O dono é o `testes`. Quando os checks forem ajustados, o `_trocou_cliente` (`bap_relatorios.py:4385`) e o `vars_cli` podem sair. Hoje são código morto, mantido só pelo `hasattr`.
2. **O código diverge do desenho:**
   - O `docs/desenho/T-0023.md` §2 (linha do #105) e o risco 6.1 dizem que "o corpo de gravação do `DialogoGarantia` **não é apagado**: fica sem uso até a T-0044, para a volta atrás ser só um commit".
   - Este commit apaga o corpo: `renomear`, validação de datas, cadastro, `origem` e os `_descricao`/`_prazo_padrao`.
   - A remoção é tecnicamente limpa: um `git revert 327a294` traz tudo de volta. Mesmo assim, contraria o desenho aprovado.
   - Para fechar, há duas saídas: (a) o gerente-projetos aceita a remoção e o dono do desenho registra a mudança no §2 e no §6 (a T-0044 perde esse item); ou (b) o corpo volta, sem uso.

## 🟢 Sugestões

1. `DialogoGarantia.salvar` (`:4403-4408`) chama `garantias.gravar`, que tem a regra de status. Um contato salvo numa garantia FINALIZADA/CANCELADA sem `dt_fechamento` no diário grava também `dt_fechamento = hoje`. Numa garantia aberta com data, grava `dt_fechamento = ""`. Reproduzi esse caso em pasta temporária. O estado não aparece na cópia congelada (0 de 12), porque todo escritor passa pelo `gravar`. Mesmo assim, um `gravar_contato` no `garantias.py` (dono: modulo-posvenda) deixaria o "só o contato" garantido pela função.
2. Restos sem uso na janela:
   - `import garantias as gm` no `__init__` (`:4238`);
   - o `self.textos` (preenchido, nunca lido);
   - no núcleo, `r["garantia"]` ainda monta `opcoes` (ordena todos os clientes a cada montagem), `produto`, `status` e `resultados` sem consumidor no PC (`relatorios_nucleo.py:7838-7847`).
   Isso fica para a T-0044.
3. Comentários velhos: `CAMPOS` "(06/11) editavel" (`:4220`), "Alexandre: editavel… digitou o codigo, o resto vem da base" (`:4273-4289`), a docstring do `abrir_garantia` "detalhe do cliente + edicao" (`:2888`) e, no núcleo, o aviso "use Nova garantia" (`:7849`).
4. Tela (para o `designer-ux`):
   - Na Garantia, a dica do rodapé "Duplo clique na linha para editar" sumiu (`:353-358`). Agora a assistente não sabe que o duplo clique abre o contato.
   - Os `Text` desabilitados continuam brancos, com cara de editáveis (`garantia-dialogo.png`).
   - O `aviso-nova-garantia.png` saiu sem o botão OK, um artefato do xvfb sem gerenciador de janelas. Vale um print com WM.
