#!/usr/bin/env python3
# 扫描目录树，逐级生成 index.html。
# 目录名用 ASCII 短码（URL 干净），中文名写在每个目录的 _name.txt。
import os, re, sys, html

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
SKIP = {".git", ".github", "__pycache__"}

CSS = """
  :root{color-scheme:light dark}
  *{box-sizing:border-box}
  body{margin:0;padding:22px 18px 40px;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif;
    background:#f7f8fa;color:#1d1f24;max-width:820px}
  @media (prefers-color-scheme:dark){body{background:#14161a;color:#e9e9ec}
    a.item{background:#1d2026!important;border-color:#2c3038!important}
    .crumb a{color:#8ab4ff!important}}
  h1{font-size:19px;margin:0 0 3px;font-weight:650}
  .sub{font-size:12.5px;color:#6b7280;margin-bottom:16px}
  .crumb{font-size:12.5px;margin-bottom:14px;line-height:1.8}
  .crumb a{color:#3b5bdb;text-decoration:none}
  .crumb i{color:#c0c4c9;font-style:normal;margin:0 5px}
  a.item{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid #e3e5e9;
    border-radius:12px;padding:12px 14px;margin-bottom:8px;text-decoration:none;color:inherit}
  a.item:active{opacity:.6}
  .ico{font-size:15px;width:20px;text-align:center;flex:none}
  .nm{flex:1;min-width:0;font-size:14.5px;line-height:1.35;word-break:break-word}
  .nm small{display:block;font-size:11.5px;color:#6b7280;margin-top:2px;font-weight:400}
  .n{font-size:11.5px;color:#6b7280;flex:none;font-variant-numeric:tabular-nums}
  .empty{font-size:13px;color:#6b7280;padding:10px 2px}
  .tip{margin-top:20px;font-size:12px;color:#6b7280;line-height:1.7}
"""

def zh(path):
    f = os.path.join(path, "_name.txt")
    if os.path.isfile(f):
        try:
            return open(f, encoding="utf-8").read().strip() or os.path.basename(path)
        except Exception:
            pass
    return os.path.basename(path)

def title_of(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            head = f.read(3000)
        m = re.search(r"<title>(.*?)</title>", head, re.S | re.I)
        if m:
            t = re.sub(r"\s+", " ", m.group(1)).strip().replace("🐴 ", "")
            return t[:80]
    except Exception:
        pass
    return os.path.splitext(os.path.basename(path))[0]

def count_html(path):
    n = 0
    for dp, dns, fns in os.walk(path):
        dns[:] = [d for d in dns if d not in SKIP and not d.startswith(".")]
        n += sum(1 for f in fns if f.lower().endswith((".html", ".htm")) and f != "index.html")
    return n

def crumb_html(path):
    rel = os.path.relpath(path, ROOT)
    if rel == ".":
        return ""
    parts = rel.split(os.sep)
    bits, acc = [], []
    for i, p in enumerate(parts):
        acc.append(p)
        bits.append(f'<a href="{"../" * (len(parts) - i)}">{html.escape(zh(os.path.join(ROOT, *acc)))}</a>')
    head = f'<a href="{"../" * len(parts)}">← 上一级</a><i>·</i>'
    return '<div class="crumb">' + head + "<i>/</i>".join(bits) + "</div>"

def write_index(path):
    name = "几何动态图库" if path == ROOT else zh(path)

    entries = []
    for e in sorted(os.listdir(path)):
        if e in SKIP or e.startswith(".") or e in ("index.html", "_name.txt"):
            continue
        full = os.path.join(path, e)
        if os.path.isdir(full):
            entries.append(("dir", e, count_html(full), full))
        elif e.lower().endswith((".html", ".htm")):
            entries.append(("file", e, None, full))

    rows = []
    for kind, e, n, full in entries:
        if kind == "dir":
            badge = f"{n} 页" if n else "空"
            rows.append(
                f'<a class="item" href="{html.escape(e)}/"><span class="ico">📁</span>'
                f'<span class="nm">{html.escape(zh(full))}</span><span class="n">{badge}</span></a>'
            )
        else:
            rows.append(
                f'<a class="item" href="{html.escape(e)}"><span class="ico">📄</span>'
                f'<span class="nm">{html.escape(title_of(full))}</span></a>'
            )

    body = "\n".join(rows) if rows else '<div class="empty">这个分类下还没有内容。</div>'
    sub = "按考试分类归档；点开即用，可拖动图形。" if path == ROOT else "点题目直接打开"

    doc = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(name)}</title><style>{CSS}</style></head>
<body>
<h1>{html.escape(name)}</h1>
<div class="sub">{html.escape(sub)}</div>
{crumb_html(path)}
{body}
<div class="tip">几何动态图库 · 手机/iPad 上可直接拖动图形</div>
</body></html>"""
    with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
        f.write(doc)

def walk(path):
    for e in sorted(os.listdir(path)):
        full = os.path.join(path, e)
        if os.path.isdir(full) and e not in SKIP and not e.startswith("."):
            walk(full)
    write_index(path)

if __name__ == "__main__":
    walk(ROOT)
    n = sum(1 for dp, dns, fns in os.walk(ROOT) if "index.html" in fns)
    print(f"生成 {n} 个 index.html")
