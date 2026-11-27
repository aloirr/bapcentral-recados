import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
const require = createRequire('/opt/node-tools/node_modules/');
const { chromium } = require('playwright');
const [porta, ckf, out] = process.argv.slice(2);
const ck = JSON.parse(readFileSync(ckf, 'utf8'));
const B = `http://localhost:${porta}`;
const b = await chromium.launch();
const CSS_PC = `
 header.bc3-faixa{margin:14px 16px 0 16px!important;border-radius:16px!important}
 .bc3-sub{margin:0 16px}
 .rc{min-height:0!important}.rc-barras{min-height:0!important}.rc-barras .area{min-height:120px!important}
 .rc-valor,.rc-leg{display:none!important}
 p.como{display:none!important}
 .rrm{margin-top:4px!important}
`;
const CSS_CEL = `
 header.bc3-faixa{margin:12px 14px 0!important;border-radius:16px!important}
 .rc-valor,.rc-leg{display:none!important} p.como{display:none!important}
 .rc-barras{display:none!important}
`;
async function shot(perfil, w, h, url, css, nome, fn) {
  const c = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  await c.addCookies([{ name: 'bap_sessao', value: ck[perfil].bap_sessao, url: B }]);
  const p = await c.newPage(); await p.goto(B + url);
  await p.addStyleTag({ content: css });
  await p.evaluate(fn, w);
  await p.screenshot({ path: `${out}/${nome}.png` });
  const m = await p.evaluate(() => ({ sh: document.scrollingElement.scrollHeight, ih: innerHeight, sw: document.scrollingElement.scrollWidth }));
  console.log(nome, JSON.stringify(m));
  await c.close();
}
const ajusta = (w) => {
  const q = document.querySelector('.bc3-quando');
  if (q) { q.title = 'Dados de 24/11/2026 08:30, horário de Manaus · visão absoluta · variação × mês fechado'; q.textContent = w < 701 ? '24/11 08:30 · 13 de 19 DU' : '24/11/2026 08:30 · nov até 19/11 · 13 de 19 DU'; }
  const h = document.querySelector('.bc3-tt h1');
  if (h && document.querySelector('.rrm')) { const i = document.createElement('span'); i.textContent = ' ⓘ'; i.title = 'Como ler'; i.style.cssText = 'font-size:14px;opacity:.85;cursor:help'; h.appendChild(i); }
  if (w < 701) { document.querySelectorAll('.bc3-k em').forEach(e => e.style.display = 'none'); }
};
await shot('diretor', 1366, 768, '/painel', CSS_PC, 'sugerido-painel-resultado__pc1366', ajusta);
await shot('diretor', 390, 844, '/painel', CSS_CEL, 'sugerido-painel-resultado__cel390', ajusta);
await shot('admin', 1366, 768, '/senha', 'header.bc3-faixa{margin:14px 16px 0 16px!important;border-radius:16px!important}', 'sugerido-senha__pc1366', () => { const a=[...document.querySelectorAll('.bc3-lado a')].find(x=>x.textContent.trim()==='Trocar senha'); if(a){a.setAttribute('aria-current','page');} });
await b.close();
