import json,os,sys
src=open('out_phone.html',encoding='utf-8').read()
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
head='''<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Fjordborn">
<meta name="theme-color" content="#000000">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<style>html,body{background:#000;height:100%;overscroll-behavior:none}</style>
'''
k=src.index('viewport-fit=cover">')+len('viewport-fit=cover">')
open(f'{out}/index.html','w',encoding='utf-8').write(src[:k]+'\n'+head+src[k:])
json.dump({"name":"Fjordborn","short_name":"Fjordborn","start_url":"./","scope":"./","display":"fullscreen","display_override":["fullscreen","standalone"],"orientation":"landscape","background_color":"#000000","theme_color":"#000000",
 "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]},open(f'{out}/manifest.webmanifest','w'),indent=1)
from PIL import Image,ImageDraw
for s in(180,192,512):
  im=Image.new('RGB',(s,s),'#1d2a30');d=ImageDraw.Draw(im);u=s/100
  d.rectangle([0,62*u,s,s],fill='#22404c')
  d.polygon([(8*u,66*u),(38*u,22*u),(56*u,48*u),(68*u,34*u),(94*u,66*u)],fill='#3a4a3e')
  d.polygon([(38*u,22*u),(46*u,34*u),(32*u,32*u)],fill='#d8dcd4')
  d.polygon([(30*u,72*u),(70*u,72*u),(62*u,82*u),(38*u,82*u)],fill='#6b4a2e')
  d.line([(50*u,72*u),(50*u,46*u)],fill='#d8c8a0',width=max(2,int(2*u)))
  d.polygon([(51*u,48*u),(66*u,64*u),(51*u,68*u)],fill='#c96f3a')
  im.save(f'{out}/icon-{s}.png')
open(f'{out}/.nojekyll','w').close()
print('ok',os.path.getsize(f'{out}/index.html'))
