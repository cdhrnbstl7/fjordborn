import math
def nz(x,y,z):  # cheap smooth-ish value noise
    s=math.sin(x*12.9898+y*78.233+z*37.719)*43758.5453;return s-math.floor(s)
def fbm(x,y,z):
    return (math.sin(x*7.1+math.sin(z*5.3))*.5+math.sin(y*9.7+x*3.1)*.3+math.sin(z*13.3+y*4.7)*.2)*.5+.5
def lerp(a,b,t):return a+(b-a)*t
def mix(c1,c2,t):t=max(0,min(1,t));return tuple(lerp(a,b,t) for a,b in zip(c1,c2))
def sm(e0,e1,x):t=max(0,min(1,(x-e0)/(e1-e0)));return t*t*(3-2*t)
def chain(nodes,parent,pts,prefix,bones=()):
    """pts: list of (pos,(rx,ry)); appended as prefix0..n; bones: indices that are bones"""
    prev=parent
    for i,(p,r) in enumerate(pts):
        nm='%s%d'%(prefix,i);nodes.append((nm,prev,p,r,i in bones));prev=nm
    return prev
def mirror(nodes,make):
    for sd,tag in ((1,'L'),(-1,'R')):make(sd,tag)

# ---------------- RED STAG ----------------
def stag_nodes(antlers=True,scale=1.0,doe=False):
    N=[];S=lambda p:(p[0]*scale,p[1]*scale,p[2]*scale)
    N.append(('root',None,S((0,1.1,-.5)),(.24,.29),True))
    N.append(('tail0','root',S((0,1.13,-.78)),(.07,.07),True));N.append(('tail1','tail0',S((0,1.0,-.86)),(.055,.07),False))
    N.append(('rump','root',S((0,1.14,-.66)),(.22,.25),False))
    N.append(('back','root',S((0,1.12,-.1)),(.27,.34),True))
    N.append(('belly','back',S((0,1.03,.12)),(.27,.36),False))
    N.append(('chest','back',S((0,1.16,.36)),(.25,.37),True))
    N.append(('brisket','chest',S((0,.96,.5)),(.15,.18),False))
    N.append(('neck','chest',S((0,1.4,.6)),(.17 if not doe else .13,.25 if not doe else .19),True))
    N.append(('neck2','neck',S((0,1.68,.74)),(.12 if not doe else .09,.15 if not doe else .11),False))
    N.append(('head','neck2',S((0,1.9,.84)),(.11,.12),True))
    N.append(('face','head',S((0,1.85,1.02)),(.085,.09),False))
    N.append(('muzzle','face',S((0,1.78,1.17)),(.06,.068),False))
    N.append(('nose','muzzle',S((0,1.75,1.23)),(.046,.05),False))
    def ears(sd,t):
        N.append(('ear'+t,'head',S((sd*.09,1.99,.8)),(.055,.03),False));N.append(('earm'+t,'ear'+t,S((sd*.2,2.06,.76)),(.085,.018),False));N.append(('eartip'+t,'earm'+t,S((sd*.3,2.1,.72)),(.035,.01),False))
    mirror(N,ears)
    def legs(sd,t):
        N.append(('fl'+t,'chest',S((sd*.15,1.05,.42)),(.12,.15),True))
        N.append(('fe'+t,'fl'+t,S((sd*.15,.78,.44)),(.07,.08),True))
        N.append(('fk'+t,'fe'+t,S((sd*.15,.46,.43)),(.042,.047),False))
        N.append(('ff'+t,'fk'+t,S((sd*.15,.14,.45)),(.032,.034),False))
        N.append(('fh'+t,'ff'+t,S((sd*.15,.03,.49)),(.042,.035),False))
        N.append(('hl'+t,'root',S((sd*.15,.98,-.55)),(.16,.24),True))
        N.append(('hs'+t,'hl'+t,S((sd*.15,.7,-.42)),(.09,.12),True))
        N.append(('hh'+t,'hs'+t,S((sd*.15,.48,-.7)),(.045,.05),False))
        N.append(('hf'+t,'hh'+t,S((sd*.15,.14,-.64)),(.032,.034),False))
        N.append(('hp'+t,'hf'+t,S((sd*.15,.03,-.6)),(.042,.035),False))
    mirror(N,legs)
    if antlers:
        def ant(sd,t):
            r=.032
            N.append(('a0'+t,'head',S((sd*.07,2.0,.8)),(r*1.25,r*1.25),False))
            N.append(('a1'+t,'a0'+t,S((sd*.2,2.2,.72)),(r,r),False))
            N.append(('brow'+t,'a1'+t,S((sd*.24,2.2,1.02)),(r*.55,r*.55),False))
            N.append(('a2'+t,'a1'+t,S((sd*.36,2.42,.6)),(r*.92,r*.92),False))
            N.append(('trez'+t,'a2'+t,S((sd*.4,2.42,.88)),(r*.5,r*.5),False))
            N.append(('a3'+t,'a2'+t,S((sd*.5,2.62,.44)),(r*.82,r*.82),False))
            N.append(('a4'+t,'a3'+t,S((sd*.56,2.8,.32)),(r*.65,r*.65),False))
            N.append(('c1'+t,'a3'+t,S((sd*.66,2.72,.62)),(r*.45,r*.45),False))
            N.append(('c2'+t,'a4'+t,S((sd*.52,2.98,.38)),(r*.42,r*.42),False))
            N.append(('c3'+t,'a4'+t,S((sd*.7,2.95,.2)),(r*.42,r*.42),False))
            N.append(('c4'+t,'a4'+t,S((sd*.62,3.02,.1)),(r*.38,r*.38),False))
        mirror(N,ant)
    return N
def stag_color(g,n):
    x,y,z=g;base=(.36,.25,.16);c=base
    c=mix(c,(.27,.19,.13),sm(1.25,1.0,y)*sm(.3,.0,abs(x))*0)  
    c=mix(c,(.62,.52,.38),sm(.95,.82,y)*sm(-.05,-.5,n[1])*sm(.5,.2,abs(z-0)))   # pale belly
    c=mix(c,(.22,.16,.11),sm(.8,.35,y))                                       # dark lower legs
    c=mix(c,(.78,.66,.46),sm(-.45,-.62,z)*sm(.85,1.15,y)*sm(.15,.05,abs(x)))  # rump patch
    c=mix(c,(.3,.22,.15),sm(1.35,1.6,y)*sm(.35,.55,z)*sm(1.9,1.7,y))         # darker shaggy neck
    c=mix(c,(.2,.15,.1),sm(.95,1.08,z))                                       # muzzle
    c=mix(c,(.05,.05,.05),sm(1.1,1.14,z))                                     # nose
    c=mix(c,(.7,.6,.45),sm(.05,.25,abs(x))*sm(1.95,2.06,y)*sm(.85,.7,z)*sm(2.2,2.05,y)*0)
    if y>1.99 and (abs(x)>.05 or y>2.1) and not (abs(x)>.12 and y<2.14 and z>.7):
        t=sm(2.0,3.1,y);c=mix((.42,.33,.22),(.86,.8,.68),t)                   # antlers: dark at base, pale tips
    if y<.08:c=(.12,.1,.09)                                                   # hooves
    v=fbm(x*3,y*3,z*3)*.12-.06;return tuple(max(0,min(1,k*(1+v))) for k in c)
def stag_shape(g,n):
    x,y,z=g
    # shaggy mane: fur tufts under the neck
    if 1.25<y<1.75 and .4<z<.8 and n[1]<.2:
        k=sm(1.25,1.4,y)*sm(1.78,1.55,y)*.05*(.6+.8*nz(x*40,y*40,z*40));return (x+n[0]*k,y+n[1]*k,z+n[2]*k)
    return None
SPECS={}
SPECS['stag']={'name':'stag','nodes':stag_nodes(True),'color':stag_color,'shape':stag_shape,'view':3.2,'subdiv':2,'tris':7000}

# ================= sculpted-mass creatures =================
def cap(pts,rs,sub=2):return {'c':pts,'r':rs,'sub':sub}
def ell(c,r,rot=None):return {'e':c,'r':r,'rot':rot}
def sym(fn):return [fn(1),fn(-1)]
def quad_bones(J):
    """J: dict of joint positions: root, back, chest, neck, head, nose, tail, tailtip, earL..., per leg: fl,fe,fk,fh / hl,hs,hh,hp (L/R)"""
    B=[('root',None,J['root'],J['back']),('spine','root',J['back'],J['chest']),('chest','spine',J['chest'],J['neck']),('neck','chest',J['neck'],J['head']),('head','neck',J['head'],J['nose']),
       ('tail','root',J['tail'],J['tailtip'])]
    for t in 'LR':
        if 'ear'+t in J:B.append(('ear'+t,'head',J['ear'+t],J['eartip'+t]))
        B+=[('fl'+t,'chest',J['fl'+t],J['fe'+t]),('fe'+t,'fl'+t,J['fe'+t],J['fh'+t]),('hl'+t,'root',J['hl'+t],J['hs'+t]),('hs'+t,'hl'+t,J['hs'+t],J['hp'+t])]
    return B

