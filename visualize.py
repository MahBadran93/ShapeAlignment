import pickle
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon, MultiLineString, MultiPolygon
import shapely.validation as val
from utils import translateToOrig, center, rotateRef, scale, normalize, symreco, similarity
import shapely.affinity as aff
import numpy as np
#from wktplot.wkt_plot import WKTPlot


MultiLineString

mypath = './pickles/'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in onlyfiles[:]: #19 20 , 
    print(file)
    with open(mypath + file, 'rb') as handle:
        mulitLine = pickle.load(handle)
        if mulitLine[0] is None:
            continue
    points = list()
    iter = 0
    for id in list(mulitLine[0]):
        for c in id.coords: 
            p1 = int(c[0])
            p2 = int(c[1])
            #c = (p1, p2)
            points.append(c)

    if len(points) < 3:
        continue

    print('group name: ', mulitLine[1], mulitLine[0])
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3)
    fig.suptitle('Element Transformation')


    # create polygon out of element coordinates
  
    elmnt = Polygon(points)
    #elmnt = elmnt.buffer(0)
    elmnt = elmnt.simplify(tolerance=0.0)

    #print('sym: ', symreco(elmnt))
    #elmnt = normalize(elmnt)
    
    # coords of the original element
    x, y = elmnt.exterior.xy
    # Find the center of MRR
    cc = center(elmnt.envelope)
    # Find center of polygon before translation
    ccPoly = center(elmnt)


    # traslate element to origin from the MRR center
    elmntTrans = translateToOrig(elmnt)
    #symreco(elmntTrans)
    # coords of the translated element
    xTrsnlt , yTrnslt = elmntTrans.exterior.xy
    # centroid of the translated element
    cx, cy = elmntTrans.centroid.xy

    # rotate element after translation
    rotElmntTrans = rotateRef(elmntTrans)
    # find centeroid of rotated element after translation
    ccRot = center(rotElmntTrans)
    # rotated element coords 
    r1, r2 = rotElmntTrans.exterior.xy


    # Scale 
    scldElement = scale(rotElmntTrans)
    s1, s2 = scldElement.exterior.xy
 

   

    # save plots 
    '''
    plot = WKTPlot(title="Symbols", save_dir="./src")
    plot.add_shape(elmnt, color="green", line_width=3)
    plot.save()
    '''

    # Plotting..
    ax1.plot(x, y)
    #ax1.plot(e1, e2)
    ax1.set_title('Original')
    ax2.plot(x, y)
    ax2.plot(cc[0], cc[1], marker='+')
    #ax1.plot(ccPoly[0], ccPoly[1], marker='.')
    ax2.set_title('MRR')
    ax2.plot(elmnt.envelope.exterior.xy[0], elmnt.envelope.exterior.xy[1] )
    ax3.plot(xTrsnlt, yTrnslt)
    ax3.plot(0, 0, marker='+')
    ax3.plot(cx, cy, marker='.')
    ax3.set_title('Translated (MRR center)')
    ax4.plot(ccRot[0], ccRot[1], marker='.' )
    ax4.plot(r1, r2)
    ax4.plot(0, 0, marker='+')
    ax4.set_title('Rotated element')
    #ax4.plot(ccRot[0], ccRot[1], marker='.' )
    ax5.plot(s1, s2)
    #ax3.plot(0, 0, marker='+')
    ax5.set_title('Scale element')
    plt.show()
