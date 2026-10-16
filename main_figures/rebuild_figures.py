"""Rebuild all six main figures from supplied arrays; no solves or smoothing."""
from pathlib import Path
import os,sys,json,copy,csv
sys.stdout.reconfigure(encoding="utf-8")
HERE=Path(__file__).resolve().parent
RUN=HERE
os.environ.setdefault("MPLCONFIGDIR",str(RUN/"cache/matplotlib"))
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
import numpy as np
import scipy.linalg as la
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap,LogNorm
from matplotlib.ticker import NullLocator,MaxNLocator
from matplotlib.collections import LineCollection,QuadMesh
from matplotlib.text import Text
from matplotlib.mathtext import MathTextParser
from pypdf import PdfReader,PdfWriter,Transformation
from PIL import Image
from classic_cavity_vector import draw_classic_cavity
DATA=HERE/"data";FIG=RUN/"figures";PRE=RUN/"preview_after";ED=RUN/"R423_editorial"
for p in [FIG,PRE,ED,HERE/"plotted_data",RUN/"cache"]:p.mkdir(parents=True,exist_ok=True)
BLUE="#2F5B8E";TEAL="#B23A2B";PURPLE="#7B6085";GOLD="#9A6A2A";GRAY="#363C42";SLATE="#6D7E8A";LIGHT="#D4D6D8"
BWEAK="#9BB1C9";DWEAK="#D88E85"
DEEP_BLUE="#153F7A";RED="#D7191C"
BLUE_RED=LinearSegmentedColormap.from_list("blue_red_R421",[DEEP_BLUE,"#FAFAFA",RED])
FIELD=LinearSegmentedColormap.from_list("field_traditional",["#2A4356","#6E8794","#B7B7A4","#E8E3CF","#EFE3B0"])
SIGNED=LinearSegmentedColormap.from_list("signed_traditional",[BLUE,"#F8F7F3",TEAL])
for name in ["arial.ttf","ariali.ttf","arialbd.ttf"]:
 p=Path("C:/Windows/Fonts")/name
 if p.exists():fm.fontManager.addfont(str(p))
plt.rcParams.update({"font.family":"Arial","font.size":6.5,"axes.labelsize":6.5,"axes.titlesize":7,
 "xtick.labelsize":6,"ytick.labelsize":6,"legend.fontsize":6,"axes.linewidth":.78,
 "lines.linewidth":1.18,"lines.markersize":3.45,"axes.spines.top":True,"axes.spines.right":True,
 "xtick.major.size":2.9,"ytick.major.size":2.9,"xtick.major.width":.68,"ytick.major.width":.68,
 "xtick.major.pad":2.1,"ytick.major.pad":2.1,"axes.labelpad":2.6,"legend.frameon":False,
 "legend.handlelength":1.55,"legend.borderpad":.15,"legend.labelspacing":.25,
 "axes.edgecolor":"#3C4146","xtick.direction":"out","ytick.direction":"out",
 "pdf.fonttype":42,"svg.fonttype":"none","axes.unicode_minus":False,
 "mathtext.fontset":"custom","mathtext.rm":"Arial","mathtext.it":"Arial:italic","mathtext.bf":"Arial:bold",
 "mathtext.sf":"Arial","mathtext.fallback":"stixsans","savefig.facecolor":"white"})
import matplotlib._mathtext as mt
mt.SHRINK_FACTOR=.78  # Cross-platform consistent MathText sizing
if Path("C:/Windows/Fonts/symbol.ttf").exists():
 from fontTools.ttLib import TTFont
 from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
 from matplotlib._mathtext import UnicodeFonts,get_unicode_index
 import matplotlib._mathtext as mt
 sf=RUN/"cache/SymbolUnicode.ttf";sf.parent.mkdir(exist_ok=True)
 font=TTFont("C:/Windows/Fonts/symbol.ttf");legacy=next(c.cmap for c in font["cmap"].tables if c.platformID==3 and c.platEncID==0)
 greek={"α":"a","β":"b","γ":"g","δ":"d","ε":"e","ϵ":"e","ζ":"z","η":"h","θ":"q","ϑ":"J","ι":"i","κ":"k","λ":"l","μ":"m","ν":"n","ξ":"x","ο":"o","π":"p","ϖ":"v","ρ":"r","σ":"s","ς":"V","τ":"t","υ":"u","φ":"j","ϕ":"f","χ":"c","ψ":"y","ω":"w","Γ":"G","Δ":"D","Θ":"Q","Λ":"L","Ξ":"X","Π":"P","Σ":"S","Φ":"F","Ψ":"Y","Ω":"W"}
 cmap={ord(k):legacy[0xf000+ord(v)] for k,v in greek.items()}
 for platform,encoding in [(0,3),(3,1)]:
  tab=CmapSubtable.newSubtable(4);tab.platformID=platform;tab.platEncID=encoding;tab.language=0;tab.cmap=cmap.copy();font["cmap"].tables.append(tab)
 font.save(sf);font.close();fm.fontManager.addfont(str(sf));symbol=fm.get_font(str(sf));original=UnicodeFonts._get_glyph
 def glyph(self,fontname,font_class,sym):
  try:code=get_unicode_index(sym)
  except ValueError:return original(self,fontname,font_class,sym)
  if 48<=code<=57:return original(self,"rm",font_class,sym)
  if code in cmap:return symbol,code,False
  return original(self,fontname,font_class,sym)
 UnicodeFonts._get_glyph=glyph
 mt.SHRINK_FACTOR=.78
STEMS={i:next(DATA.glob(f"fig{i}_*.npz")).stem for i in range(1,5)}
Z={i:np.load(DATA/(STEMS[i]+".npz")) for i in STEMS}
META={i:json.loads((DATA/(STEMS[i]+".json")).read_text(encoding="utf-8")) for i in STEMS}
AUDIT={"new_physics_runs":0,"width_mm":180,"figures":{}}
if (ED/"FIGURE_BUILD_AUDIT.json").exists():
 AUDIT["figures"].update(json.loads((ED/"FIGURE_BUILD_AUDIT.json").read_text(encoding="utf-8"))["figures"])
def arr(n,a,l):return Z[n][f"axis{a}_line{l}_x"],Z[n][f"axis{a}_line{l}_y"]
def line(ax,n,a,l,color,ls=None,marker=None,label=None,**kw):
 x,y=arr(n,a,l);m=META[n]["axes"][a]["lines"][l]
 p=ax.plot(x,y,color=color,ls=m["linestyle"] if ls is None else ls,marker=m["marker"] if marker is None else marker,
  mfc="white",mec=color,label=label,**kw)[0]
 p._source=f"{STEMS[n]}:axis{a}_line{l}"
 return p
def figure(h):return plt.figure(figsize=(180/25.4,h/25.4),dpi=180)
def rect(f,x,y,w,h):return [x/180,1-(y+h)/(f.get_figheight()*25.4),w/180,h/(f.get_figheight()*25.4)]
def _soft_sketch(obj,scale=.18,length=75,randomness=1.1):
 try: obj.set_sketch_params(scale=scale,length=length,randomness=randomness)
 except Exception: pass
