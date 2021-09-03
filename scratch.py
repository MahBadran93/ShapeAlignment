import pickle
import shapley
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon, MultiLineString
from utils import translateToOrig, center, translateToPoly, scalePoly, scaleUnitNorm
import shapely.affinity as aff

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3)
fig.suptitle('Symbols')

mypath = 'C:/Users/user/Desktop/shapProj/pickles/'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in onlyfiles[:1]:
    with open(mypath + file, 'rb') as handle:
        mulitLine = pickle.load(handle)
        if mulitLine is None:
            continue
    #print('pp', len(list(mulitLine.values())))
    points = list()
    for id in list(mulitLine.values()):
        for c in id.coords:
            points.append(c)
    if len(points) < 3:
        continue
    # create polygon out of coordinates
    a = Polygon(points[:-1])
    noTrans = Polygon(points[:-1])

    a_rotate = aff.rotate(a, 90)
    a_scale = aff.scale(a, 10, 10, origin=(0, 0))
    a_scale_Rot = aff.rotate(a_scale, 90)

    # print(ls_points)
    # print(set_points)
    # print(ls_set_points)

    # translate polygon to origin
    a = translateToOrig(a)
    a_rotate = translateToOrig(a_rotate)
    a_scale = translateToOrig(a_scale)
    a_scale_Rot = translateToOrig(a_scale_Rot)




    # find the minimum rotated bounding box
    a_bbox = a.minimum_rotated_rectangle
    r_bbox = a_rotate.minimum_rotated_rectangle
    s_bbox = a_scale.minimum_rotated_rectangle
    
    #a_bbox = translateToOrigin(a_bbox)
    #params = mulitLine.bounds
    #h = params[3] - params[1]
    #w = params[2] - params[0]
    #c1 = (params[3] + params[1]) / 2
    #c2 = (params[2] + params[0]) / 2
    #center = (c1, c2)
    #print('height:', h,'width:', w)

    # Find the centroid
    centroid = a.centroid.xy
    r_centroid = a_rotate.centroid.xy
    # Find the center
    center = a_bbox.centroid.xy
    r_center = r_bbox.centroid.xy

    # Create centroid points for both polygons
    centroid_P = (centroid[0][0], centroid[1][0])
    r_centroidP = (r_centroid[0][0], r_centroid[1][0])

    center_P = (center[0][0], center[1][0])
    r_centerP = (r_center[0][0], r_center[1][0])

    print('centroid:', centroid_P, 'center:', center_P)

    # Scale
    #a = aff.scale(a, 3, origin=(0, 0))
    #a = scalePoly(a, 3)
    #a = scaleUnitNorm(a)

    # Coords
    x, y = a.exterior.xy
    sX, sY = a_scale.exterior.xy
    rX, rY = a_rotate.exterior.xy
    nX, nY = noTrans.exterior.xy
    sRX, sRY = a_scale_Rot.exterior.xy

    # Coords bboxes
    x_bbox, y_bbox = a_bbox.exterior.xy
    sX_bbox, sY_bbox = s_bbox.exterior.xy
    rX_bbox, rY_bbox = r_bbox.exterior.xy

    ax1.plot(nX, nY)
    ax2.plot(x, y)
    ax2.plot(centroid_P[0], centroid_P[1], marker='.', markersize=10)
    ax3.plot(x, y)
    ax3.plot(centroid_P[0], centroid_P[1], marker='.', markersize=10)
    ax3.plot(x_bbox, y_bbox)
    ax4.plot(x, y)
    ax4.plot(centroid_P[0], centroid_P[1], marker='.', markersize=10)
    ax4.plot(x_bbox, y_bbox)
    ax4.plot(center_P[0], center_P[1], marker='+', markersize=10)
    ax5.plot(rX, rY)
    ax5.plot(rX_bbox, rY_bbox)
    ax5.plot(r_centroidP[0], r_centroidP[1], marker='.', markersize=10)
    ax5.plot(r_centerP[0], r_centerP[1], marker='+', markersize=10)
    ax6.plot(sRX, sRY)

    #plt.plot(x_bbox, y_bbox)
    plt.show()

