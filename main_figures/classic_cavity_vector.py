"""Smooth silver Kerr-ring schematic. All geometry and shading are reproducible.
The device is schematic: no dimensions, measured geometry or extra solitons are implied.
The sole ring pulse is a display mapping of the supplied bright-state intensity.
"""
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Rectangle, Ellipse, FancyArrowPatch
from matplotlib.transforms import Affine2D
from scipy.interpolate import PchipInterpolator

BG="#EDF6FC"
RED="#D7191C"
EDGE="#79828B"

def _ellipse_path(cx,cy,rx,ry):
    return Affine2D().scale(rx,ry).translate(cx,cy).transform_path(Path.unit_circle())

def _annulus(cx,cy,rx,ry,ix,iy):
    outer=_ellipse_path(cx,cy,rx,ry)
    # Reflect the inner circle to reverse winding, leaving a true open hole.
    inner=Affine2D().scale(-ix,iy).translate(cx,cy).transform_path(Path.unit_circle())
    return Path.make_compound_path(outer,inner)

def _closed(x,y):
    v=np.column_stack([x,y])
    return Path(np.vstack([v,v[0]]),np.r_[Path.MOVETO,np.full(len(v)-1,Path.LINETO),Path.CLOSEPOLY])

def _gradient(ax,path,extent,rgb,z,edge=None,lw=.45):
    clip=PathPatch(path,facecolor="none",edgecolor="none",zorder=z)
    ax.add_patch(clip)
    image=ax.imshow(rgb,extent=extent,origin="lower",interpolation="bilinear",zorder=z)
    image.set_clip_path(clip)
    if edge:
        ax.add_patch(PathPatch(path,facecolor="none",edgecolor=edge,lw=lw,zorder=z+.02,
                               antialiased=True,joinstyle="round"))
    return clip

def _mix(weight,dark,light):
    return np.asarray(dark)[None,None,:]*(1-weight[...,None])+np.asarray(light)[None,None,:]*weight[...,None]