def style_axis(a):
 # Traditional paper-style boxed axes with restrained hand-crafted feeling.
 for sp in a.spines.values():
  sp.set_visible(True);sp.set_linewidth(.78);sp.set_color("#3C4146")
  _soft_sketch(sp,scale=.12,length=90,randomness=1.0)
 a.tick_params(direction="out",length=2.9,width=.68,top=False,right=False,colors="#30363B")
 a.set_facecolor("white")
 return a
def ax(f,x,y,w,h,**kwargs):
 a=f.add_axes(rect(f,x,y,w,h),**kwargs)
 a.xaxis.set_major_locator(MaxNLocator(4));a.yaxis.set_major_locator(MaxNLocator(3))
 style_axis(a)
 return a
def tag(f,x,y,l,title):
 H=f.get_figheight()*25.4
 f.text((x-4.5)/180,1-y/H,l,fontsize=8,fontweight="bold",va="baseline")
 f.text(x/180,1-y/H,title,fontsize=7,va="baseline")
def text(f,x,y,s,**kw):
 H=f.get_figheight()*25.4
 return f.text(x/180,1-y/H,s,fontsize=kw.pop("fontsize",6),**kw)
def zero(a):a.axhline(0,color="#C8CDCF",lw=.55,zorder=0)
def front_positions():
 x,I=arr(1,6,0);g=np.abs(np.gradient(I,x))
 return [float(x[np.flatnonzero((x<0)&(x>-30))[np.argmax(g[(x<0)&(x>-30)])]]),float(x[np.flatnonzero((x>0)&(x<30))[np.argmax(g[(x>0)&(x<30)])]])]
def fronts(a,positions=None,width=.75):
 for x in front_positions() if positions is None else positions:a.axvspan(x-width,x+width,color=LIGHT,alpha=.45,lw=0,zorder=0)
def leg(a,**kw):return a.legend(**kw)
def antique_axis_off(a,rough=.16):
 # For schematic panes: no ticks, but visible rectangular border can be enabled separately by caller.
 for artist in list(a.lines)+list(a.patches)+list(a.collections):
  _soft_sketch(artist,scale=rough,length=85,randomness=1.1)
 return a
def save(f,name,description):
 math_sizes=[];upright_digits=0;parser=MathTextParser("path")
 for t in f.findobj(Text):
  if "$" in t.get_text():
   if t.get_fontsize()<6.5:t.set_fontsize(6.5)
   parsed=parser.parse(t.get_text(),dpi=72,prop=t.get_fontproperties())
   for font,size,code,*rest in parsed.glyphs:
    math_sizes.append(float(size))
    if 48<=code<=57:
     assert "italic" not in font.style_name.lower(),(name,t.get_text(),font.style_name)
     upright_digits+=1
 assert not math_sizes or min(math_sizes)>=5-1e-8,(name,min(math_sizes))
 for aa in f.axes:
  try:
   # Box all quantitative panels and keep colorbars old-school as well.
   if aa.axison:
    style_axis(aa)
    # Preserve tick labels only on left/bottom; all four borders remain visible.
    for art in list(aa.patches)+list(aa.collections):
     if getattr(art,'axes',None) is aa and aa.get_navigate() is not None:
      pass
   # Light hand-crafted feel for schematic axes that suppress ticks.
   if not getattr(aa,"_smooth_schematic",False) and ((not aa.get_xticks().size and not aa.get_yticks().size) or len(aa.lines)<=1 and not aa.has_data()):
    antique_axis_off(aa,rough=.14)
  except Exception:
   pass
 f.canvas.draw();renderer=f.canvas.get_renderer();W,H=f.canvas.get_width_height();boxes=[];outside=[];hidden=set()
 for aa in f.axes:
  for axis,lim in [(aa.xaxis,aa.get_xlim()),(aa.yaxis,aa.get_ylim())]:
   for tick in axis.get_major_ticks()+axis.get_minor_ticks():
    if not min(lim)<=tick.get_loc()<=max(lim):hidden.update([id(tick.label1),id(tick.label2)])
 for t in f.findobj(Text):
  if t.get_visible() and t.get_text() and id(t) not in hidden:
   b=t.get_window_extent(renderer)
   if b.width and b.height:
    item={"text":t.get_text(),"bounds_mm":[float(v/f.dpi*25.4) for v in [b.x0,b.y0,b.width,b.height]]}
    boxes.append(item)
    if b.x0 < -1 or b.y0 < -1 or b.x1 > W+2 or b.y1 > H+2:outside.append(item)
 payload={};curves=[]
 for i,a in enumerate(f.axes):
  for j,l in enumerate(a.lines):
   x=np.asarray(l.get_xdata());y=np.asarray(l.get_ydata())
   if x.dtype.kind in "biufc" and y.dtype.kind in "biufc":
    payload[f"axis{i}_line{j}_x"]=x;payload[f"axis{i}_line{j}_y"]=y
    curves.append({"series":f"axis{i}_line{j}","source":getattr(l,"_source","explicit calculation from supplied arrays"),"xlabel":a.get_xlabel(),"ylabel":a.get_ylabel()})
  for j,c in enumerate(a.collections):
   if isinstance(c,QuadMesh):
    payload[f"axis{i}_mesh{j}"]=np.asarray(c.get_array());payload[f"axis{i}_mesh{j}_coordinates"]=c.get_coordinates()
 np.savez_compressed(HERE/"plotted_data"/(name+".npz"),**payload)
 (HERE/"plotted_data"/(name+".json")).write_text(json.dumps(curves,ensure_ascii=False,indent=2),encoding="utf-8")
 with (HERE/"plotted_data"/(name+".csv")).open("w",encoding="utf-8",newline="") as fp:
  wr=csv.writer(fp);wr.writerow(["series","sample","x","y"])
  for c in curves:
   key=c["series"];x=payload[key+"_x"];y=payload[key+"_y"]
   if x.ndim==y.ndim==1:
    for k,(xx,yy) in enumerate(zip(x,y)):wr.writerow([key,k,xx,yy])
 for ext in ["pdf","svg"]:f.savefig(FIG/(name+"."+ext),dpi=600)
 f.savefig(PRE/(name+".png"),dpi=280)
 f.savefig(FIG/(name+".png"),dpi=450)
 (ED/(name+"_text_boxes.json")).write_text(json.dumps(boxes,ensure_ascii=False,indent=2),encoding="utf-8")
 AUDIT["figures"][name]={"width_mm":180,"height_mm":round(f.get_figheight()*25.4,3),"axes":len(f.axes),"purpose":description,"text_outside_canvas":outside,"math_glyph_point_range":[min(math_sizes),max(math_sizes)] if math_sizes else None,"upright_math_digits_checked":upright_digits}
 plt.close(f);print("Exported",name,flush=True)

