"""Export only the Fig.1a device, using identical code and scientific profile."""
from pathlib import Path
import rebuild_figures as r
def main():
 f=r.plt.figure(figsize=(62/25.4,38.75/25.4),dpi=300)
 a=f.add_axes([0,0,1,1])
 x,I=r.arr(1,2,0)
 r.draw_classic_cavity(a,x,I)
 out=Path(__file__).resolve().parent/"device_preview";out.mkdir(exist_ok=True)
 for ext in ["pdf","svg","png"]:
  f.savefig(out/("Fig1a_device_R422."+ext),dpi=600)
 r.plt.close(f)
 print(str(out))
if __name__=="__main__":main()
