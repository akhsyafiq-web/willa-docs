#!/usr/bin/env python3
"""
Build index.html — satu file HTML statis untuk melihat seluruh isi repo
dokumentasi ini di browser (sidebar dari SUMMARY.md + konten tiap halaman).
Dinamai index.html supaya bisa langsung di-deploy sebagai static site
(mis. Vercel) tanpa konfigurasi tambahan.

Jalankan ulang setiap kali ada halaman .md yang berubah/ditambahkan:

    python3 scripts/build-docs-viewer.py

Catatan:
- Ini BUKAN bagian dari struktur GitBook (tidak didaftarkan di SUMMARY.md),
  murni alat bantu preview lokal / output untuk static hosting.
- Path gambar dibiarkan relatif terhadap root repo, jadi index.html
  harus tetap berada di root repo (sejajar dengan SUMMARY.md) supaya
  assets/*.png tetap tampil.
- Parser markdown di sini scoped untuk subset sintaks yang dipakai di
  style-guide.md (heading, list, table, blockquote/callout, <small>,
  <details>, gambar, link). Bukan parser CommonMark umum.
"""
import os, re, html, json

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "index.html")

# ---------- markdown helpers ----------

def slug(path_no_ext):
    return path_no_ext.replace("/", "--")

def norm_join(base_dir, rel):
    p = os.path.normpath(os.path.join(base_dir, rel))
    return p.replace(os.sep, "/")

def esc(s):
    return html.escape(s, quote=False)

INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
ITALIC_RE = re.compile(r"(?<!_)_([^_]+)_(?!_)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

def inline(text, base_dir):
    codes = []
    def code_sub(m):
        codes.append(esc(m.group(1)))
        return f"\x00CODE{len(codes)-1}\x00"
    text = INLINE_CODE_RE.sub(code_sub, text)
    text = esc(text)

    def link_sub(m):
        label, target = m.group(1), m.group(2)
        label_r = BOLD_RE.sub(r"<strong>\1</strong>", label)
        if target.startswith("http://") or target.startswith("https://"):
            return f'<a href="{target}" class="ext-link" target="_blank" rel="noopener">{label_r}</a>'
        tgt, anchor = (target.split("#", 1) + [""])[:2] if "#" in target else (target, "")
        page_id = slug(norm_join(base_dir, tgt).rsplit(".md", 1)[0]) if tgt else ""
        return f'<a href="javascript:void(0)" class="int-link" data-page="{page_id}">{label_r}</a>'

    text = LINK_RE.sub(link_sub, text)
    text = BOLD_RE.sub(r"<strong>\1</strong>", text)
    text = ITALIC_RE.sub(r"<em>\1</em>", text)
    for idx, c in enumerate(codes):
        text = text.replace(f"\x00CODE{idx}\x00", f"<code>{c}</code>")
    return text

def slugify_heading(text):
    s = re.sub(r"[^a-z0-9\s-]", "", text.lower())
    return re.sub(r"\s+", "-", s.strip())

CALLOUT_MAP = [("🚧", "draft"), ("ℹ️", "info"), ("⚠️", "warning"), ("✅", "do"), ("❌", "dont")]

def callout_class(content):
    for emoji, cls in CALLOUT_MAP:
        if content.startswith(emoji):
            return cls
    return "note"

def render_table(lines, base_dir):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    header, _sep, *body = rows
    out = ['<div class="table-wrap"><table><thead><tr>']
    out += [f"<th>{inline(c, base_dir)}</th>" for c in header]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{inline(c, base_dir)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)

def render_details(block_lines, base_dir):
    text = "\n".join(block_lines)
    m = re.search(r"<summary>(.*?)</summary>", text, re.S)
    summary = m.group(1).strip() if m else ""
    inner = re.sub(r"<details>|</details>|<summary>.*?</summary>", "", text, flags=re.S).strip()
    parts = []
    for para in re.split(r"\n\s*\n", inner):
        para = para.strip()
        if para:
            parts.append(f"<p>{inline(' '.join(l.strip() for l in para.splitlines()), base_dir)}</p>")
    return (f'<details class="faq"><summary>{inline(summary, base_dir)}</summary>'
            f'<div class="faq-body">{"".join(parts)}</div></details>')

def render_body(body, base_dir):
    lines = body.split("\n")
    i, n = 0, len(lines)
    out, seen_h1 = [], False
    while i < n:
        stripped = lines[i].strip()
        if stripped == "":
            i += 1; continue
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            if level == 1 and not seen_h1:
                seen_h1 = True; i += 1; continue
            out.append(f'<h{level} id="{slugify_heading(text)}">{inline(text, base_dir)}</h{level}>')
            i += 1; continue
        if stripped.startswith(">"):
            bq = []
            while i < n and lines[i].strip().startswith(">"):
                seg = lines[i].strip()[1:].strip()
                if seg: bq.append(seg)
                i += 1
            cls = callout_class(" ".join(bq))
            out.append(f'<blockquote class="callout callout-{cls}">{inline(" ".join(bq), base_dir)}</blockquote>')
            continue
        if stripped.startswith("<details>"):
            block = []
            while i < n and "</details>" not in lines[i]:
                block.append(lines[i]); i += 1
            if i < n: block.append(lines[i]); i += 1
            out.append(render_details(block, base_dir)); continue
        if stripped.startswith("<!--"):
            # HTML comment (mis. hint embed gambar) — teruskan apa adanya,
            # tidak di-escape, sehingga tetap invisible di halaman ter-render.
            block = [lines[i]]
            while i < n and "-->" not in block[-1]:
                i += 1
                if i < n: block.append(lines[i])
            i += 1
            out.append("\n".join(block)); continue
        if stripped.startswith("<small>"):
            inner = re.sub(r"</?small>", "", stripped).strip()
            out.append(f'<p class="text-small">{inline(inner, base_dir)}</p>'); i += 1; continue
        if stripped.startswith("!["):
            m = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
            if m:
                alt, src = m.group(1), m.group(2)
                out.append(f'<figure class="doc-image"><img src="{norm_join(base_dir, src)}" alt="{esc(alt)}" loading="lazy"></figure>')
            i += 1; continue
        if stripped.startswith("|"):
            tbl = []
            while i < n and lines[i].strip().startswith("|"):
                tbl.append(lines[i]); i += 1
            out.append(render_table(tbl, base_dir)); continue
        if re.match(r"^\d+\.\s", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s", "", lines[i].strip())); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(it, base_dir)}</li>" for it in items) + "</ol>"); continue
        if stripped.startswith("- "):
            items = []
            while i < n and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:]); i += 1
            out.append("<ul>" + "".join(f"<li>{inline(it, base_dir)}</li>" for it in items) + "</ul>"); continue
        if stripped == "---":
            out.append("<hr>"); i += 1; continue
        para = []
        stop = ("#", ">", "<details", "<small", "![", "|", "- ")
        while i < n and lines[i].strip() != "" and not lines[i].strip().startswith(stop) and not re.match(r"^\d+\.\s", lines[i].strip()):
            para.append(lines[i].strip()); i += 1
        out.append(f"<p>{inline(' '.join(para), base_dir)}</p>")
    return "\n".join(out)