def fig1():
 f=figure(142);tag(f,7,7,"a","Periodic pump and Kerr cavity")
 tau,pump=arr(1,1,0);tau=tau*80
 a=ax(f,7,14,53,12)
 for j in [-2,-1,0,1,2]:a.plot(tau/80+j,pump/max(pump),color=RED)
 a.fill_between(np.tile(tau/80,5)+np.repeat([-2,-1,0,1,2],len(tau)),np.tile(pump/max(pump),5),color=RED,alpha=.12)
 a.set(xlim=(-2.5,2.5),ylim=(0,1.3));a.axis("off")
 a.annotate("",xy=(0,1.18),xytext=(1,1.18),arrowprops={"arrowstyle":"<->","lw":.6,"color":GRAY})
 a.text(.5,1.21,r"$T$",ha="center",va="bottom",fontsize=6.5);a.text(-2.48,1.12,r"$S(\tau)$",fontsize=6.5)
 art=ax(f,1,29,62,38.75);pulse_tau,pulse_I=arr(1,2,0);draw_classic_cavity(art,pulse_tau,pulse_I)
 a=ax(f,8,75,51,10);a.plot(tau/80,pump/max(pump),color=PURPLE,label="Pump")
 x,I=arr(1,2,0);a.plot(x/80,I/max(I),color=BLUE,label="Intensity")
 a.set(xlim=(-.5,.5),ylim=(0,1.1),xlabel=r"$\tau/T$");a.set_yticks([]);a.spines["left"].set_visible(False);a.set_xticks([-.5,0,.5]);a.legend(loc="upper center",bbox_to_anchor=(.5,1.9),ncol=2,columnspacing=.8)
 for start,end,col,label in [(-.4,-.13,GRAY,r"$d_1$"),(.4,.13,TEAL,"Restoring")]:
  a.annotate("",xy=(end,-.73),xytext=(start,-.73),xycoords=("data","axes fraction"),arrowprops={"arrowstyle":"->","lw":.65,"color":col},annotation_clip=False)
  a.text(end,-.68,label,transform=a.get_xaxis_transform(),ha="right" if end<0 else "left",va="bottom",fontsize=6)
 for col,x0,ids,title,ltr,lim in [(BLUE,77,[1,2,3,4],"Bright soliton","b",2),(TEAL,133,[5,6,7,8],"Dark soliton","c",25)]:
  tag(f,x0,7,ltr,title)
  p=ax(f,x0,14,43,12);line(p,1,ids[0],0,PURPLE);xx,yy=arr(1,ids[0],0);p.fill_between(xx,0,yy,color=PURPLE,alpha=.12)
  p.axvspan(-lim/(80 if ltr=="b" else 160),lim/(80 if ltr=="b" else 160),color=col,alpha=.15,lw=0)
  p.set(xlim=(-.5,.5),ylim=(0,2.6 if ltr=="b" else 4.5),ylabel=r"$|S|$",xlabel=r"$\tau/T$");p.set_xticks([-.5,0,.5]);p.set_yticks([0,2] if ltr=="b" else [0,4])
  p=ax(f,x0,39,43,15);line(p,1,ids[1],0,col);xx,yy=arr(1,ids[1],0);p.fill_between(xx,0,yy,color=col,alpha=.10)
  p.set(xlim=(-lim,lim),ylim=(0,13.5 if ltr=="b" else 6),ylabel=r"$|\psi_{\rm s}|^2$");p.tick_params(labelbottom=False)
  p=ax(f,x0,59,43,9);line(p,1,ids[2],0,GOLD);zero(p);p.set(xlim=(-lim,lim),ylabel=r"$\arg\psi_{\rm s}$",xlabel=r"Fast time $\tau$");p.set_xticks([-2,0,2] if ltr=="b" else [-20,0,20])
  p=ax(f,x0,82,43,13);line(p,1,ids[3],0,col,alpha=.3,lw=.65);seg=Z[1][f"axis{ids[3]}_collection0_segments"]
  p.add_collection(LineCollection(seg,colors=col,linewidths=.55));p.set(xlim=(-80,80),ylim=(-65,2),ylabel="Power (dB)",xlabel=r"Comb tooth $m$");p.set_xticks([-60,0,60]);p.set_yticks([-60,0])
 tag(f,13,110,"d","Bright: right mode and adjoint")
 for x0,idx,lab,col in [(13,10,r"$R_Q$",BLUE),(58,11,r"$L_Q$",GOLD)]:
  a=ax(f,x0,116,31,17);line(a,1,idx,0,col);line(a,1,idx,1,col);zero(a)
  a.set(xlim=(-2,2),ylim=(-1.15,1.15),xlabel=r"Fast time $\tau$",ylabel="Mode / max" if idx==10 else "");a.set_xticks([-2,0,2]);a.set_yticks([-1,0,1]);a.text(.03,.85,lab,transform=a.transAxes)
 for x0,idx,ltr,title,col in [(111,12,"e","Dark: width",TEAL),(152,13,"f","Dark: position",GOLD)]:
  tag(f,x0,110,ltr,title);a=ax(f,x0,116,25,17);fronts(a);line(a,1,idx,0,col);zero(a)
  a.set(xlim=(-23,23),ylim=(-1.2,1.45),xlabel=r"Fast time $\tau$",ylabel=r"$\delta I$/max" if idx==12 else "");a.set_xticks([-20,0,20]);a.set_yticks([-1,0,1])
  for fr,sg in zip(front_positions(),[1 if idx==12 else -1,-1]):a.annotate("",xy=(fr+sg*3,1.3),xytext=(fr-sg*3,1.3),arrowprops={"arrowstyle":"->","lw":.6,"color":GRAY})
 save(f,STEMS[1],"Bright/dark fields; display-normalized left/right modes; width versus position front motion.")
 # Variant: the cavity artwork is Matplotlib vector geometry on the original canvas.
 # Do NOT merge the formerly selected external artwork into this alternative PDF.

