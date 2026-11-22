# Blender: sculpt one-piece creatures from overlapping masses.
# parts: ellipsoids {'e':centre,'r':(rx,ry,rz),'rot':(deg x,y,z)}, tapered limbs {'c':[p0,p1,...],'r':[r0,r1,...]},
# branching thin structures (antlers, horns, claws) as skin graphs {'skin':[(name,parent,pos,radius)]}.
# All fused by a voxel remesh, smoothed so joins blend like sculpted muscle, decimated, rigged with the spec's bones.
import bpy, sys, json, math, struct, importlib, mathutils
sys.path.insert(0,'/home/claude/beasts');import specs;importlib.reload(specs)
cv=lambda p:mathutils.Vector((p[0],-p[2],p[1]))
bk=lambda v:(v[0],v[2],-v[1])
def link(ob):bpy.context.scene.collection.objects.link(ob);return ob
def ellipsoid(e,r,rot):
    me=bpy.data.meshes.new('e');import bmesh;bm=bmesh.new();bmesh.ops.create_uvsphere(bm,u_segments=24,v_segments=16,radius=1);bm.to_mesh(me);bm.free()
    ob=link(bpy.data.objects.new('e',me));ob.scale=(r[0],r[2],r[1]);ob.rotation_mode='XYZ'
    ob.rotation_euler=(math.radians(-rot[0]) if rot else 0,math.radians(-(rot[2] if rot else 0)),math.radians(rot[1]) if rot else 0)
    ob.location=cv(e);return ob
def skinmesh(nodes,sub=2):
    idx={n[0]:i for i,n in enumerate(nodes)};me=bpy.data.meshes.new('s');me.from_pydata([cv(n[2]) for n in nodes],[(idx[n[1]],i) for i,n in enumerate(nodes) if n[1]],[]);me.update()
    ob=link(bpy.data.objects.new('s',me));m=ob.modifiers.new('Skin','SKIN');sv=me.skin_vertices[0].data
    for i,n in enumerate(nodes):r=n[3] if isinstance(n[3],(tuple,list)) else (n[3],n[3]);sv[i].radius=r;sv[i].use_root=(i==0)
    s=ob.modifiers.new('Sub','SUBSURF');s.levels=sub;return ob
