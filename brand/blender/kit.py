import bpy, bmesh, math, sys, os, numpy as np
from mathutils import Vector
REPO = sys.argv[sys.argv.index("--")+1]
OUT  = sys.argv[sys.argv.index("--")+2]
VIEWS = sys.argv[sys.argv.index("--")+3].split(",")   # e.g. front,back,three
SAMPLES = int(sys.argv[sys.argv.index("--")+4])
def hexc(h, a=1):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    lin=lambda v: v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4
    return (lin(c[0]),lin(c[1]),lin(c[2]),a)
BODY, PANEL, THREAD, DEEP = "#7FB2DD", "#F1F2EF", "#F4D24A", "#2E5C8A"
INK = "#151617"

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# ---------- logo decals from the parts sheets ----------
def make_decal(sheet, box, name, rgb):
    img = bpy.data.images.load(f"{REPO}/brand/garments/logo/{sheet}")
    W,H = img.size; px = np.array(img.pixels[:], dtype=np.float32).reshape(H,W,4)
    x,y,w,h = box; pad=3
    crop = px[H-(y+h+pad):H-(y-pad), x-pad:x+w+pad, :].copy()
    a = np.clip((crop[...,0]-0.27)/0.5, 0, 1)
    crop[...,0],crop[...,1],crop[...,2] = rgb[0],rgb[1],rgb[2]; crop[...,3]=a
    out = bpy.data.images.new(name, crop.shape[1], crop.shape[0], alpha=True)
    out.pixels = crop.ravel().tolist(); out.pack(); out.colorspace_settings.name='sRGB'
    return out, crop.shape[1]/crop.shape[0]
ink_lin = hexc(INK)[:3]
SILVER=(0.78,0.79,0.80)
SYM, SYM_AR = make_decal("offnorm-logo-parts.png",(300,118,339,243),"sym",ink_lin)
WM,  WM_AR  = make_decal("offnorm-logo-full.png",(179,673,781,83),"wm",ink_lin)
WMR, _ = make_decal("offnorm-logo-full.png",(179,673,781,83),"wm_ref",SILVER)

# ---------- materials ----------
def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes=True; m.node_tree.nodes.clear(); return m
def jersey(name, col, ribs=None):
    m=new_mat(name); n=m.node_tree.nodes; l=m.node_tree.links
    out=n.new("ShaderNodeOutputMaterial"); b=n.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value=hexc(col); b.inputs["Roughness"].default_value=0.88
    b.inputs["Sheen Weight"].default_value=0.5; b.inputs["Sheen Roughness"].default_value=0.5
    tc=n.new("ShaderNodeTexCoord"); mp=n.new("ShaderNodeMapping")
    w=n.new("ShaderNodeTexWave"); w.wave_type='BANDS'; w.bands_direction='X'; w.inputs["Scale"].default_value=1; w.inputs["Distortion"].default_value=0.6
    ns=n.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value=500; ns.inputs["Detail"].default_value=2
    mx=n.new("ShaderNodeMath"); mx.operation='ADD'
    bump=n.new("ShaderNodeBump"); bump.inputs["Strength"].default_value=0.8; bump.inputs["Distance"].default_value=0.006
    l.new(tc.outputs["UV"],mp.inputs["Vector"]); mp.inputs["Scale"].default_value=(ribs or (150,150,1))
    l.new(mp.outputs["Vector"],w.inputs["Vector"]); l.new(tc.outputs["Object"],ns.inputs["Vector"])
    l.new(w.outputs["Fac"],mx.inputs[0]); l.new(ns.outputs["Fac"],mx.inputs[1])
    l.new(mx.outputs["Value"],bump.inputs["Height"]); l.new(bump.outputs["Normal"],b.inputs["Normal"])
    l.new(b.outputs["BSDF"],out.inputs["Surface"]); return m