def fig2():
 f=figure(142);tag(f,14,7,"a","Bright: reflection-related branches")
 a=ax(f,14,13,75,23);a.axhline(0,color=RED,ls="--",lw=.7);line(a,2,0,1,BLUE);line(a,2,0,2,RED,ls="--")
 a.set(xlim=(0,2),ylim=(-.75,.75),ylabel=r"$q_{\rm B}$");a.tick_params(labelbottom=False)
 a.text(.60,.06,"Computed",transform=a.transAxes);a.text(.60,.86,"Reflected",transform=a.transAxes);a.text(.73,.56,"Even",transform=a.transAxes)
 a=ax(f,14,42,75,13);line(a,2,1,0,BLUE,label="Static slope");line(a,2,1,1,BLUE,marker="o",ls="none",ms=2.5,label="Jacobian");zero(a)
 a.set(xlim=(-2.5,2.5),xlabel=r"Offset $\mu_0$ ($10^{-4}$)",ylabel=r"$\lambda_Q$ ($10^{-7}$)");leg(a,loc="lower right",ncol=2,fontsize=5.5)
 tag(f,120,7,"b","Bright: reflected fields")
 a=ax(f,120,13,55,17);line(a,2,2,0,BLUE);line(a,2,2,1,RED,ls="--");a.set(xlim=(-1.25,1.25),ylabel=r"$|\psi_{\rm s}|^2$");a.tick_params(labelbottom=False)
 a=ax(f,120,40,55,15);line(a,2,3,0,SLATE);x,y=arr(2,3,0);a.fill_between(x,0,y,where=y>=0,color=BLUE,alpha=.13);a.fill_between(x,0,y,where=y<0,color=RED,alpha=1);zero(a)
 a.set(xlim=(-1.25,1.25),xlabel=r"Fast time $\tau$",ylabel=r"$(I-I^{\rm ref})/2$")
 tag(f,14,65,"c","Dark: width-fold trajectories")
 a=ax(f,14,72,79,24)
 for l,c,lab in [(0,DEEP_BLUE,"Family 17"),(1,TEAL,"Family 29")]:line(a,2,4,l,c,label=lab,lw=1.2 if l==1 else 1.1)
 a.axhline(0,color=GRAY,ls="--",lw=.7,label="Fixed drive")
 a.set(xscale="log",xlim=(1e-4,1),xlabel=r"Pump deformation $\eta$",ylabel=r"$(S_{{\rm pk},f}-S_{\rm M})/10^{-3}$");leg(a,loc="upper left",fontsize=5.8)
 tag(f,117,65,"d","Dark: separate fold states")
 for x0,idx,cm,vlim,label in [(117,10,BLUE_RED,None,r"$I$"),(148,12,BLUE_RED,(-.061851806258602204,.061851806258602204),r"$\Delta I$")]:
  a=ax(f,x0,72,21,24);z=Z[2];key=f"axis{idx}_collection0";co=z[key+"_coordinates"];val=z[key+"_values"]
  im=a.pcolormesh(co[:,:,0],co[:,:,1],val,cmap=cm,shading="flat",vmin=None if vlim is None else vlim[0],vmax=None if vlim is None else vlim[1],rasterized=True)
  a.set(xlim=(-35,35),yscale="log",ylim=(1e-4,1),xlabel=r"$\tau$");a.set_xticks([-30,0,30])
  if idx==10:a.set_ylabel(r"$\eta$")
  else:a.tick_params(labelleft=False)
  cb=f.colorbar(im,cax=ax(f,x0+22.5,72,1.2,24));cb.ax.set_title(label,fontsize=6.5,pad=4);cb.ax.tick_params(labelsize=5.5)
  cb.set_ticks([0,2,4] if idx==10 else [-.05,0,.05])
 tag(f,14,113,"e","Fixed-drive intersection")
 a=ax(f,14,120,42,14);line(a,2,5,0,TEAL,lw=1.25);a.axhline(0,color=GRAY,ls="--",lw=.7);line(a,2,5,2,TEAL,marker="o",ms=3.2,mew=.9)
 a.set(xlim=(0,2.5),xlabel=r"$\eta$ ($10^{-3}$)",ylabel=r"$(S_{{\rm pk},f}-S_{\rm M})/10^{-6}$")
 for x0,idx,ltr,title,col,lim in [(83,6,"f","Width zero mode",TEAL,20),(141,8,"g","Background zero mode",DEEP_BLUE,80)]:
  tag(f,x0,113,ltr,title)
  a=ax(f,x0,119,34,5);line(a,2,idx,0,col);a.set(xlim=(-lim,lim),ylabel=r"$I$");a.tick_params(labelbottom=False);a.set_yticks([0,4])
  a=ax(f,x0,128,34,6);line(a,2,idx+1,0,col);zero(a);a.set(xlim=(-lim,lim),ylim=(-1.12,1.12),xlabel=r"Fast time $\tau$",ylabel=r"$\delta I$/max");a.set_xticks([-lim,0,lim]);a.set_yticks([-1,0,1])
 save(f,STEMS[2],"Critical bright odd direction and distinct dark width/background folds; fold states are not time frames.")

