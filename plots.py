from matplotlib import pyplot
from shapely.geometry import LineString, Polygon
from utils import translateToOrig, rotateRef, scale



# xs = [x[0] for x in points]
# ys = [x[1] for x in points] 

COLOR = {
    True:  '#6699cc',
    False: '#ffcc33'
    }

SIZE = 10

def v_color(ob):
    return COLOR[ob.is_simple]



def plot_string(ax1,ax2,ax3,ax4,ax5, mltline, colorMain='red', colorMRR='green'):
   
    lines = list()
    lineTrans = translateToOrig(mltline)
    lineTransCentd = lineTrans.centroid.coords.xy

    # Original 
    for line in list(mltline):
        for c in line.coords:
            lines.append(c)
        x, y = line.coords.xy
        ax1.plot(x, y, color=colorMain, zorder=1)
        ax2.plot(x, y, color=colorMain, zorder=1)

    # Plot center and centroid 
    cx, cy = mltline.envelope.centroid.xy
    mx, my = mltline.envelope.exterior.xy
    ax2.plot(mx, my, color=colorMRR, zorder=1)
    ax2.plot(cx, cy, marker='+', markersize = 6, color=colorMRR, zorder=1)

    # Translation 
    for line in list(lineTrans):
        for c in line.coords:
            lines.append(c)
        x, y = line.coords.xy
        
        ax3.plot(x, y, color=colorMain, zorder=1)
        ax3.plot(0, 0, marker='+')
        ax3.plot(lineTransCentd[0], lineTransCentd[1], marker='o')
    
    # Rotation 
    rottdStrtL = rotateRef(lineTrans)
    for line in list(rottdStrtL):
        for c in line.coords:
            lines.append(c)
        x, y = line.coords.xy
        
        ax4.plot(x, y, color=colorMain, zorder=1)
        #ax3.plot(0, 0, marker='+')
        #ax3.plot(lineTransCentd[0], lineTransCentd[1], marker='o')

    # Plot center and centorid after rotation 
    rx, ry = rottdStrtL.centroid.coords.xy
    ax4.plot(rx, ry, marker='o', color=colorMRR, zorder=1)
    ax4.plot(0, 0, marker='+', markersize = 6, color=colorMRR, zorder=1)
    

    # Scaling 
    scldStrtLn = scale(rottdStrtL)
    for line in list(scldStrtLn):
        for c in line.coords:
            lines.append(c)
        x, y = line.coords.xy 
        ax5.plot(x, y, color=colorMain, zorder=1)
    


    # Translate 
    #transldString = translateToOrig(mltline)
    #tx, ty = transldString.coords.xy
    #ax3.plot(tx, ty, color=colorMRR, zorder=1)

def plot_poly(ax, mltline, colorMain='red', colorCent='blue'):
    x, y = mltline.exterior.xy
    ax.plot(x, y, color=colorMain, zorder=1)


def plot_bounds(ax, ob):
    x, y = zip(*list((p.x, p.y) for p in ob.boundary))
    ax.plot(x, y, 'o', color='#000000', zorder=1)

def plot_line(ax, ob):
    x, y = ob.xy
    ax.plot(x, y, color=v_color(ob), alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

