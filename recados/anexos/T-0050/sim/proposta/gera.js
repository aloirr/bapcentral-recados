// T-0050: gera os HTML estáticos da simulação (dados 100% fictícios) e tira os PNGs.
const fs = require('fs');
const path = require('path');
const http = require('http');
const { chromium } = require('playwright');

const RAIZ = __dirname;
const SAIDA = process.argv[2];

// menu (render.GRUPOS_MENU do #158 + Diretoria) e nomes curtos (NOME_MENU)
const GRUPOS = [
  ['Diretoria', [['vc_painel', 'Painel Executivo']]],
  ['Pré-venda', [['pv_pedidos', 'Pedidos'], ['pv_indicadores', 'Indicadores']]],
  ['Pós-venda', [['pl_entregas', 'Entregas'], ['pl_inadimplencia', 'Inadimplência'], ['pl_frw', 'Estoque FRW']]],
  ['Vendas', [['vc_visitas', 'Visita'], ['vc_meta', 'Metas Equipe'], ['vc_base', 'Clientes'], ['vc_planner', 'Roteirização'], ['pl_giro', 'Giro de produtos']]],
  ['Analista Comercial', [['vc_saldo', 'Saldo'], ['vc_markup', 'Markup'], ['vc_preco', 'Preço'], ['an_divergencias', 'Divergências']]],
];
const LG = ['admin', 'gerente', 'analista'];
const PERFIS_RID = {  // o trade ainda não tem farol no site (o Expositores entra na T-0025 v2)
  vc_painel: [...LG, 'diretor'],
  pv_pedidos: [...LG, 'diretor', 'pre_venda'], pv_indicadores: [...LG, 'diretor', 'pre_venda'],
  pl_entregas: [...LG, 'diretor', 'pos_venda'], pl_inadimplencia: [...LG, 'diretor', 'pos_venda'],
  pl_frw: [...LG, 'diretor', 'pre_venda', 'pos_venda'],
  vc_visitas: [...LG, 'diretor', 'vendas'], vc_meta: [...LG, 'diretor', 'vendas'], vc_base: [...LG, 'diretor', 'vendas'],
  vc_planner: [...LG, 'diretor', 'vendas'], pl_giro: [...LG, 'diretor', 'vendas'],
  vc_saldo: [...LG, 'diretor'], vc_markup: [...LG, 'diretor'], vc_preco: [...LG, 'diretor'], an_divergencias: [...LG, 'diretor'],
};
const ROT = { admin: 'Admin', diretor: 'Diretor', gerente: 'Gerente', analista: 'Analista', trade: 'Trade',
  pre_venda: 'Pré-venda', pos_venda: 'Pós-venda', vendas: 'Vendas' };

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const plural = (n, um, varios) => `${n} ${n === 1 ? um : varios}`;

function lateral() {
  let h = '';
  for (const [g, itens] of GRUPOS) {
    h += `<div class="bc3-grupo"><small>${g}</small>${itens.map(([, n]) => `<a href="#">${n}</a>`).join('')}</div>`;
  }
  h += `<div class="bc3-grupo"><small>Conta</small><a href="#" class="on" aria-current="page">Usuários</a><a href="#">Trocar senha</a></div>`;
  return h;
}

