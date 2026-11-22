# Packs built creatures into one compact blob for the game: int16 positions, int8 normals, rgb, 4 bone indices + weights, uint16 triangles.
import json,struct,sys,zlib,base64,array
names=sys.argv[1:];out=bytearray();meta={}
for nm in names:
    m=json.load(open('/home/claude/beasts/out/%s.json'%nm));b=open('/home/claude/beasts/out/%s.bin'%nm,'rb').read();nv=m['nv'];nt=m['nt']
    o=0;P=array.array('f',b[o:o+nv*12]);o+=nv*12;N=array.array('f',b[o:o+nv*12]);o+=nv*12;C=b[o:o+nv*3];o+=nv*3;SI=b[o:o+nv*4];o+=nv*4;SW=b[o:o+nv*4];o+=nv*4;T=array.array('I',b[o:o+nt*12])
    mn=[min(P[i::3]) for i in range(3)];mx=[max(P[i::3]) for i in range(3)];sc=[(mx[i]-mn[i])/65535 or 1 for i in range(3)]
    start=len(out)
    out+=struct.pack('<%dH'%(nv*3),*[int(round((P[i]-mn[i%3])/sc[i%3])) for i in range(nv*3)])
    out+=struct.pack('<%db'%(nv*3),*[max(-127,min(127,int(round(N[i]*127)))) for i in range(nv*3)])
    out+=C+SI+SW
    if len(out)%2:out+=b'\0'
    T=list(T)
    for i in range(0,len(T),3):T[i+1],T[i+2]=T[i+2],T[i+1]   # the builder wound triangles backwards; put them right
    out+=struct.pack('<%dH'%(nt*3),*T)
    if len(out)%4:out+=b'\0'*(4-len(out)%4)
    meta[nm]={'iface':m.get('iface'),'o':start,'nv':nv,'nt':nt,'mn':mn,'sc':sc,'bones':m['bones']}
z=base64.b64encode(zlib.compress(bytes(out),9)).decode()
json.dump({'meta':meta,'data':z},open('/home/claude/beasts/beasts.json','w'))
print('packed',len(out),'raw',len(z),'b64')
