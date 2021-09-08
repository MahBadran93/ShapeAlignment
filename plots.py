from matplotlib import pyplot
from shapely.geometry import LineString, Polygon, Point
from utils import translateToOrig, rotateRef, scale, symreco
import  shapely.affinity as aff 



# xs = [x[0] for x in points]
# ys = [x[1] for x in points] 



def plot_transforms(ax1,ax2,ax3,ax4,ax5, mltline, colorMain='red', colorMRR='green'):
   
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
        
    #........................................................................................

    # Plot center and centroid 
    cx, cy = mltline.envelope.centroid.xy # minimum_rotated_rectangle
    mx, my = mltline.envelope.exterior.xy
    ax2.plot(mx, my, color=colorMRR, zorder=1)
    ax2.plot(cx, cy, marker='+', markersize = 6, color=colorMRR, zorder=1)
    ax2.plot(mltlineCntrd[0], mltlineCntrd[1], marker='o')
    ax2.set_title('MRR')
    #.............................................................................................

    # Translation 
    for line in list(lineTrans):
        for c in line.coords:
            lines.append(c)
        x, y = line.coords.xy
        
        ax3.plot(x, y, color=colorMain, zorder=1)
        ax3.plot(0, 0, marker='+')
        ax3.plot(lineTransCentd[0], lineTransCentd[1], marker='o')
        ax3.set_title('Translation')

   
    #.......................................................................................................

    # Rotation 
    if symreco(mltline, aff.rotate(mltline, 180)):
        print('shape is symmetric...')
        lineTransMRR = lineTrans.envelope 
        x, y = lineTransMRR.exterior.xy
        # (width, height)
        edge_length = (Point(x[0], y[0]).distance(Point(x[1], y[1])), Point(x[1], y[1]).distance(Point(x[2], y[2])))
        width = edge_length[0]
        height = edge_length[1]
        if width > height:
            rottdStrtL = aff.rotate(lineTrans, 90)
            for line in list(rottdStrtL):
                for c in line.coords:
                    lines.append(c)
                x, y = line.coords.xy
                ax4.plot(x, y, color=colorMain, zorder=1)
                ax4.set_title('Rotation')
        else:
            rottdStrtL = aff.rotate(lineTrans, 0)
            for line in list(rottdStrtL):
                for c in line.coords:
                    lines.append(c)
                x, y = line.coords.xy
                ax4.plot(x, y, color=colorMain, zorder=1)
                ax4.set_title('Rotation')
    else:
        rottdStrtL = rotateRef(lineTrans)
        for line in list(rottdStrtL):
            for c in line.coords:
                lines.append(c)
            x, y = line.coords.xy
            ax4.plot(x, y, color=colorMain, zorder=1)
            ax4.set_title('Rotation')

        # Plot center and centorid after rotation 
        rx, ry = rottdStrtL.centroid.coords.xy
        ax4.plot(rx, ry, marker='o', color=colorMRR, zorder=1)
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