def mcap(a,b,r):return {'mc':[a,b],'r':r}
def deer(doe=False,s=1.0):
    S=lambda p:(p[0]*s,p[1]*s,p[2]*s);R=lambda r:r*s
    P=[];X=.15
    P+=[ell(S((0,1.14,.24)),(R(.2),R(.29),R(.36)),(-5,0,0)),        # ribcage, deep
        ell(S((0,.99,.37)),(R(.13),R(.15),R(.18))),                   # brisket
        ell(S((0,1.08,-.12)),(R(.19),R(.22),R(.3)),(4,0,0)),          # belly, tucking up behind
        ell(S((0,1.17,-.38)),(R(.17),R(.16),R(.25))),                 # loin
        ell(S((0,1.15,-.6)),(R(.17),R(.19),R(.17)),(15,0,0)),         # pelvis
        ell(S((0,1.31,.3)),(R(.08),R(.09),R(.2)),(-10,0,0))]          # withers
    P+=sym(lambda d:ell(S((d*.11,1.02,-.6)),(R(.1),R(.24),R(.17)),(12,0,0)))   # haunches
    P+=sym(lambda d:ell(S((d*.13,1.1,.34)),(R(.085),R(.22),R(.12)),(-15,0,0))) # shoulders
    nr=.105 if doe else .14
    P+=[mcap(S((0,1.24,.44)),S((0,1.56,.64)),R(nr*1.15)),mcap(S((0,1.5,.6)),S((0,1.82,.8)),R(nr*.78))]
    if not doe:P+=[ell(S((0,1.38,.6)),(R(.12),R(.2),R(.12)),(-35,0,0))]
    P+=[ell(S((0,1.9,.84)),(R(.088),R(.095),R(.11)),(-10,0,0)),
        mcap(S((0,1.88,.9)),S((0,1.765,1.11)),R(.052)),
        ell(S((0,1.755,1.12)),(R(.042),R(.048),R(.055))),
        ell(S((0,1.8,.96)),(R(.052),R(.045),R(.12)),(22,0,0))]
    P+=sym(lambda d:ell(S((d*.055,1.87,.9)),(R(.04),R(.05),R(.07))))                       # cheeks
    P+=sym(lambda d:cap([S((d*.08,1.97,.8)),S((d*.18,2.04,.76)),S((d*.28,2.09,.72))],[(R(.014),R(.045)),(R(.011),R(.068)),(R(.006),R(.028))]))
    P+=sym(lambda d:mcap(S((d*.14,1.05,.36)),S((d*X,.76,.43)),R(.068)))+sym(lambda d:mcap(S((d*.13,1.02,-.52)),S((d*X,.72,-.44)),R(.09)))
    P+=sym(lambda d:mcap(S((d*X,.77,.43)),S((d*X,.47,.43)),R(.043)))+sym(lambda d:mcap(S((d*X,.73,-.44)),S((d*X,.49,-.67)),R(.05)))
    P+=sym(lambda d:cap([S((d*X,.5,.43)),S((d*X,.46,.43)),S((d*X,.15,.45)),S((d*X,.05,.48))],[R(.034),R(.032),R(.025),R(.029)]))
    P+=sym(lambda d:cap([S((d*X,.52,-.66)),S((d*X,.47,-.68)),S((d*X,.15,-.62)),S((d*X,.05,-.58))],[R(.036),R(.033),R(.025),R(.029)]))
    P+=sym(lambda d:ell(S((d*X,.035,.5)),(R(.034),R(.034),R(.048))))+sym(lambda d:ell(S((d*X,.035,-.56)),(R(.034),R(.034),R(.048))))
    P+=sym(lambda d:ell(S((d*X,.46,.43)),(R(.036),R(.042),R(.036))))+sym(lambda d:ell(S((d*X,.47,-.68)),(R(.034),R(.042),R(.042))))
    P+=[ell(S((0,1.1,-.8)),(R(.055),R(.1),R(.045)),(35,0,0))]
    if not doe:
        def ant(d):
            r=.03;n=lambda nm,par,p,rr:(nm,par,S((d*p[0],p[1],p[2])),R(rr))
            return {'skin':[n('a0',None,(.07,1.98,.8),r*1.25),n('a1','a0',(.2,2.2,.72),r),n('brow','a1',(.24,2.2,1.02),r*.55),n('a2','a1',(.36,2.42,.6),r*.9),n('trez','a2',(.42,2.43,.88),r*.5),
              n('a3','a2',(.5,2.62,.44),r*.8),n('a4','a3',(.56,2.8,.32),r*.65),n('c1','a3',(.66,2.72,.62),r*.45),n('c2','a4',(.52,2.98,.38),r*.42),n('c3','a4',(.7,2.95,.2),r*.42),n('c4','a4',(.62,3.02,.1),r*.38)],'sub':2}
        P+=sym(ant)
    J={'root':S((0,1.12,-.45)),'back':S((0,1.14,-.05)),'chest':S((0,1.16,.3)),'neck':S((0,1.32,.5)),'head':S((0,1.86,.8)),'nose':S((0,1.75,1.18)),'tail':S((0,1.14,-.74)),'tailtip':S((0,.98,-.84)),
       'earL':S((.1,1.98,.8)),'eartipL':S((.3,2.08,.72)),'earR':S((-.1,1.98,.8)),'eartipR':S((-.3,2.08,.72))}
    for d,t in ((1,'L'),(-1,'R')):
        J.update({'fl'+t:S((d*X,1.02,.38)),'fe'+t:S((d*X,.76,.43)),'fh'+t:S((d*X,.04,.48)),'hl'+t:S((d*X,1.0,-.5)),'hs'+t:S((d*X,.72,-.44)),'hp'+t:S((d*X,.04,-.58))})
    return P,quad_bones(J)
def doe_color(g,n):
    x,y,z=g;c=(.5,.34,.2)
    c=mix(c,(.84,.76,.62),sm(.98,.86,y)*sm(-.05,-.5,n[1]))           # pale belly
    c=mix(c,(.8,.7,.55),sm(1.45,1.3,y)*sm(.62,.75,z)*sm(.1,-.3,n[1])*sm(1.8,1.6,y)) # throat
    c=mix(c,(.28,.2,.14),sm(.7,.3,y))
    c=mix(c,(.86,.8,.68),sm(-.62,-.76,z)*sm(.85,1.12,y)*sm(.14,.04,abs(x)))  # white rump
    c=mix(c,(.25,.17,.11),sm(1.0,1.14,z)*sm(1.7,1.8,y));c=mix(c,(.04,.04,.04),sm(1.16,1.21,z))
    # spotted coat along the back and flanks
    if y>1.0 and -.62<z<.42 and n[1]>-.25:
        # rows of small pale dots along the flanks, like a fallow doe
        gz=z/.075;gy=(y-1.0)/.07;iz=round(gz+ (round(gy)%2)*.5);iy=round(gy);dz=(gz+(round(gy)%2)*.5-iz)*.075;dy=(gy-iy)*.07
        if iy>=1 and nz(iz*1.7,iy*3.1,x>0)>.25 and math.hypot(dz,dy)<.017+.006*nz(iz,iy,1):c=mix(c,(.95,.9,.8),.9)
    if y<.075:c=(.1,.09,.08)
    v=fbm(x*4,y*4,z*4)*.1-.05;return tuple(max(0,min(1,k*(1+v))) for k in c)
def stag2_color(g,n):
    x,y,z=g;c=(.38,.26,.16)
    c=mix(c,(.6,.5,.37),sm(.98,.86,y)*sm(-.05,-.5,n[1]))
    c=mix(c,(.26,.19,.13),sm(1.28,1.5,y)*sm(.38,.6,z)*sm(1.95,1.7,y))   # dark shaggy neck
    c=mix(c,(.22,.16,.11),sm(.7,.3,y))
    c=mix(c,(.78,.68,.5),sm(-.62,-.76,z)*sm(.85,1.12,y)*sm(.14,.04,abs(x)))
    c=mix(c,(.22,.16,.11),sm(1.0,1.14,z)*sm(1.7,1.8,y));c=mix(c,(.04,.04,.04),sm(1.16,1.21,z))
    if y>1.99 and (abs(x)>.04 or y>2.1) and not (abs(x)>.13 and y<2.13 and z>.66):c=mix((.4,.32,.22),(.88,.82,.7),sm(2.0,3.05,y))
    if y<.075:c=(.1,.09,.08)
    v=fbm(x*4,y*4,z*4)*.12-.06;return tuple(max(0,min(1,k*(1+v))) for k in c)
def fur_shape(amp,zone=None):
    def f(g,n):
        if zone and not zone(g,n):return None
        k=amp*(nz(g[0]*55,g[1]*55,g[2]*55)-.5);return (g[0]+n[0]*k,g[1]+n[1]*k,g[2]+n[2]*k)
    return f
_p,_b=deer(False);SPECS['stag']={'name':'stag','parts':_p,'bones':_b,'color':stag2_color,'view':3.3,'voxel':.011,'tris':7000,
  'shape':fur_shape(.03,lambda g,n:1.25<g[1]<1.75 and .4<g[2]<.82 and n[1]<.3)}
_p,_b=deer(True,.9);SPECS['doe']={'name':'doe','parts':_p,'bones':_b,'color':lambda g,n:doe_color((g[0]/.9,g[1]/.9,g[2]/.9),n),'view':2.2,'voxel':.01,'tris':6000}

def legbones(J,fr,hr,X):
    for d,t in ((1,'L'),(-1,'R')):J.update({'fl'+t:(d*X,fr[0][1],fr[0][2]),'fe'+t:(d*X,fr[1][1],fr[1][2]),'fh'+t:(d*X,fr[2][1],fr[2][2]),'hl'+t:(d*X,hr[0][1],hr[0][2]),'hs'+t:(d*X,hr[1][1],hr[1][2]),'hp'+t:(d*X,hr[2][1],hr[2][2])})
    return J
# ---------------- WILD BOAR ----------------
def boar():
    P=[];X=.12
    P+=[ell((0,.8,.2),(.17,.3,.3),(-10,0,0)),ell((0,.69,-.04),(.17,.25,.32)),ell((0,.68,-.36),(.16,.22,.22),(10,0,0)),ell((0,.9,.14),(.09,.13,.3),(-12,0,0))]
    P+=sym(lambda d:ell((d*.1,.62,-.4),(.1,.2,.16),(10,0,0)))+sym(lambda d:ell((d*.12,.66,.26),(.09,.2,.13),(-10,0,0)))
    P+=[ell((0,.68,.48),(.14,.21,.22),(30,0,0)),mcap((0,.62,.6),(0,.46,.9),.08),ell((0,.45,.93),(.07,.064,.03)),ell((0,.5,.68),(.1,.08,.19),(25,0,0))]
    P+=sym(lambda d:ell((d*.09,.62,.62),(.06,.08,.1)))
    P+=sym(lambda d:cap([(d*.08,.8,.5),(d*.13,.9,.47),(d*.15,.97,.43)],[(.012,.04),(.01,.045),(.005,.02)]))
    P+=sym(lambda d:{'skin':[('t0',None,(d*.075,.47,.8),.022),('t1','t0',(d*.12,.52,.86),.016),('t2','t1',(d*.13,.6,.83),.008)]})
    P+=sym(lambda d:mcap((d*.12,.68,.27),(d*X,.4,.3),.07))+sym(lambda d:mcap((d*.11,.66,-.4),(d*X,.42,-.44),.08))
    P+=sym(lambda d:cap([(d*X,.42,.3),(d*X,.13,.3),(d*X,.04,.33)],[.045,.033,.036]))+sym(lambda d:cap([(d*X,.43,-.44),(d*X,.13,-.4),(d*X,.04,-.37)],[.045,.033,.036]))
    P+=[cap([(0,.74,-.56),(0,.6,-.64),(0,.48,-.66)],[.018,.013,.01]),ell((0,.47,-.665),(.03,.06,.03))]
    J={'root':(0,.7,-.32),'back':(0,.72,-.02),'chest':(0,.78,.22),'neck':(0,.72,.42),'head':(0,.64,.56),'nose':(0,.46,.88),'tail':(0,.74,-.56),'tailtip':(0,.48,-.66),
       'earL':(.08,.8,.5),'eartipL':(.15,.97,.43),'earR':(-.08,.8,.5),'eartipR':(-.15,.97,.43)}
    legbones(J,[(0,.66,.27),(0,.42,.3),(0,.04,.33)],[(0,.64,-.4),(0,.43,-.44),(0,.04,-.37)],X)
    return P,quad_bones(J)
def boar_color(g,n):
    x,y,z=g;c=(.24,.2,.17)
    t=nz(x*60,y*60,z*60);c=mix(c,(.42,.36,.3),t*.45)                  # grizzled bristle tips
    c=mix(c,(.15,.12,.1),sm(.45,.2,y))                                  # dark legs
    c=mix(c,(.36,.28,.26),sm(.78,.88,z)*sm(.6,.5,y))                    # snout
    if z>.87 and y<.5:c=(.2,.15,.15)
    if y>.42 and z>.78 and abs(x)>.05 and y<.62 and (abs(x)>.06):pass
    if (abs(x)>.06 and .46<y<.62 and .78<z<.9 and n[1]>-.5 and abs(x)<.16) and y>.5:c=(.88,.84,.72)  # tusks
    if y<.06:c=(.08,.07,.06)
    return c
def boar_shape(g,n):
    x,y,z=g
    if abs(x)<.09 and n[1]>.5 and -.35<z<.55 and y>.74:  # bristly mane crest along the spine
        k=(.02+.06*sm(-.35,.2,z)*sm(.6,.3,z))*(.6+.4*fbm(x*20,y*20,z*35))*sm(.09,.02,abs(x));return (x,y+k,z)
    k=.012*(nz(x*90,y*90,z*90)-.5);return (x+n[0]*k,y+n[1]*k,z+n[2]*k)
_p,_b=boar();SPECS['boar']={'name':'boar','parts':_p,'bones':_b,'color':boar_color,'shape':boar_shape,'view':1.4,'voxel':.008,'tris':5000}