def draw_classic_cavity(ax,pulse_tau,pulse_intensity):
    """Circular annulus in oblique projection, straight bus, one upward red pulse."""
    ax._smooth_schematic=True
    ax.axis("off")
    cx,cy=.65,.388
    rx,ry=.365,.202
    ix,iy=.313,.173
    depth=.046
    ext=(.035,1.265,.055,.765)
    gx,gy=np.meshgrid(np.linspace(ext[0],ext[1],1000),np.linspace(ext[2],ext[3],600))
    # Pale blue substrate; no warm tint, texture or sketch perturbation.
    shade=np.clip(.55+.28*(gy-ext[2])/(ext[3]-ext[2]),0,1)
    background=_mix(shade,[.895,.946,.980],[.958,.981,.998])
    _gradient(ax,Rectangle((ext[0],ext[2]),ext[1]-ext[0],ext[3]-ext[2]).get_path().transformed(
        Rectangle((ext[0],ext[2]),ext[1]-ext[0],ext[3]-ext[2]).get_patch_transform()),ext,background,0)
    # Soft grounding shadow stays on the substrate.
    for d,alpha in [(0,.035),(.008,.025),(.016,.018)]:
        ax.add_patch(Ellipse((cx,cy-depth-.014),2*(rx+d),2*(ry*.92+d*.5),
                            facecolor="#647F94",edgecolor="none",alpha=alpha,zorder=.5))
    # Straight silver bus; the visible gap at the closest point is 0.005 schematic units,
    # under one quarter of the projected waveguide width, not a device dimension.
    ax.add_patch(Rectangle((.10,.595),1.10,.026,facecolor="#AEB7BF",edgecolor="#8D98A1",lw=.4,zorder=1))
    bpath=Rectangle((.10,.613),1.10,.026)
    bs=np.clip(.65+.30*np.exp(-((gy-.631)/.007)**2)+.04*(gx-.1),0,1)
    _gradient(ax,bpath.get_path().transformed(bpath.get_patch_transform()),ext,
              _mix(bs,[.66,.69,.72],[.995,.998,1.]),1.1,edge="#B3BDC5",lw=.4)
    ax.add_patch(PathPatch(Path([[.105,.637],[1.195,.637]],[Path.MOVETO,Path.LINETO]),
                           fill=False,lw=.75,edgecolor="white",zorder=1.2))
    ax.annotate("",xy=(1.205,.625),xytext=(1.12,.625),
                arrowprops=dict(arrowstyle="->",color="#596771",lw=.65,mutation_scale=6))
    # Inner back wall and outer front wall create a continuous solid annulus.
    th=np.linspace(0,np.pi,401)
    x=cx+ix*np.cos(th);y=cy+iy*np.sin(th)
    innerwall=_closed(np.r_[x,x[::-1]],np.r_[y,(y-depth)[::-1]])
    value=np.clip(.22+.65*(gy-(cy-depth))/(2*ry),0,1)
    _gradient(ax,innerwall,ext,_mix(value,[.51,.55,.59],[.88,.90,.92]),2,edge="#909AA3",lw=.35)
    th=np.linspace(np.pi,2*np.pi,501)
    x=cx+rx*np.cos(th);y=cy+ry*np.sin(th)
    frontwall=_closed(np.r_[x,x[::-1]],np.r_[y,(y-depth)[::-1]])
    shine=np.clip(.34+.46*np.exp(-((gx-.49)/.38)**2)+.11*(gy-.12)/.25,0,1)
    _gradient(ax,frontwall,ext,_mix(shine,[.50,.54,.58],[.88,.91,.93]),2.2,edge="#7D8791",lw=.5)
    # Polished top face. Radial and broad specular highlights have no jagged seams.
    radial=np.sqrt(((gx-cx)/rx)**2+((gy-cy)/ry)**2)
    silver=np.clip(.62+.18*(gy-cy)/ry+.20*np.exp(-((radial-.93)/.035)**2)
                   +.055*np.exp(-((gx-.47)/.20)**2),0,1)
    _gradient(ax,_annulus(cx,cy,rx,ry,ix,iy),ext,
              _mix(silver,[.64,.68,.71],[.995,.998,1.]),3,edge="#909AA3",lw=.5)
    # Thin, geometrically exact bevels and clean specular rim.
    ax.add_patch(PathPatch(_annulus(cx,cy,rx-.002,ry-.001,rx-.009,ry-.005),
                           facecolor="#F7FBFD",edgecolor="none",zorder=3.2))
    ax.add_patch(PathPatch(_ellipse_path(cx,cy,ix,iy),fill=False,
                           edgecolor="#858F98",lw=.5,zorder=3.3))
    th=np.linspace(.08,np.pi-.08,401)
    ax.add_patch(PathPatch(Path(np.column_stack([cx+(ix+.004)*np.cos(th),cy+(iy+.002)*np.sin(th)])),
                           fill=False,edgecolor="#FFFFFF",lw=.75,zorder=3.4))
    # One upright intracavity pulse; periodic copies are shown in the separate pump train.
    t=np.asarray(pulse_tau,float);I=np.asarray(pulse_intensity,float)
    q=np.abs(t)<=1.35
    u=np.linspace(float(t[q].min()),float(t[q].max()),800)
    background=float(np.median(np.r_[I[q][:4],I[q][-4:]]))
    amp=np.maximum(PchipInterpolator(t[q],I[q])(u)-background,0)/(float(np.max(I))-background)
    theta=-1.02+.80*u
    px=cx+.338*np.cos(theta)
    base=cy+.187*np.sin(theta)
    top=base+.283*amp
    pulse_path=_closed(np.r_[px,px[::-1]],np.r_[top,base[::-1]])
    # Red body with a lighter broad specular reflection.
    reflection=np.clip(.20+.55*np.exp(-((gx-.790)/.035)**2)+.08*(gy-.25),0,1)
    red_rgb=_mix(reflection,[.70,.025,.035],[1.,.40,.39])
    _gradient(ax,pulse_path,ext,red_rgb,5)
    ax.add_patch(PathPatch(Path(np.column_stack([px[amp>.02],top[amp>.02]])),fill=False,
                           edgecolor="#D12B31",lw=1.20,joinstyle="round",zorder=5.2))
    # A fine highlight follows the ascending shoulder without changing the pulse profile.
    shoulder=(u>-.50)&(u<-.03)
    ax.add_patch(PathPatch(Path(np.column_stack([px[shoulder]-.002,top[shoulder]+.001])),
                           fill=False,edgecolor="#FFB3AC",lw=.5,zorder=5.3))
    # Circulation cue in a clear region of the hole.
    th=np.linspace(np.deg2rad(158),np.deg2rad(102),150)
    vx=cx+.255*np.cos(th);vy=cy+.135*np.sin(th)
    ax.add_patch(PathPatch(Path(np.column_stack([vx,vy])),fill=False,
                           edgecolor=RED,lw=.95,zorder=6))
    ax.add_patch(FancyArrowPatch((vx[-8],vy[-8]),(vx[-1],vy[-1]),
                                arrowstyle="-|>",mutation_scale=7,color=RED,lw=.75,zorder=6))
    # Labels occupy clear margins, with no letters on a waveguide or pulse.
    ax.text(.105,.674,r"$S(\tau)$",fontsize=6.5,color="#3D4A55",va="bottom")
    ax.text(.65,.674,"Bus waveguide",fontsize=5.8,color="#536673",ha="center",va="bottom")
    ax.text(1.15,.674,"Output",fontsize=6.4,color="#3D4A55",ha="center",va="bottom")
    ax.annotate("Kerr cavity",xy=(.365,.235),xytext=(.13,.075),fontsize=6.5,
                color="#3D4A55",va="center",ha="left",
                arrowprops=dict(arrowstyle="-",color="#8B9DAA",lw=.5))
    ax.set_xlim(0,1.30);ax.set_ylim(0,.82)
    ax.set_aspect("equal",adjustable="box")

