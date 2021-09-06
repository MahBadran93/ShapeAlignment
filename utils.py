import shapely.geometry as geom
import shapely.affinity as aff
import numpy as np
import matplotlib.pyplot as plt
import math
import cv2
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import shapely.geometry
from shapely.geometry.point import Point

def normalize (poly):
    polyArray = np.array(poly.exterior.xy)

    maxX = np.max(polyArray[0])
    maxY = np.max(polyArray[1])

    x = polyArray[0]/maxX
    y = polyArray[1]/maxY
    
    points = [list(points) for points in zip(x, y)]
    polyNorm = Polygon(points)

    x, y = polyNorm.exterior.xy

    return polyNorm



def center (poly):
    c1, c2 = poly.centroid.xy
    centerPoly = (c1, c2)
    centerPoint= (centerPoly[0][0], centerPoly[1][0])
    return centerPoint



def translateToOrig (poly, origin=(0, 0)):
    # Find the minimum rotation rectangle
    #polyMRR = poly.minimum_rotated_rectangle
    polyMRR = poly.envelope

    # Find Center of MRR
    centerp = center(polyMRR)

    # Find offset point to translate polygon to origin
    xOff = -(centerp[0] - origin[0])
    yOff = -(centerp[1] - origin[0])

    trnsltPoly = aff.translate(poly, xoff=xOff, yoff=yOff)

    return trnsltPoly



def rotateRef (poly, baseV=(1, 0)):

    # center of the polygon after translation to origin: Centroid 
    centroid = center(poly)

    # Round the centroid 
    #cent1 = round(centroid[0])
    #cent2 = round(centroid[1])


    # Using arsin 
    '''
    cntrdNorm = np.sqrt(centroid[0]**2 + centroid[1]**2)
    #thetaRad =  centroid[0] / cntrdNorm 
    #thetaRad = math.degrees(thetaRad)
    val = centroid[1] / cntrdNorm
    angle = np.arcsin(val)
    angle = math.degrees(angle)
    
    '''
     # Using cross product 
    dotP = (centroid[0] * baseV[0]) + (centroid[1] * baseV[1]) 
    normCntrd = np.sqrt(centroid[0]**2 + centroid[1]**2)
    normBaseV = np.sqrt(baseV[0]**2 + baseV[1]**2)
    val = dotP / (normCntrd * normBaseV)
    angle = math.acos(val)
    angle = math.degrees(angle)
    
    centroid = np.array(centroid)
    centroid = np.round(centroid, 2)

    if centroid[1] >= 0:
        rotAngle = 270.0 - angle
    elif centroid[1] <= 0 and centroid[0] <= 0:
        rotAngle = 90 - angle #(270.0 + angle) - 360.0
    elif centroid[1] <= 0 and centroid[0] >= 0:
        rotAngle = -(90 - angle) #-(270.0 + (180.0 - angle))


    '''
    if angle < 270.0 or angle == 270.0:
        rotAngle = 270.0 - angle
        print(rotAngle)
    else: 
        rotAngle = (270.0 + angle) - 360.0
        print('After', rotAngle)
    '''
    

    rotPoly = aff.rotate(poly, rotAngle)

    return rotPoly



def scale (poly):
    xFactor = 1
    (minx, miny, maxx, maxy) = poly.bounds 
    polyHgt = maxy - miny
    polywdth = maxx - minx 

    yFactor = 10 / polyHgt
    return aff.scale(poly,xfact=xFactor, yfact=yFactor)


def similarity (poly1, poly2):
    poly1 = poly1.buffer(0)
    poly2 = poly2.buffer(0)
    intxGeom = poly1.intersection (poly2) 
    overlap = 0.5 * (intxGeom.area/poly1.area + intxGeom.area/poly2.area)
    return overlap
        

def symreco (poly):
    # check the area of overlap between a symbol and its 180 degree rotation symbol.
    # the closer to, the more symmetric is the shape.
    isSym = False
    rotelmnt =  aff.rotate(poly, 180)
    overlap = similarity(poly, rotelmnt)
    if (overlap >= 0.99):
        isSym = True
    return isSym













