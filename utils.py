import shapely.geometry as geom
import shapely.affinity as aff
import numpy as np
import matplotlib.pyplot as plt
import math
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
    if centroid == (0, 0):
        rotAngle = 0
    else:
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

def rotateSym (poly):
    pass

def scale (poly):
    xFactor = 1
    (minx, miny, maxx, maxy) = poly.bounds 
    polyHgt = maxy - miny
    polywdth = maxx - minx 

    xFactor = 10 / polywdth
    yFactor = 10 / polyHgt
    return aff.scale(poly,xfact=xFactor, yfact=yFactor)


def similarity (poly1, poly2, polygon = 0):
    isSym = 0
    if polygon:
        oThreshold = 0.90
        intxGeom = poly1.intersection (poly1)
        uninGeom = poly1.union (poly2)
        overlap = intxGeom.area / uninGeom.area
        print('interrrr', overlap)
        #overlap = 0.5 * (intxGeom.area/poly1.area + intxGeom.area/poly2.area)
        if overlap > oThreshold:
            isSym = 1
        return overlap, isSym
    else:
        dThreshold = 1e-10
        distance = poly1.hausdorff_distance(poly2)
        if distance < dThreshold:
            isSym = 1
        return distance, isSym



def symreco (poly1, poly2, polygon=0):
    # check the area of overlap between a symbol and its 180 degree rotation symbol.
    # the closer to, the more symmetric is the shape.

    # distance threshold 
    threshold = 1e-10

    isSym = False
    if polygon:
        rotelmnt =  aff.rotate(poly1, 180)
        overlap = similarity(poly1, rotelmnt)
        if (overlap >= 0.99):
            isSym = True
        return isSym
    else:
        distance = poly1.hausdorff_distance(poly2)
        if distance < threshold:
            isSym = True
        return isSym
            

def transform(geom):

    # Translation 
    lineTrans = translateToOrig(geom)
    # Rotation
    if symreco(lineTrans, aff.rotate(lineTrans, 180)):
        print('shape is symmetric...')
        lineTransMRR = lineTrans.envelope 
        x, y = lineTransMRR.exterior.xy
        # (width, height)
        edge_length = (Point(x[0], y[0]).distance(Point(x[1], y[1])), Point(x[1], y[1]).distance(Point(x[2], y[2])))
        width = edge_length[0]
        height = edge_length[1]
        if width > height:
            rottdStrtL = aff.rotate(lineTrans, 90)
        else:
            rottdStrtL = aff.rotate(lineTrans, 0)
    else:
        rottdStrtL = rotateRef(lineTrans)
    
    # Scaling  
    scldStrtLn = scale(rottdStrtL)

    return scldStrtLn 


def tomultpolygon (geom):
    STROKED_GLYPH_BUFFER_PERC = 2.0
    minX, minY, maxX, maxY = geom.bounds
    bufferDist = 0.01 * STROKED_GLYPH_BUFFER_PERC * max (maxX - minX, maxY - minY)
    bufferGeom = geom.buffer (bufferDist)
    return bufferGeom










