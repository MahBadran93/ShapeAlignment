from shapely.geometry import MultiLineString, Polygon, MultiPolygon
import matplotlib.pyplot as plt
#from wktplot.wkt_plot import WKTPlot
import numpy as np
from utils import normalize, center


#mline1 = MultiLineString([((0, 0), (0, 2)), ((1, 1),  (2, 2), (2, 0), (1, 1))])
mline1 = MultiLineString([((-195.6987489504394, -323.658819168724), (-194.1987512350694, -323.6562011761752)), ((-197.2092186360047, -317.6614462997932),
 (-194.2092232052648, -317.6562103146954)), ((-197.1987466658093, -323.6614371612729), (-195.6987489504394, -323.658819168724))])

#mline1 = MultiLineString([(0, 0), (1, 1), (0, 2),  (1, 1.5), (1.5, 1), (2, 0)])
#points = mline1.coords[0]
i = 0
line = []
for i in list(mline1):
    for c in i.coords:
        c = np.abs(c)
        line.append(c)

poly = Polygon(line)
x, y = poly.exterior.xy

c1, c2 = center(poly)
polyArray = np.array(poly.exterior.xy)

#c1, c2 = (sum(polyArray[0])/len(polyArray[0]),sum(polyArray[1])/len(polyArray[1]))
plt.plot(x, y)
plt.plot(c1, c2, marker='.')
plt.show()