# ---------------- GREY WOLF ----------------
def wolf():
    P=[];X=.09
    P+=[ell((0,.8,.24),(.15,.24,.27),(-6,0,0)),ell((0,.79,-.06),(.13,.17,.27),(4,0,0)),ell((0,.82,-.33),(.13,.16,.19),(8,0,0)),ell((0,.94,.42),(.16,.19,.17),(-30,0,0))]
    P+=sym(lambda d:ell((d*.085,.72,-.34),(.075,.2,.14),(18,0,0)))+sym(lambda d:ell((d*.1,.8,.28),(.065,.17,.1),(-12,0,0)))
    P+=[ell((0,1.04,.55),(.115,.105,.115)),mcap((0,1.02,.62),(0,.975,.82),.055),ell((0,.98,.835),(.034,.03,.024)),ell((0,.975,.7),(.055,.04,.12),(10,0,0))]
    P+=sym(lambda d:ell((d*.1,1.0,.54),(.065,.085,.08)))
    P+=sym(lambda d:cap([(d*.065,1.12,.53),(d*.08,1.2,.53),(d*.09,1.27,.52)],[(.014,.045),(.01,.034),(.004,.01)]))
    P+=sym(lambda d:mcap((d*.1,.78,.3),(d*X,.5,.32),.05))+sym(lambda d:mcap((d*.09,.74,-.34),(d*X,.53,-.25),.055))+sym(lambda d:mcap((d*X,.53,-.25),(d*X,.33,-.39),.045))
    P+=sym(lambda d:cap([(d*X,.52,.32),(d*X,.13,.33),(d*X,.03,.36)],[.042,.032,.036]))+sym(lambda d:cap([(d*X,.34,-.39),(d*X,.32,-.4),(d*X,.11,-.36),(d*X,.03,-.32)],[.04,.038,.032,.036]))
    P+=[cap([(0,.86,-.46),(0,.74,-.56),(0,.6,-.63),(0,.45,-.67),(0,.36,-.68)],[.045,.065,.07,.055,.02])]
    J={'root':(0,.8,-.3),'back':(0,.8,-.05),'chest':(0,.82,.22),'neck':(0,.9,.4),'head':(0,1.04,.56),'nose':(0,.97,.85),'tail':(0,.86,-.47),'tailtip':(0,.48,-.7),
       'earL':(.06,1.12,.54),'eartipL':(.085,1.27,.53),'earR':(-.06,1.12,.54),'eartipR':(-.085,1.27,.53)}
    legbones(J,[(0,.78,.3),(0,.52,.32),(0,.03,.36)],[(0,.78,-.34),(0,.53,-.24),(0,.03,-.32)],X)
    return P,quad_bones(J)
def wolf_color(g,n):
    x,y,z=g;c=(.56,.53,.48)
    c=mix(c,(.18,.17,.16),sm(.05,.6,n[1])*sm(.78,.92,y)*sm(.45,.15,z)*sm(-.55,-.35,z)) # dark saddle
    c=mix(c,(.68,.6,.48),sm(.3,-.2,n[1])*sm(.95,.8,y)*sm(-.35,.3,z)*.6)               # tawny flanks
    c=mix(c,(.86,.82,.72),sm(.0,-.5,n[1])*sm(.95,.7,y))                               # cream underside
    c=mix(c,(.82,.77,.66),sm(.62,.45,y))                                               # pale legs
    c=mix(c,(.86,.82,.74),sm(.65,.78,z)*sm(1.05,.95,y))                                # pale muzzle and cheeks
    c=mix(c,(.25,.24,.23),sm(1.08,1.16,y)*sm(.4,.6,z))                                 # dark brow and ears
    if z>.83 and y>.95:c=(.05,.05,.05)
    c=mix(c,(.1,.1,.1),sm(.5,.4,y)*sm(-.6,-.66,z))                                     # black tail tip
    t=nz(x*70,y*70,z*70)*.12-.06;return tuple(max(0,min(1,k*(1+t))) for k in c)
_p,_b=wolf();SPECS['wolf']={'name':'wolf','parts':_p,'bones':_b,'color':wolf_color,'shape':fur_shape(.014),'view':1.6,'voxel':.008,'tris':5000}

# ---------------- BROWN BEAR ----------------
def bear():
    P=[];X=.25
    P+=[ell((0,1.14,.3),(.34,.34,.34)),ell((0,.95,.4),(.34,.36,.3)),ell((0,.92,-.05),(.38,.4,.46)),ell((0,1.0,-.5),(.34,.36,.3),(8,0,0))]
    P+=sym(lambda d:ell((d*.22,.86,-.52),(.16,.32,.26),(10,0,0)))+sym(lambda d:ell((d*.24,.92,.42),(.15,.32,.22),(-10,0,0)))
    P+=[mcap((0,1.02,.56),(0,1.0,.8),.24),ell((0,1.04,.9),(.2,.18,.17)),mcap((0,.98,1.02),(0,.92,1.25),.08),ell((0,.925,1.28),(.05,.042,.03)),ell((0,.9,1.05),(.1,.08,.16),(10,0,0))]
    P+=sym(lambda d:ell((d*.16,1.24,.85),(.075,.075,.035)))
    P+=sym(lambda d:mcap((d*.24,.92,.45),(d*X,.42,.5),.16))+sym(lambda d:mcap((d*X,.42,.5),(d*X,.12,.52),.12))+sym(lambda d:ell((d*X,.07,.58),(.12,.075,.17)))
    P+=sym(lambda d:mcap((d*.24,.92,-.5),(d*X,.45,-.44),.18))+sym(lambda d:mcap((d*X,.45,-.44),(d*X,.12,-.5),.12))+sym(lambda d:ell((d*X,.07,-.44),(.12,.075,.17)))
    for d in (1,-1):
        for z0 in (.58,-.44):
            for k in range(4):P.append({'skin':[('c0',None,(d*X+(k-1.5)*.05,.07,z0+.13),.016),('c1','c0',(d*X+(k-1.5)*.055,.04,z0+.21),.009),('c2','c1',(d*X+(k-1.5)*.055,.015,z0+.24),.004)]})
    P+=[ell((0,.98,-.78),(.06,.06,.05))]
    J={'root':(0,.98,-.42),'back':(0,.98,-.05),'chest':(0,1.02,.32),'neck':(0,1.02,.56),'head':(0,1.02,.9),'nose':(0,.93,1.24),'tail':(0,.98,-.76),'tailtip':(0,.96,-.82),
       'earL':(.13,1.16,.86),'eartipL':(.17,1.24,.86),'earR':(-.13,1.16,.86),'eartipR':(-.17,1.24,.86)}
    legbones(J,[(0,.92,.45),(0,.42,.5),(0,.06,.58)],[(0,.92,-.5),(0,.45,-.44),(0,.06,-.44)],X)
    return P,quad_bones(J)
def bear_color(g,n):
    x,y,z=g;c=(.33,.23,.15)
    t=nz(x*55,y*55,z*55);c=mix(c,(.55,.42,.28),sm(.2,.9,n[1])*sm(.95,1.35,y)*t*.8)     # sun-bleached tips on hump and back
    c=mix(c,(.17,.12,.08),sm(.55,.2,y))                                                # dark legs
    c=mix(c,(.5,.38,.25),sm(1.02,1.12,z)*sm(1.05,.9,y))                                # tan muzzle
    if z>1.26 and y>.88:c=(.05,.04,.04)
    if y<.06 and (z>.62 or -.4<z<-.2):c=(.78,.74,.66)                                   # claws
    v=nz(x*80,y*80,z*80)*.14-.07;return tuple(max(0,min(1,k*(1+v))) for k in c)
_p,_b=bear();SPECS['bear']={'name':'bear','parts':_p,'bones':_b,'color':bear_color,'shape':fur_shape(.025),'view':2.0,'voxel':.012,'tris':6000}
def rime_color(g,n):
    x,y,z=g;c=(.8,.82,.84)
    c=mix(c,(.5,.55,.6),sm(.15,.75,n[1])*sm(.8,.95,y)*sm(.4,.1,z)*sm(-.5,-.3,z))
    c=mix(c,(.95,.95,.93),sm(.0,-.5,n[1]))
    c=mix(c,(.55,.6,.66),sm(1.08,1.16,y)*sm(.4,.6,z))
    if z>.83 and y>.95:c=(.06,.06,.08)
    t=nz(x*70,y*70,z*70)*.08-.04;return tuple(max(0,min(1,k*(1+t))) for k in c)
_p,_b=wolf();SPECS['rimewolf']={'name':'rimewolf','parts':_p,'bones':_b,'color':rime_color,'shape':fur_shape(.016),'view':1.6,'voxel':.008,'tris':5000}

# ================= MONSTERS =================
BIPED_IF={'legs':['legL','legR'],'arms':['armL','armR'],'head':'head','body':'spine'}
def biped_bones(J,tail=None):
    B=[('root',None,J['hip'],J['waist']),('spine','root',J['waist'],J['chest']),('neck','spine',J['chest'],J['neckt']),('head','neck',J['neckt'],J['face'])]
    for t,d in (('L',1),('R',-1)):
        m=lambda p:(d*p[0],p[1],p[2])
        B+=[('arm'+t,'spine',m(J['sh']),m(J['el'])),('fore'+t,'arm'+t,m(J['el']),m(J['wr'])),('leg'+t,'root',m(J['hp']),m(J['kn'])),('shin'+t,'leg'+t,m(J['kn']),m(J['an']))]
    if tail:B.append(('tail','root',tail[0],tail[1]))
    return B
def spike(base,tip,r0,r1=.004):return {'skin':[('s0',None,base,r0),('s1','s0',tip,r1)],'sub':1}
def horn(pts,rs):return {'skin':[('h%d'%i,('h%d'%(i-1) if i else None),p,r) for i,(p,r) in enumerate(zip(pts,rs))],'sub':2}
def gtone(c,g,amp=.12,f=40):
    v=nz(g[0]*f,g[1]*f,g[2]*f)*amp-amp/2;return tuple(max(0,min(1,k*(1+v))) for k in c)

# ---- Cinderhorn Ogre (fat red horned brute) ----
def ogre():
    P=[]
    P+=[ell((0,1.55,.3),(.95,.88,.9)),ell((0,2.3,0),(.82,.55,.58)),ell((0,2.65,-.08),(.5,.25,.38)),ell((0,1.3,0),(.62,.35,.5))]
    P+=sym(lambda d:ell((d*.82,2.42,0),(.36,.32,.36)))
    P+=[ell((0,2.78,.42),(.28,.27,.3)),ell((0,2.6,.55),(.27,.17,.24)),ell((0,2.88,.6),(.27,.08,.1)),ell((0,2.72,.72),(.1,.09,.08))]
    P+=sym(lambda d:mcap((d*.88,2.45,0),(d*1.08,1.75,.06),.27))+sym(lambda d:mcap((d*1.08,1.75,.06),(d*1.14,1.12,.22),.24))+sym(lambda d:ell((d*1.15,.95,.27),(.2,.22,.19)))
    P+=sym(lambda d:mcap((d*.48,1.3,0),(d*.55,.72,.06),.33))+sym(lambda d:mcap((d*.55,.72,.06),(d*.55,.2,0),.26))+sym(lambda d:ell((d*.55,.11,.13),(.23,.12,.31)))
    P+=sym(lambda d:horn([(d*.18,2.96,.42),(d*.45,3.15,.36),(d*.62,3.45,.26),(d*.58,3.72,.1)],[.1,.08,.05,.012]))
    P+=sym(lambda d:spike((d*.13,2.55,.75),(d*.19,2.74,.82),.04))
    for i in range(7):P.append(spike((0,2.62-i*.2,-.5+i*.02-(.1 if i>2 else 0)),(0,2.82-i*.2,-.86+i*.02-(.1 if i>2 else 0)),.07-.004*i))
    P+=sym(lambda d:spike((d*.95,2.7,-.1),(d*1.25,2.95,-.2),.06))
    P+=[ell((0,.98,.68),(.42,.32,.06),(6,0,0)),ell((0,.98,-.52),(.42,.32,.06),(-8,0,0))]   # loincloth flaps
    J={'hip':(0,1.3,0),'waist':(0,1.9,0),'chest':(0,2.6,0),'neckt':(0,2.75,.38),'face':(0,2.75,.8),'sh':(.9,2.45,0),'el':(1.08,1.75,.06),'wr':(1.15,1.0,.24),'hp':(.48,1.3,0),'kn':(.55,.72,.06),'an':(.55,.12,.05)}
    return P,biped_bones(J)