def nylon_rib(name, col):
    m=new_mat(name); n=m.node_tree.nodes; l=m.node_tree.links
    out=n.new("ShaderNodeOutputMaterial"); b=n.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value=hexc(col); b.inputs["Roughness"].default_value=0.42
    b.inputs["Sheen Weight"].default_value=0.7; b.inputs["Anisotropic"].default_value=0.4
    tc=n.new("ShaderNodeTexCoord"); mp=n.new("ShaderNodeMapping"); w=n.new("ShaderNodeTexWave")
    w.wave_type='BANDS'; w.bands_direction='X'; w.wave_profile='SAW'; w.inputs["Scale"].default_value=1; w.inputs["Distortion"].default_value=0.0
    bump=n.new("ShaderNodeBump"); bump.inputs["Strength"].default_value=1.0; bump.inputs["Distance"].default_value=0.012
    l.new(tc.outputs["UV"],mp.inputs["Vector"]); mp.inputs["Scale"].default_value=(70,1,1)
    l.new(mp.outputs["Vector"],w.inputs["Vector"]); l.new(w.outputs["Fac"],bump.inputs["Height"])
    l.new(bump.outputs["Normal"],b.inputs["Normal"]); l.new(b.outputs["BSDF"],out.inputs["Surface"])
    # rib shading: darken the valleys a little
    mix=n.new("ShaderNodeMix"); mix.data_type='RGBA'; mix.inputs[6].default_value=hexc(col)
    dark=[c*0.78 for c in hexc(col)[:3]]+[1]; mix.inputs[7].default_value=dark
    l.new(w.outputs["Fac"],mix.inputs[0]); l.new(mix.outputs[2],b.inputs["Base Color"]); return m
def decal_mat(name, image):
    m=new_mat(name); n=m.node_tree.nodes; l=m.node_tree.links
    out=n.new("ShaderNodeOutputMaterial"); t=n.new("ShaderNodeTexImage"); t.image=image; t.extension='CLIP'
    b=n.new("ShaderNodeBsdfPrincipled"); b.inputs["Roughness"].default_value=0.7
    l.new(t.outputs["Color"],b.inputs["Base Color"]); l.new(t.outputs["Alpha"],b.inputs["Alpha"]); l.new(b.outputs["BSDF"],out.inputs["Surface"])
    m.surface_render_method='BLENDED' if hasattr(m,'surface_render_method') else None
    return m
M_TEE   = jersey("cotton jersey", BODY)
M_PANEL = jersey("cotton jersey panel", PANEL)
M_COLLAR= jersey("collar rib", "#6F9CC7", ribs=(120,120,1))
M_TIGHT = nylon_rib("nylon rib", BODY)
M_BAND  = nylon_rib("waistband", DEEP)
M_SYM = decal_mat("sym", SYM); M_WM = decal_mat("wm", WM)
def reflective_mat(name,image):
    m=new_mat(name); n=m.node_tree.nodes; l=m.node_tree.links
    out=n.new("ShaderNodeOutputMaterial"); t=n.new("ShaderNodeTexImage"); t.image=image; t.extension='CLIP'
    b=n.new("ShaderNodeBsdfPrincipled"); b.inputs["Metallic"].default_value=0.85; b.inputs["Roughness"].default_value=0.32
    b.inputs["Emission Color"].default_value=(1,1,1,1); b.inputs["Emission Strength"].default_value=0.0
    ns=n.new("ShaderNodeTexNoise"); ns.inputs["Scale"].default_value=2200; ns.inputs["Detail"].default_value=1
    bm=n.new("ShaderNodeBump"); bm.inputs["Strength"].default_value=0.5; bm.inputs["Distance"].default_value=0.003
    tc=n.new("ShaderNodeTexCoord"); l.new(tc.outputs["Object"],ns.inputs["Vector"]); l.new(ns.outputs["Fac"],bm.inputs["Height"]); l.new(bm.outputs["Normal"],b.inputs["Normal"])
    l.new(t.outputs["Color"],b.inputs["Base Color"]); l.new(t.outputs["Alpha"],b.inputs["Alpha"]); l.new(b.outputs["BSDF"],out.inputs["Surface"]); return m
M_REF = reflective_mat("reflective wordmark", WMR)