def fig3():
 f=figure(160);tag(f,12,6,"a","Bright: mismatch-fold prediction")
 a=ax(f,12,12,50,24);a.axvspan(0,2.5,color=BLUE,alpha=.07,lw=0);line(a,3,0,0,BLUE)
 for l in range(1,5):line(a,3,0,l,BLUE,marker="o",ls="none",ms=3.3)
 a.set(xlim=(0,6),ylim=(0,2.9),ylabel=r"$|d_{1,\rm SN}|$ ($10^{-8}$)");a.tick_params(labelbottom=False);a.text(.03,.86,r"$3/2$ law",transform=a.transAxes)
 a=ax(f,12,40,50,8)
 for l in range(4):line(a,3,1,l,BLUE,marker="o",ls="none",ms=2.8)
 a.axhline(.1,color=GRAY,ls="--",lw=.6);a.set(xlim=(0,6),ylim=(0,.12),ylabel="Error (%)",xlabel=r"$\mu_0$ ($10^{-4}$)");a.set_yticks([0,.1])
 a=ax(f,74,12,18,36);line(a,3,11,0,BLUE);line(a,3,11,1,BLUE,marker="o",ls="none",ms=2.8)
 a.set(xlim=(-1.3,1.3),ylim=(-2.2,2.2),xlabel=r"$d_1/d_f$",ylabel=r"$q_{\rm B}/q_f$");a.set_xticks([-1,1]);a.set_yticks([-2,0,2])
 tag(f,112,6,"b","Dark: finite-front forcing")
 for idx,y,h,lab,col in [(2,12,8,r"$I_{\rm CW}$",DEEP_BLUE),(3,25,7,r"$(1-g)/10^{-3}$",GOLD),(4,38,10,r"$K_W(1-g)/10^{-3}$",TEAL)]:
  a=ax(f,118,y,57,h);line(a,3,idx,0,col)
  if idx==3:line(a,3,idx,1,GOLD,marker="o",ls="none",ms=2.6)
  for l in [len(META[3]["axes"][idx]["lines"])-2,len(META[3]["axes"][idx]["lines"])-1]:a.axvline(arr(3,idx,l)[0][0],color=SLATE,lw=.5,ls=":",alpha=.6)
  if idx==4:
   x,v=arr(3,idx,0);a.fill_between(x,0,v,where=v>=0,color=TEAL,alpha=.16);a.fill_between(x,0,v,where=v<0,color=PURPLE,alpha=.16);zero(a)
  a.set(xlim=(-25,25),ylabel=lab);a.set_xticks([-20,0,20]);a.yaxis.set_major_locator(MaxNLocator(2))
  if idx==4:a.set_xlabel(r"Fast time $\tau$")
  else:a.tick_params(labelbottom=False)
 tag(f,12,58,"c","Dark: 12 width-fold thresholds")
 a=ax(f,12,65,81,24)
 for l,col,lab in [(0,GOLD,"Point fronts"),(1,TEAL,"Adjoint weight"),(2,TEAL,r"LLE, $\sigma=80$"),(3,GOLD,None),(4,TEAL,None),(5,TEAL,r"LLE, $\sigma=60$")]:
  line(a,3,5,l,col,marker="o" if l==2 else "^" if l==5 else "None",ms=2.7,label=lab)
 a.set(yscale="log",xlim=(13,35),ylim=(8e-5,1.4),ylabel=r"Threshold $\eta_{\rm f}$");a.tick_params(labelbottom=False)
 leg(a,loc="lower left",bbox_to_anchor=(0,1.01),fontsize=5.2,ncol=4,columnspacing=.7,handlelength=1.35)
 # A linear-scale close-up replays the same sigma=80 arrays without offsetting data.
 from matplotlib.patches import Rectangle
 a.add_patch(Rectangle((23.45,.0078),.75,.0068,facecolor="none",edgecolor=SLATE,lw=.65))
 z=ax(f,67,67,23,10)
 for l,col in [(0,GOLD),(1,TEAL),(2,TEAL)]:
  line(z,3,5,l,col,marker="o" if l==2 else "None",ms=3.2,lw=1.05)
 z.set(xlim=(23.45,24.2),ylim=(.0078,.0146))
 z.set_xticks([23.6,24.0]);z.set_yticks([.008,.014])
 z.tick_params(labelsize=5.2,pad=1)
 z.text(.52,.98,r"$\sigma=80$",transform=z.transAxes,ha="center",va="top",fontsize=5.5)
 a=ax(f,12,93,81,10)
 for l,c in [(0,GOLD),(1,TEAL),(2,GOLD),(3,TEAL)]:line(a,3,6,l,c,marker="o" if l<2 else "^",ls="none",ms=2.7)
 a.axhline(0,color=SLATE,lw=.65,ls="--",zorder=0);a.set(xlim=(13,35),ylim=(-7,45),xlabel=r"CW front separation $W_{\rm D}$",ylabel="Error (%)");a.set_yticks([0,40])
 text(f,12,116,"Mean absolute error:  24.74%  →  4.18%",fontsize=6.5)
 tag(f,111,58,"d","Dark: position-rate increments")
 a=ax(f,111,65,62,8)
 for l,c in [(0,TEAL),(1,SLATE)]:line(a,3,7,l,c)
 zero(a);a.set(xlim=(-18,18),ylim=(-1.2,1.2),ylabel=r"$\delta I_Q$");a.set_xticks([]);a.set_yticks([-1,1])
 a=ax(f,111,81,62,18)
 for l,c,lab in [(0,TEAL,"CW 0"),(2,SLATE,"CW 4")]:
  line(a,3,8,l,c,label=lab);line(a,3,8,l+1,c,marker="o",ls="none",ms=2.7)
 a.set(xscale="log",yscale="log",xlim=(2e-4,.12),ylim=(2e-7,2e-4),ylabel=r"$\Delta\lambda_Q$");a.tick_params(labelbottom=False);leg(a,loc="upper left",ncol=2,fontsize=5.5)
 a=ax(f,111,103,62,7)
 for l,c in [(0,TEAL),(1,SLATE)]:line(a,3,10,l,c,marker="o",ls="none",ms=2.6)
 a.axhline(0,color=SLATE,lw=.65,ls="--",zorder=0);a.set(xscale="log",xlim=(2e-4,.12),ylim=(-4,1),xlabel=r"Pump deformation $\eta$",ylabel="Error (%)");a.set_yticks([-3,0])
 b=json.loads((RUN/"figure_sources/data/r408/bright_cw_position_rate_replay.json").read_text(encoding="utf-8"))
 d=json.loads((RUN/"figure_sources/data/r408/dark_joint_response_replay.json").read_text(encoding="utf-8"))
 z=np.load(RUN/"figure_sources/data/r408/dark_joint_response_replay.npz")
 tag(f,12,123,"e","Bright: position-rate prediction")
 x=np.array([r["sigma"] for r in b["rows"]]);p=np.array([r["prediction"] for r in b["rows"]]);v=np.array([r["LLE"] for r in b["rows"]])
 a=ax(f,12,129,71,15);a.semilogy(x,p,color=BLUE);a.plot(x,v,"o",mfc="white",mec=BLUE,ms=3);a.set(xlim=(3.5,21.5),ylim=(4e-4,2e-2),ylabel=r"$\lambda_Q$");a.tick_params(labelbottom=False);a.yaxis.set_minor_locator(NullLocator())
 a=ax(f,12,147,71,5);a.plot(x,abs(p/v-1)*100,"o-",color=BLUE,mfc="white",ms=2.7);a.set(xlim=(3.5,21.5),ylim=(0,1.9),ylabel="Error (%)",xlabel=r"Pump width $\sigma$");a.set_xticks([5,10,20]);a.set_yticks([0,1])
 tag(f,111,123,"f","Dark: local nonzero-mismatch response")
 rows=sorted(d["rows"],key=lambda r:r["increment"]);h=1.192758477442962e-9;x=np.array([r["increment"]/h for r in rows]);v=np.array([r["field_change_relative"] for r in rows])*100
 xx=np.linspace(-2,2,301);p=abs(xx*h)*np.linalg.norm(z["stationary_d1_derivative"])/np.linalg.norm(z["reference"])*100
 a=ax(f,111,129,62,15);a.plot(xx,p,color=TEAL);a.plot(x,v,"o",mfc="white",mec=TEAL,ms=3);a.set(xlim=(-2.3,2.3),ylim=(0,1.18),ylabel="Field change (%)");a.tick_params(labelbottom=False)
 a=ax(f,111,147,62,5);a.plot(x,[r["increment_prediction_relative_error"]*100 for r in rows],"o-",mfc="white",color=TEAL,ms=2.7);a.set(xlim=(-2.3,2.3),ylim=(0,7.2),xlabel=r"Mismatch increment $\delta d_1/h$",ylabel="Error (%)");a.set_xticks([-2,0,2]);a.set_yticks([0,6])
 save(f,STEMS[3],"Four mismatch folds; 12 dark thresholds; dark/bright position rates; local dark field increments. Error denominators remain experiment-specific.")

