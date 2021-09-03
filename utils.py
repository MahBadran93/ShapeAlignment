import shapely.geometry as geom
import shapely.affinity as aff
import numpy as np
import matplotlib.pyplot as plt

def center (poly):

    centerPoly = poly.centroid.xy
    centerPoint= (centerPoly[0][0], centerPoly[1][0])
    return centerPoint

def translateToOrig (poly, origin=(0, 0)):

    # Find the minimum rotation rectangle
    polyMRR = poly.minimum_rotated_rectangle

    # Find Center of MRR
    centerp = center(polyMRR)

    # Find offset point to translate polygon to origin
    xOff = -(centerp[0] - origin[0])
    yOff = -(centerp[1] - origin[0])

    trnsltPoly = aff.translate(poly, xoff=xOff, yoff=yOff)

    return trnsltPoly


def translateToPoly(poly1, poly2):
    # Find centroid of both polygons
    centroidOrigin = poly1.centroid.xy
    centroidTotranslate = poly2.centroid.xy

    # Create centroid points for both polygons
    cntrdOriginPoint = (centroidOrigin[0][0], centroidOrigin[1][0])
    cntrdTotranslatePoint = (centroidTotranslate[0][0], centroidTotranslate[1][0])

    # Find offset point to translate polygon to polygon
    Centroid_def_x = -(cntrdTotranslatePoint[0] - cntrdOriginPoint[0])
    Centroid_def_y = -(cntrdTotranslatePoint[1] - cntrdOriginPoint[1])

    translated_Poly = aff.translate(poly2, xoff=Centroid_def_x, yoff=Centroid_def_y)

    translated_Poly = aff.rotate(translated_Poly, 90)

    return translated_Poly

def scalePoly(poly, factor, rltvPoint= (2.0, 2.0)):
    x, y = poly.exterior.xy
    sub_x = [x - rltvPoint[0] for x in x]
    sub_y = [y - rltvPoint[1] for y in y]

    mult_x = [factor * sub_x for sub_x in sub_x]
    mult_y = [factor * sub_y for sub_y in sub_y]

    add_x = [mult_x + rltvPoint[0] for mult_x in mult_x]
    add_y = [mult_y * rltvPoint[1] for mult_y in mult_y]

    polyScaled = geom.Polygon(list(zip(add_x, add_y)))
    #polyScaled = aff.scale(poly, x_new, y_new, origin=(0, 0))
    #polyScaled = geom.Polygon((xOffset, yOffset))
    return polyScaled

def scaleUnitNorm(poly):
    X, Y = poly.exterior.xy
    print(type(X))
    muX = np.array(X).mean(0)
    muY = np.array(Y).mean(0)

    X0 = X - muX
    Y0 = Y - muY

    ssX = np.linalg.norm(X0) ** 2  # (X0**2.).sum()
    ssY = np.linalg.norm(Y0) ** 2  # (Y0**2.).sum()

    # centred Frobenius norm
    normX = np.sqrt(ssX)
    normY = np.sqrt(ssY)

    # scale to equal (unit) norm
    X0 /= normX
    Y0 /= normY
    poly_scaled = geom.Polygon(list(zip(X0, Y0)))

    return poly_scaled

def similarityCoef(poly1, poly2):
    pass

