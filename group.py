import pickle
from os import listdir
from os.path import isfile, join
from plots import plot_comparison
from utils import tomultpolygon, transform, similarity
import matplotlib.pyplot as plt 

listOfGeom = []

mypath = './pickles/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in onlyfiles[:]: 
    with open(mypath + file, 'rb') as handle:
        mulitLine = pickle.load(handle)
        if mulitLine[0] is None:
            continue
    listOfGeom.append((mulitLine[0], mulitLine[1]))

ShapeId = 400 # check 400 // check 80 and 2 and 3
ShapeId2 = 69
testGroup = []

# ............... Plot comparison with polygons and line strings...........
# trsfmdGeom1 =  transform(listOfGeom[ShapeId1][0]) #listOfGeom[shapeId1]
# trsfmdGeom1P = tomultpolygon(trsfmdGeom1)
# trsfmdGeom2 =  transform(listOfGeom[ShapeId2][0]) #listOfGeom[shapeId2]
# trsfmdGeom2P = tomultpolygon(trsfmdGeom2)
# plot_comparison(listOfGeom[ShapeId1][0], listOfGeom[ShapeId2][0],trsfmdGeom1, trsfmdGeom2)

# .................. Apply grouping and plot ............................. 
trsfmdGeom1 =  transform(listOfGeom[ShapeId][0]) #listOfGeom[shapeId1]
trsfmdGeom1P = tomultpolygon(trsfmdGeom1)
print('length of geom: ', len(listOfGeom))
for j in range(len(listOfGeom)):
    # Transform (Translate -> Rotate -> Scale )
    trsfmdGeom2 =  transform(listOfGeom[j][0]) #listOfGeom[shapeId2]
    # Convert to multipolygon object 
    trsfmdGeom2P = tomultpolygon(trsfmdGeom2)
    dist, isSim = similarity(trsfmdGeom1P, trsfmdGeom2P, polygon=1)
    if isSim == 1:
        testGroup.append((listOfGeom[j][0], listOfGeom[j][1]))

print('length: ', len(testGroup))

for i in range(len(testGroup)):
    print('Symbol: ',testGroup[i][1])
    for line in testGroup[i][0]:
        x, y = line.coords.xy
        plt.plot(x, y)
    plt.show()