def fig4():
 f=figure(153);tag(f,12,7,"a","Dark: prescribed mixed excitation")
 for idx,y,comp in [(0,15,r"$\mathrm{Re}\,\delta\psi_0/\epsilon$"),(2,32,r"$\mathrm{Im}\,\delta\psi_0/\epsilon$")]:
  a=ax(f,12,y,56,12);fronts(a)
  for l,c,lab in [(0,GRAY,"Initial"),(1,TEAL,r"$a_WR_W$"),(2,GOLD,r"$a_QR_Q$")]:line(a,4,idx,l,c,label=lab,lw=1.2 if l else 1.1)
  zero(a);a.set(xlim=(-25,25),ylabel=comp);a.set_xticks([-20,0,20])
  if idx==0:a.tick_params(labelbottom=False)
  else:a.set_xlabel(r"Fast time $\tau$")
  z=ax(f,74,y,15,12)
  for l,c in [(0,GRAY),(1,TEAL),(2,GOLD)]:line(z,4,idx+1,l,c,lw=1.15 if c!=GRAY else 1.0)
  z.set(xlim=(13,17));z.set_xticks([13,17]);z.set_yticks([0,.1])
  if idx==0:z.tick_params(labelbottom=False)
  else:z.set_xlabel(r"$\tau$")
 text(f,74,11,"Front",fontsize=6)
 tag(f,104,7,"b","Dark: fixed one- and two-mode errors")
 a=ax(f,104,15,70,30)
 for l,c,lab,lsv in [(0,SLATE,"Width only","--"),(1,GOLD,"Position only",":"),(2,TEAL,"Both","-")]:line(a,4,4,l,c,label=lab,lw=1.25 if l==2 else 1.1,ls=lsv)
 leg(a,loc="center right",bbox_to_anchor=(.98,.57),ncol=1,fontsize=5.5)
 a.axvspan(.05,1,color=GRAY,alpha=.08);a.axvspan(20,40,color=TEAL,alpha=.08)
 a.set(yscale="log",xlim=(0,40),ylim=(1e-7,2),ylabel=r"Field error $e_\psi$",xlabel=r"Time $t$");a.set_yticks([1e-6,1e-3,1]);a.set_xticks([0,20,40])
 tag(f,12,56,"c","Dark: residual comb error")
 a=ax(f,12,63,43,24);key="axis5_collection0";co=Z[4][key+"_coordinates"];v=Z[4][key+"_values"]
 im=a.pcolormesh(co[:,:,0],co[:,:,1],v,cmap=BLUE_RED,vmin=-10,vmax=-4,shading="flat",rasterized=True)
 a.set(xlim=(17.5,42.5),ylim=(-80,80),ylabel=r"Comb tooth $m$");a.set_xticks([20,30,40]);a.tick_params(labelbottom=False);a.set_yticks([-60,0,60])
 cb=f.colorbar(im,cax=ax(f,58,63,1.3,24),ticks=[-9,-7,-5]);cb.ax.set_title(r"$\log_{10}e_m$",fontsize=6,pad=9);cb.ax.tick_params(labelsize=5.5)
 a=ax(f,77,63,12,24)
 for l,c in [(0,SLATE),(1,GRAY)]:line(a,4,7,l,c,label=r"$t=20$" if l==0 else r"$t=40$")
 leg(a,loc="upper center",bbox_to_anchor=(.5,-.32),fontsize=5.2)
 a.set(xlim=(-50,1),ylim=(-80,80),xlabel="dB");a.set_xticks([-40,0]);a.set_yticks([]);a.set_title("Power",fontsize=6,pad=4)
 a=ax(f,12,92,43,8);line(a,4,8,0,TEAL,marker="o",ms=2.7);a.set(xlim=(17.5,42.5),ylim=(0,1.1),ylabel=r"$P/P_{20}$",xlabel=r"Saved time $t$");a.set_xticks([20,30,40]);a.set_yticks([0,1])
 tag(f,104,56,"d",r"Dark: field at $t=30$")
 for idx,y,lab in [(9,63,r"$\mathrm{Re}\,\delta\psi/\epsilon$"),(10,88,r"$\mathrm{Im}\,\delta\psi/\epsilon$")]:
  a=ax(f,104,y,31,12);fronts(a)
  for l,c in [(1,GRAY),(2,TEAL),(3,SLATE)]:line(a,4,idx,l,c)
  zero(a);a.set(xlim=(-25,25),ylabel=lab);a.set_xticks([-20,0,20])
  if idx==9:a.tick_params(labelbottom=False)
  else:a.set_xlabel(r"Fast time $\tau$")
 for x0,y,idx,ltr,title,ylabel in [(154,63,11,"e","Comb phase",r"$\delta\phi/10^{-8}$"),(154,88,12,"f","Comb power",r"$\delta p_1/10^{-7}$")]:
  tag(f,x0,y-7,ltr,title);a=ax(f,x0,y,21,12)
  for l,c in [(0,SLATE),(1,TEAL),(2,GRAY)]:line(a,4,idx,l,c)
  a.set(xlim=(19,41),ylabel=ylabel);a.set_xticks([20,40])
  if idx==11:a.tick_params(labelbottom=False)
  else:a.set_xlabel(r"$t$")
 rows=json.loads((RUN/"figure_sources/data/r409/compact_summary.json").read_text(encoding="utf-8"))
 for x0,case,ltr in [(14,"Bright","g"),(111,"Dark","h")]:
  tag(f,x0,113,ltr,case+": adding initially excited modes")
  a=ax(f,x0,120,64,22);rr=[r for r in rows if r["case"]==case];m=np.array([r["M"] for r in rr])
  for key,c,ls,lab in [("early_field",BLUE if case=="Bright" else TEAL,"-","Field"),("early_phase",PURPLE,"--","Phase"),("early_power",GOLD,":","Power")]:
   a.plot(m,np.array([r[key] for r in rr])*100,color=c,ls=ls,marker="o" if key=="early_field" else None,ms=2.5,mfc="white",label=lab)
  a.set(xscale="log",yscale="log",xlim=(.85 if case=="Bright" else 1.6,5000),ylim=(1e-4,500) if case=="Bright" else (1e-5,100),xlabel=r"Retained real directions $M$",ylabel="Early error (%)")
  a.xaxis.set_minor_locator(NullLocator());a.yaxis.set_minor_locator(NullLocator());leg(a,loc="upper right",ncol=1,fontsize=5.7)
 save(f,STEMS[4],"Initial excitation; late two-mode accuracy versus early non-monotonic multimode convergence; original comb diagnostics retained.")

B=np.load(DATA/"bright_display_data.npz");D=np.load(DATA/"dark_display_data.npz");DZ=np.load(DATA/"dark_design.npz")
def grid(n,T):return -T/2+np.arange(n)*T/n,2*np.pi*np.fft.fftfreq(n,T/n)
def circular(z,T):
 tau,k=grid(len(z),T);return np.angle(np.sum(abs(z)**2*np.exp(2j*np.pi*tau/T)))*T/(2*np.pi)
def relative_change(p,S,p0,S0,T):
 def diff(a,b):return (a-b+T/2)%T-T/2
 return diff(circular(p,T),circular(p0,T))-diff(circular(S,T),circular(S0,T))
def phasepanel(f,x,y,letter,case):
 bright=case=="Bright";col=BLUE if bright else TEAL
 if bright:p0=B["bright_psi0"];S0=B["bright_S0"];p=B["bright_phase_psi_1"];S=B["bright_phase_S_1"];T=80;shift=0;lim=2;scale=1e-2;qscale=1e-7
 else:
  z=np.load(DATA/"dark_phase_N2048_1.npz");p0=z["psi0"];S0=z["S0"];p=z["psi"];S=z["S"];T=160;shift=1024;lim=25;scale=1e-4;qscale=1e-4
 tau,k=grid(len(p),T);dx=relative_change(p,S,p0,S0,T);tangent=-np.fft.ifft(1j*k*np.fft.fft(p0))
 di=2*np.real(np.conj(p0)*(p-p0));tr=2*np.real(np.conj(p0)*dx*tangent)
 tag(f,x,y,letter,case+": phase input")
 a=ax(f,x,y+7,39,21);a.plot(tau,np.roll(di,shift)/scale,color=col,label="New state");a.plot(tau,np.roll(tr,shift)/scale,color=col if bright else DEEP_BLUE,ls="--",label="Translation")
 a.set(xlim=(-lim,lim),ylabel=rf"$\delta I$ ($10^{{{int(np.log10(scale))}}}$)");a.tick_params(labelbottom=False);leg(a,loc="upper left" if bright else "lower left",fontsize=5.5)
 a=ax(f,x,y+37,39,10);a.plot(tau,np.roll(np.angle(S/S0),shift)/qscale,color=PURPLE);zero(a)
 a.set(xlim=(-T/2,T/2),xlabel=r"Fast time $\tau$",ylabel=rf"$\delta\arg S$ ($10^{{{int(np.log10(qscale))}}}$)");a.set_xticks([-T/2,0,T/2])
