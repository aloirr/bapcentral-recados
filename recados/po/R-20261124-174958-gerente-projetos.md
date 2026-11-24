---
id: R-20261124-174958-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: resposta
prioridade: normal
tarefa: null
responde_a: R-20261124-174526-po
encerra: false
contrato: null
criado_em: 2026-11-24T17:49:58-04:00
---
# 4 faróis na web: desenho técnico pronto e 4 decisões para o Alexandre

## Resumo (gerente-projetos)
- Nenhum dos 4 faróis está no pacote do robô hoje, e a web ainda não desenha os blocos que eles usam (só `rrm`). A 1ª entrega leva a base comum: contrato "farol" no pacote, renderizador genérico, menu e perfis.
- Ordem recomendada: Inadimplência (G com a base; o farol em si é P) → Pedidos (M) → Entregas (M) → Visita (M). Previsão após o "backlog": 1ª simulação PNG PC × web em cerca de 2 dias úteis (base comum); os demais, cerca de 1 dia útil cada.
- O que grava no PC fica fora da web: autorização de venda, edição de entrega (`_EDICOES_POS_VENDA`), e-mail/WhatsApp da inadimplência, "Atualizar visitas". O validador da web recusa as chaves de edição.
- Suposições do po: de acordo com os perfis; Visita na web = "mês atual, BAP inteira", com o "baixado em" à vista (o dado depende do "Atualizar visitas" manual no PC).

## Decisões para o Alexandre (resposta pronta "N X")
1. Entrada no backlog: (A) T-0017 com os 4 faróis, um por entrega, na ordem acima; (B) só o Farol de Inadimplência agora. Recomendo A. Resposta: "1 A".
2. Nome de vendedor e supervisor no Render (gráficos de Pedidos, Inadimplência e Visita): (A) mandar, como o gerente já vê no PC, sem cliente nem CNPJ (adendo à ADR 0001); (B) trocar pelo código; (C) tirar esses gráficos. Recomendo A. Resposta: "2 A".
3. "Mesmo conteúdo": (A) cartões + Resumo gerencial, sem as tabelas linha a linha (elas têm cliente e CNPJ); tabela com cliente só numa onda futura com ADR própria. Recomendo A. Resposta: "3 A".
4. Filtro por estado: (A) muda os cartões; os gráficos seguem da BAP inteira, com o aviso na tela; (B) gráficos por estado também (mais trabalho no robô, cada farol vira M+). Recomendo A. Resposta: "4 A".

## Desenho técnico completo (engenheiro-software)

## 0. O que já existe (base de tudo)
- A web roda no **M2** (adendo da ADR 0001): o PC monta e manda JSON pronto e a web não roda o `montar`. O 4f do robô (`bap_automation.montar_pacote_web`, `selecionar_abas_web` e `recortes_por_uf`) manda **só o `vc_painel`**, com as abas `res`/`prod`.
- A web (`web/app/pacotes.py`) aceita só `ACEITOS = ("vc_painel",)` e valida o bloco `rrm`. O `web/app/render.py` só desenha cartões `rrm`. Os perfis (`web/app/usuarios.py`) são só `admin`/`diretor`/`gerente`.
- **Nenhum dos 4 faróis está no pacote hoje.** O renderizador também não é genérico ainda: falta desenhar `kpis`, `insights`, `barras`, `hbarras` e `tabela`.
- Regra do M2 que continua valendo: a web não executa callable (`kpis_de`, `recortes`, `edicao`, `detalhe_pedido`). O filtro por estado vem pronto do PC, como na T-0014.

