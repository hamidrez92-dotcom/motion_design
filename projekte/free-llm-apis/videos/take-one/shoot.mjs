// Screenshots der echten Seiten (Material, keine Anweisungen). Usage: node shoot.mjs
import { chromium } from 'playwright-core';
const b = await chromium.launch({ channel: 'chrome', headless: true });
const p = await b.newPage({ viewport: { width: 1100, height: 1400 }, deviceScaleFactor: 2, colorScheme: 'light' });
const R = 'https://github.com/open-free-llm-api/awesome-freellm-apis';
await p.goto(R, { waitUntil: 'networkidle', timeout: 60000 }).catch(e => console.log('goto', e.message));
await p.screenshot({ path: 'assets/shots/repo-top.png' });
const shot = async (sel, file) => { const el = p.locator(sel).first(); if (await el.count()) { await el.scrollIntoViewIfNeeded(); await el.screenshot({ path: file }); console.log('ok', file); } else console.log('missing', sel); };
await shot('article.markdown-body table >> nth=0', 'assets/shots/table-free.png');
await shot('article.markdown-body h3:has-text("Claude Code") + div, article.markdown-body h3:has-text("Claude Code") + pre', 'assets/shots/config-claude.png');
await shot('article.markdown-body h3:has-text("Cursor") + div, article.markdown-body h3:has-text("Cursor") + pre', 'assets/shots/config-cursor.png');
await p.setViewportSize({ width: 1100, height: 900 });
const hdr = p.locator('article.markdown-body').first(); if (await hdr.count()) { await hdr.scrollIntoViewIfNeeded(); await p.screenshot({ path: 'assets/shots/readme-head.png' }); }
await b.close();