def fig5():
 f=figure(145);text(f,12,7,"BRIGHT SOLITON",fontweight="bold",fontsize=7);phasepanel(f,12,14,"a","Bright")
 tag(f,76,14,"b","Fixed pump-field budget")
 a=ax(f,76,21,42,36);theta=np.linspace(0,2*np.pi,500);sc=np.array([1e-4,.01])
 for m,c,ls,lab in [(3,PURPLE,"-","With phase"),(2,BLUE,"--","2 amplitude inputs")]:
  ev,U=la.eigh(B["bright_H"][:m,:m]);white=U@np.diag(ev**-.5)@U.T
  U,s,V=la.svd((B["bright_A"][:,:m]@white)*1e-8/sc[:,None],full_matrices=False);xy=U@(s[:,None]*np.array([np.cos(theta),np.sin(theta)]))
  if m==3:a.fill(*xy,color=c,alpha=.06,lw=0)
  a.plot(*xy,color=c,ls=ls,label=lab,zorder=4 if m==2 else 2)
 a.set(xlabel=r"$\delta x$ ($10^{-4}$)",ylabel=r"$\delta\lambda_s/|\lambda_{s,0}|$ (%)");a.set_xticks([-1,0,1]);a.set_yticks([-1,0,1])
 leg(a,loc="lower center",bbox_to_anchor=(.5,1.02),ncol=2,fontsize=5.5,columnspacing=.8);text(f,76,66,r"$\rho=10^{-8}$; stored amplitude tangents",fontsize=5.7)
 rows=json.loads((DATA/"bright_frozen_control_tests.json").read_text(encoding="utf-8"));xx=np.array([r["u"] for r in rows])/1e-8
 tag(f,136,14,"c","Independent pump tests")
 a=ax(f,136,21,38,14)
 for j,c,l,lab in [(0,BLUE,"-","Position"),(1,TEAL,"--","Slow rate")]:a.plot(xx,[r["error_percent"][j] for r in rows],ls=l,marker="o" if j==0 else "^",mfc="white",ms=2.8,color=c,label=lab)
 a.set(xlim=(-7,7),ylim=(0,11),ylabel="Error (%)");a.tick_params(labelbottom=False);a.set_yticks([0,10]);leg(a,loc="upper center",ncol=2,bbox_to_anchor=(.5,1.35),fontsize=5.2,columnspacing=.4)
 for j,y,col,scale,lab in [(0,45,BLUE,1e-4,r"$\delta x/10^{-4}$"),(1,63,TEAL,.01,r"$\delta\lambda_s/|\lambda_{s,0}|$ (%)")]:
  a=ax(f,136,y-2,38,9);a.plot(xx,np.array([r["prediction"][j] for r in rows])/scale,color=col,ls="--");a.plot(xx,np.array([r["actual"][j] for r in rows])/scale,"o",mfc="white",mec=col,ms=2.7)
  a.set(xlim=(-7,7),ylabel=lab);a.set_xticks([-6,0,6])
  if j==0:a.tick_params(labelbottom=False)
  else:a.set_xlabel(r"$u$ ($10^{-8}$)")
 text(f,12,77,"DARK SOLITON",fontweight="bold",fontsize=7);phasepanel(f,12,84,"d","Dark")
 tag(f,76,84,"e","Equal-power rate direction")
 base=np.load(DATA/"dark_target_N2048_2.npz");tau,k=grid(2048,160)
 for y,typ,scale,label in [(103,"pump",1e-4,r"$\delta I_S/I_{S,\max}$ ($10^{-4}$)"),(132,"state",1e-3,r"$\delta I$ ($10^{-3}$)")]:
  a=ax(f,76,y-12,42,18 if typ=="pump" else 12)
  for ix,c,ls,lab in [(3,DEEP_BLUE,"--","Weak"),(4,TEAL,"-","Strong")]:
   z=np.load(DATA/f"dark_target_N2048_{ix}.npz");v=(abs(z["S"])**2-abs(base["S"])**2)/max(abs(base["S"])**2) if typ=="pump" else abs(z["psi"])**2-abs(base["psi"])**2
   a.plot(tau,np.roll(v,1024)/scale,color=c,ls=ls,label=lab)
  a.set(xlim=(-25,25),ylabel=label);a.set_xticks([-20,0,20])
  if typ=="pump":a.tick_params(labelbottom=False);leg(a,loc="lower center",bbox_to_anchor=(.5,1.02),ncol=2,fontsize=5.5)
  else:a.set_xlabel(r"Fast time $\tau$")
 tag(f,136,84,"f","Both slow rates")
 rows=[r for r in json.loads((DATA/"dark_target_results.json").read_text(encoding="utf-8")) if r["N"]==2048]
 for j,y,c,label in [(0,103,TEAL,"Width"),(1,132,DEEP_BLUE,"Position")]:
  a=ax(f,136,y-12,38,18 if j==0 else 12);xx=np.array([r["u"] for r in rows])/1e-4
  pred=-np.array([r["predicted_lambdas"][j]-DZ["lam"][j] for r in rows])/abs(DZ["lam"][j])*100
  act=-np.array([r["lambdas"][j]-DZ["lam"][j] for r in rows])/abs(DZ["lam"][j])*100
  a.plot(xx,pred,color=c,ls="--");a.plot(xx,act,"o",mfc="white",mec=c,ms=2.7)
  a.set(xlim=(-1.25,1.25),ylim=(-9,9),ylabel=label+" change (%)");a.set_xticks([-1,0,1]);a.set_yticks([-8,0,8])
  if j==0:a.tick_params(labelbottom=False)
  else:a.set_xlabel(r"$u$ ($10^{-4}$)")
 save(f,"fig5_intrinsic_drive_response","Actual Gram-budget response ellipse, stored bright inputs, equal-power paths and separately labelled field and rate predictions.")

