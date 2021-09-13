from matplotlib import pyplot
from shapely.geometry import LineString, Polygon, Point
from utils import translateToOrig, rotateRef, scale, symreco, tomultpolygon
import  shapely.affinity as aff 
import matplotlib.pyplot as plt



# xs = [x[0] for x in points]
# ys = [x[1] for x in points] 

def plot_comparison (geom1, geom2, transformed1, transformed2):

    """
    Plots original multiple lines object compared to their corresponding polygons
    Input:
        - geom1: multi line string object (shapely)
        - geom2: multi line string object (shapely)
        - transformed1: transformed multi line string object (shapely)
        - transformed2: transformed multi line string object (shapely)
    
    """

    # Figure 
    figComp , ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(nrows=2, ncols=4)
    plt.rc('font', size=5)     

    # First shape 
    for line in list(geom1):
        x, y = line.coords.xy
        ax1.plot(x, y)
        ax1.set_title('Original linestring 1')
    geomM1 = tomultpolygon(geom1)

    if geomM1.geom_type == 'Polygon':
        x1, y1 = geomM1.exterior.xy
        ax2.plot(x1, y1)
        ax2.set_title('Multi polygon 1')
    else: # in case of multiple polygons 
        for poly in geomM1:
            x1, y1 = poly.exterior.xy
            ax2.plot(x1, y1)
            ax2.set_title('Multi polygon 1')
    
    # Second shape 
    for line in list(geom2):
        x, y = line.coords.xy
        ax3.plot(x, y)
        ax3.set_title('Original linestring 2 ')
    geomM2 = tomultpolygon(geom2)
    if geomM2.geom_type == 'Polygon':
        x1, y1 = geomM2.exterior.xy
        ax4.plot(x1, y1)
        ax4.set_title('Multi polygon 2')
    else: # in case of multiple polygons 
        for poly in geomM2:
            x1, y1 = poly.exterior.xy
            ax4.plot(x1, y1)
            ax4.set_title('Multi polygon 2')

    # Transformed shape 1
    for line in list(transformed1):
        x, y = line.coords.xy
        ax5.plot(x, y)
        ax5.set_title('Transformed shape 1')
    trfrmd1 = tomultpolygon(transformed1)
    if trfrmd1.geom_type == 'Polygon':
        x1, y1 = trfrmd1.exterior.xy
        ax6.plot(x1, y1)
        ax6.set_title('Multi polygon transformed 1')
    else: # in case of multiple polygons 
        for poly in trfrmd1:
            x1, y1 = poly.exterior.xy
            ax6.plot(x1, y1)
            ax6.set_title('Multi polygon transformed 1')


    # Transformed shape 2
    for line in list(transformed2):
        x, y = line.coords.xy
        ax7.plot(x, y)
        ax7.set_title('Transformed shape 2')

    trfrmd2 = tomultpolygon(transformed2)
    if trfrmd2.geom_type == 'Polygon':
        x1, y1 = trfrmd2.exterior.xy
        ax8.plot(x1, y1)
        ax8.set_title('Multi polygon transformed 2')
    else: # in case of multiple polygons 
        for poly in trfrmd2:
            x1, y1 = poly.exterior.xy
            ax8.plot(x1, y1)
            ax8.set_title('Multi polygon transformed 2')
    plt.show()


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

def similarity (geom1, geom2, ax1, ax2):
    pass
