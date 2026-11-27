import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
const require = createRequire('/opt/node-tools/node_modules/');
const { chromium } = require('playwright');
const [porta, ckf, out] = process.argv.slice(2);
const ck = JSON.parse(readFileSync(ckf, 'utf8'));
const B = `http://localhost:${porta}`;
const b = await chromium.launch();
async function pg(perfil, w, h) {
  const c = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  if (perfil) await c.addCookies([{ name: 'bap_sessao', value: ck[perfil].bap_sessao, url: B }]);
  return c.newPage();
}
const med = {};
for (const [nv, w, h] of [['pc1366', 1366, 768], ['pc1920', 1920, 1080], ['cel390', 390, 844]]) {
  // Desativar aberto
  let p = await pg('admin', w, h);
  await p.goto(B + '/usuarios');
  await p.locator('.u-perigo summary').nth(1).click();
  await p.screenshot({ path: `${out}/usuarios-desativar__${nv}.png` });
  med[`usuarios-desativar-${nv}`] = await p.evaluate(() => { const f = document.querySelectorAll('.u-perigo[open] form')[0]; const r = f.getBoundingClientRect(); return { right: r.right, left: r.left, vw: innerWidth, sw: document.scrollingElement.scrollWidth, cw: document.scrollingElement.clientWidth }; });
  // Novo usuário aberto
  await p.goto(B + '/usuarios');
  await p.locator('.u-novo summary').click();
  await p.screenshot({ path: `${out}/usuarios-novo__${nv}.png` });
  await p.close();
  // painel: medidas e página inteira
  for (const aba of ['resultado', 'produtividade', 'por_dia_util', 'resumo', 'faturamento', 'markup']) {
    p = await pg('diretor', w, h);
    await p.goto(B + '/painel?aba=' + aba);
    med[`painel-${aba}-${nv}`] = await p.evaluate(() => {
      const fx = document.querySelector('.bc3-faixa'); const r = fx.getBoundingClientRect();
      const abas = [...document.querySelectorAll('.bc3-abas > a, .bc3-abas > details > summary')].filter(e => e.offsetParent).map(e => Math.round(e.getBoundingClientRect().height));
      const sub = document.querySelector('.bc3-sub'); 
      return { faixaH: Math.round(r.height), faixaTop: Math.round(r.top), faixaL: Math.round(r.left), faixaR: Math.round(innerWidth - r.right), sh: document.scrollingElement.scrollHeight, ih: innerHeight, sw: document.scrollingElement.scrollWidth, cw: document.scrollingElement.clientWidth, abasH: abas, subH: sub ? Math.round(sub.getBoundingClientRect().height) : 0, uf: !!document.querySelector('.bc3-faixa .bc3-uf'), ufOff: !!document.querySelector('.bc3-uf-off'), ufOffAria: document.querySelector('.bc3-uf-off')?.getAttribute('aria-disabled') ?? null };
    });
    if (aba === 'resultado' || aba === 'faturamento') await p.screenshot({ path: `${out}/painel-${aba}-inteira__${nv}.png`, fullPage: true });
    if (aba === 'resultado' && nv !== 'cel390') { await p.locator('.bc3-ind summary').click(); await p.screenshot({ path: `${out}/painel-indicadores__${nv}.png` }); }
    if (aba === 'resultado' && nv === 'cel390') { await p.locator('.bc3-mais-abas summary').click(); await p.screenshot({ path: `${out}/painel-mais__${nv}.png` }); }
    await p.close();
  }
  // farol: faixa para comparar
  p = await pg('pre_venda', w, h);
  await p.goto(B + '/');
  med[`farol-${nv}`] = await p.evaluate(() => { const r = document.querySelector('.bc3-faixa').getBoundingClientRect(); return { url: location.pathname, faixaH: Math.round(r.height), faixaTop: Math.round(r.top), faixaL: Math.round(r.left), faixaR: Math.round(innerWidth - r.right) }; });
  await p.close();
  for (const [perf, url] of [['admin', '/senha'], ['admin', '/usuarios'], ['admin', '/farol/pv_pedidos/parcial']]) {
    p = await pg(perf, w, h); await p.goto(B + url);
    med[`${url}-${nv}`] = await p.evaluate(() => { const r = document.querySelector('.bc3-faixa').getBoundingClientRect(); const at = document.querySelector('.bc3-lado [aria-current="page"]'); return { faixaH: Math.round(r.height), faixaTop: Math.round(r.top), faixaL: Math.round(r.left), ativo: at ? at.textContent.trim() : null, prim: [...document.querySelectorAll('.bt-principal, .bc3-bt-verde')].filter(e=>e.offsetParent).map(e=>e.textContent.trim()), sh: document.scrollingElement.scrollHeight, ih: innerHeight }; });
    await p.close();
  }
}
// redirecionamentos
for (const perf of ['admin', 'diretor', 'gerente', 'pre_venda', 'pos_venda', 'vendas']) {
  const p = await pg(perf, 1366, 768); await p.goto(B + '/'); med['home-' + perf] = new URL(p.url()).pathname; await p.close();
}
console.log(JSON.stringify(med, null, 1));
await b.close();
