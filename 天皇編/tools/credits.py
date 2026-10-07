# 使い方: python credits.py （天皇編フォルダで実行）img/meta.json から sources.html の画像クレジット表を作り直す
import sys, json, re, pathlib, html
sys.stdout.reconfigure(encoding="utf-8")
d=pathlib.Path("."); meta=json.loads((d/"img/meta.json").read_text("utf-8"))
pages={f.name:f.read_text("utf-8") for f in sorted(d.glob("era-*.html"))}
def where(k):
    for n,s in pages.items():
        m=re.search(r'id="'+k+r'">\s*<summary><span class="num">(.*?)</span><span class="name">(.*?)(<small>|</span>)',s,re.S)
        if m:
            num=re.sub(r"<[^>]+>","",m.group(1)); name=re.sub(r"<rt>.*?</rt>|<[^>]+>","",m.group(2))
            return n,num+" "+name
    return None,k
def lic(t):
    m=re.match(r"CC (BY(?:-SA)?) (\d\.\d)",t)
    if m: return f'<a href="https://creativecommons.org/licenses/{m.group(1).lower()}/{m.group(2)}/deed.ja">{t}</a>'
    if t=="CC0": return '<a href="https://creativecommons.org/publicdomain/zero/1.0/deed.ja">CC0</a>'
    return html.escape(t)
order=lambda k:(k[0]!="e", int(k[1:]))
rows=[]
for k in sorted(meta,key=order):
    m=meta[k]; n,label=where(k)
    artist=re.split(r"[:：]\s*\d",m["artist"])[0].strip() or "不明"
    rows.append(f'        <tr><td><a href="{n}#{k}">{html.escape(label)}</a></td><td>{html.escape(artist)}</td><td>{lic(m["license"])}</td><td><a href="{html.escape(m["url"])}">{html.escape(m["file"])}</a></td></tr>')
block=("    <!-- credits:start（credits.py で自動生成） -->\n    <div class=\"table-wrap\">\n      <table>\n        <tr><th>使っている欄</th><th>作者</th><th>ライセンス</th><th>元のページ（Wikimedia Commons）</th></tr>\n"
       +"\n".join(rows)+"\n      </table>\n    </div>\n    <!-- credits:end -->")
s=(d/"sources.html").read_text("utf-8")
if "credits:start" in s:
    s=re.sub(r"    <!-- credits:start.*?<!-- credits:end -->",lambda _:block,s,flags=re.S)
else:
    s=re.sub(r'    <p class="note info"><span class="note-title">準備中</span>現在、画像はまだ使っていません。</p>',lambda _:block,s)
(d/"sources.html").write_text(s,"utf-8"); print(len(rows),"rows")