def ogre_color(g,n):
    x,y,z=g;c=(.62,.14,.1)
    v=abs(math.sin(x*9+math.sin(y*7)*1.5)*math.sin(y*8+math.sin(z*6)*1.3));c=mix(c,(.42,.08,.06),sm(.12,.0,v)*.55)   # fine dark vein lines
    c=mix(c,(.7,.22,.15),sm(.2,-.4,n[1])*sm(.5,1.0,z)*sm(1.0,2.0,y)*.4)
    if .85<y<1.32 and abs(x)<.7 and (abs(z)>.45 or n[1]<.3):c=(.24,.17,.11)   # loincloth
    if y<.24:c=(.3,.07,.06)
    if (y>2.9 and abs(x)>.14 and z<.55) or (z<-.55 and y>1.6 and abs(x)<.1) or (abs(x)>.92 and y>2.78 and n[1]>.2):c=mix((.82,.76,.64),(.3,.24,.2),sm(3.3,3.75,y) if y>2.9 else 0)   # horns and bone spikes
    if abs(x)>.12 and y>2.55 and z>.76 and y<2.76:c=(.88,.82,.7)    # tusks
    return gtone(c,g,.1,30)
_p,_b=ogre();SPECS['ogre']={'name':'ogre','parts':_p,'bones':_b,'color':ogre_color,'iface':BIPED_IF,'view':4.2,'voxel':.018,'tris':7000}

# ---- Gilded Centipede (rearing, gold-shelled, sickle jaws) ----
def centipede():
    P=[];B=[];segs=[];prev=None;pts=[]
    for i in range(12):
        y=[1.75,1.35,.95,.62][i] if i<4 else .45;z=[.0,-.35,-.62,-.95][i] if i<4 else -.95-(i-3)*.6;pts.append((0,y,z))
    for i,(x,y,z) in enumerate(pts):
        w=.46-.018*i
        P.append(ell((0,y,z),(w,.26,.3),(-35 if i<3 else 0,0,0)))
        if i>0:
            for d in (1,-1):
                if i<4:P.append(horn([(d*w*.8,y,z),(d*(w+.35),y-.05,z+.25),(d*(w+.45),y-.25,z+.45)],[.05,.035,.008]))
                else:P.append(horn([(d*w*.85,y-.05,z),(d*(w+.42),y+.05,z+.05),(d*(w+.62),.02,z+.18)],[.05,.035,.01]))
        nm='seg%d'%i;nxt=pts[i+1] if i+1<len(pts) else (0,.4,z-.5);B.append((nm,prev,(x,y,z),nxt));prev=nm;segs.append(nm)
    P+=[ell((0,2.0,.3),(.36,.3,.38),(-20,0,0)),ell((0,2.25,.18),(.22,.18,.22))]
    P+=sym(lambda d:horn([(d*.28,1.95,.5),(d*.55,1.85,.85),(d*.48,1.62,1.2),(d*.18,1.48,1.32)],[.075,.06,.04,.008]))
    P+=sym(lambda d:horn([(d*.18,2.3,.3),(d*.35,2.6,.15),(d*.4,2.85,-.05)],[.05,.035,.008]))
    P+=[horn([(0,2.35,.25),(0,2.7,.05),(0,2.95,-.15)],[.08,.05,.01])]
    B.append(('head','seg0',(0,1.9,.15),(0,2.0,.7)))
    return P,B,segs
def centi_color(g,n):
    x,y,z=g;c=(.86,.56,.14)
    c=mix(c,(.92,.88,.78),sm(.1,-.5,n[1])*(1 if y<1.3 else sm(.2,-.4,n[2])))       # pale banded belly
    if abs(x)>.5:c=mix((.8,.42,.1),(.92,.88,.8),sm(.25,.0,y) if y<.3 else sm(.65,.95,abs(x)))   # legs: orange with pale tips
    v=fbm(x*9,y*9,z*9);c=mix(c,(.55,.28,.06),sm(.6,.85,v)*.6)
    if z>1.0:c=(.9,.86,.76)
    return gtone(c,g,.08,40)
_p,_b,_s=centipede();SPECS['centipede']={'name':'centipede','parts':_p,'bones':_b,'color':centi_color,'iface':{'segs':_s,'head':'head','legs':[],'arms':[]},'view':3.2,'voxel':.014,'tris':6500}

# ---- Sunscale Stalker (hunched blue lizardman, cream belly, red crest) ----
def lizard():
    P=[]
    P+=[ell((0,1.15,-.12),(.25,.25,.25)),ell((0,1.42,.05),(.27,.33,.27),(-30,0,0)),ell((0,1.76,.26),(.36,.3,.3),(-30,0,0))]
    P+=sym(lambda d:ell((d*.32,1.86,.3),(.15,.15,.15)))
    P+=[mcap((0,1.84,.4),(0,2.0,.6),.14),ell((0,2.06,.68),(.13,.12,.16)),mcap((0,2.03,.75),(0,1.97,1.04),.075),ell((0,1.93,.82),(.09,.05,.18),(10,0,0))]
    P+=sym(lambda d:mcap((d*.2,1.15,-.1),(d*.25,.76,.16),.14))+sym(lambda d:mcap((d*.25,.76,.16),(d*.25,.42,-.12),.08))+sym(lambda d:mcap((d*.25,.42,-.12),(d*.25,.08,0),.055))+sym(lambda d:ell((d*.25,.05,.12),(.08,.04,.15)))
    P+=sym(lambda d:mcap((d*.36,1.86,.3),(d*.46,1.46,.38),.09))+sym(lambda d:mcap((d*.46,1.46,.38),(d*.46,1.06,.5),.07))+sym(lambda d:ell((d*.46,.98,.55),(.07,.08,.06)))
    for d in (1,-1):
        for k in range(3):P.append(spike((d*(.43+k*.03),.94,.58),(d*(.43+k*.04),.8,.7),.02))
        for k in range(3):P.append(spike((d*.25+(k-1)*.04,.04,.24),(d*.25+(k-1)*.05,.02,.36),.018))
    P+=[horn([(0,1.15,-.3),(0,1.0,-.8),(0,.7,-1.3),(0,.42,-1.8),(0,.22,-2.3)],[.2,.15,.1,.06,.015])]
    for i in range(9):  # dorsal crest from head down the back
        t=i/8;bx=(0,2.15-t*.95,.55-t*.85);P.append(spike(bx,(0,bx[1]+.35-.15*t,bx[2]-.12),.05-.02*t))
    for i in range(5):P.append(spike((0,1.0-i*.13,-.8-i*.27),(0,1.18-i*.13,-.9-i*.27),.04))
    P+=sym(lambda d:horn([(d*.08,2.14,.6),(d*.15,2.3,.4),(d*.18,2.4,.2)],[.035,.025,.006]))
    for k in range(5):
        a=-1.1+k*.55;P.append(spike((math.sin(a)*.12,1.9+math.cos(a)*.02,.72),(math.sin(a)*.3,1.82,.62),.03))   # throat frill
    P+=sym(lambda d:spike((d*.06,1.95,.98),(d*.07,1.86,1.0),.014))   # fangs
    J={'hip':(0,1.15,-.1),'waist':(0,1.45,.05),'chest':(0,1.82,.3),'neckt':(0,2.0,.6),'face':(0,1.98,1.02),'sh':(.36,1.86,.3),'el':(.46,1.46,.38),'wr':(.46,1.0,.52),'hp':(.2,1.15,-.1),'kn':(.25,.76,.16),'an':(.25,.08,0)}
    return P,biped_bones(J,tail=((0,1.15,-.3),(0,.5,-1.6)))
def lizard_color(g,n):
    x,y,z=g;c=(.14,.19,.44)
    v=nz(x*55,y*55,z*55);c=mix(c,(.28,.38,.7),sm(.6,.9,v)*.6)                         # scale speckle
    belly=sm(.15,.6,n[2])*sm(.12,.0,abs(x)-.05) if 1.0<y<1.9 and z>-.2 else 0
    c=mix(c,(.88,.82,.64),max(belly,sm(-.1,-.6,n[1])*sm(1.95,1.85,y)*sm(.6,.85,z)))      # cream belly and throat
    if (abs(x)<.05 and n[1]>.0 and ((y>1.3 and z<.6 and z>-.4) or (z<-.7))) :c=(.72,.16,.12)  # red crest
    if y>1.8 and z>.6 and z<.76 and abs(x)>.1 and n[2]>.3:c=(.72,.16,.12)                 # frill
    if y<.09 or (y<1.0 and abs(x)>.4 and z>.55):c=(.86,.82,.72)                          # claws
    if y>2.15 and abs(x)>.06 and z<.62:c=(.85,.8,.68)
    return gtone(c,g,.08,40)
_p,_b=lizard();SPECS['lizard']={'name':'lizard','parts':_p,'bones':_b,'color':lizard_color,'iface':dict(BIPED_IF,tail='tail'),'view':3.0,'voxel':.012,'tris':6500}

# ---- Goblin Raider ----
def goblin():
    P=[]
    P+=[ell((0,.86,0),(.15,.13,.12)),ell((0,1.03,.03),(.15,.17,.13)),ell((0,1.25,.03),(.2,.15,.13),(-15,0,0))]
    P+=sym(lambda d:ell((d*.19,1.3,.02),(.08,.08,.08)))
    P+=[mcap((0,1.33,.07),(0,1.42,.14),.07),ell((0,1.52,.14),(.18,.17,.18)),ell((0,1.43,.24),(.14,.08,.13)),horn([(0,1.54,.3),(0,1.48,.4),(0,1.42,.42)],[.045,.035,.014])]
    P+=sym(lambda d:horn([(d*.15,1.56,.1),(d*.34,1.62,.02),(d*.52,1.7,-.06)],[.045,.035,.008]))
    P+=sym(lambda d:mcap((d*.09,.86,0),(d*.12,.52,.16),.065))+sym(lambda d:mcap((d*.12,.52,.16),(d*.11,.08,-.02),.045))+sym(lambda d:ell((d*.11,.04,.06),(.05,.035,.1)))
    P+=sym(lambda d:mcap((d*.21,1.3,.02),(d*.27,1.0,.06),.05))+sym(lambda d:mcap((d*.27,1.0,.06),(d*.3,.72,.14),.04))+sym(lambda d:ell((d*.3,.66,.16),(.045,.05,.04)))
    P+=[ell((0,1.33,-.02),(.27,.1,.19)),ell((0,1.2,-.14),(.22,.2,.06),(-8,0,0))]      # fur mantle
    P+=sym(lambda d:spike((d*.04,1.42,.24),(d*.045,1.36,.26),.012))
    J={'hip':(0,.86,0),'waist':(0,1.05,.03),'chest':(0,1.32,.05),'neckt':(0,1.45,.1),'face':(0,1.5,.32),'sh':(.21,1.3,.02),'el':(.27,1.0,.06),'wr':(.3,.68,.15),'hp':(.09,.86,0),'kn':(.12,.52,.16),'an':(.11,.06,-.02)}
    return P,biped_bones(J)
