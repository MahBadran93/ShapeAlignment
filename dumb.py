sumInt = 0.0
        sumUn = 0.0
        for gm1, gm2 in zip(poly1, poly2):
            intxGeom = gm1.intersection (gm2) 
            sumInt+=intxGeom.area
            print(sumInt)
            uninGeom = gm1.union (gm2)
            sumUn+=uninGeom.area
        overlap = sumInt / sumUn




         # Using arsin to find the angle of rotation
    '''
    cntrdNorm = np.sqrt(centroid[0]**2 + centroid[1]**2)
    #thetaRad =  centroid[0] / cntrdNorm 
    #thetaRad = math.degrees(thetaRad)
    val = centroid[1] / cntrdNorm
    angle = np.arcsin(val)
    angle = math.degrees(angle)
    '''




    '''
    if angle < 270.0 or angle == 270.0:
        rotAngle = 270.0 - angle
        print(rotAngle)
    else: 
        rotAngle = (270.0 + angle) - 360.0
        print('After', rotAngle)
    '''
    