# ---------- geometry ----------
def tb(p): return (p[0], -p[2], p[1])          # three.js (x,y,z) -> Blender (x,-z,y)
def sup(c,n): return math.copysign(abs(c)**(2/n), c)
def grid_mesh(name, rows, cols, fn, mat, closed_v=False, off=(0,0,0), uvfn=None):
    verts=[]; faces=[]; uvs=[]
    C = cols
    for i in range(rows+1):
        for j in range(C+1 if not closed_v else C):
            u=i/rows; v=j/C
            p=tb(fn(u,v)); verts.append((p[0]+off[0],p[1]+off[1],p[2]+off[2]))
    stride = C+1 if not closed_v else C
    for i in range(rows):
        for j in range(C if closed_v else C):
            j2 = (j+1)%stride if closed_v else j+1
            faces.append((i*stride+j, i*stride+j2, (i+1)*stride+j2, (i+1)*stride+j))
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update()
    ob=bpy.data.objects.new(name,me); sc.collection.objects.link(ob)
    uvl=me.uv_layers.new(name="UV")
    for poly in me.polygons:
        for li in poly.loop_indices:
            vi=me.loops[li].vertex_index; i=vi//stride; j=vi%stride
            uvl.data[li].uv=(j/C, i/rows) if not closed_v else ((j/C), i/rows)
    for p in me.polygons: p.use_smooth=True
    bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bm.to_mesh(me); bm.free()
    ob.data.materials.append(mat); return ob

def torso(th_u,v):
    y=-0.55+th_u*1.02
    if y<=0.2: a=0.365-0.012*((y+0.55)/0.75); b=0.2
    else:
        t=(y-0.2)/0.27; a=0.13+(0.353-0.13)*math.sqrt(max(0,1-t*t)); b=0.2+(0.115-0.2)*t
    th=v*2*math.pi+math.pi/2*0  # full loop; th=0 at +x
    # front = +z: use th in [0,pi] for front
    fold=0.006*math.sin(y*21+math.cos(th)*5)*(1 if y<0.15 else 0)
    return [a*sup(math.cos(th),2.6), y, (b+fold)*sup(math.sin(th),2.6)]

def sleeve(sx,u0,u1,mat,name):
    x0,y0,x1,y1=0.206,0.296,0.56,0.066
    L=math.hypot(x1-x0,y1-y0); dx,dy=(x1-x0)/L,(y1-y0)/L
    def f(u,v):
        uu=u0+(u1-u0)*u; cx=x0+(x1-x0)*uu; cy=y0+(y1-y0)*uu; r=0.14-uu*0.04; ph=v*2*math.pi
        return [sx*(cx+r*math.cos(ph)*-dy), cy+r*math.cos(ph)*dx, r*0.8*math.sin(ph)]
    return grid_mesh(name,14,36,f,mat,closed_v=True)

TEE_OFF=(-0.78,0,0)
objs=[]
objs.append(grid_mesh("torso",70,72,torso,M_TEE,closed_v=True,off=TEE_OFF))
objs.append(sleeve(+1,0,1,M_TEE,"sleeve_left"))                     # viewer's right = wearer's left, no panel
objs.append(sleeve(-1,0,0.55,M_TEE,"sleeve_right_a"))               # wearer's right arm: body then white panel
objs.append(sleeve(-1,0.55,1,M_PANEL,"sleeve_right_b"))
for o in objs[1:]: o.location=Vector(TEE_OFF)
# collar
bpy.ops.mesh.primitive_torus_add(major_radius=1,minor_radius=0.085,major_segments=64,minor_segments=12,location=(TEE_OFF[0],0,0.468))
col=bpy.context.object; col.scale=(0.131,0.116,0.16); col.data.materials.append(M_COLLAR); bpy.ops.object.shade_smooth()

# tights (3/4): two tapered legs and a waistband, hanging beside the tee
TX=0.55
def leg(cx,name):
    def f(u,v):
        z=0.30-u*1.0; rx=0.185-0.085*u**0.9; ry=0.15-0.06*u**0.9
        th=v*2*math.pi; return [cx+rx*math.cos(th), z, ry*math.sin(th)]
    ob=grid_mesh(name,40,64,f,M_TIGHT,closed_v=True,off=(TX,0,0)); return ob
legL=leg(-0.185,"leg_l"); legR=leg(0.185,"leg_r")
def band(u,v):
    th=v*2*math.pi; return [0.372*math.cos(th)*1.0, 0.36-u*0.09, 0.158*math.sin(th)]
wb=grid_mesh("waistband",3,72,band,M_BAND,closed_v=True,off=(TX,0,0))
# drawcord-style tab
bpy.ops.mesh.primitive_cube_add(size=1,location=(TX+0.08,-0.165,0.305)); tab=bpy.context.object; tab.scale=(0.05,0.004,0.028); tab.data.materials.append(M_BAND)