def goblin_color(g,n):
    x,y,z=g;c=(.42,.56,.22)
    c=mix(c,(.3,.4,.16),sm(.6,.85,fbm(x*8,y*8,z*8))*.6)
    if (1.24<y<1.45 and (z<.05 or abs(x)>.17) and abs(x)<.32 and not (y>1.4 and abs(x)<.1)) or (z<-.1 and 1.0<y<1.42):c=(.32,.24,.17)   # fur mantle
    if .78<y<.95 and abs(x)<.17:c=(.36,.26,.18)
    if y<.06:c=(.2,.17,.13)
    return gtone(c,g,.1,50)
_p,_b=goblin();SPECS['goblin']={'name':'goblin','parts':_p,'bones':_b,'color':goblin_color,'iface':BIPED_IF,'view':2.0,'voxel':.008,'tris':5000}

# ---- Hobgoblin Brute ----
def hobgob():
    P=[]
    P+=[ell((0,1.15,0),(.24,.2,.18)),ell((0,1.38,.04),(.27,.24,.2)),ell((0,1.72,.02),(.42,.28,.26),(-8,0,0)),ell((0,1.88,-.06),(.3,.14,.2))]
    P+=sym(lambda d:ell((d*.38,1.82,.0),(.16,.15,.16)))
    P+=[mcap((0,1.9,.05),(0,2.0,.12),.11),ell((0,2.12,.12),(.15,.16,.16)),ell((0,2.04,.2),(.13,.09,.12)),ell((0,2.17,.24),(.13,.04,.06))]
    P+=sym(lambda d:horn([(d*.13,2.16,.08),(d*.26,2.2,.02),(d*.36,2.25,-.04)],[.035,.025,.006]))
    P+=sym(lambda d:spike((d*.08,2.0,.28),(d*.1,2.08,.3),.016))
    for i in range(6):P.append(spike((0,2.25-i*.05,.16-i*.07),(0,2.42-i*.05,.1-i*.08),.04))   # mohawk
    P+=sym(lambda d:mcap((d*.13,1.15,0),(d*.16,.62,.08),.12))+sym(lambda d:mcap((d*.16,.62,.08),(d*.16,.1,-.02),.085))+sym(lambda d:ell((d*.16,.05,.07),(.08,.05,.14)))
    P+=sym(lambda d:mcap((d*.42,1.84,0),(d*.5,1.42,.04),.11))+sym(lambda d:mcap((d*.5,1.42,.04),(d*.54,1.02,.14),.095))+sym(lambda d:ell((d*.55,.94,.17),(.09,.1,.09)))
    J={'hip':(0,1.15,0),'waist':(0,1.4,.04),'chest':(0,1.85,.02),'neckt':(0,2.0,.12),'face':(0,2.06,.32),'sh':(.42,1.84,0),'el':(.5,1.42,.04),'wr':(.54,.98,.16),'hp':(.13,1.15,0),'kn':(.16,.62,.08),'an':(.16,.08,-.02)}
    return P,biped_bones(J)
def hob_color(g,n):
    x,y,z=g;c=(.74,.52,.28)
    c=mix(c,(.55,.36,.18),sm(.6,.85,fbm(x*7,y*7,z*7))*.6)
    if y>2.24 and abs(x)<.05:c=(.12,.1,.09)
    if .95<y<1.3 and abs(x)<.3:c=(.25,.2,.16)
    if y<.32:c=(.3,.22,.15)                                       # wraps
    return gtone(c,g,.1,40)
_p,_b=hobgob();SPECS['hobgob']={'name':'hobgob','parts':_p,'bones':_b,'color':hob_color,'iface':BIPED_IF,'view':2.8,'voxel':.01,'tris':5500}

# ================= SPIRITS =================
def neg(c,r,rot=None):d=ell(c,r,rot);d['neg']=True;return d
FLOAT_IF={'legs':[],'arms':['armL','armR'],'head':'head','body':'root','flutter':[],'float':1}
def spirit_bones(J,extra=()):
    B=[('root',None,J['base'],J['waist']),('spine','root',J['waist'],J['chest']),('neck','spine',J['chest'],J['neckt']),('head','neck',J['neckt'],J['face'])]
    for t,d in (('L',1),('R',-1)):
        m=lambda p:(d*p[0],p[1],p[2])
        B+=[('arm'+t,'spine',m(J['sh']),m(J['el'])),('fore'+t,'arm'+t,m(J['el']),m(J['wr'])),('hand'+t,'fore'+t,m(J['wr']),m(J['tip']))]
    return B+list(extra)
def claws(d,w,n=4,L=.13,r=.014,spread=.035,down=.6):
    """long bony fingers from a hand at w, reaching forward then hooking down"""
    out=[]
    for k in range(n):
        o=(k-(n-1)/2)*spread;x0=d*(w[0]+o*.6);p0=(x0,w[1],w[2]+.02);p1=(x0+d*o*.5,w[1]-.03,w[2]+L);p2=(x0+d*o*.8,w[1]-.03-L*down,w[2]+L*1.6);p3=(x0+d*o*.9,w[1]-L*1.3*down,w[2]+L*1.75)
        out.append(horn([p0,p1,p2,p3],[r,r*.85,r*.6,r*.18]))
    out.append(horn([(d*(w[0]-.03),w[1],w[2]),(d*(w[0]-.07),w[1]-.04,w[2]+.08),(d*(w[0]-.07),w[1]-.1,w[2]+.14)],[r,r*.7,r*.2]))   # thumb
    return out

# ---- Hooded wraith: tall cowl with a hollow void face, hunched shoulders, robe tearing into rags, bone-thin scabbed hands ----
def wraith():
    P=[]
    P+=[ell((0,2.36,-.06),(.27,.33,.3)),ell((0,2.6,-.12),(.15,.2,.18),(-25,0,0)),ell((0,2.74,-.2),(.06,.1,.08),(-40,0,0)),ell((0,2.38,.14),(.26,.34,.16),(12,0,0)),neg((0,2.26,.22),(.17,.25,.26))]   # hood, peak, cowl rim, the void
    P+=[ell((0,2.06,-.03),(.33,.14,.25))]+sym(lambda d:ell((d*.33,1.98,-.03),(.13,.12,.15),(0,0,d*-25)))
    P+=[ell((0,1.74,-.01),(.32,.32,.23)),ell((0,1.38,-.02),(.27,.33,.2)),ell((0,1.04,-.02),(.24,.32,.19)),ell((0,.78,-.03),(.2,.2,.16))]
    for k in range(12):
        a=k/12*6.283+.2;P.append(ell((math.sin(a)*.25,1.32,math.cos(a)*.2-.02),(.045,.55,.045),(math.cos(a)*-4,0,math.sin(a)*4)))   # hanging folds          # robe to a flared hem
    for d in (1,-1):
        P.append(cap([(d*.36,1.99,0),(d*.56,1.66,.08),(d*.67,1.36,.24)],[.075,.085,.15],sub=2))          # bell sleeve widening to the cuff
        P.append(mcap((d*.62,1.44,.18),(d*.7,1.24,.36),.03))                                            # bone forearm out of the cuff
        P.append(ell((d*.71,1.2,.4),(.045,.035,.055)))
        P+=claws(d,(.71,1.19,.42),L=.12,r=.013)
    J={'base':(0,.9,0),'waist':(0,1.45,0),'chest':(0,2.0,0),'neckt':(0,2.22,0),'face':(0,2.3,.35),'sh':(.38,2.0,0),'el':(.56,1.66,.08),'wr':(.7,1.22,.38),'tip':(.74,1.0,.66)}
    return P,spirit_bones(J)
def wraith_color(g,n):
    x,y,z=g;c=(.07,.068,.075)
    v=fbm(x*6,y*3,z*6);c=mix(c,(.15,.14,.155),sm(.45,.85,v)*.7)                     # worn cloth
    c=mix(c,(.03,.03,.035),sm(.1,-.6,n[1])*.6)                                     # folds in shadow underneath
    if y>2.0 and z>.08 and abs(x)<.19 and n[2]<.5 and y<2.55:c=(.004,.004,.006)                # the void inside the hood
    r=math.hypot(x-(.71 if x>0 else -.71),0)
    if abs(x)>.6 and y<1.4 and z>.3:                                                 # bone arms and scabbed grey hands
        c=mix((.46,.43,.4),(.42,.2,.17),sm(.6,.9,nz(x*70,y*70,z*70))*.7)
    return gtone(c,g,.1,30)
SPECS['wraith']={'name':'wraith','parts':wraith()[0],'bones':wraith()[1],'color':wraith_color,'iface':dict(FLOAT_IF,mat='cloth'),'view':3.0,'voxel':.009,'tris':8000}

# ---- Bone wraith: a skull with stringy hair, open ribcage and spine, tattered mantle, long skeletal arms, no legs ----
def bonewraith():
    P=[]
    P+=[ell((0,2.32,.02),(.15,.17,.18)),ell((0,2.22,.13),(.12,.13,.1))]+sym(lambda d:ell((d*.085,2.2,.17),(.045,.035,.045)))
    P+=sym(lambda d:neg((d*.055,2.26,.23),(.042,.042,.05)))+[neg((0,2.18,.245),(.02,.03,.03))]
    P+=[ell((0,2.07,.13),(.1,.045,.09),(-12,0,0))]                                  # jaw hanging open
    for k in range(5):P.append(spike((-.06+k*.03,2.135,.21),(-.06+k*.03,2.105,.215),.011))
    for k in range(4):P.append(ell((0,2.06-k*.045,-.03),(.035,.022,.035)))           # neck bones
    for k in range(13):y=1.92-k*.075;P.append(ell((0,y,-.1+k*.003),(.04,.028,.04)));P.append(spike((0,y,-.12),(0,y-.03,-.17),.016))
    for k in range(6):
        y=1.84-k*.1;w=.2+.03*math.sin(k/5*3)
        P+=sym(lambda d:horn([(d*.03,y,-.1),(d*w*.85,y,-.07),(d*w,y-.05,.05),(d*w*.7,y-.1,.16),(d*.05,y-.12,.2 if k<4 else .15)],[.02,.019,.018,.016,.012]))
    P+=[ell((0,1.68,.2),(.03,.16,.022))]
    P+=sym(lambda d:horn([(d*.02,1.94,.14),(d*.16,1.98,.08),(d*.3,1.98,-.01)],[.022,.02,.02]))
    P+=[ell((0,1.98,-.2),(.3,.07,.1)),ell((0,1.6,-.24),(.22,.36,.035),(8,0,0))]+sym(lambda d:ell((d*.3,1.98,-.08),(.09,.05,.1),(0,0,d*-20)))   # mantle and back drape
    for d in (1,-1):
        P.append(mcap((d*.32,1.95,0),(d*.56,1.66,.14),.035));P.append(ell((d*.56,1.66,.14),(.045,.045,.045)))
        P.append(mcap((d*.555,1.66,.13),(d*.72,1.46,.38),.022));P.append(mcap((d*.575,1.64,.15),(d*.745,1.44,.36),.018))
        P.append(ell((d*.74,1.42,.42),(.05,.03,.055)))
        P+=claws(d,(.74,1.41,.44),L=.14,r=.012)
    J={'base':(0,.95,-.06),'waist':(0,1.45,-.08),'chest':(0,1.95,-.05),'neckt':(0,2.1,0),'face':(0,2.22,.3),'sh':(.32,1.95,0),'el':(.56,1.66,.14),'wr':(.74,1.43,.4),'tip':(.78,1.25,.66)}
    return P,spirit_bones(J)
