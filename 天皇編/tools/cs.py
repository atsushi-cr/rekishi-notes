import sys, json, urllib.request, urllib.parse, re
sys.stdout.reconfigure(encoding="utf-8")
API="https://commons.wikimedia.org/w/api.php"
def q(params):
    params.update(format="json")
    req=urllib.request.Request(API+"?"+urllib.parse.urlencode(params),headers={"User-Agent":"rekishi-notes/1.0 (personal study)"})
    return json.load(urllib.request.urlopen(req,timeout=30))
for term in sys.argv[1:]:
    r=q(dict(action="query",generator="search",gsrsearch=term+" filetype:bitmap",gsrnamespace=6,gsrlimit=6,prop="imageinfo",iiprop="extmetadata|size",iiextmetadatafilter="LicenseShortName|Artist"))
    print("##",term)
    for p in sorted(r.get("query",{}).get("pages",{}).values(),key=lambda x:x.get("index",0)):
        ii=p["imageinfo"][0]; m=ii.get("extmetadata",{})
        art=re.sub("<[^>]+>","",m.get("Artist",{}).get("value",""))[:40]
        print(" ",p["title"][5:][:70],"|",m.get("LicenseShortName",{}).get("value"),"|",ii["width"],"x",ii["height"],"|",art)