# ---------- decals snapped to the cloth ----------
def decal(name, mat, ar, width, loc, target, direction, rotz=0, mode="XYZ"):
    bpy.ops.mesh.primitive_plane_add(size=1,location=loc)
    p=bpy.context.object; p.name=name; p.scale=(width,width/ar,1)
    p.rotation_mode=mode; p.rotation_euler=direction; bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.subdivide(number_cuts=10); bpy.ops.object.mode_set(mode='OBJECT')
    p.data.materials.append(mat)
    sw=p.modifiers.new("snap","SHRINKWRAP"); sw.target=target; sw.wrap_method='PROJECT'; sw.use_project_x=False
    sw.use_negative_direction=True; sw.use_positive_direction=True; sw.offset=0.0012
    sw.project_limit=0.5
    bpy.context.view_layer.update(); return p
# axes: plane faces +z by default. Front of tee faces -y: rotate -90 about X so normal points -y.
decal("sym_tee", M_SYM, SYM_AR, 0.15, (TEE_OFF[0],-0.4,0.22), objs[0], (math.radians(90),0,0))
decal("wm_tee_back", M_WM, WM_AR, 0.36, (TEE_OFF[0],0.4,0.22), objs[0], (math.radians(90),0,math.radians(180)))
decal("wm_tight", M_REF, WM_AR, 0.62, (TX+0.185+0.07,-0.2,-0.14), legR, (math.radians(90),0,math.radians(90)), mode="ZYX")
sc.render.engine='CYCLES'

# ---------- studio ----------
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True
bg=w.node_tree.nodes["Background"]; bg.inputs[0].default_value=(0.86,0.86,0.85,1); bg.inputs[1].default_value=1.0
sc.view_settings.view_transform='Standard'
bpy.ops.mesh.primitive_plane_add(size=60,location=(0,0,-1.25)); fl=bpy.context.object
fm=new_mat("floor"); fb=fm.node_tree.nodes.new("ShaderNodeBsdfPrincipled"); fb.inputs["Base Color"].default_value=(0.62,0.62,0.61,1); fb.inputs["Roughness"].default_value=1
fo=fm.node_tree.nodes.new("ShaderNodeOutputMaterial"); fm.node_tree.links.new(fb.outputs[0],fo.inputs[0]); fl.data.materials.append(fm)
def area(name,loc,energy,size,target=(0.0,0,-0.1)):
    bpy.ops.object.light_add(type='AREA',location=loc); L=bpy.context.object; L.data.energy=energy; L.data.size=size
    d=Vector(target)-Vector(loc); L.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); return L
area("key",(-2.5,-3.2,2.2),300,2.6); area("fill",(3.2,-2.4,0.8),110,3.2); area("rim",(0.5,3.0,2.0),200,2.0)
bpy.ops.object.camera_add(); cam=bpy.context.object; sc.camera=cam; cam.data.lens=85; cam.data.sensor_width=36
LIGHTS=[o for o in bpy.data.objects if o.type=='LIGHT']
def set_flash(on):
    for L in LIGHTS: L.data.energy = L.data.energy*0.08 if on else L.data.energy
    bg.inputs[1].default_value = 0.08 if on else 1.0
    M_REF.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 2.8 if on else 0.0
def shoot(view):
    if view=="flash": set_flash(True)
    if view=="front":  cam.location=(-0.12,-9.5,-0.05); tgt=(-0.12,0,-0.05); 
    elif view=="back": cam.location=(-0.12, 9.5,-0.05); tgt=(-0.12,0,-0.05)
    elif view=="three": cam.location=(-4.4,-8.0,0.55);  tgt=(-0.12,0,-0.05)
    elif view=="flash": cam.location=(0.55+0.2,-4.2,-0.1); tgt=(0.55+0.2,0,-0.1)
    elif view=="closetee":   cam.location=(-0.78,-4.2,0.2); tgt=(-0.78,0,0.15)
    elif view=="closetight": cam.location=(0.55+0.2,-4.2,-0.1); tgt=(0.55+0.2,0,-0.1)
    cam.rotation_euler=(Vector(tgt)-Vector(cam.location)).to_track_quat('-Z','Y').to_euler()
    sc.render.resolution_x=1800; sc.render.resolution_y=1200
    sc.cycles.samples=SAMPLES; sc.cycles.use_denoising=True
    sc.render.filepath=f"{OUT}/kit_{view}.png"; sc.render.image_settings.file_format='PNG'
    bpy.ops.render.render(write_still=True)
# back view: tee decal faces +y; camera behind sees it. Tights have no back logo.
for v in VIEWS: shoot(v)
