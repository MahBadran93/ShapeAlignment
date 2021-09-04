import pickle
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon, MultiLineString
from utils import translateToOrig, center, rotateRef, scale
import shapely.affinity as aff

MultiLineString

mypath = './pickles/'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in onlyfiles[:]: #19 20 
    with open(mypath + file, 'rb') as handle:
        mulitLine = pickle.load(handle)
        if mulitLine is None:
            continue
    # print('pp', len(list(mulitLine.values())))
    points = list()
    for id in list(mulitLine.values()):
        for c in id.coords:
            points.append(c)
    if len(points) < 3:
        continue

    
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3)
    fig.suptitle('Element Transformation')

    # create polygon out of element coordinates
    elmnt = Polygon(points[:-1])
    # coords of the element itself
    x, y = elmnt.exterior.xy

    # Find MRR separetly for the element for test
    # e1 and e2 are the x, y coords of the MRR of the element
    e1, e2 = elmnt.minimum_rotated_rectangle.exterior.xy


    # Find the center of MRR
    cc = center(elmnt.minimum_rotated_rectangle)
    # Find center of polygon before translation
    ccPoly = center(elmnt)


    # traslate element to origin from the MRR center
    elmntTrans = translateToOrig(elmnt)
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
 

   

   

    # Plotting..
    ax1.plot(x, y)
    ax1.plot(e1, e2)
    ax1.plot(cc[0], cc[1], marker='+')
    ax1.plot(ccPoly[0], ccPoly[1], marker='.')
    ax1.set_title('Original')
    ax2.plot(xTrsnlt, yTrnslt)
    ax2.plot(0, 0, marker='+')
    ax2.plot(cx, cy, marker='.')
    ax2.set_title('Translated (MRR center)')
    ax3.plot(ccRot[0], ccRot[1], marker='.' )
    ax3.plot(r1, r2)
    ax3.plot(0, 0, marker='+')
    ax3.set_title('Rotated element')
    #ax4.plot(ccRot[0], ccRot[1], marker='.' )
    ax4.plot(s1, s2)
    #ax3.plot(0, 0, marker='+')
    ax4.set_title('Scale element')
    plt.show()
