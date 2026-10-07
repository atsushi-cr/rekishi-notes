# 使い方: python ins.py era-N.html captions.json  （{key: [alt, caption]}）各天皇欄の body 先頭に図を入れる
import sys, json, re, pathlib, html
sys.stdout.reconfigure(encoding="utf-8")
page=pathlib.Path(sys.argv[1]); meta=json.loads((page.parent/"img/meta.json").read_text("utf-8"))
caps=json.loads(pathlib.Path(sys.argv[2]).read_text("utf-8"))
s=page.read_text("utf-8")
for k,(alt,cap) in caps.items():
    m=meta[k]; cls="pf wide" if m["w"]>m["h"] else "pf"
    fig=f'<figure class="{cls}"><img src="img/{k}.webp" alt="{html.escape(alt)}" width="{m["w"]}" height="{m["h"]}" loading="lazy" decoding="async"><figcaption>{cap}</figcaption></figure>'
    pat=re.compile(r'(<details class="emp[^"]*" id="'+k+r'">.*?<div class="body">)(?!<figure)(\n\s*)?',re.S)
    s,n=pat.subn(lambda mo: mo.group(1)+(mo.group(2) or "")+fig+(mo.group(2) or ""),s,count=1)
    print(k,"ok" if n else "NOT FOUND")
page.write_text(s,"utf-8")
