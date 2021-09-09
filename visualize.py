import pickle
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from shapely.geometry import Polygon, MultiLineString, MultiPolygon, LineString
from shapely.ops import linemerge
import shapely.validation as val
from utils import translateToOrig, center, rotateRef, scale, normalize, symreco, similarity, transform, tomultpolygon
import shapely.affinity as aff
import numpy as np
import plots 


# First: use transform function to transform the multlinestrings (Translate, scale and rotation)
# Second: use similarity function for comparision. It will return 1 if they are similar and 0 if they are not.

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

    #..................... Create Figures ...................................
    #fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3)
    figComp , ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2)
    #fig.suptitle(str( mulitLine[1])+ ' ' + 'Element Transformation')

    # Plot comparision between the line string shape and their polygon representation
    plots.plot_comparison(mulitLine[0], ax1,ax2)
    plt.show()
    
    # Append all line string objects into a list 
    listOfMult.append(mulitLine[0])
    
    count+=1 
    #scaled = plots.plot_transforms(ax1,ax2,ax3,ax4,ax5, mulitLine[0])
    #plt.show()

    if count > 45:
        scaled = transform(listOfMult[10])
        scaled2 =transform(listOfMult[39])
        scaled = tomultpolygon(scaled)
        scaled2 = tomultpolygon(scaled2)
        
        dist, isSim = similarity(scaled, scaled2, polygon=1)
        print('similar:', isSim, 'dist', dist)

        # # Transform    # try 9 10 ..... 7 8 .... 11 12   14 40
        #scaled = transform(mulitLine[0])
        #scaled = tomultpolygon(scaled)
        # # convert to mult polygon 

        centrd = scaled.centroid.coords.xy
        cntrd2 = scaled.envelope.centroid.coords.xy

        if scaled.geom_type == 'MultiPolygon':
            for poly in list(scaled):
                x, y = poly.exterior.xy
                plt.plot(x, y)
                plt.plot(centrd[0], centrd[1], marker='.')
                plt.plot(cntrd2[0], cntrd2[1], marker='+')
            plt.show()
            for poly in list(scaled2):
                x, y = poly.exterior.xy
                plt.plot(x, y)
            plt.show()
        else:
            x, y = scaled.exterior.xy
            x2, y2 = scaled2.exterior.xy
            plt.plot(x, y)
            plt.plot(centrd[0], centrd[1], marker='.')
            plt.plot(cntrd2[0], cntrd2[1], marker='+')
            plt.show()
            plt.plot(x2, y2)
            plt.show()


    
    #scaled = plots.plot_transforms(ax1,ax2,ax3,ax4,ax5, mulitLine[0])
    #plt.show()

    