## 1. Por farol
| | Farol de Pedidos `pv_pedidos` | Farol de Visita `vc_visitas` | Farol de Entregas `pl_entregas` | Farol de Inadimplência `pl_inadimplencia` |
|---|---|---|---|---|
| (a) Onde monta | `relatorios_nucleo.farol_pedidos` (:1556) + `_painel_pedidos` (:18542) | `farol_visitas` (:13231) + `_painel_visitas` (:14409) | `entregas` (:6805) + `_painel_entregas_exec` (:7040) | `farol_inadimplencia` (:6229) + `_painel_inadimplencia` (:18792) |
| Blocos (contrato §8) | 2 tabelas, 8 kpis (`kpis_faixa`), painel com insights/barras/hbarras | 7 tabelas, 10 kpis, painel só com `barras`; `abrir`; parâmetros (mês, supervisor, comparativo) | 1 tabela (+1 junta), 7 kpis, painel com insights/barras/hbarras/**tabela** (frete por UF) | 7 tabelas, 6 kpis, painel com insights/barras/hbarras |
| Fonte (bloco `bap_dados`) | `tabela`, `posvenda` (devoluções), autorizações | Visitas/ (Máxima), Planner, `ROTA_PROTHEUS_*.json` | `posvenda` + `transportadoras_config.json` | `inadimplencia`, fotos de títulos |
| (b) No pacote? | Não | Não | Não | Não |
| (c) Bloco novo na web | kpis + insights/barras/hbarras | só barras + kpis (o mais simples) | + `tabela` no painel | igual a Pedidos |
| (d) Grava no PC (fora da web) | autorização de venda (`AUTORIZA_EM`, `_edicao_autorizacao`, `autorizacoes.gravar`); "Parcial Pedidos" | "Atualizar visitas" (`visitas_maxima`), "Parcial Visitas", ABRIR (`r["abrir"]`) | edição da entrega (`r["editar"]`, `_entrega_editavel` → `_EDICOES_POS_VENDA`); "Parcial Entregas" | "Enviar por e-mail", "Cobrar no WhatsApp" |
| (e) Dado pessoal | tabelas com razão social, fantasia, CNPJ e vendedor: **fora**. O hbarras "Pedidos em aberto por vendedor" tem nome de vendedor | tabelas por vendedor: **fora**. O painel por supervisor tem nome | transportadora e cidade (não é pessoa). A tabela de notas com cliente fica **fora** | "Títulos" e "Por cliente": **fora**. O hbarras "Em atraso por vendedor" tem nome |
| RN | GER-004/005 (internos e 000040), GER-006 (UF = filial), GER-008; teto de 15% do desconto | GER-007 (hoje fora do DU), GER-008, GER-010 (lote de 16/10), aderência ao Planner (RN-ROT) | RN-POS: SLA em dias corridos, DT. PREVISTA desde o pedido, frete mínimo; GER-006 | GER-004/005/006/008; faixas de atraso |
| Tamanho | M | M | M | P (depois do renderizador) |

## 2. Mudanças comuns (antes do 1º farol)
1. **Contrato** (engenheiro-software, `.coord/contratos/relatorio.md` §10): nova forma "farol" no pacote, `relatorios[rid] = {titulo, kpis, painel:{blocos}, insights_painel, avisos, recortes:{uf:{kpis, painel?}}}`.
   - Sem `tabelas` nem `juntas`, sem callables e sem `_`.
   - Mudança compatível: a web antiga recusaria o `rid` novo. Por isso a web publica antes e o robô depois, e a versão do contrato fica em 1 [SUPOSIÇÃO].
   - Precisa de um adendo na ADR 0001, porque "sem dado pessoal no Render nesta fase" muda se o nome de vendedor for.
2. **Robô** (modulo-robo, `bap_automation.py`), em funções puras com teste:
   - `selecionar_farol_web(rid, r)`;
   - `recortes_farol_por_uf(r)`: chama o `kpis_de` com as linhas filtradas por FILIAL→UF (RN-GER-006) e manda os kpis por estado prontos;
   - `coletar_relatorios_web` monta os rids da lista `FAROIS_WEB`, com `MÊS`/`ANO` explícitos, e cada `montar` fica num `try` isolado: falha de um farol não derruba o pacote.
3. **Web** (modulo-web):
   - `pacotes.ACEITOS` + `validar_farol`;
   - renderizador genérico de `kpis`, `insights`, `barras` e `hbarras` (e depois `tabela`), em HTML/CSS sem biblioteca nova (barras em CSS) e no tamanho de 390 px;
   - bloco desconhecido mostra "ainda não disponível na web";
   - menu com os 4 itens;
   - perfis novos `pos_venda`, `pre_venda` e `vendas` (`usuarios.PERFIS`).
4. **Testes** (testes, `tests/test_T00xx_*`): PC × pacote no mesmo dia, com o total e um estado, valor × regra, e fixture sem dado pessoal.

## 3. Ordem recomendada (um farol por entrega)
1. **Inadimplência**: a primeira entrega é G, porque leva o contrato, o renderizador genérico e o 1º farol. O farol em si é P: é o mais "padrão" (`painel_farol.montar`), já foi conferido no ADR §4.3 e o Diretor já o monta. Donos: engenheiro-software (contrato + adendo), modulo-robo, modulo-web, testes, designer-ux.
2. **Pedidos** (M): mesmos blocos. É preciso garantir que a autorização não vire botão. `kpis_faixa` = cartões em faixa. Donos: modulo-robo, modulo-web, testes, designer-ux.
3. **Entregas** (M): bloco `tabela` no painel (frete por estado), com a coluna da tabela já sem dado pessoal. Donos: modulo-robo, modulo-web, testes (modulo-posvenda só se mexer no `transportadoras` em modo leitura: hoje não, porque o PC monta).
4. **Visita** (M): parâmetros (mês, supervisor) viram visões prontas ou só "mês atual, BAP inteira". O dado depende do "Atualizar visitas" manual no PC. Donos: modulo-robo, modulo-web, testes; modulo-rota só para leitura do `visitas_nucleo`.
- Revisor-codigo e corretor-redundancias em todas. Simulação PC × web (PNG) antes de cada PR.

## 4. Riscos e decisões para o Alexandre (via po)
- **D1. Nome de vendedor/supervisor no Render** (hbarras de Pedidos e Inadimplência, painel de Visita). Recomendo mandar: é o que o gerente já vê, sem CNPJ nem cliente. A alternativa é trocar pelo código ou tirar o gráfico, mas aí o número não bate visualmente com o PC.
- **D2. "Mesmo conteúdo" = cartões + Resumo gerencial, sem as tabelas linha a linha** (as tabelas têm cliente/CNPJ). Tabela com cliente na web só na onda com as bases no Render e com ADR própria.
- R1. O UF da web vale só para os kpis (o painel do PC não segue filtro). A web deve dizer "cartões por estado; gráficos da BAP inteira".
- R2. Visita desatualizada se ninguém clicar em "Atualizar visitas" antes do 4f: mostrar o "baixado em" do farol.
- R3. Tempo do 4f: +~4 s de `montar` (inventário §8), desprezível. Pacote: alguns KB a mais.
- R4. Perfis novos = mudança de login (modulo-web), com teste de acesso negado por perfil.
- R5. Dado digitado (regra 7): nada é gravado, porque a web não tem `edicao` nem `editar` (o validador recusa as chaves).