def fig6():
 f=figure(170);bright_time=B["bright_t"]*(-float(B["bright_lam_0"]));dark_time=D["t"]*(-max(D["lam0"]))
 for case,x0,ltr,time,Q in [("Bright",14,"a",bright_time,B),("Dark",107,"b",dark_time,D)]:
  text(f,x0,6,case.upper()+" SOLITON",fontweight="bold",fontsize=7);tag(f,x0,13,ltr,"Baseline and strong control")
  for j,x in [(0,x0),(1,x0+37)]:
   a=ax(f,x,19,32,23);key=f"heat_{[0,2][j]}" if case=="Bright" else f"heat_{j}"
   im=a.pcolormesh(time,Q["heat_tau"],Q[key].T,cmap="inferno",norm=LogNorm(1e-6,.1),shading="nearest",rasterized=True)
   a.set(xlabel=r"$\Gamma_0t$",ylim=(-2,2) if case=="Bright" else (-22,22));a.set_xticks([0,3,6])
   if j==0 and case=="Bright":a.set_ylabel(r"Fast time $\tau$")
   elif j==1:a.tick_params(labelleft=False)
   a.set_title("Baseline" if j==0 else "Strong",fontsize=6,pad=4)
 cb=f.colorbar(im,cax=ax(f,94,19,1.6,23),ticks=[1e-6,1e-4,1e-2]);cb.ax.set_yticklabels(["−6","−4","−2"]);cb.ax.set_title(r"$\log_{10}q$",fontsize=6,pad=5);cb.ax.tick_params(labelsize=5.5)
 for x0,colors in [(14,[GRAY,BWEAK,BLUE]),(107,[GRAY,DWEAK,TEAL])]:
  f.legend(handles=[Line2D([],[],color=c,ls=ls,label=lab,lw=1.4 if lab=="Strong" else 1.15) for c,ls,lab in zip(colors,[":","--","-"],["Baseline","Weak","Strong"])],loc="center",bbox_to_anchor=((x0+34)/180,1-54.5/170),ncol=3,fontsize=5.8,columnspacing=.9)
 for case,x0,ltr,time,colors in [("Bright",14,"c",bright_time,[GRAY,BWEAK,BLUE]),("Dark",107,"d",dark_time,[GRAY,DWEAK,TEAL])]:
  tag(f,x0,61,ltr,"Same initial field across pumps")
  for sj,x in [(0,x0),(1,x0+38)]:
   a=ax(f,x,67,32,18)
   for ti,(col,ls) in enumerate(zip(colors,[":","--","-"])):
    dist=B[f"bright_D_{ti}_{sj}"] if case=="Bright" else D["D"][:,2*ti+sj];a.semilogy(time,dist,color=col,ls=ls,lw=1.25 if ls=="-" else 1.05)
   a.set(xlim=(0,max(time)),xlabel=r"$\Gamma_0t$",ylabel=r"Distance $D_j$" if sj==0 else "");a.set_xticks([0,3,6]);a.set_title("Initial −" if sj==0 else "Initial +",fontsize=6,pad=4)
 for case,x0,ltr,time,colors in [("Bright",14,"e",bright_time,[BWEAK,BLUE]),("Dark",107,"f",dark_time,[DWEAK,TEAL])]:
  tag(f,x0,99,ltr,"Residual and normalized decay gains");a=ax(f,x0,105,69,19)
  for ci,col in [(1,colors[0]),(2,colors[1])]:
   raw=[];scaled=[]
   for sj in range(2):
    if case=="Bright":
     own=B[f"bright_D_{ci}_{sj}"];base=B[f"bright_D_0_{sj}"];raw.append(1-own/base);scaled.append(1-(own/own[0])/(base/base[0]))
    else:raw.append(D["gain"][:,2*(ci-1)+sj]);scaled.append(D["normalized_gain"][:,2*(ci-1)+sj])
   for vals,ls in [(raw,"-"),(scaled,"--")]:
    v=np.array(vals)*100;a.plot(time,v.mean(axis=0),color=col,ls=ls,lw=1.3 if ls=="-" else 1.1);a.fill_between(time,v.min(axis=0),v.max(axis=0),color=col,alpha=.11,lw=0)
  zero(a);a.set(xlim=(0,max(time)),ylim=(-3,51),xlabel=r"$\Gamma_0t$",ylabel="Reduction (%)");a.set_xticks([0,3,6]);a.set_yticks([0,25,50])
 text(f,14,137,"Solid: residual gain   Dashed: initial-distance-normalized gain",fontsize=5.8);text(f,107,137,"Bands: range of the two initial signs",fontsize=5.8)
 br=json.loads((DATA/"bright_existing_fold_rows.json").read_text(encoding="utf-8"));dr=json.loads((DATA/"dark_fold_results.json").read_text(encoding="utf-8"))
 for case,x0,ltr,z,colors in [("Bright",14,"g",np.load(DATA/"bright_fold.npz"),[BWEAK,BLUE]),("Dark",107,"h",np.load(DATA/"dark_fold_N2048_0.npz"),[DWEAK,TEAL])]:
  tag(f,x0,145,ltr,"Internal fold" if case=="Bright" else "Width fold");T=float(np.ravel(z["T"])[0]);tau,k=grid(len(z["psi"]),T)
  r=z["mode"] if case=="Bright" else z["null"];v=2*np.real(np.conj(z["psi"])*r);v/=max(abs(v))
  if case=="Dark":v=np.roll(v,len(v)//2)
  a=ax(f,x0,150,31,11);a.plot(tau,v,color=BLUE if case=="Bright" else TEAL,lw=1.3);zero(a)
  a.set(xlim=(-2,2) if case=="Bright" else (-12,12),ylim=(-1.15,1.15),xlabel=r"Fast time $\tau$",ylabel=r"$\delta I_{\rm f}$/max");a.set_yticks([-1,0,1])
  scale=1e-8 if case=="Bright" else 1e-5
  rows=[r for r in br if r["N"]==2048] if case=="Bright" else [r for r in dr if r["N"]==2048 and r["u"]>0]
  pred=np.array([r["forecast_shift"] if case=="Bright" else r["predicted_shift"] for r in rows])/scale;act=np.array([r["actual_shift"] for r in rows])/scale
  a=ax(f,x0+42,150,26,11)
  for j,c in enumerate(colors):
   a.plot([pred[j],act[j]],[j,j],color=c,lw=1.15);a.plot(pred[j],j,"|",color=c,ms=5.5,mew=1.0);a.plot(act[j],j,"o",color=c,mfc="white",ms=3.2,mew=.95)
  a.set(ylim=(-.5,1.5),xlabel=rf"$\delta\Delta_f$ ($10^{{{int(np.log10(scale))}}}$)");a.set_yticks([0,1],["Weak","Strong"]);a.set_xlim(min(0,min(act)*1.15),max(0,max(act)*1.15))
 save(f,"fig6_controlled_recovery","Same initial fields, own stationary targets, shared q scale, distinct residual/normalized gains and signed fold shifts.")
if __name__=="__main__":
 selected=set(map(int,sys.argv[1:])) if len(sys.argv)>1 else set(range(1,7))
 for n,fun in enumerate([fig1,fig2,fig3,fig4,fig5,fig6],1):
  if n in selected:fun()
 (ED/"FIGURE_BUILD_AUDIT.json").write_text(json.dumps(AUDIT,ensure_ascii=False,indent=2),encoding="utf-8")
