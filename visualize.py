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
for file in onlyfiles[:]: #13 14 , 
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

    print('group name: ', mulitLine[1])
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3)
    fig.suptitle('Element Transformation')
    rottt = aff.rotate( mulitLine[0], 180)
    #print(rottt.equals(mulitLine[0]))

    points0 = list()
    for i in mulitLine[0]:
        for line in i.coords:
            points0.append(line)
    poly = Polygon(points)

    points = list()
    for i in rottt:
        for line in i.coords:
            points.append(line)
    rotttPoly = Polygon(points)

    points2 = list()
    for i in mulitLine[0]:
        for line in i.coords:
            points2.append(line)
    rottt2 = Polygon(points2)
    x, y = poly.exterior.xy
    ax6.plot(x, y)
    print(symreco(mulitLine[0], rottt) )
    plots.plot_string(ax1,ax2,ax3,ax4,ax5, mulitLine[0])
    plt.show()

    
