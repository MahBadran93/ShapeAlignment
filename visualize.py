import pickle
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon, MultiLineString, MultiPolygon, LineString
from shapely.ops import linemerge
import shapely.validation as val
from utils import translateToOrig, center, rotateRef, scale, normalize, symreco, similarity
import shapely.affinity as aff
import numpy as np
import plots 



mypath = './pickles/'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in onlyfiles[:]: #19 20 , 
    with open(mypath + file, 'rb') as handle:
        mulitLine = pickle.load(handle)
        if mulitLine[0] is None:
            continue
    points = list()
    iter = 0
    for id in list(mulitLine[0]):
        for c in id.coords:
            points.append(c)

    if len(points) < 3:
        continue
    #print('group name: ', mulitLine[1], mulitLine[0])
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3)
    fig.suptitle('Element Transformation')

    plots.plot_string(ax1,ax2,ax3,ax4,ax5, mulitLine[0])
    plt.show()

    '''
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
    # plot = WKTPlot(title="Symbols", save_dir="./src")
    # plot.add_shape(elmnt, color="green", line_width=3)
    # plot.save()
    '''
    #plots.plot_bounds(ax1, elmnt)
    # Plotting..
    #ax1.plot(x, y)
    #ax1.plot(e1, e2)
    # ax1.set_title('Original')
    # ax2.plot(x, y)
    # ax2.plot(cc[0], cc[1], marker='+')
    # #ax1.plot(ccPoly[0], ccPoly[1], marker='.')
    # ax2.set_title('MRR')
    # ax2.plot(elmnt.envelope.exterior.xy[0], elmnt.envelope.exterior.xy[1] )
    # ax3.plot(xTrsnlt, yTrnslt)
    # ax3.plot(0, 0, marker='+')
    # ax3.plot(cx, cy, marker='.')
    # ax3.plot(cnrtdMult[0][0], cnrtdMult[0][1], marker='o')
    # ax3.set_title('Translated (MRR center)')
    # ax4.plot(ccRot[0], ccRot[1], marker='.' )
    # ax4.plot(r1, r2)
    # ax4.plot(0, 0, marker='+')
    # ax4.set_title('Rotated element')
    # #ax4.plot(ccRot[0], ccRot[1], marker='.' )
    # ax5.plot(s1, s2)
    # #ax3.plot(0, 0, marker='+')
    # ax5.set_title('Scale element')
    # plt.show()
    '''
    
