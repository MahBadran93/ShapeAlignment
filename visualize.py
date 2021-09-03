import pickle
import shapley
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon, MultiLineString
from utils import translateToOrig, center, translateToPoly, scalePoly, scaleUnitNorm
import shapely.affinity as aff

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3)
fig.suptitle('Element Transformation')

mypath = 'C:/Users/user/Desktop/shapProj/pickles/'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in onlyfiles[:1]:
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

    # create polygon out of element coordinates
    elmnt = Polygon(points)

    # Find MRR separetly for the element for test
    # e1 and e2 are the x, y coords of the MRR of the element
    e1, e2 = elmnt.minimum_rotated_rectangle.exterior.xy

    # Find the center of MRR
    cc = center(elmnt.minimum_rotated_rectangle)

    # traslate element to origin from the MRR center
    elmntTrans = translateToOrig(elmnt)

    # coords of the element itself
    x, y = elmnt.exterior.xy

    # coords of the translated element
    xTrsnlt , yTrnslt = elmntTrans.exterior.xy

    # centroid of the translated element
    cx, cy = elmntTrans.centroid.xy

    # Plotting..
    ax1.plot(x, y)
    ax1.plot(e1, e2)
    ax1.plot(cc[0], cc[1], marker='+')
    ax1.set_title('Original')
    ax2.plot(xTrsnlt, yTrnslt)
    ax2.plot(0, 0, marker='+')
    ax2.plot(cx, cy, marker='.')
    ax2.set_title('Translated (MRR center)')
    plt.show()

