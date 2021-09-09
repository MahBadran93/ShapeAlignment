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
    figComp , ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    #fig.suptitle(str( mulitLine[1])+ ' ' + 'Element Transformation')


    
    # Append all line string objects into a list 
    listOfMult.append(mulitLine[0])
    
    count+=1 

    if count > 8:
        
        # Transfrom the shapes 
        shapeId1 = 1
        shapeId2 = 2
        trsfmdGeom1 = transform(listOfMult[shapeId1])
        trsfmdGeom2 =transform(listOfMult[shapeId2])
        trsfmdGeom1P = tomultpolygon(trsfmdGeom1)
        trsfmdGeom2P = tomultpolygon(trsfmdGeom2)

        # Find the similarity between the two shapes. If you want to test with polygons and IOU, pass polygon= 1
        # IF you want to test the similarity with the original line string objects, pass polygon= 0
        dist, isSim = similarity(trsfmdGeom1P, trsfmdGeom2P, polygon=1)

       

        if isSim == 1: 
            figComp.suptitle('The shapes are similar' + ' , ' + 'overlap:' + str(dist))
        else: 
            figComp.suptitle('The shapes are not similar' + ', ' + 'overlap:' + str(dist))

         # Plot comparision between the line string shape and their polygon representation
        plots.plot_comparison(listOfMult[shapeId1], listOfMult[shapeId2], ax1,ax2, ax3, ax4)
        plt.show()


        break

    #scaled = plots.plot_transforms(ax1,ax2,ax3,ax4,ax5, mulitLine[0])
    #plt.show()


    