function casca(corpo, faixaKs) {
  const ks = faixaKs.map(([r, v]) => `<div class="bc3-k"><small>${r}</small><b>${v}</b></div>`).join('');
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Usuários · BAP AUTOPARTS</title><link rel="stylesheet" href="/static/estilo.css"><link rel="stylesheet" href="/static/sim-farois.css"></head>
<body class="bc3"><div class="bc3-app">
<aside class="bc3-lado" id="bc3-lado" aria-label="Menu"><a class="bc3-marca" href="#"><i aria-hidden="true"></i><span>BAP Central<small>BAP AUTOPARTS</small></span></a>
<nav class="bc3-nav" aria-label="Seções">${lateral()}</nav>
<form class="bc3-eu"><i aria-hidden="true">AD</i><span>admin.ficticio</span><button type="button">Sair</button></form></aside>
<div class="bc3-main"><div class="bc3-topo-cel"><a class="bc3-marca" href="#"><i aria-hidden="true"></i><span>BAP Central<small>BAP AUTOPARTS</small></span></a>
<button type="button" class="bc3-menu" aria-label="Abrir o menu">☰</button></div>
<main class="bc3-corpo"><header class="bc3-faixa simples"><div class="bc3-tt"><h1>Usuários</h1></div><div class="bc3-ks">${ks}</div></header>
${corpo}</main></div></div></body></html>`;
}

// painel de faróis: perfil, marcados (Set de rids), última mudança
function partes(perfil, marcados, nomeCampo = 'farol') {
  const doPerfil = (rid) => PERFIS_RID[rid].includes(perfil);
  const bloco = (filtro, cls, tag) => {
    let h = '';
    for (const [g, itens] of GRUPOS) {
      const its = itens.filter(([r]) => filtro(r));
      if (!its.length) continue;
      h += `<div class="f-grupo"><h3>${g}</h3>` + its.map(([r, n]) =>
        `<label class="f-item"><input type="checkbox" name="${nomeCampo}" value="${r}"${marcados.has(r) ? ' checked' : ''}><span class="f-nome">${n}</span><span class="selo f-tag selo-${tag}">${tag}</span></label>`).join('') + '</div>';
    }
    return h;
  };
  const nPerfil = Object.keys(PERFIS_RID).filter(doPerfil).length;
  const temFora = Object.keys(PERFIS_RID).some((r) => !doPerfil(r));
  return `<div class="f-partes">
<fieldset class="f-parte f-perfil"><legend>Do perfil</legend>
${nPerfil ? `<p class="f-nota">Desmarque para tirar.</p><div class="f-grupos">${bloco(doPerfil, 'f-perfil', 'tirado')}</div>` : '<p class="f-nota">Este perfil ainda não tem farol no site.</p>'}</fieldset>
${temFora ? `<fieldset class="f-parte f-lib"><legend>Liberar além do perfil</legend>
<p class="f-nota">Liberado, o farol abre só no Resumo: sem as tabelas de clientes e sem Exportar. O Painel Executivo abre completo.</p>
<div class="f-grupos">${bloco((r) => !doPerfil(r), 'f-lib', 'liberado')}</div></fieldset>` : ''}
</div>`;
}

function painelFarois(u) {
  return `<details class="u-det u-farois"${u.aberto ? ' open' : ''}><summary class="bc3-bt">Faróis</summary>
<form method="post" action="/usuarios"><input type="hidden" name="acao" value="acesso"><input type="hidden" name="lista" value="1">
${partes(u.perfil, u.marcados)}
${u.quando ? `<p class="f-quando">Alterado em ${u.quando} por admin.ficticio</p>` : ''}<div class="f-rodape"><button type="submit" class="bt-neutro">Salvar acesso</button></div></form></details>`;
}

function linha(u, antes) {
  const selos = [];
  if (!u.ativo) selos.push('<span class="selo selo-cinza">Desativado</span>');
  if (u.troca) selos.push('<span class="selo selo-atencao">Troca de senha pendente</span>');
  if (!antes && u.tirados) selos.push(`<span class="selo selo-tirado">${plural(u.tirados, 'farol tirado', 'faróis tirados')}</span>`);
  if (!antes && u.liberados) selos.push(`<span class="selo selo-liberado">${plural(u.liberados, 'farol liberado', 'faróis liberados')}</span>`);
  const farois = antes ? '' : painelFarois(u);
  return `<li class="u-linha"><span class="u-nome">${u.login}</span><span class="u-perfil">${ROT[u.perfil]}</span>
<span class="u-selos">${selos.join('')}</span><span class="u-acoes">${farois}
<details class="u-det"><summary class="bc3-bt">Trocar senha</summary></details>
${u.ativo ? '<details class="u-det u-perigo"><summary class="bc3-bt bt-perigo">Desativar</summary></details>' : '<form class="linha"><button type="button" class="bc3-bt">Ativar</button></form>'}
</span></li>`;
}

function padrao(perfil) { return new Set(Object.keys(PERFIS_RID).filter((r) => PERFIS_RID[r].includes(perfil))); }

function usuarios(estado) {
  // estado: antes | lista | aberto | salvo | erro
  const u3m = padrao('vendas'); u3m.add('pv_pedidos');
  if (estado === 'aberto') { u3m.delete('vc_planner'); u3m.add('vc_painel'); }
  if (estado === 'erro') u3m.clear();
  const salvo = estado === 'salvo';
  const u5m = padrao('pos_venda'); u5m.delete('pl_frw');
  return [
    { login: 'admin.ficticio', perfil: 'admin', ativo: true, marcados: padrao('admin'), aberto: estado === 'admin' },
    { login: 'usuario.ficticio.01', perfil: 'diretor', ativo: true, marcados: padrao('diretor') },
    { login: 'usuario.ficticio.02', perfil: 'trade', ativo: true, marcados: estado === 'trade' ? new Set(['pv_pedidos']) : new Set(), aberto: estado === 'trade' },
    { login: 'usuario.ficticio.03', perfil: 'vendas', ativo: true, marcados: u3m,
      aberto: estado === 'aberto' || estado === 'erro',
      tirados: salvo ? 1 : 0, liberados: salvo ? 2 : 1,
      quando: salvo ? '27/11/2026 06:30' : '26/11/2026 17:42' },
    { login: 'usuario.ficticio.04', perfil: 'pre_venda', ativo: true, troca: true, marcados: padrao('pre_venda') },
    { login: 'usuario.ficticio.05', perfil: 'pos_venda', ativo: true, marcados: u5m, tirados: 1, quando: '25/11/2026 09:15' },
    { login: 'usuario.ficticio.06', perfil: 'analista', ativo: true, marcados: padrao('analista') },
    { login: 'usuario.ficticio.07', perfil: 'vendas', ativo: false, marcados: padrao('vendas') },
  ];
}

function telaUsuarios(estado, { novoAberto = false } = {}) {
  const antes = estado === 'antes';
  const lista = usuarios(estado);
  const ks = [['Ativos', 7], ['Desativados', 1], ['Troca pendente', 1]];
  let msg = '';
  if (estado === 'salvo') msg = '<p class="ok" role="status">Acesso de usuario.ficticio.03 salvo. Liberado: Painel Executivo. Tirado: Roteirização.</p>';
  if (estado === 'erro') msg = '<p class="erro" role="alert">usuario.ficticio.03: marque ao menos um farol. Para tirar todo o acesso, use Desativar.</p>';
  const perfis = ['admin', 'diretor', 'gerente', 'analista', 'trade', 'pos_venda', 'pre_venda', 'vendas'];
  const novo = antes
    ? `<details class="u-novo"><summary class="bc3-bt bc3-bt-verde">Novo usuário</summary></details>`
    : `<details class="u-novo"${novoAberto ? ' open' : ''}><summary class="bc3-bt bc3-bt-verde">Novo usuário</summary>
<form method="post" action="/usuarios" class="caixa u-novo-form"><input type="hidden" name="acao" value="criar">
<div class="u-novo-campos"><label>Usuário <input name="login" value="usuario.ficticio.08"></label>
<label>Perfil <select name="perfil">${perfis.map((p) => `<option${p === 'pre_venda' ? ' selected' : ''}>${ROT[p]}</option>`).join('')}</select></label>
<label>Senha inicial (trocada no 1º acesso) <input type="password" value="xxxxxxxxxxxx"></label></div>
${partes('pre_venda', padrao('pre_venda'))}
<div class="f-rodape"><button type="submit" class="bt-neutro">Criar</button></div></form></details>`;
  const corpo = `${msg}${novo}<ul class="u-lista">${lista.map((u) => linha(u, antes)).join('')}</ul>`;
  return casca(corpo, ks);
}

function telaAntesDepois(titulo, a, d, largura) {
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>
body{margin:0;font:16px Inter,Arial,sans-serif;background:#F3F4F2;color:#1E2722}
.ad{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:20px}
h1{font-size:20px;margin:16px 20px 0}h2{font-size:15px;margin:0 0 8px;text-transform:uppercase;letter-spacing:.06em;color:#5E6B63}
img{width:${largura}px;border:1px solid #E3E8E4;border-radius:8px;display:block}</style></head>
<body><h1>${titulo}</h1><div class="ad"><div><h2>Antes (hoje)</h2><img src="${a}"></div><div><h2>Depois (proposta T-0050)</h2><img src="${d}"></div></div></body></html>`;
}

