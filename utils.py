import shapely.geometry as geom
import shapely.affinity as aff
import numpy as np
import matplotlib.pyplot as plt
import math
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import shapely.geometry
from shapely.geometry.point import Point


def normalize (geom):

    """
        Normalize a shapely geometric object 
        Input: 
            - geom: Shapely gometric object 

    """
    geomArray = np.array(geom.exterior.xy)

    maxX = np.max(geomArray[0])
    maxY = np.max(geomArray[1])

    x = geomArray[0]/maxX
    y = geomArray[1]/maxY
    
    points = [list(points) for points in zip(x, y)]
    polyNorm = Polygon(points)

    x, y = polyNorm.exterior.xy

    return polyNorm


def center (geom):

    """
         Find the centroid of a shapely geometric object 
         Input:
            - geom: Shapely gometric object
    
    """

    c1, c2 = geom.centroid.xy
    centerPoly = (c1, c2)
    centerPoint= (centerPoly[0][0], centerPoly[1][0])
    return centerPoint


def translateToOrig (geom, origin=(0, 0)):

    """
        Translate a shapely geometric object to the origin reference frame
        Input: 
            - geom:  Shapely gometric object

    """

    # Find the minimum rotation rectangle
    #geomMRR = geom.minimum_rotated_rectangle
    geomMRR = geom.envelope

    # Find Center of MRR
    centerp = center(geomMRR)

    # Find offset point to translate geometric object to origin
    xOff = -(centerp[0] - origin[0])
    yOff = -(centerp[1] - origin[0])

    trnsltPoly = aff.translate(geom, xoff=xOff, yoff=yOff)

    return trnsltPoly


def rotateRef (geom, baseV=(1, 0), polygon = 0):

    """
        Rotate a translated geometric object toward the center of grvity (object centroid)
        Input:
            - geom: Shapely gometric object (multi line string or multi polygon) Translated to the origin 
    
    """
    # Check if a geometric object is symmetrical 
    if symreco(geom, polygon=polygon):
        print('shape is symmetric...')
        centroid = center(geom)
        centerMRR = center(geom.envelope)
        #print('centroid',centroid, 'centermrr', centerMRR)

        # Find width and height of the minimal rotated rectangle object 
        geomTranslMRR = geom.envelope 
        x, y = geomTranslMRR.exterior.xy
        # width and height
        edge_length = (Point(x[0], y[0]).distance(Point(x[1], y[1])), Point(x[1], y[1]).distance(Point(x[2], y[2])))
        width = edge_length[0]
        height = edge_length[1]
        # Rotate 
        if width > height:
            rotGeom = aff.rotate(geom, 90)
        else:
            rotGeom = aff.rotate(geom, 0)
        return rotGeom
    else:
        # if the object is not symmetrical 
        # centeroid of the translated geometric object and center of MRR 
        centroid = center(geom)
        centermrr = center(geom.envelope)
        #print('centroid',centroid, 'centermrr', centermrr)

        # Find the angle of rotation 
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
            
            print(centroid)

            centroid = np.array(centroid)
            centroid = np.round(centroid, 2)

            print(centroid)
            if centroid[1] >= 0:
                rotAngle = 270.0 - angle
            elif centroid[1] <= 0 and centroid[0] <= 0:
                rotAngle = 90 - angle #(270.0 + angle) - 360.0
            elif centroid[1] <= 0 and centroid[0] >= 0:
                rotAngle = -(90 - angle) #-(270.0 + (180.0 - angle))

        rotGeom = aff.rotate(geom, rotAngle)

        return rotGeom


def scale (geom):

    """
        Scale a shapely geometric object 
        Input:
            - geom: Shapely gometric object (multi line string or multi polygon) Translated to the origin
    """

    xFactor = 1
    yFactor = 1
    (minx, miny, maxx, maxy) = geom.bounds 
    geomHgt = maxy - miny
    geomWdth = maxx - minx 

    xFactor = 10 / geomWdth
    yFactor = 10 / geomHgt

    return aff.scale(geom, xfact=xFactor, yfact=yFactor)


def similarity (geom1, geom2, polygon = 0):
    """
    Find the similarity between two geometric objects
    Input: 
        - geom1: the first geometric object
        - geom2: the second geometric object 
        - polygon: a flag to know if the geometric object you pass is a polygon or multiline string object
            - in case of polygon (polygon= 1): Intesection over union will be used to find the similarity
            - in case of multi line string (polygon= 0): Hausdorff distance will be used measure the similarity  
    """

    similar = 0

    if polygon:
        oThreshold = 0.90
        intxGeom = geom1.intersection (geom2)
        uninGeom = geom1.union (geom2)
        overlap = intxGeom.area / uninGeom.area
        #overlap = 0.5 * (intxGeom.area/geom1.area + intxGeom.area/geom2.area)
        if overlap > oThreshold:
            similar = 1
        return overlap, similar
    else:
        dThreshold = 1e-10
        distance = geom1.hausdorff_distance(geom2)
        if distance < dThreshold:
            similar = 1
        return distance, similar


def symreco (geom, polygon=0):
    
    """
    Check if a geometric object is symmetric 
    Input: 
        - geom: Shapely geometric object 
    """
    # check the area of overlap between a symbol and its 180 degree rotation symbol.
    # the closer to, the more symmetric is the shape.

    # distance threshold 
    threshold = 1e-10

    isSym = False
    if polygon:
        rotGeom =  aff.rotate(geom, 180)
        distance, overlap = similarity(geom, rotGeom, polygon=polygon)
        if (overlap >= 0.99):
            isSym = True
        return isSym
    else:
        roteGeom =  aff.rotate(geom, 180)
        distance = geom.hausdorff_distance(roteGeom)
        if distance < threshold:
            isSym = True
        return isSym
            

def transform(geom, polygon = 0):

    """
        Transfrom a geometric object (Translation, Rotation and scaling)
        Input: 

    """
    # Translation 
    geomTrans = translateToOrig(geom)
    # Rotation
    rotdGeom = rotateRef(geomTrans, polygon=polygon)
    # Scaling  
    scldGeom = scale(rotdGeom)

    return scldGeom 


def tomultpolygon (geom):

    """
    Convert mult line string object to multi polygon object
    Input: 
        - geom: multi line string geometric object
    """
    STROKED_GLYPH_BUFFER_PERC = 2.0
    minX, minY, maxX, maxY = geom.bounds
    bufferDist = 0.01 * STROKED_GLYPH_BUFFER_PERC * max (maxX - minX, maxY - minY)
    bufferGeom = geom.buffer (bufferDist)
    return bufferGeom