def bone_color(g,n):
    x,y,z=g;c=(.6,.54,.43)
    c=mix(c,(.32,.27,.2),sm(.2,-.7,n[1])*.6+sm(.55,.85,fbm(x*14,y*14,z*14))*.35)      # aged, stained bone
    if (z<-.17 and y>1.15) or (y>1.9 and abs(x)>.2 and abs(x)<.42 and z<-.0) :c=mix((.07,.065,.07),(.14,.13,.13),fbm(x*6,y*4,z*6))   # mantle cloth
    if y>2.15 and abs(x)<.1 and z>.2 and n[2]>.2 and abs(x)>.02 and y<2.31:c=mix(c,(.05,.04,.03),sm(2.2,2.25,y)*sm(.0,.04,abs(x)))   # sockets darken
    return gtone(c,g,.08,40)
SPECS['bonewraith']={'name':'bonewraith','parts':bonewraith()[0],'bones':bonewraith()[1],'color':bone_color,'iface':dict(FLOAT_IF,mat='cloth'),'view':3.0,'voxel':.007,'tris':9000}

# ---- Drowned ghost (original): bulbous head, sunken eyes, gaping wail, long reaching arms with hooked claws, a body tapering into a curling tail ----
def ghost():
    P=[]
    P+=[ell((0,2.0,0),(.5,.5,.45)),ell((0,1.56,-.03),(.42,.4,.35)),ell((0,1.18,-.1),(.3,.32,.27))]
    P.append(cap([(0,1.0,-.16),(0,.72,-.3),(0,.52,-.5),(0,.46,-.74),(0,.56,-.92)],[.25,.19,.13,.07,.02],sub=2))
    P+=[ell((0,2.14,.33),(.34,.07,.1),(-10,0,0))]+sym(lambda d:ell((d*.27,1.88,.3),(.14,.11,.12)))+[ell((0,1.42,.24),(.2,.1,.12))]   # brow, cheeks, sagging chin
    P+=sym(lambda d:neg((d*.17,2.0,.43),(.11,.1,.12)))+[neg((0,1.64,.4),(.15,.17,.22))]                                                 # sunken eyes, wailing mouth
    P+=sym(lambda d:neg((d*.03,1.84,.47),(.015,.025,.03)))
    for d in (1,-1):
        P.append(cap([(d*.4,1.72,0),(d*.7,1.45,.16),(d*.82,1.2,.42)],[.14,.1,.075],sub=2))
        P.append(ell((d*.84,1.16,.5),(.1,.06,.12)))
        for k in range(3):
            o=(k-1)*.055;P.append(horn([(d*(.84+o),1.15,.56),(d*(.86+o*1.4),1.12,.72),(d*(.87+o*1.6),1.0,.86),(d*(.86+o*1.6),.9,.86)],[.032,.026,.016,.004]))
        P.append(horn([(d*.79,1.15,.52),(d*.74,1.1,.64),(d*.73,1.02,.7)],[.028,.018,.004]))
    J={'base':(0,1.1,-.1),'waist':(0,1.55,0),'chest':(0,1.85,0),'neckt':(0,1.95,0),'face':(0,2.05,.45),'sh':(.4,1.72,0),'el':(.7,1.45,.16),'wr':(.83,1.18,.45),'tip':(.86,.95,.85)}
    tail=[('tail0','root',(0,1.0,-.16),(0,.72,-.3)),('tail1','tail0',(0,.72,-.3),(0,.52,-.5)),('tail2','tail1',(0,.52,-.5),(0,.46,-.74)),('tail3','tail2',(0,.46,-.74),(0,.56,-.92))]
    return P,spirit_bones(J,tail)
def ghost_color(g,n):
    x,y,z=g;c=(.62,1.0,.7)
    c=mix(c,(.25,.75,.42),sm(1.3,.5,y))                                                            # deeper green toward the tail
    if z>.3 and ((abs(abs(x)-.17)<.11 and 1.89<y<2.11) or (abs(x)<.15 and 1.48<y<1.8)) and n[2]<.6:c=(.02,.12,.06)   # hollow eyes and throat
    return c
SPECS['ghost']={'name':'ghost','parts':ghost()[0],'bones':ghost()[1],'color':ghost_color,'iface':dict(FLOAT_IF,mat='ghost',flutter=['tail0','tail1','tail2','tail3']),'view':2.8,'voxel':.012,'tris':6000}

# ================= TOMB UNDEAD =================
# ---- Draugr: a rotting skeletal warrior — skull grin under an iron cap, open leather vest over bare ribs, studded pauldrons, sinew on the bones ----
def draugr():
    P=[]
    P+=[ell((0,1.0,-.01),(.15,.08,.1)),ell((0,1.035,0),(.18,.04,.13))]+sym(lambda d:ell((d*.1,.97,-.02),(.07,.06,.06)))     # pelvis, belt, hip bones
    for k in range(7):P.append(ell((0,1.08+k*.06,-.075),(.026,.019,.026)))                               # spine
    for k in range(6):
        y=1.45-k*.064;w=.15+.03*math.sin(k/5*3)
        P+=sym(lambda d:horn([(d*.02,y,-.075),(d*w*.85,y,-.055),(d*w,y-.035,.03),(d*w*.72,y-.065,.105),(d*.035,y-.075,.125)],[.013,.012,.012,.011,.009]))
    P+=[ell((0,1.33,.125),(.018,.11,.012))]
    P+=sym(lambda d:horn([(d*.02,1.5,.1),(d*.12,1.52,.06),(d*.21,1.5,-.0)],[.014,.013,.013]))           # collarbones
    P+=[ell((0,1.3,-.11),(.19,.21,.045)),ell((0,1.47,-.05),(.19,.05,.08))]                              # vest back and yoke
    P+=sym(lambda d:ell((d*.19,1.27,.0),(.035,.18,.085),(0,0,d*6)))                                      # narrow vest fronts at the flanks
    P+=sym(lambda d:ell((d*.23,1.5,-.01),(.085,.05,.09),(0,0,d*-22)))                                    # pauldrons
    P+=[mcap((.19,1.47,.08),(-.14,1.06,.12),.014)]                                                       # strap
    P+=[ell((0,1.035,.13),(.03,.026,.014)),ell((0,.88,.1),(.1,.14,.018),(8,0,0)),ell((0,.9,-.1),(.11,.13,.018),(-6,0,0))]   # buckle, loincloth front and back
    for k in range(3):P.append(ell((0,1.54+k*.03,-.02),(.023,.015,.023)))                                # neck
    # the skull: round cranium, deep sockets, cheekbones, teeth, and a jaw hanging loose
    P+=[ell((0,1.725,-.02),(.104,.108,.112)),ell((0,1.705,.1),(.088,.02,.03)),ell((0,1.668,.108),(.011,.026,.016)),ell((0,1.622,.082),(.064,.034,.05))]
    P+=sym(lambda d:ell((d*.066,1.645,.09),(.03,.022,.036)))+sym(lambda d:ell((d*.088,1.68,.05),(.022,.04,.05)))                 # cheekbones, temples
    for k in range(6):P.append(spike((-.045+k*.018,1.605,.115),(-.045+k*.018,1.58,.12),.008))
    P+=[ell((0,1.535,.075),(.068,.024,.06),(-25,0,0))]+sym(lambda d:mcap((d*.06,1.55,.03),(d*.065,1.6,.02),.012))
    for k in range(5):P.append(spike((-.036+k*.018,1.548,.112),(-.036+k*.018,1.566,.118),.007))
    P+=[ell((0,1.785,-.01),(.116,.075,.128)),ell((0,1.745,-.01),(.122,.016,.134)),ell((0,1.855,-.01),(.016,.02,.1))]   # iron cap
    for d in (1,-1):
        P.append(mcap((d*.22,1.47,0),(d*.27,1.2,.04),.022));P.append(ell((d*.27,1.2,.04),(.028,.026,.026)))
        P.append(mcap((d*.268,1.2,.035),(d*.3,.97,.14),.016));P.append(mcap((d*.278,1.19,.045),(d*.31,.96,.13),.013))
        P.append(mcap((d*.24,1.41,.02),(d*.262,1.26,.04),.018))
        P.append(ell((d*.305,.94,.155),(.032,.022,.038)))
        P+=claws(d,(.305,.935,.165),n=4,L=.065,r=.008,spread=.022,down=.5)
        P.append(ell((d*.105,.9,.01),(.07,.09,.07)))                                                     # ragged breeches, short
        P.append(mcap((d*.105,.84,.02),(d*.12,.58,.05),.025));P.append(ell((d*.12,.565,.06),(.034,.036,.034)))   # bare femur, knee
        P.append(mcap((d*.12,.55,.055),(d*.11,.12,-.01),.021));P.append(mcap((d*.125,.52,.04),(d*.115,.14,-.01),.016))
        P.append(mcap((d*.122,.46,.04),(d*.116,.28,.0),.03))                                              # wraps
        P.append(ell((d*.11,.07,0),(.04,.035,.04)))
        for t in range(4):P.append(horn([(d*(.09+t*.014),.05,.03),(d*(.09+t*.016),.025,.11),(d*(.09+t*.017),.012,.15)],[.012,.01,.006]))   # bony toes
    J={'hip':(0,1.0,0),'waist':(0,1.18,0),'chest':(0,1.45,0),'neckt':(0,1.56,.0),'face':(0,1.66,.2),'sh':(.22,1.47,0),'el':(.27,1.2,.04),'wr':(.3,.96,.14),'hp':(.1,.98,0),'kn':(.12,.56,.06),'an':(.11,.09,-.01)}
    return P,biped_bones(J)
def draugr_color(g,n):
    x,y,z=g;ax=abs(x)
    bone=mix((.7,.63,.48),(.42,.36,.24),sm(.45,.8,fbm(x*14,y*14,z*14))*.7)
    bone=mix(bone,(.3,.33,.2),sm(.6,.85,fbm(x*6+3,y*6,z*6))*.55)                                        # green rot
    leather=mix((.3,.2,.12),(.2,.13,.08),fbm(x*10,y*10,z*10))
    iron=mix((.36,.25,.18),(.22,.2,.19),sm(.4,.7,fbm(x*20,y*20,z*20)))
    c=bone
    if 1.65<y<1.698 and .014<ax<.064 and z>.07:c=(.05,.04,.03)
    elif 1.62<y<1.66 and ax<.012 and z>.09:c=(.06,.05,.04)
    elif y>1.735 and (y>1.75 or z<.06 or ax>.09):c=iron
    elif (z<-.075 and 1.08<y<1.52 and ax>.035) or (1.45<y<1.56 and ax>.15 and ax<.34) or (1.44<y<1.52 and z<-.02 and ax<.2):c=leather
    elif 1.1<y<1.45 and ax>.16 and ax<.24 and z<.09:c=leather       # the vest fronts
    elif .99<y<1.075 and ax<.2:c=iron if (z>.12 and ax<.04) else leather
    elif .76<y<.99 and ax<.2:c=mix((.3,.26,.19),(.2,.17,.12),fbm(x*9,y*9,z*9))
    elif .26<y<.48 and ax>.07:c=mix((.32,.27,.2),(.22,.19,.14),fbm(x*12,y*12,z*12))
    elif y<.1 and z<.06:c=leather
    if ax>.22 and 1.26<y<1.42 and z>-.01 and z<.06:c=mix((.32,.24,.15),(.22,.16,.1),fbm(x*15,y*15,z*15))   # sinew
    if (1.45<y<1.56 and ax>.15 and ax<.34) and fbm(x*40,y*40,z*40)>.7:c=iron                            # studs
    return c
