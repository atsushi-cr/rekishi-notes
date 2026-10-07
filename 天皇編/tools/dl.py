# 使い方: python dl.py 出力先 key=File名 ... → img を WebP 化し、メタ情報を meta.json に追記
import sys, json, re, io, time, pathlib, urllib.request, urllib.parse
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")
UA={"User-Agent":"rekishi-notes/1.0 (personal study site)"}
out=pathlib.Path(sys.argv[1]); out.mkdir(exist_ok=True)
pairs=[a.split("=",1) for a in sys.argv[2:]]
p=dict(action="query",format="json",titles="|".join("File:"+t for _,t in pairs),prop="imageinfo",
       iiprop="url|extmetadata|size",iiurlwidth=520,iiextmetadatafilter="LicenseShortName|Artist|ImageDescription")
r=json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(p),headers=UA),timeout=30))
norm={n["to"]:n["from"] for n in r["query"].get("normalized",[])}
info={}
for pg in r["query"]["pages"].values():
    t=pg["title"]; info[norm.get(t,t)[5:]]=pg
metaf=out/"meta.json"; meta=json.loads(metaf.read_text("utf-8")) if metaf.exists() else {}
for key,title in pairs:
    pg=info.get(title)
    if not pg or "imageinfo" not in pg: print("NG",key,title); continue
    ii=pg["imageinfo"][0]; m=ii["extmetadata"]; cl=lambda k: re.sub(r"<[^>]+>","",m.get(k,{}).get("value","")).strip()
    data=urllib.request.urlopen(urllib.request.Request(ii["thumburl"],headers=UA),timeout=60).read(); time.sleep(2)
    im=Image.open(io.BytesIO(data)).convert("RGB")
    wide=im.width>im.height*1.15
    tw=480 if wide else 240
    if im.width>tw: im=im.resize((tw,round(im.height*tw/im.width)),Image.LANCZOS)
    if not wide and im.height>360: im=im.resize((round(im.width*360/im.height),360),Image.LANCZOS)  # 縦長は切らずに縮小
    f=out/f"{key}.webp"; im.save(f,"WEBP",quality=72,method=6)
    meta[key]=dict(file=title,url=ii["descriptionurl"],license=cl("LicenseShortName"),artist=cl("Artist")[:120],desc=cl("ImageDescription")[:160],w=im.width,h=im.height)
    print(key,f.stat().st_size//1024,"KB",im.size,meta[key]["license"],"|",meta[key]["artist"][:50],"|",meta[key]["desc"][:80])
metaf.write_text(json.dumps(meta,ensure_ascii=False,indent=1),"utf-8")
