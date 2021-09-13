import pickle
from os import listdir
from os.path import isfile, join
from plots import plot_comparison
from utils import tomultpolygon, transform, similarity
import matplotlib.pyplot as plt 
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon



listOfGeom = []

mypath = './pickles/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
for file in onlyfiles[:]: 
    with open(mypath + file, 'rb') as handle:
        mulitLine = pickle.load(handle)
        if mulitLine[0] is None:
            continue
    listOfGeom.append((mulitLine[0],mulitLine[1]))

# Here check why 2660001 item is not proporely found with similarity 
filtered_shapes = [shape for shape in listOfGeom if shape[1] == '266001'] #P0081, 266001, P0001
print(len(filtered_shapes))

ShapeId1 = 6 # check 400 // check 80 and 2 and 3
ShapeId2 = 7
testGroup = []

trsfmdGeom1 =  transform(filtered_shapes[ShapeId1][0]) #listOfGeom[shapeId1]
trsfmdGeom1P = tomultpolygon(trsfmdGeom1)
trsfmdGeom2 =  transform(filtered_shapes[ShapeId2][0]) #listOfGeom[shapeId2]
trsfmdGeom2P = tomultpolygon(trsfmdGeom2)
dist, isSim = similarity(trsfmdGeom1P, trsfmdGeom2P, polygon=1)
if isSim == 1:
    print('similar')
else: 
    print('not similar')
print( trsfmdGeom1P.geom_type, trsfmdGeom2P.geom_type)
#plot_comparison(filtered_shapes[ShapeId1][0], filtered_shapes[ShapeId2][0], trsfmdGeom1, trsfmdGeom2)

# plot intersection 
listPoly = []
if trsfmdGeom1P.geom_type == 'MultiPolygon' and trsfmdGeom2P.geom_type == 'MultiPolygon':
    for poly in trsfmdGeom1P:
        listPoly.append(poly)
    for poly2 in trsfmdGeom2P:
        listPoly.append(poly2)

    patches  = PatchCollection([Polygon(poly.exterior) for poly in listPoly] , facecolor='red', linewidth=.5, alpha=.5)

if trsfmdGeom1P.geom_type == 'MultiPolygon' and trsfmdGeom2P.geom_type == 'Polygon':
    for poly in trsfmdGeom1P:
        listPoly.append(poly)
    listPoly.append(trsfmdGeom2P)
    patches  = PatchCollection([Polygon(poly.exterior) for poly in listPoly], facecolor='red', linewidth=.5, alpha=.5)

if trsfmdGeom1P.geom_type == 'Polygon' and trsfmdGeom2P.geom_type == 'MultiPolygon':
    for poly in trsfmdGeom2P:
        listPoly.append(poly)
    listPoly.append(trsfmdGeom1P)
    patches  = PatchCollection([Polygon(poly.exterior) for poly in listPoly], facecolor='red', linewidth=.5, alpha=.5)

if trsfmdGeom1P.geom_type == 'Polygon' and trsfmdGeom2P.geom_type == 'Polygon':
    patches  = PatchCollection([Polygon(trsfmdGeom1P.exterior) , Polygon(trsfmdGeom2P.exterior)], facecolor='red', linewidth=.5, alpha=.5)

fig, ax = plt.subplots(1, 1, subplot_kw=dict(aspect='equal'))
ax.add_collection(patches, autolim=True)
ax.autoscale_view()
ax.set_title('separate polygons')

#plt.show()
for i in range(len(filtered_shapes)):
    for line in filtered_shapes[i][0]:
        x, y = line.coords.xy 
        plt.plot(x, y)
    plt.show()