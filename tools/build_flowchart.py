"""Build flowchart.html from the ```mermaid blocks in README.md (keeps both in sync).
Usage:  python tools/build_flowchart.py"""
import re, html, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
md = (root / 'README.md').read_text(encoding='utf-8')
# 每個 mermaid 區塊取前面最近的 ### 標題
blocks = []
for m in re.finditer(r'```mermaid\n(.*?)```', md, re.S):
    heads = re.findall(r'^### (.+)$', md[:m.start()], re.M)
    blocks.append((heads[-1] if heads else 'Diagram', m.group(1).strip()))
sections = '\n'.join(
    f'<section class="card" id="d{i}"><h2>{html.escape(t)}</h2>'
    f'<pre class="mermaid">{html.escape(code)}</pre>'
    f'<details><summary>Mermaid source</summary><pre class="src">{html.escape(code)}</pre></details></section>'
    for i, (t, code) in enumerate(blocks, 1))
toc = ' · '.join(f'<a href="#d{i}">{html.escape(t)}</a>' for i, (t, _) in enumerate(blocks, 1))
page = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Test Summary Tool – Flowcharts</title>
<style>
:root{{color-scheme:light;--page:#f9f9f7;--card:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--border:rgba(11,11,11,.1);--accent:#2a78d6}}
:root[data-theme=dark]{{color-scheme:dark;--page:#0d0d0d;--card:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--border:rgba(255,255,255,.1);--accent:#3987e5}}
body{{margin:0;background:var(--page);color:var(--ink);font:14px/1.5 system-ui,"Segoe UI","Microsoft JhengHei",sans-serif}}
header{{padding:14px 22px;background:var(--card);border-bottom:1px solid var(--border);display:flex;gap:12px;align-items:center;flex-wrap:wrap}}
header h1{{font-size:18px;margin:0;flex:1}} a{{color:var(--accent)}}
main{{max-width:1200px;margin:0 auto;padding:16px 22px 60px}}
.toc{{color:var(--ink2);margin-bottom:14px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 18px;margin-bottom:16px}}
.card h2{{font-size:16px;margin:0 0 10px}}
pre.mermaid{{text-align:center;background:none;margin:0}}
pre.src{{background:var(--page);padding:10px;border-radius:6px;overflow:auto;font-size:12px}}
details summary{{cursor:pointer;color:var(--ink2);margin-top:8px}}
button{{font:inherit;background:var(--page);color:var(--ink);border:1px solid var(--border);border-radius:6px;padding:4px 10px;cursor:pointer}}
#offline{{display:none;background:#fab219;color:#0b0b0b;padding:8px 12px;border-radius:8px;margin-bottom:12px}}
</style></head><body>
<header><h1>Test Summary Yield / Bin Trend / SBL – How it works</h1>
<a href="README.md">README</a> <a href="test_summary_trend.html">Open the tool</a> <button id="theme">◐ Theme</button></header>
<main>
<div id="offline">⚠ Could not load Mermaid (no internet). The diagram source is shown instead — it is the same as in README.md.</div>
<div class="toc">{toc}</div>
{sections}
<p style="color:var(--ink2);font-size:12px">Generated from README.md by tools/build_flowchart.py — edit the README, then re-run the script.</p>
</main>
<script>
const saved=localStorage.getItem('flow.theme'); if(saved) document.documentElement.dataset.theme=saved;
else if(matchMedia('(prefers-color-scheme: dark)').matches) document.documentElement.dataset.theme='dark';
const SRC=[...document.querySelectorAll('pre.mermaid')].map(p=>p.textContent);
async function draw(){{
  if(!window.mermaid){{ document.getElementById('offline').style.display='block'; document.querySelectorAll('pre.mermaid').forEach(p=>p.style.textAlign='left'); return; }}
  const dark=document.documentElement.dataset.theme==='dark';
  mermaid.initialize({{startOnLoad:false,theme:dark?'dark':'default',securityLevel:'strict',flowchart:{{htmlLabels:true,curve:'basis'}},fontFamily:'system-ui,"Microsoft JhengHei",sans-serif'}});
  document.querySelectorAll('pre.mermaid').forEach((p,i)=>{{ p.removeAttribute('data-processed'); p.textContent=SRC[i]; }});
  await mermaid.run({{querySelector:'pre.mermaid'}});
}}
document.getElementById('theme').onclick=()=>{{ const d=document.documentElement; d.dataset.theme=d.dataset.theme==='dark'?'light':'dark'; localStorage.setItem('flow.theme',d.dataset.theme); draw(); }};
</script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js" onload="draw()" onerror="draw()"></script>
</body></html>
'''
(root / 'flowchart.html').write_text(page, encoding='utf-8')
print(f'flowchart.html: {len(blocks)} diagrams')
