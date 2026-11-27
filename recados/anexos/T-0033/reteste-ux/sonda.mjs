// Reteste UX T-0033 no 94b3440 (designer-ux). Só lê. Uso: node sonda.mjs <porta> <ck.json> <saida-png>
import { createRequire } from 'node:module';
import { readFileSync, mkdirSync } from 'node:fs';
const require = createRequire('/opt/node-tools/node_modules/');
const { chromium } = require('playwright');
const [porta, ckf, out] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
const ck = JSON.parse(readFileSync(ckf, 'utf8'));
const P = `http://localhost:${porta}`;
const b = await chromium.launch();
const URLS = [
  ['pv_pedidos', 'resumo'], ['pv_pedidos', 'pedidos'], ['pv_pedidos', 'pedidos', 'PA'], ['pv_pedidos', 'solicitacao'],
  ['pl_entregas', 'resumo'], ['pl_entregas', 'entregas'], ['pl_entregas', 'entregas', 'PA'],
  ['pl_inadimplencia', 'resumo'], ['pl_inadimplencia', 'titulos'], ['pl_inadimplencia', 'titulos', 'PA'], ['pl_inadimplencia', 'cliente'], ['pl_inadimplencia', 'cobrar'],
  ['vc_visitas', 'resumo'], ['vc_visitas', 'vendedor'], ['vc_visitas', 'dia'], ['vc_visitas', 'aderencia'], ['vc_visitas', 'cliente'], ['vc_visitas', 'supervisor'],
  ['vc_meta', 'resumo'], ['vc_meta', 'equipe'], ['vc_meta', 'equipe', 'PA'],
];
const PNG = /entregas_entregas$|entregas_entregas_PA|pedidos_pedidos_PA|visitas_(resumo|vendedor|aderencia|cliente)$|meta_equipe$|inadimplencia_titulos$|inadimplencia_titulos_PA|meta_equipe_PA/;
for (const [vn, w, h, mob] of [['pc1366', 1366, 768, false], ['cel390', 390, 844, true]]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2, hasTouch: mob, isMobile: mob });
  await ctx.addCookies(Object.entries(ck.admin).map(([name, value]) => ({ name, value, url: P + '/' })));
  const p = await ctx.newPage();
  for (const [rid, aba, uf] of URLS) {
    const url = `/farol/${rid}${aba === 'resumo' ? '?' : '?aba=' + aba}${uf ? '&uf=' + uf : ''}`;
    const r = await p.goto(P + url, { waitUntil: 'networkidle' });
    await p.waitForTimeout(150);
    const m = await p.evaluate(() => {
      const vis = (e) => e && e.offsetParent !== null;
      const fx = document.querySelector('.bc3-faixa');
      const sub = document.querySelector('.bc3-sub');
      const abas = [...document.querySelectorAll('.bc3-abas > a')].filter(vis);
      const tx = document.body.innerText;
      const cortes = [...document.querySelectorAll('.bc3-faixa small, .bc3-faixa em, .bc3-k small, .bc3-k b, .bc3-abas a, .bc3-aviso-k')].filter(vis)
        .filter((e) => e.scrollWidth > e.clientWidth + 1 || getComputedStyle(e).textOverflow === 'ellipsis' && e.scrollWidth > e.clientWidth).map((e) => e.textContent.trim());
      const busca = document.querySelector('.bc3-busca input');
      let buscaCorte = null;
      if (vis(busca)) { const c = document.createElement('canvas').getContext('2d'); const s = getComputedStyle(busca); c.font = `${s.fontSize} ${s.fontFamily}`; buscaCorte = Math.round(c.measureText(busca.placeholder).width) + '/' + Math.round(busca.clientWidth - parseFloat(s.paddingLeft) - parseFloat(s.paddingRight)); }
      const th = [...document.querySelectorAll('.tab-dados thead th, .tab-dados thead td')].filter(vis).map((e) => e.textContent.trim().replace(/\s+/g, ' '));
      const tabs = [...document.querySelectorAll('table')].filter(vis).map((t) => [...t.querySelectorAll('thead th')].map((e) => e.textContent.trim().replace(/\s+/g, ' ')).slice(0, 3).join('|'));
      const totais = [...document.querySelectorAll('tr')].filter(vis).filter((t) => /total/i.test(t.className) || /^\s*total/i.test(t.innerText)).map((t) => t.innerText.replace(/\s+/g, ' ').slice(0, 60));
      const filt = document.querySelector('.bc3-filt > summary');
      const filtMarker = filt ? getComputedStyle(filt).listStyleType + '|' + getComputedStyle(filt, '::after').content : null;
      const ader = [...document.querySelectorAll('.ader tbody td')].filter(vis).slice(0, 60).map((t) => { const el = t.querySelector('span,i,b,em') || t; const s = getComputedStyle(el); return t.textContent.trim() + '|' + s.backgroundColor + '|' + s.color; }).filter((k) => /%/.test(k));
      const lista = [...document.querySelectorAll('.bc3-lista > *, .m3 > *, details.m3l > summary')].filter(vis).slice(0, 3).map((e) => e.innerText.replace(/\s+/g, ' ').slice(0, 90));
      const caixas = [...document.querySelectorAll('.rolagem, .rolagem-dados, .bc3-lista, main, .bc3-juntas, .bc3-faixa, .bc3-sub')].filter(vis).filter((e) => e.scrollWidth > e.clientWidth + 1 && getComputedStyle(e).overflowX !== 'visible').map((e) => e.className + ' ' + e.scrollWidth + '>' + e.clientWidth);
      const sel = (q) => [...document.querySelectorAll(q)].filter(vis);
      const vcel = [...document.querySelectorAll('td, .bc3-lista *')].filter(vis).filter((e) => /VENDEDOR FICTICIO/.test(e.textContent) && e.children.length === 0).slice(0, 2).map((e) => e.textContent.trim() + (e.scrollWidth > e.clientWidth + 1 ? ' [CORTADO]' : ''));
      return {
        faixaH: fx ? Math.round(fx.getBoundingClientRect().height) : null,
        ks: sel('.bc3-k').map((k) => k.innerText.replace(/\s+/g, ' ')).slice(0, 7),
        avisoK: sel('.bc3-aviso-k').map((e) => e.textContent.trim()),
        semUf: (tx.match(/Sem filtro por estado/g) || []).length, semUfSelo: sel('.bc3-faixa .bc3-uf').some((e) => /Sem filtro/.test(e.textContent)),
        uf: sel('.bc3-uf').map((e) => e.className + ':' + e.textContent.trim().replace(/\s+/g, ' ')),
        avisos: sel('.aviso').map((e) => e.textContent.trim().slice(0, 70)),
        abas: abas.map((a) => a.textContent.trim().replace(/\s+/g, ' ')), linhasAbas: new Set(abas.map((a) => Math.round(a.getBoundingClientRect().top))).size,
        abasAltas: abas.filter((a) => a.getBoundingClientRect().height > 48).map((a) => a.textContent.trim().replace(/\s+/g, ' ') + ':' + Math.round(a.getBoundingClientRect().height)),
        mais: vis(document.querySelector('.bc3-mais-abas')),
        subTops: sub ? new Set([...sub.children].filter(vis).map((c) => Math.round(c.getBoundingClientRect().top))).size : 0,
        cortes, buscaCorte, filtMarker, tabs, th: th.slice(0, 4), totais: totais.slice(0, 3), ader: ader.slice(0, 6), lista, caixas, vcel,
        verMais0: /Ver mais 0/.test(tx), rolaH: document.scrollingElement.scrollWidth - innerWidth, rolaV: document.scrollingElement.scrollHeight - innerHeight,
      };
    });
    console.log(JSON.stringify({ v: vn, url, st: r.status(), ...m }));
    const nome = `${rid}_${aba}${uf ? '_' + uf : ''}`;
    if (PNG.test(nome)) await p.screenshot({ path: `${out}/${nome}__${vn}.png` });
  }
  if (mob) {   // "Mais" aberto (C3) e Metas inteira (C10)
    for (const u of ['vc_visitas?aba=vendedor', 'pl_inadimplencia?aba=titulos', 'vc_meta?aba=equipe']) {
      await p.goto(P + '/farol/' + u, { waitUntil: 'networkidle' });
      await p.locator('.bc3-abas details > summary').first().tap(); await p.waitForTimeout(300);
      const r = await p.evaluate(() => { const d = document.querySelector('.bc3-abas details'); return { open: d.open, itens: [...d.querySelectorAll('div a')].map((m) => { const r = m.getBoundingClientRect(); const e = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return m.textContent.trim() + ':' + (e === m || m.contains(e) ? 'ok' : 'COBERTO') + ':h' + Math.round(r.height); }) }; });
      console.log('MAIS', u, JSON.stringify(r));
      if (u.startsWith('vc_visitas')) await p.screenshot({ path: `${out}/mais-visita__cel390.png` });
    }
    await p.goto(P + '/farol/vc_meta?aba=equipe', { waitUntil: 'networkidle' });
    await p.screenshot({ path: `${out}/vc_meta_equipe-inteira__cel390.png`, fullPage: true });
  }
  await ctx.close();
}
await b.close();