(async () => {
  fs.mkdirSync(path.join(RAIZ, 'html'), { recursive: true });
  const pags = {
    'antes': telaUsuarios('antes'),
    'lista': telaUsuarios('lista'),
    'aberto': telaUsuarios('aberto'),
    'salvo': telaUsuarios('salvo'),
    'erro': telaUsuarios('erro'),
    'novo': telaUsuarios('lista', { novoAberto: true }),
    'admin': telaUsuarios('admin'),
    'trade': telaUsuarios('trade'),
  };
  for (const [k, h] of Object.entries(pags)) fs.writeFileSync(path.join(RAIZ, 'html', k + '.html'), h);

  const srv = http.createServer((req, res) => {
    const p = path.join(RAIZ, decodeURIComponent(req.url.split('?')[0]));
    if (!p.startsWith(RAIZ) || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
    const tipo = { '.css': 'text/css', '.html': 'text/html; charset=utf-8', '.png': 'image/png', '.woff2': 'font/woff2', '.js': 'text/javascript' }[path.extname(p)] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': tipo }); fs.createReadStream(p).pipe(res);
  }).listen(0);
  const base = `http://127.0.0.1:${srv.address().port}`;
  const nav = await chromium.launch();
  const telas = {
    pc: { viewport: { width: 1366, height: 768 } },
    cel: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true },
  };
  const tiros = [
    ['0-antes-usuarios', 'antes', {}],
    ['1-usuarios-lista', 'lista', {}],
    ['2-farois-aberto', 'aberto', { cel: [['a', 'li:has(.u-farois[open])', 'start'], ['b', '.u-farois[open]>form', 'end']] }],
    ['3-salvo', 'salvo', {}],
    ['4-novo-usuario', 'novo', { cel: [['a', null], ['b', '.u-novo-form', 'end']] }],
    ['5-erro-nenhum-farol', 'erro', { cel: [['a', null], ['b', 'li:has(.u-farois[open])', 'start']] }],
    ['6-farois-admin', 'admin', { cel: [['a', 'li:has(.u-farois[open])', 'start'], ['b', '.u-farois[open]>form', 'end']] }],
    ['7-farois-trade', 'trade', { cel: [['a', 'li:has(.u-farois[open])', 'start'], ['b', '.u-farois[open]>form', 'end']] }],
  ];
  for (const [disp, opc] of Object.entries(telas)) {
    const ctx = await nav.newContext({ ...opc, deviceScaleFactor: 2, locale: 'pt-BR', timezoneId: 'America/Manaus' });
    const pg = await ctx.newPage();
    for (const [nome, pag, o] of tiros) {
      await pg.goto(`${base}/html/${pag}.html`);
      await pg.evaluate(() => document.fonts.ready);
      await pg.waitForTimeout(250);
      const arq = path.join(SAIDA, `${nome}-${disp}.png`);
      if (disp === 'cel' && o.cel) {
        for (const [suf, sel, bloco] of o.cel) {
          if (sel) await pg.evaluate(([s, b]) => { document.querySelector(s).scrollIntoView({ block: b }); if (b === 'start') window.scrollBy(0, -76); else window.scrollBy(0, 70); }, [sel, bloco]);
          await pg.waitForTimeout(150);
          await pg.screenshot({ path: path.join(SAIDA, `${nome}-${disp}-${suf}.png`) });
        }
      } else await pg.screenshot({ path: arq, fullPage: !!(o.full && o.full[disp]) });
      // medições: rolagem lateral e alvos < 44 px no celular
      const m = await pg.evaluate((cel) => {
        const r = { rolagemLateral: document.documentElement.scrollWidth > document.documentElement.clientWidth, alturaPagina: document.documentElement.scrollHeight, alvosPequenos: [] };
        if (cel) for (const el of document.querySelectorAll('.bc3-corpo button, .bc3-corpo summary, .bc3-corpo .f-item, .bc3-corpo input:not([type=hidden]):not([type=checkbox]), .bc3-corpo select')) {
          const b = el.getBoundingClientRect(); if (el.checkVisibility() && b.height && b.height < 44) r.alvosPequenos.push(el.className || el.tagName);
        }
        const st = document.createElement('style'); st.textContent = '.f-tag{display:inline-block!important}'; document.head.appendChild(st);
        r.seloQuebra = [...document.querySelectorAll('.f-item')].filter((it) => it.checkVisibility() && Math.abs(it.querySelector('.f-tag').getBoundingClientRect().top - it.querySelector('.f-nome').getBoundingClientRect().top) > 6).map((it) => it.textContent);
        st.remove();
        return r;
      }, disp === 'cel');
      console.log(nome, disp, JSON.stringify(m));
    }
    await ctx.close();
  }
  // composições antes × depois (deviceScaleFactor 2)
  const ctx = await nav.newContext({ viewport: { width: 1400, height: 600 }, deviceScaleFactor: 2, locale: 'pt-BR', timezoneId: 'America/Manaus' });
  const pg = await ctx.newPage();
  fs.mkdirSync(path.join(RAIZ, 'shots'), { recursive: true });
  for (const f of fs.readdirSync(SAIDA)) if (f.endsWith('.png')) fs.copyFileSync(path.join(SAIDA, f), path.join(RAIZ, 'shots', f));
  const comps = [
    ['antes-depois-pc', 'Tela Usuários a 1366 px: antes × depois (painel Faróis aberto)', '/shots/0-antes-usuarios-pc.png', '/shots/2-farois-aberto-pc.png', 683],
    ['antes-depois-cel', 'Tela Usuários a 390 px: antes × depois (lista com os selos)', '/shots/0-antes-usuarios-cel.png', '/shots/1-usuarios-lista-cel.png', 390],
  ];
  for (const [nome, t, a, d, w] of comps) {
    fs.writeFileSync(path.join(RAIZ, 'html', nome + '.html'), telaAntesDepois(t, a, d, w));
    await pg.goto(`${base}/html/${nome}.html`);
    await pg.waitForLoadState('networkidle');
    await pg.screenshot({ path: path.join(SAIDA, `${nome}.png`), fullPage: true });
  }
  await nav.close(); srv.close();
})();