def build(sp):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    obs=[]
    # body masses are metaballs so they melt into each other like flesh
    mb=bpy.data.metaballs.new('mb');mo=link(bpy.data.objects.new('mb',mb));mb.resolution=sp.get('mbres',.014);mb.render_resolution=mb.resolution;mb.threshold=.6
    for p in sp['parts']:
        if 'e' in p:
            e=mb.elements.new();e.type='ELLIPSOID';e.stiffness=2;e.radius=1/.575;r=p['r'];e.size_x=r[0]*p.get('k',1);e.size_y=r[2]*p.get('k',1);e.size_z=r[1]*p.get('k',1);e.co=cv(p['e']);e.use_negative=bool(p.get('neg'))
            rot=p.get('rot') or (0,0,0);q=mathutils.Euler((math.radians(-rot[0]),math.radians(-rot[2]),math.radians(rot[1])),'XYZ').to_quaternion();e.rotation=q
        elif 'mc' in p:
            a=cv(p['mc'][0]);b=cv(p['mc'][1]);d=b-a;e=mb.elements.new();e.type='CAPSULE';e.stiffness=2;e.radius=p['r']/.575;e.size_x=d.length/2;e.co=(a+b)/2
            e.rotation=mathutils.Vector((1,0,0)).rotation_difference(d.normalized())
    bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();bm_me=bpy.data.meshes.new_from_object(mo.evaluated_get(dg));bobj=link(bpy.data.objects.new('body',bm_me));bpy.data.objects.remove(mo);obs.append(bobj)
    for p in sp['parts']:
        if 'e' in p or 'mc' in p:pass
        elif 'c' in p:
            pts=p['c'];rs=p['r'];nodes=[('n%d'%i,('n%d'%(i-1) if i else None),pts[i],rs[i]) for i in range(len(pts))];obs.append(skinmesh(nodes,p.get('sub',2)))
        elif 'skin' in p:obs.append(skinmesh(p['skin'],p.get('sub',2)))
    # apply modifiers and join
    for ob in obs:
        bpy.context.view_layer.objects.active=ob
        for m in list(ob.modifiers):bpy.ops.object.modifier_apply(modifier=m.name)
        ob.select_set(True)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in obs:ob.select_set(True)
    bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);bpy.ops.object.join()
    ob=bpy.context.view_layer.objects.active;ob.name=sp['name']
    rm=ob.modifiers.new('R','REMESH');rm.mode='VOXEL';rm.voxel_size=sp.get('voxel',.012);rm.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier='R')
    # drop loose crumbs left by spike tips thinner than the voxel size
    import bmesh as _bm;bm=_bm.new();bm.from_mesh(ob.data);bm.verts.ensure_lookup_table();seen=set();kill=[]
    for v in bm.verts:
        if v.index in seen:continue
        stack=[v];isl=[];seen.add(v.index)
        while stack:
            a=stack.pop();isl.append(a)
            for e in a.link_edges:
                o=e.other_vert(a)
                if o.index not in seen:seen.add(o.index);stack.append(o)
        if len(isl)<200:kill+=isl
    _bm.ops.delete(bm,geom=kill,context='VERTS');bm.to_mesh(ob.data);bm.free()
    sm=ob.modifiers.new('S','CORRECTIVE_SMOOTH') if False else ob.modifiers.new('S','SMOOTH');sm.factor=sp.get('sfac',.6);sm.iterations=sp.get('siter',12);bpy.ops.object.modifier_apply(modifier='S')
    me=ob.data
    if 'shape' in sp:
        for v in me.vertices:
            g=bk(v.co);n=bk(v.normal);ng=sp['shape'](g,n)
            if ng is not None:v.co=cv(ng)
    tgt=sp.get('tris',7000);nt0=sum(len(p.vertices)-2 for p in me.polygons)
    if nt0>tgt:dm=ob.modifiers.new('D','DECIMATE');dm.ratio=tgt/nt0;bpy.ops.object.modifier_apply(modifier='D')
    for p in ob.data.polygons:p.use_smooth=True
    # rig
    arm=bpy.data.armatures.new('Rig');rig=link(bpy.data.objects.new('Rig',arm));bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT');eb={}
    for b in sp['bones']:
        e=arm.edit_bones.new(b[0]);e.head=cv(b[2]);e.tail=cv(b[3]);eb[b[0]]=e
    for b in sp['bones']:
        if b[1]:eb[b[0]].parent=eb[b[1]]
    bpy.ops.object.mode_set(mode='OBJECT');bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    me=ob.data;me.calc_loop_triangles();bn=[b[0] for b in sp['bones']];gi={g.index:g.name for g in ob.vertex_groups}
    P=[];NR=[];C=[];SI=[];SW=[];nofit=0
    for v in me.vertices:
        g=bk(v.co);nn=bk(v.normal);P+=g;NR+=nn
        c=sp['color'](g,nn);C+=[max(0,min(255,int(x*255))) for x in c]
        ws=sorted([(gr.weight,bn.index(gi[gr.group])) for gr in v.groups if gi.get(gr.group) in bn and gr.weight>.01],reverse=True)[:4]
        if not ws:
            nofit+=1;ds=[]
            for k,b in enumerate(sp['bones']):
                a=mathutils.Vector(b[2]);t=mathutils.Vector(b[3]);d=t-a;q=mathutils.Vector(g);u=max(0,min(1,(q-a).dot(d)/max(1e-6,d.dot(d))));ds.append(((a+d*u-q).length,k))
            ds.sort();d0=ds[0][0]+1e-4;ws=[(1/((dd+1e-4)/d0)**6,k) for dd,k in ds[:3] if dd<d0*2.2]
        t=sum(w for w,_ in ws);ws=[(w/t,b) for w,b in ws]+[(0,0)]*(4-len(ws))
        SI+=[b for _,b in ws];SW+=[int(round(w*255)) for w,_ in ws]
    T=[]
    for t in me.loop_triangles:T+=[t.vertices[0],t.vertices[2],t.vertices[1]]
    nv=len(me.vertices);open('/home/claude/beasts/out/%s.bin'%sp['name'],'wb').write(struct.pack('<%df'%len(P),*P)+struct.pack('<%df'%len(NR),*NR)+bytes(C)+bytes(SI)+bytes(SW)+struct.pack('<%dI'%len(T),*T))
    json.dump({'name':sp['name'],'iface':sp.get('iface'),'nv':nv,'nt':len(T)//3,'bones':[{'n':b[0],'p':b[1],'h':list(b[2])} for b in sp['bones']]},open('/home/claude/beasts/out/%s.json'%sp['name'],'w'))
    col=me.color_attributes.new('Col','BYTE_COLOR','POINT')
    for i in range(nv):col.data[i].color=(C[i*3]/255,C[i*3+1]/255,C[i*3+2]/255,1)
    sc=bpy.context.scene;sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='STUDIO';sc.display.shading.color_type='VERTEX';sc.display.shading.show_cavity=True;sc.render.resolution_x=900;sc.render.resolution_y=600
    H=sp.get('view',2.0);camd=bpy.data.cameras.new('C');camd.type='ORTHO';camd.ortho_scale=H*1.55;cam=link(bpy.data.objects.new('C',camd));sc.camera=cam
    for tag,ang,el in (('side',90,84),('q',35,80),('front',0,86)):
        a=math.radians(ang);r=8;cam.location=(math.sin(a)*r,-math.cos(a)*r,H*.45+r*math.cos(math.radians(el)));cam.rotation_euler=(math.radians(el),0,a)
        sc.render.filepath='/home/claude/beasts/out/%s_%s.png'%(sp['name'],tag);bpy.ops.render.render(write_still=True)
    print('BUILT',sp['name'],nv,len(T)//3,len(sp['bones']),'unweighted',nofit)
for nm in sys.argv[sys.argv.index('--')+1:]:build(specs.SPECS[nm])
