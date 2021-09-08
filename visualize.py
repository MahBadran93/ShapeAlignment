import pickle
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon, MultiLineString, MultiPolygon, LineString
from shapely.ops import linemerge
import shapely.validation as val
from utils import translateToOrig, center, rotateRef, scale, normalize, symreco, similarity, transform
import shapely.affinity as aff
import numpy as np
import plots 



mypath = './pickles/'
count = 0
listOfMult = []

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
    #fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3)
    #fig.suptitle(str( mulitLine[1])+ ' ' + 'Element Transformation')
    rottt = aff.rotate( mulitLine[0], 180)
  
    listOfMult.append(mulitLine[0])
    count+=1 
    if(count > 44):
        lines = list()
        scaled = transform(listOfMult[0])
        scaled2 =transform(listOfMult[44])
        geom1 =  scaled #listOfMult[0]
        geom2 = scaled2 #listOfMult[44]  


        for line in list(geom1):
                for c in line.coords:
                    lines.append(c)
                x, y = line.coords.xy
                plt.plot(x, y)
        plt.show()
        lines = list()
        for line in list(geom2):
                for c in line.coords:
                    lines.append(c)
                x, y = line.coords.xy
                plt.plot(x, y)
        dist, isSim = similarity(geom1, geom2)
        print('similar:', isSim, 'dist', dist)
        plt.show()
        break



    #scaled = plots.plot_transforms(ax1,ax2,ax3,ax4,ax5, mulitLine[0])
    #plt.show()

    
