from matplotlib import pyplot
from shapely.geometry import LineString, Polygon, Point
from utils import translateToOrig, rotateRef, scale, symreco, tomultpolygon
import  shapely.affinity as aff 



# xs = [x[0] for x in points]
# ys = [x[1] for x in points] 

def plot_comparison (geom, ax1, ax2):
    """
    Plots original multiple lines object compared to their corresponding polygons
    Input:
        - geom: multi line string object (shapely)
    
    """
    for line in list(geom):
        x, y = line.coords.xy
        ax1.plot(x, y)
        ax1.set_title('Original linestrings')
    geom = tomultpolygon(geom)
    if geom.geom_type == 'Polygon':
        x1, y1 = geom.exterior.xy
        ax2.plot(x1, y1)
        ax2.set_title('Multi polygon')
    else: # in case of multiple polygons 
        for poly in tomultpolygon(geom):
            x1, y1 = poly.exterior.xy
            ax2.plot(x1, y1)
            ax2.set_title('Multi polygon')



def plot_transforms (ax1,ax2,ax3,ax4,ax5, mltline, colorMain='red', colorMRR='green'):
    
    """
    Plot the transformation process
    Input:
        - the axis plots from matplotlib 
        - mltline : A shapely multiple line string object 
    
    """
    #........................................................................................

    lines = list()
    lineTrans = translateToOrig(mltline)
    mltlineCntrd = mltline.centroid.coords.xy
    lineTransCentd = lineTrans.centroid.coords.xy

    # Original 
    for line in list(mltline):
        for c in line.coords:
            lines.append(c)
        x, y = line.coords.xy
        ax1.plot(x, y, color=colorMain, zorder=1)
        ax1.set_title('Original')
        ax2.plot(x, y, color=colorMain, zorder=1)
        

    # Plot center and centroid 
    cx, cy = mltline.envelope.centroid.xy # minimum_rotated_rectangle
    mx, my = mltline.envelope.exterior.xy
    ax2.plot(mx, my, color=colorMRR, zorder=1)
    ax2.plot(cx, cy, marker='+', markersize = 6, color=colorMRR, zorder=1)
    ax2.plot(mltlineCntrd[0], mltlineCntrd[1], marker='.')
    ax2.set_title('MRR')


    #.............................................................................................

    # Translation 
    for line in list(lineTrans):
        for c in line.coords:
            lines.append(c)
        x, y = line.coords.xy
        
        ax3.plot(x, y, color=colorMain, zorder=1)
        ax3.plot(0, 0, marker='+')
        ax3.plot(lineTransCentd[0], lineTransCentd[1], marker='.')
        ax3.set_title('Translation')

   
    #.......................................................................................................

    # Rotation 
    rottdStrtL = rotateRef(lineTrans)
    for line in list(rottdStrtL):
        for c in line.coords:
            lines.append(c)
        x, y = line.coords.xy
        ax4.plot(x, y, color=colorMain, zorder=1)
        ax4.set_title('Rotation')

    # Plot center and centorid after rotation 
    rx, ry = rottdStrtL.centroid.coords.xy
    ax4.plot(rx, ry, marker='.', color=colorMRR, zorder=1)
    ax4.plot(0, 0, marker='+', markersize = 6, color=colorMRR, zorder=1)
    #.................................................................................................
    

    # Scaling 
    scldStrtLn = scale(rottdStrtL)
    for line in list(scldStrtLn):
        for c in line.coords:
            lines.append(c)
        x, y = line.coords.xy 
        ax5.plot(x, y, color=colorMain, zorder=1)
    ax5.set_title('scaling')

    return scldStrtLn