_p,_b=draugr();SPECS['draugr']={'name':'draugr','parts':_p,'bones':_b,'color':draugr_color,'iface':dict(BIPED_IF,mat='bone'),'view':2.2,'voxel':.0065,'tris':16000,'ao':1.1,'aodist':.18}

# ---- Barrow Knight: a towering armoured dead lord — great-helm with a dark slit, layered pauldrons, ridged breastplate, faulds, plated legs ----
def barrowknight():
    P=[]
    # great-helm: a tall flat-faced bucket with a vertical ridge, a dark eye slit and breathing holes
    P+=[ell((0,2.3,-.01),(.13,.15,.14)),ell((0,2.2,0),(.135,.1,.14)),ell((0,2.25,.1),(.115,.15,.05)),ell((0,2.25,.152),(.016,.14,.016)),ell((0,2.43,-.02),(.11,.03,.12))]
    P+=[ell((0,2.09,.01),(.15,.06,.135)),ell((0,2.04,.01),(.17,.04,.15))]                                                       # gorget lames
    P+=[ell((0,1.88,.03),(.3,.2,.2)),ell((0,1.66,.02),(.21,.13,.16)),ell((0,1.86,.2),(.022,.16,.025)),ell((0,1.96,-.06),(.28,.12,.15))]   # breastplate: broad chest, narrow waist
    for d in (1,-1):
        P+=[ell((d*.34,2.02,0),(.18,.11,.18),(0,0,d*-22)),ell((d*.41,1.93,0),(.15,.06,.16),(0,0,d*-30)),ell((d*.46,1.85,.01),(.12,.05,.14),(0,0,d*-38)),ell((d*.22,2.12,0),(.02,.07,.13))]   # pauldrons with a raised guard at the neck
        P+=[mcap((d*.38,1.9,0),(d*.445,1.58,.06),.075),ell((d*.45,1.56,.06),(.08,.075,.08)),ell((d*.5,1.56,.04),(.03,.06,.06)),mcap((d*.45,1.55,.07),(d*.48,1.26,.16),.065)]
        P+=[ell((d*.485,1.24,.17),(.095,.06,.1)),ell((d*.49,1.15,.19),(.07,.07,.085))]                                         # flared gauntlet cuff and hand
        P+=[horn([(d*(.47+k*.018),1.12,.23),(d*(.47+k*.02),1.05,.27),(d*(.47+k*.021),.99,.26)],[.03,.026,.02]) for k in range(-1,3)]
        P+=[ell((d*.16,1.29,.07),(.11,.12,.04),(10,0,0))]                                                                     # tassets over the thighs
        P+=[mcap((d*.14,1.22,0),(d*.165,.74,.06),.1),ell((d*.165,.7,.09),(.08,.08,.08)),ell((d*.21,.7,.07),(.025,.07,.06))]   # cuisse, poleyn and its fan
        P+=[mcap((d*.162,.66,.07),(d*.152,.4,.02),.085),mcap((d*.152,.4,.02),(d*.15,.16,-.01),.068),ell((d*.15,.08,.05),(.08,.07,.17))]   # greave swelling at the calf, sabaton
    P+=[ell((0,1.5,0),(.22,.07,.16)),ell((0,1.42,.01),(.25,.05,.18)),ell((0,1.35,0),(.27,.05,.19))]                           # faulds
    P+=[ell((0,2.02,-.13),(.33,.08,.14))]
    J={'hip':(0,1.25,0),'waist':(0,1.5,0),'chest':(0,1.9,0),'neckt':(0,2.12,.02),'face':(0,2.22,.25),'sh':(.38,1.95,0),'el':(.45,1.56,.06),'wr':(.485,1.22,.16),'hp':(.14,1.22,0),'kn':(.165,.7,.08),'an':(.15,.12,-.01)}
    return P,biped_bones(J)
def knight_color(g,n):
    x,y,z=g;ax=abs(x)
    iron=mix((.17,.17,.18),(.09,.09,.1),sm(.4,.75,fbm(x*9,y*9,z*9)))
    iron=mix(iron,(.42,.42,.44),sm(.55,.95,n[1]*.5+abs(n[0])*.3)*.35)                                     # worn bright where edges catch the light
    iron=mix(iron,(.3,.2,.14),sm(.65,.85,fbm(x*14+5,y*14,z*14))*.5)                                       # rust bloom
    c=iron
    if 2.255<y<2.285 and z>.12 and .02<ax<.1:c=(.01,.01,.01)                                              # the eye slit
    if 2.14<y<2.22 and z>.12 and .03<ax<.09 and fbm(x*60,y*60,z*60)>.62:c=(.02,.02,.02)                   # breathing holes
    if (z<-.04 and 1.92<y<2.12) or (y>1.9 and y<2.1 and z<-.1):c=mix((.07,.065,.07),(.12,.11,.11),fbm(x*8,y*8,z*8))   # mantle
    if ax>.42 and 1.3<y<1.52 and fbm(x*30,y*30,z*30)>.78:c=(.75,.22,.06)                                   # embers in the cracks of the vambraces
    return c
_p,_b=barrowknight();SPECS['barrowknight']={'name':'barrowknight','parts':_p,'bones':_b,'color':knight_color,'iface':dict(BIPED_IF,mat='metal'),'view':2.9,'voxel':.009,'tris':12000}

# ---- Ghoul: a hunched corpse-eater — grey-blue starved body, sunken face with a gaping mouth, long arms and claws, bone necklace ----
def ghoul():
    P=[]
    # starved, hunched trunk: a deep ribcage over a hollow belly, sharp hips, a ridge of vertebrae down the bent back
    P+=[ell((0,.96,-.045),(.135,.075,.095)),ell((0,1.07,-.01),(.095,.09,.07)),ell((0,1.3,.05),(.138,.165,.105),(-30,0,0)),ell((0,1.4,.09),(.155,.06,.095),(-30,0,0))]
    P+=[neg((0,1.12,.085),(.075,.05,.035))]                                                                   # the belly sucked in under the ribs
    for k in range(5):
        y=1.39-k*.05;w=.145-k*.004;P+=sym(lambda d:horn([(d*.03,y+.01,.165-k*.012),(d*w*.7,y,.15-k*.012),(d*w,y-.03,.07-k*.006),(d*w*.9,y-.06,-.01),(d*w*.5,y-.07,-.05)],[.011,.012,.012,.011,.009]))
    P+=[ell((0,1.3,.165),(.022,.1,.012),(-30,0,0))]                                                       # sternum
    for k in range(9):a2=k/8;P.append(ell((0,1.0+a2*.47,-.06+a2*a2*.16-(.03 if a2>.3 else 0)),(.022,.017,.022)))   # vertebrae
    P+=sym(lambda d:ell((d*.1,1.36,-.0),(.065,.085,.016),(25,d*25,0)))                                     # shoulder blades
    P+=sym(lambda d:horn([(d*.025,1.47,.2),(d*.11,1.48,.17),(d*.19,1.45,.1)],[.013,.012,.012]))            # collarbones
    P+=[mcap((0,1.43,.16),(0,1.5,.3),.037),ell((0,1.47,.25),(.03,.05,.02),(30,0,0))]                     # stringy neck, throat
    # long gaunt skull: high cranium, heavy brow, sunken sockets, cheekbones like blades, the jaw hanging wide
    P+=[ell((0,1.575,.33),(.088,.095,.115),(-10,0,0)),ell((0,1.578,.425),(.072,.02,.028)),ell((0,1.518,.445),(.062,.032,.05)),ell((0,1.547,.468),(.01,.018,.013))]
    P+=sym(lambda d:neg((d*.036,1.553,.452),(.022,.016,.02)))
    P+=sym(lambda d:ell((d*.062,1.528,.425),(.022,.014,.034)))+sym(lambda d:ell((d*.075,1.5,.39),(.012,.03,.03)))
    P+=sym(lambda d:horn([(d*.08,1.58,.31),(d*.115,1.6,.28),(d*.13,1.635,.26)],[.016,.01,.003]))         # small torn ears
    P+=[ell((0,1.42,.41),(.056,.022,.062),(34,0,0)),ell((0,1.47,.39),(.05,.04,.05)),mcap((0,1.47,.37),(0,1.43,.41),.03)]+sym(lambda d:mcap((d*.052,1.5,.4),(d*.05,1.43,.39),.009))   # jaw and the cords of the cheeks
    for k in range(7):P.append(spike((-.042+k*.014,1.494,.47-abs(k-3)*.004),(-.042+k*.014,1.465,.474-abs(k-3)*.004),.006))
    for k in range(6):P.append(spike((-.035+k*.014,1.437,.452-abs(k-2.5)*.004),(-.035+k*.014,1.466,.458),.005))
    for d in (1,-1):
        # long thin arms with knotted elbows and big hooked hands
        P+=[mcap((d*.19,1.42,.1),(d*.29,1.09,.18),.034),ell((d*.205,1.33,.12),(.045,.07,.045)),ell((d*.295,1.08,.17),(.036,.034,.034)),ell((d*.29,1.08,.15),(.022,.022,.03))]
        P+=[mcap((d*.295,1.07,.19),(d*.335,.75,.29),.027),mcap((d*.31,1.0,.21),(d*.33,.8,.27),.022),ell((d*.34,.71,.31),(.048,.03,.06))]
        P+=claws(d,(.345,.69,.33),n=4,L=.13,r=.011,spread=.03,down=.6)
        P+=[horn([(d*.32,.71,.3),(d*.29,.68,.34),(d*.285,.65,.37)],[.011,.009,.003])]                    # thumb
        # bony legs: thin thighs, swollen knees, sinewy shins, long-toed feet
        P+=[mcap((d*.11,.94,-.04),(d*.14,.53,.1),.042),ell((d*.14,.52,.11),(.04,.045,.04)),mcap((d*.14,.5,.09),(d*.13,.11,-.03),.03),mcap((d*.135,.45,.06),(d*.128,.2,-.0),.028)]
        P+=[ell((d*.13,.05,.03),(.045,.03,.1))]+[horn([(d*(.1+t*.02),.04,.1),(d*(.1+t*.022),.02,.19),(d*(.1+t*.024),.0,.24)],[.011,.009,.003]) for t in range(4)]
    P+=[ell((0,.9,-.03),(.1,.06,.085))]   # loincloth on a cord
    J={'hip':(0,.95,-.05),'waist':(0,1.15,0),'chest':(0,1.42,.12),'neckt':(0,1.5,.27),'face':(0,1.52,.45),'sh':(.2,1.42,.1),'el':(.3,1.08,.18),'wr':(.34,.72,.3),'hp':(.11,.93,-.05),'kn':(.14,.52,.1),'an':(.13,.08,-.03)}
    return P,biped_bones(J)
