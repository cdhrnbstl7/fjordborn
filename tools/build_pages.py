# Builds the desktop app's offline game page from game/fjordborn.html (run from the repo root).
import re,os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s=open(os.path.join(root,'game','fjordborn.html'),encoding='utf-8').read()
head=open(os.path.join(root,'game','app_head.txt'),encoding='utf-8').read()
a=s.replace('<title>Fjordborn Desktop</title>','<title>Fjordborn</title>\n<script>window.FJORD_APP=true</script>',1)
a=a.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>','<script src="lib/three.min.js"></script>')
m=re.search(r'<link[^>]*fonts.googleapis.com[^>]*>',a);ff=''
for fam,f,w in [('Grenze Gotisch','grenze-gotisch-latin-500-normal',500),('Grenze Gotisch','grenze-gotisch-latin-700-normal',700),('Alegreya Sans','alegreya-sans-latin-400-normal',400),('Alegreya Sans','alegreya-sans-latin-500-normal',500),('Alegreya Sans','alegreya-sans-latin-700-normal',700)]:
    ff+="@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:swap;src:url(fonts/%s.woff2) format('woff2')}\n"%(fam,w,f)
a=a.replace(m.group(0),'<style>\n'+ff+'</style>')
open(os.path.join(root,'launcher','app','game','index.html'),'w',encoding='utf-8').write(head+a+'\n</html>\n')
print('built launcher/app/game/index.html')