def parse_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m: return {}, text
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.split("\n"):
        if ":" not in line: continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if key == "roles":
            inner = val.strip("[]").strip()
            fm[key] = [r.strip() for r in inner.split(",") if r.strip()]
        else:
            fm[key] = val.strip('"')
    return fm, body

# ---------- parse SUMMARY.md ----------

summary_text = open(os.path.join(ROOT, "SUMMARY.md"), encoding="utf-8").read()
nav_groups = [{"title": None, "items": []}]
for raw in summary_text.split("\n"):
    if raw.startswith("## "):
        nav_groups.append({"title": raw[3:].strip(), "items": []}); continue
    m = re.match(r"^(\s*)\*\s+\[(.+?)\]\((.+?)\)\s*$", raw)
    if m:
        indent, label, path = m.groups()
        nav_groups[-1]["items"].append({"depth": len(indent) // 2, "label": label, "path": path})
nav_groups = [g for g in nav_groups if g["items"]]
flat_pages = [it["path"] for g in nav_groups for it in g["items"]]

# ---------- render pages ----------

pages_html, page_meta = [], {}
for g in nav_groups:
    for it in g["items"]:
        rel_path = it["path"]
        base_dir = os.path.dirname(rel_path)
        page_id = slug(rel_path.rsplit(".md", 1)[0])
        raw = open(os.path.join(ROOT, rel_path), encoding="utf-8").read()
        fm, body = parse_front_matter(raw)
        title = fm.get("title", it["label"])
        description = fm.get("description", "")
        roles = fm.get("roles", [])
        status = fm.get("status", "draft")
        last_updated = fm.get("last_updated", "")
        body_html = render_body(body, base_dir)
        page_meta[page_id] = {"title": title, "path": rel_path, "group": g["title"]}
        role_badges = "".join(f'<span class="badge badge-role">{esc(r)}</span>' for r in roles) or \
            '<span class="badge badge-role badge-muted">semua peran belum ditentukan</span>'
        status_badge = f'<span class="badge badge-status status-{status}">{esc(status)}</span>'
        crumbs = ["Dokumentasi"]
        if g["title"]: crumbs.append(g["title"])
        if it["depth"] > 0:
            idx = g["items"].index(it)
            anc, depth_needed = [], it["depth"] - 1
            for j in range(idx - 1, -1, -1):
                if g["items"][j]["depth"] == depth_needed:
                    anc.append(g["items"][j]["label"]); depth_needed -= 1
                if depth_needed < 0: break
            crumbs.extend(reversed(anc))
        deduped = []
        for c in crumbs:
            if not deduped or deduped[-1] != c: deduped.append(c)
        breadcrumb_html = " <span class=\"crumb-sep\">/</span> ".join(esc(c) for c in deduped)

        pages_html.append(f'''
<section class="page" id="page-{page_id}" data-title="{esc(title)}" hidden>
  <nav class="breadcrumb">{breadcrumb_html}</nav>
  <header class="page-header">
    <h1>{esc(title)}</h1>
    <p class="page-description">{esc(description)}</p>
    <div class="badges">{status_badge}{role_badges}</div>
  </header>
  <div class="page-body">
{body_html}
  </div>
  <footer class="page-footer">
    <span class="last-updated">Terakhir diperbarui: {esc(last_updated)}</span>
  </footer>
</section>''')

# ---------- sidebar ----------

def build_group_tree(items):
    root, stack = [], [(-1, None)]
    stack = [(-1, root)]
    for it in items:
        node = {"label": it["label"], "path": it["path"], "children": []}
        while stack and stack[-1][0] >= it["depth"]:
            stack.pop()
        stack[-1][1].append(node)
        stack.append((it["depth"], node["children"]))
    return root

def render_nav_tree(nodes):
    out = ['<ul class="nav-list">']
    for node in nodes:
        page_id = slug(node["path"].rsplit(".md", 1)[0])
        has_children = bool(node["children"])
        out.append(f'<li class="{"has-children" if has_children else ""}">')
        out.append(f'<a href="javascript:void(0)" class="nav-link" data-page="{page_id}">{esc(node["label"])}</a>')
        if has_children:
            out.append(render_nav_tree(node["children"]))
        out.append("</li>")
    out.append("</ul>")
    return "".join(out)

sidebar_parts = []
for g in nav_groups:
    tree = build_group_tree(g["items"])
    if g["title"]:
        sidebar_parts.append(f'<div class="nav-group"><div class="nav-group-title">{esc(g["title"])}</div>{render_nav_tree(tree)}</div>')
    else:
        sidebar_parts.append(f'<div class="nav-group nav-group-top">{render_nav_tree(tree)}</div>')
sidebar_html = "\n".join(sidebar_parts)

first_page_id = slug(flat_pages[0].rsplit(".md", 1)[0])
order_json = json.dumps([slug(p.rsplit(".md", 1)[0]) for p in flat_pages])
meta_json = json.dumps(page_meta, ensure_ascii=False)
pages_joined = "\n".join(pages_html)

# ---------- HTML shell ----------

TEMPLATE = r"""<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dokumentasi Willa PMS</title>
<link rel="icon" type="image/png" href="assets/favicon.png">
<style>
:root{
  --primary:#821CDD;
  --primary-dark:#6c17b8;
  --primary-light:#f4e9fc;
  --primary-line:#e3c6f7;
  --bg:#ffffff;
  --bg-sidebar:#fafafa;
  --text:#1f1f23;
  --text-muted:#6b6b76;
  --text-faint:#9a9aa5;
  --border:#e5e5e5;
  --code-bg:#f3f1f6;
  --status-published:#0f9d58;
  --status-published-bg:#e6f6ec;
  --status-draft:#b7791f;
  --status-draft-bg:#fdf3e0;
  --radius:8px;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
  color:var(--text);
  background:var(--bg);
  font-size:15px;
  line-height:1.65;
}
a{color:var(--primary);text-decoration:none}
a:hover{text-decoration:underline}
img{max-width:100%}

#app{display:flex;min-height:100vh}

#sidebar{
  width:280px;flex:none;
  background:var(--bg-sidebar);
  border-right:1px solid var(--border);
  height:100vh;position:sticky;top:0;
  display:flex;flex-direction:column;
  overflow:hidden;
  transition:transform .2s ease;
  z-index:20;
}
.sidebar-header{padding:18px 18px 12px;border-bottom:1px solid var(--border)}
.brand{display:flex;align-items:center;gap:8px;font-weight:700;font-size:15px;color:var(--text);margin-bottom:12px}
.brand-mark{
  width:26px;height:26px;border-radius:7px;
  display:block;object-fit:cover;
  flex:none;
}
.search-box{position:relative}
.search-box input{
  width:100%;padding:8px 10px 8px 30px;border:1px solid var(--border);border-radius:7px;
  font-size:13px;background:#fff;color:var(--text);
}
.search-box input:focus{outline:2px solid var(--primary-line);border-color:var(--primary)}
.search-box svg{position:absolute;left:9px;top:50%;transform:translateY(-50%);color:var(--text-faint)}

.sidebar-nav{flex:1;overflow-y:auto;padding:14px 10px 24px}
.nav-group{margin-bottom:18px}
.nav-group-top{margin-bottom:6px}
.nav-group-title{
  font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  color:var(--text-faint);padding:0 10px;margin-bottom:6px;
}
ul.nav-list{list-style:none;margin:0;padding:0}
ul.nav-list ul.nav-list{margin-left:14px;border-left:1px solid var(--border);padding-left:6px}
.nav-link{
  display:block;padding:6px 10px;border-radius:6px;font-size:13.5px;
  color:var(--text);border-left:2px solid transparent;
}
.nav-link:hover{background:var(--primary-light);text-decoration:none}
.nav-link.active{
  background:var(--primary-light);color:var(--primary-dark);font-weight:600;
  border-left-color:var(--primary);
}
li.nav-hidden{display:none}

#sidebar-toggle{
  display:none;position:fixed;top:14px;left:14px;z-index:30;
  background:var(--primary);color:#fff;border:none;border-radius:7px;
  width:38px;height:38px;align-items:center;justify-content:center;cursor:pointer;
  box-shadow:0 2px 8px rgba(0,0,0,.18);
}
#sidebar-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:15}

#content-wrap{flex:1;min-width:0;display:flex;justify-content:center}
main#content{flex:1;max-width:820px;padding:36px 40px 80px;min-width:0}
#toc{width:220px;flex:none;padding:36px 20px;position:sticky;top:0;height:100vh;overflow-y:auto}
#toc .toc-title{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--text-faint);margin-bottom:10px}
#toc ul{list-style:none;margin:0;padding:0;border-left:2px solid var(--border)}
#toc li{margin:0}
#toc a{display:block;padding:5px 0 5px 12px;font-size:13px;color:var(--text-muted);border-left:2px solid transparent;margin-left:-2px}
#toc a.active{color:var(--primary);border-left-color:var(--primary);font-weight:600}
#toc a.toc-h3{padding-left:24px;font-size:12.5px}

.breadcrumb{font-size:13px;color:var(--text-muted);margin-bottom:14px}
.crumb-sep{color:var(--text-faint);margin:0 2px}

.page-header h1{font-size:32px;margin:0 0 8px;letter-spacing:-.01em}
.page-description{color:var(--text-muted);font-size:15.5px;margin:0 0 14px}
.badges{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}
.badge{display:inline-block;padding:3px 9px;border-radius:999px;font-size:11.5px;font-weight:600;border:1px solid transparent}
.badge-status.status-published{background:var(--status-published-bg);color:var(--status-published)}
.badge-status.status-draft{background:var(--status-draft-bg);color:var(--status-draft)}
.badge-role{background:var(--primary-light);color:var(--primary-dark)}
.badge-muted{background:#f2f2f4;color:var(--text-faint)}

.page-body{margin-top:26px}
.page-body h1{font-size:26px;margin:32px 0 12px}
.page-body h2{font-size:21px;margin:34px 0 12px;padding-top:6px;border-top:1px solid var(--border)}
.page-body h2:first-child{border-top:none;padding-top:0;margin-top:0}
.page-body h3{font-size:17px;margin:24px 0 10px}
.page-body h4{font-size:15px;margin:20px 0 8px}
.page-body p{margin:0 0 14px}
.page-body p.text-small{color:var(--text-muted);font-size:13px}
.page-body ul,.page-body ol{margin:0 0 14px;padding-left:22px}
.page-body li{margin:4px 0}
.page-body code{background:var(--code-bg);border-radius:4px;padding:2px 6px;font-size:.88em;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.page-body strong{font-weight:650}
.page-body hr{border:none;border-top:1px solid var(--border);margin:28px 0}

.page-body blockquote.callout{margin:0 0 16px;padding:12px 14px;border-left:3px solid var(--border);border-radius:0 var(--radius) var(--radius) 0;background:#fafafa;font-size:14px}
.callout-info{border-left-color:#3b82f6;background:#eff6ff}
.callout-warning{border-left-color:#f59e0b;background:#fffbeb}
.callout-do{border-left-color:#16a34a;background:#f0fdf4}
.callout-dont{border-left-color:#dc2626;background:#fef2f2}
.callout-draft{border-left-color:var(--primary);background:var(--primary-light)}

.doc-image{margin:0 0 20px;text-align:center}
.doc-image img{border:1px solid var(--border);border-radius:var(--radius);max-width:100%}

.table-wrap{overflow-x:auto;margin:0 0 18px}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{border:1px solid var(--border);padding:8px 10px;text-align:left}
th{background:#faf7fc;font-weight:650}

details.faq{border:1px solid var(--border);border-radius:var(--radius);padding:10px 14px;margin:0 0 10px;background:#fff}
details.faq summary{cursor:pointer;font-weight:600;font-size:14px;list-style:revert}
details.faq .faq-body{margin-top:8px;color:var(--text-muted);font-size:13.8px}
details.faq .faq-body p:last-child{margin-bottom:0}

.page-footer{margin-top:40px;padding-top:14px;border-top:1px solid var(--border);font-size:12.5px;color:var(--text-faint)}

.pagerow{display:flex;justify-content:space-between;gap:14px;margin-top:26px}
.pager-link{flex:1;border:1px solid var(--border);border-radius:var(--radius);padding:10px 14px;font-size:13px;color:var(--text-muted)}
.pager-link .pager-dir{display:block;font-size:11px;color:var(--text-faint);margin-bottom:2px}
.pager-link.next{text-align:right}
.pager-link:hover{border-color:var(--primary);background:var(--primary-light)}

@media (max-width:1100px){#toc{display:none}}
@media (max-width:820px){
  #sidebar{position:fixed;left:0;top:0;transform:translateX(-100%);width:82vw;max-width:300px}
  #sidebar.open{transform:translateX(0)}
  #sidebar-toggle{display:flex}
  #sidebar-overlay.open{display:block}
  main#content{padding:70px 20px 60px}
  .page-header h1{font-size:26px}
}
</style>
</head>
<body>
<div id="app">
  <button id="sidebar-toggle" aria-label="Buka menu">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
  </button>
  <div id="sidebar-overlay"></div>

  <aside id="sidebar">
    <div class="sidebar-header">
      <div class="brand"><img class="brand-mark" src="assets/brand-icon.png" alt="Logo Willa PMS"> Dokumentasi Willa PMS</div>
      <div class="search-box">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input id="nav-search" type="text" placeholder="Cari halaman...">
      </div>
    </div>
    <nav class="sidebar-nav" id="sidebar-nav">
__SIDEBAR__
    </nav>
  </aside>

  <div id="content-wrap">
    <main id="content">
      <div id="pages">
__PAGES__
      </div>
      <div class="pagerow" id="pagerow"></div>
    </main>
    <aside id="toc">
      <div class="toc-title">Di halaman ini</div>
      <ul id="toc-list"></ul>
    </aside>
  </div>
</div>

<script>
const PAGE_ORDER = __ORDER_JSON__;
const PAGE_META = __META_JSON__;
const FIRST_PAGE = "__FIRST__";

function $all(sel, ctx){ return Array.from((ctx||document).querySelectorAll(sel)); }

function showPage(id, opts){
  opts = opts || {};
  if(!PAGE_META[id]) id = FIRST_PAGE;
  $all('.page').forEach(function(p){ p.hidden = true; });
  const target = document.getElementById('page-' + id);
  if(target) target.hidden = false;

  $all('.nav-link').forEach(function(a){ a.classList.toggle('active', a.dataset.page === id); });
  const activeLink = $all('.nav-link').find(function(a){ return a.dataset.page === id; });
  if(activeLink){
    let li = activeLink.closest('li');
    while(li){
      li.classList.add('nav-open');
      li = li.parentElement ? li.parentElement.closest('li') : null;
    }
  }

  buildTOC(target);
  buildPager(id);
  if(!opts.silent){
    document.getElementById('content').scrollTop = 0;
    window.scrollTo(0,0);
  }
  history.replaceState(null, '', '#' + id);
  document.title = (PAGE_META[id] ? PAGE_META[id].title : 'Dokumentasi') + ' · Willa PMS';
  closeSidebarMobile();
}

function buildTOC(section){
  const list = document.getElementById('toc-list');
  list.innerHTML = '';
  if(!section) return;
  const heads = $all('.page-body h2, .page-body h3', section);
  heads.forEach(function(h){
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = 'javascript:void(0)';
    a.textContent = h.textContent;
    a.className = h.tagName === 'H3' ? 'toc-h3' : '';
    a.addEventListener('click', function(){ h.scrollIntoView({behavior:'smooth', block:'start'}); });
    li.appendChild(a);
    list.appendChild(li);
  });
}

function buildPager(id){
  const idx = PAGE_ORDER.indexOf(id);
  const row = document.getElementById('pagerow');
  row.innerHTML = '';
  if(idx > 0){
    const prevId = PAGE_ORDER[idx-1];
    const a = document.createElement('a');
    a.href = 'javascript:void(0)'; a.className = 'pager-link prev'; a.dataset.page = prevId;
    a.innerHTML = '<span class="pager-dir">← Sebelumnya</span>' + (PAGE_META[prevId] ? PAGE_META[prevId].title : '');
    row.appendChild(a);
  } else { row.appendChild(document.createElement('span')); }
  if(idx >= 0 && idx < PAGE_ORDER.length - 1){
    const nextId = PAGE_ORDER[idx+1];
    const a = document.createElement('a');
    a.href = 'javascript:void(0)'; a.className = 'pager-link next'; a.dataset.page = nextId;
    a.innerHTML = '<span class="pager-dir">Selanjutnya →</span>' + (PAGE_META[nextId] ? PAGE_META[nextId].title : '');
    row.appendChild(a);
  }
}

document.addEventListener('click', function(e){
  const link = e.target.closest('[data-page]');
  if(link){ e.preventDefault(); showPage(link.dataset.page); }
});

document.getElementById('nav-search').addEventListener('input', function(e){
  const q = e.target.value.trim().toLowerCase();
  $all('#sidebar-nav li').forEach(function(li){
    const link = li.querySelector(':scope > .nav-link');
    if(!link) return;
    const text = link.textContent.toLowerCase();
    const childMatch = q && $all('.nav-link', li).some(function(a){ return a.textContent.toLowerCase().includes(q); });
    const match = !q || text.includes(q) || childMatch;
    li.classList.toggle('nav-hidden', !match);
  });
});

const toggleBtn = document.getElementById('sidebar-toggle');
const overlay = document.getElementById('sidebar-overlay');
const sidebar = document.getElementById('sidebar');
function closeSidebarMobile(){ sidebar.classList.remove('open'); overlay.classList.remove('open'); }
toggleBtn.addEventListener('click', function(){ sidebar.classList.toggle('open'); overlay.classList.toggle('open'); });
overlay.addEventListener('click', closeSidebarMobile);

window.addEventListener('hashchange', function(){
  const id = location.hash.replace('#','');
  showPage(id || FIRST_PAGE);
});

const initial = location.hash.replace('#','') || FIRST_PAGE;
showPage(initial, {silent:true});
</script>
</body>
</html>
"""

out = (TEMPLATE
       .replace("__SIDEBAR__", sidebar_html)
       .replace("__PAGES__", pages_joined)
       .replace("__ORDER_JSON__", order_json)
       .replace("__META_JSON__", meta_json)
       .replace("__FIRST__", first_page_id))

with open(OUT, "w", encoding="utf-8") as f:
    f.write(out)

print(f"OK: {len(pages_html)} halaman -> {OUT} ({os.path.getsize(OUT)} bytes)")