def ghoul_color(g,n):
    x,y,z=g;ax=abs(x)
    c=mix((.27,.28,.28),(.15,.16,.17),sm(.4,.8,fbm(x*11,y*11,z*11)))                                      # cold grey-blue dead skin
    c=mix(c,(.21,.25,.16),sm(.5,.85,fbm(x*4+2,y*4,z*4+1))*.6)                                             # green rot spreading in patches
    c=mix(c,(.3,.34,.36),sm(.3,.9,n[1])*.2)                                                                 # dust settled on the tops
    bru=0
    for jx,jy,jz,rr in ((.295,1.08,.17,.07),(.14,.52,.11,.07),(.34,.7,.31,.09),(.205,1.36,.12,.07),(.13,.06,.05,.08)):
        bru=max(bru,1-min(1,math.sqrt((ax-jx)**2+(y-jy)**2+(z-jz)**2)/rr))
    c=mix(c,(.27,.15,.28),sm(0,1,bru)*.5)                                                                    # purple bruising pooled at the joints
    if ax>.29 and y<.72 and z>.33:c=mix(c,(.06,.05,.05),sm(.7,.62,y))                                     # black, cracked claws
    if y<.03 and z>.18:c=mix(c,(.06,.05,.05),.8)
    if 1.44<y<1.5 and ax<.055 and z>.41:c=(.32,.06,.28)                                                   # the mouth, livid purple inside
    if 1.535<y<1.575 and .014<ax<.06 and z>.425:c=(.03,.02,.04)                                           # sunken sockets
    if 1.5<y<1.6 and .02<ax<.08 and z>.38:c=mix(c,(.25,.12,.26),.4)                                       # bruised around the eyes
    rib=1.1<y<1.4 and z>.03 and ax>.05
    if rib:c=mix(c,(.3,.32,.32),sm(.0,.8,n[1]+n[2]*.3)*.25)
    if .84<y<.98 and ax<.12:c=mix((.22,.16,.11),(.12,.09,.06),fbm(x*14,y*14,z*14))                        # a filthy wrap
    return c
_p,_b=ghoul();SPECS['ghoul']={'name':'ghoul','parts':_p,'bones':_b,'color':ghoul_color,'iface':dict(BIPED_IF,mat='skin'),'view':2.0,'voxel':.0055,'tris':14000,'ao':1.0,'aodist':.2}

# ---------------- REDMANE RAVAGER: a hunched, knuckle-walking ape-wolf of the Sunmeads nights ----------------
def ravager():
    P=[]
    # a towering hump of shoulder over a tucked waist and narrow hips
    P+=[ell((0,1.4,.2),(.34,.4,.4),(-12,0,0)),ell((0,1.62,.0),(.29,.22,.34),(-8,0,0)),ell((0,1.17,-.27),(.22,.24,.3),(10,0,0)),ell((0,1.04,-.58),(.23,.23,.24))]
    P+=sym(lambda d:ell((d*.2,1.3,.33),(.15,.2,.18),(0,0,d*15)))                                          # chest slabs
    P+=sym(lambda d:ell((d*.3,1.47,.2),(.16,.17,.18)))                                                    # shoulder caps
    P+=[ell((0,1.55,.36),(.31,.28,.3),(-25,0,0))]                                                         # the base of the mane
    # long neck thrust low, a heavy wolfish skull, a grey bone jaw hanging open
    P+=[mcap((0,1.5,.45),(0,1.36,.76),.14),ell((0,1.38,.84),(.17,.15,.19),(-8,0,0)),mcap((0,1.33,.95),(0,1.27,1.15),.085),ell((0,1.28,1.17),(.042,.032,.032))]
    P+=sym(lambda d:ell((d*.075,1.42,.93),(.045,.022,.05),(0,0,d*-12)))                                  # brow ridges
    P+=sym(lambda d:ell((d*.1,1.31,.86),(.05,.06,.07)))                                                   # jaw muscles
    P+=[ell((0,1.18,.99),(.075,.035,.14),(-14,0,0)),ell((0,1.205,.9),(.085,.04,.08))]                    # lower jaw
    for k in range(5):
        x=-.044+k*.022
        P.append(spike((x,1.26,1.09-abs(k-2)*.02),(x,1.2,1.11-abs(k-2)*.02),.008))
        P.append(spike((x*.9,1.205,1.07-abs(k-2)*.02),(x*.9,1.255,1.085-abs(k-2)*.02),.007))
    P+=sym(lambda d:spike((d*.05,1.27,1.06),(d*.053,1.17,1.08),.012))                                   # long canines
    P+=sym(lambda d:spike((d*.045,1.2,1.04),(d*.05,1.29,1.06),.01))
    P+=sym(lambda d:horn([(d*.1,1.47,.78),(d*.15,1.56,.7),(d*.17,1.62,.62)],[.03,.018,.004]))           # swept ears
    # the mane: heavy clumps of fur swept back off the neck and shoulders, drooping at the tips like a wet lion's mane
    import math,random
    rnd=random.Random(7)
    for r_ in range(5):
        t=r_/4;cy=1.52+t*.16;cz=.6-t*.62;rad=.22+math.sin(t*math.pi)*.12
        for j in range(9):
            a=math.radians(-112+j*28+(r_%2)*14+rnd.uniform(-6,6));sx=math.sin(a);cyy=math.cos(a)
            b=(sx*rad,cy+cyy*rad*.85,cz);L_=(.3+.16*math.sin(t*math.pi))*rnd.uniform(.8,1.2)
            dx,dy,dz=sx*.6,cyy*.45+.15,-.8
            dl=math.sqrt(dx*dx+dy*dy+dz*dz);dx,dy,dz=dx/dl,dy/dl,dz/dl
            m=(b[0]+dx*L_*.45,b[1]+dy*L_*.45+.03,b[2]+dz*L_*.45);tp=(b[0]+dx*L_*.95,b[1]+dy*L_*.6-.09,b[2]+dz*L_)
            P.append(horn([b,m,tp],[.085,.05,.006]))
    # arms: long, roped with muscle, walking on knuckles; shaggy pale fur at the elbows and down the forearms
    for d in (1,-1):
        P+=[mcap((d*.32,1.44,.22),(d*.38,.88,.3),.13),ell((d*.36,1.2,.26),(.15,.21,.15)),ell((d*.34,1.32,.33),(.1,.12,.1)),ell((d*.38,.86,.29),(.1,.09,.1))]
        P+=[mcap((d*.38,.86,.3),(d*.35,.2,.42),.1),ell((d*.38,.62,.35),(.13,.21,.12)),ell((d*.35,.12,.46),(.11,.075,.13))]
        for k in range(3):
            y=.9-k*.13;P.append(horn([(d*.4,y,.22),(d*(.46+k*.01),y-.08,.13),(d*(.47+k*.01),y-.2,.08)],[.06,.035,.005]))
        P.append(horn([(d*.47,.78,.3),(d*.56,.7,.27),(d*.6,.58,.25)],[.05,.03,.004]))
        for k in range(4):
            x=d*(.3+k*.03);P.append(horn([(x,.1,.53),(x,.09,.62),(x,.03,.7),(x,-.01,.72)],[.022,.018,.01,.002]))
        # hind legs: thick thigh, a long hock, a splayed paw
        P+=[mcap((d*.21,1.02,-.55),(d*.25,.6,-.42),.13),ell((d*.22,.86,-.52),(.15,.22,.18)),mcap((d*.25,.6,-.42),(d*.24,.3,-.78),.07),mcap((d*.24,.3,-.78),(d*.22,.05,-.62),.06)]
        P+=[ell((d*.22,.04,-.55),(.08,.04,.12))]+[horn([(d*(.19+k*.02),.04,-.46),(d*(.19+k*.022),.02,-.4),(d*(.19+k*.024),-.01,-.36)],[.016,.012,.002]) for k in range(4)]
        for k in range(3):P.append(horn([(d*.26,.55-k*.08,-.47),(d*.32,.5-k*.08,-.53),(d*.34,.42-k*.08,-.56)],[.04,.022,.004]))
    # a long whip of a tail ending in a tuft
    P+=[cap([(0,1.08,-.78),(0,1.0,-1.0),(0,.85,-1.25),(0,.72,-1.5),(0,.66,-1.72)],[.07,.06,.045,.03,.02])]
    for k in range(6):a=k/6*6.283;P.append(horn([(0,.67,-1.68),(math.cos(a)*.06,.66+math.sin(a)*.06,-1.82),(math.cos(a)*.09,.64+math.sin(a)*.08,-1.94)],[.035,.02,.003]))
    J={'root':(0,1.06,-.58),'back':(0,1.22,-.2),'chest':(0,1.45,.25),'neck':(0,1.48,.5),'head':(0,1.38,.82),'nose':(0,1.28,1.16),'tail':(0,1.08,-.78),'tailtip':(0,.66,-1.72),
       'earL':(.1,1.47,.78),'eartipL':(.17,1.62,.62),'earR':(-.1,1.47,.78),'eartipR':(-.17,1.62,.62)}
    for d,t in ((1,'L'),(-1,'R')):J.update({'fl'+t:(d*.32,1.44,.22),'fe'+t:(d*.38,.86,.3),'fh'+t:(d*.35,.08,.46),'hl'+t:(d*.21,1.02,-.55),'hs'+t:(d*.24,.32,-.76),'hp'+t:(d*.22,.03,-.56)})
    return P,quad_bones(J)
def ravager_color(g,n):
    import math
    x,y,z=g;ax=abs(x)
    c=mix((.27,.07,.055),(.13,.035,.03),sm(.35,.8,fbm(x*6,y*6,z*6)))                                     # deep crimson hide
    c=mix(c,(.36,.11,.07),sm(.2,.9,n[1])*.3)                                                           # sheen on the tops of the muscle
    c=mix(c,(.14,.02,.02),sm(.1,-.6,n[1])*.5)                                                          # dark under the belly
    d_m=math.sqrt(ax*ax+(y-1.58)**2*.8)                                                                 # distance out from the neck line
    mane=1.38<y and -.2<z<.78 and d_m>.24
    if mane:c=mix(mix((.42,.12,.06),(.3,.08,.05),fbm(x*12,y*12,z*12)),(.06,.02,.02),sm(.3,.55,d_m))                                          # rust-red mane darkening to black tips
    fz=sm(.78,.45,y+fbm(x*9,y*9,z*9)*.18)*(1 if (ax>.26 and z>.05) else sm(.6,.35,y) if (z<-.3 and ax>.18) else 0)
    c=mix(c,mix((.58,.5,.42),(.38,.31,.26),fbm(x*20,y*20,z*20)),fz*.9)                                        # pale shaggy fur on forearms and hocks
    if z>.5 and y<.12 and ax>.28:c=mix((.22,.22,.24),(.42,.43,.46),sm(.6,.72,z))                       # iron-grey claws
    if z<-.36 and y<.05 and ax>.16:c=(.2,.2,.22)
    if z>.9 and 1.13<y<1.215 and ax<.085:c=mix((.22,.21,.2),(.36,.34,.31),sm(.92,1.08,z))
    if z>.95 and 1.215<=y<1.25 and ax<.07:c=(.12,.02,.02)                  # the bone jaw plate
    if z>1.04 and (1.19<y<1.215 or 1.245<y<1.27) and ax<.065:c=(.72,.66,.55)                                              # teeth
    if z>1.13 and y>1.25 and ax<.05:c=(.04,.03,.03)                                                    # nose
    if 1.37<y<1.43 and .045<ax<.1 and z>.9:c=(.05,.01,.01)                                             # sunken eyes
    if z<-1.55:c=mix((.09,.02,.02),(.6,.15,.08),sm(-1.6,-1.9,z))                                       # tail tuft
    return c
_p,_b=ravager();SPECS['ravager']={'name':'ravager','parts':_p,'bones':_b,'color':ravager_color,'shape':fur_shape(.02,lambda g,n:g[1]>1.3 or abs(g[0])>.3),'view':3.0,'voxel':.011,'tris':16000,'ao':.6,'aodist':.25}
