# Builds phone + desktop artifact pages and the offline app page from src.html (desktop edition source).
import re,sys
s=open('GAME_SRC').read()
assert "const EDITION='desktop'" in s and '<title>Fjordborn Desktop</title>' in s
open('/home/claude/work/out_desktop.html','w').write('<!DOCTYPE html>\n<html lang="en">\n'+s+'</html>\n')
p=s.replace("const EDITION='desktop'","const EDITION='phone'",1).replace('<title>Fjordborn Desktop</title>','<title>Fjordborn</title>',1)
open('/home/claude/work/out_phone.html','w').write('<!DOCTYPE html>\n<html lang="en">\n'+p+'</html>\n')
# offline app page
fav=open('/home/claude/work/app_head.txt').read()
a=s.replace('<title>Fjordborn Desktop</title>','<title>Fjordborn</title>\n<script>window.FJORD_APP=true</script>',1)
a=a.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>','<script src="lib/three.min.js"></script>')
m=re.search(r'<link[^>]*fonts.googleapis.com[^>]*>',a);ff=''
for fam,f,w in [('Grenze Gotisch','grenze-gotisch-latin-500-normal',500),('Grenze Gotisch','grenze-gotisch-latin-700-normal',700),('Alegreya Sans','alegreya-sans-latin-400-normal',400),('Alegreya Sans','alegreya-sans-latin-500-normal',500),('Alegreya Sans','alegreya-sans-latin-700-normal',700)]:
    ff+="@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:swap;src:url(fonts/%s.woff2) format('woff2')}\n"%(fam,w,f)
a=a.replace(m.group(0),'<style>\n'+ff+'</style>')
open('/home/claude/launcher/app/game/index.html','w').write(fav+a+'\n</html>\n')
for v in ['phone','desktop']:
    t=(p if v=='phone' else s).replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>','<script src="lib/three.min.js"></script>')
    t=t.replace(re.search(r'<link[^>]*fonts.googleapis.com[^>]*>',t).group(0),'<style>\n'+ff+'</style>')
    open('/home/claude/launcher/app/game/test_%s.html'%v,'w').write('<!doctype html><html><head><meta charset=utf-8><style>[hidden]:not([hidden=until-found i]){display:none!important}html,body{margin:0;height:100%;background:#000;overflow:hidden}</style>'+t+'</html>')
# extract script for node checks
js=max(re.findall(r'<script>\n([\s\S]*?)</script>',s),key=len)
open('/home/claude/work/game.js','w').write(js)
print('built')
