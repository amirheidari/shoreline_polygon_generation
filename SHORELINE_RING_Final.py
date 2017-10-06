# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 17:07:08 2017

@author: USER!
"""
from matplotlib import pyplot as plt
from shapely.geometry import Polygon, LineString, Point, MultiPoint
from descartes import PolygonPatch
import shapefile
from shapely.ops import polygonize_full, polygonize, split, snap
import numpy as np


fig = plt.figure(1, figsize=(5,5), dpi=90)

sf = shapefile.Reader("mygeodata/gulf")
shape_ex = sf.shape(0)
gulf=Polygon(shape_ex.points[:])

line2= gulf.exterior

width=0.3
poline=line2.buffer(width)

poly3=gulf.intersection(poline)
ax = fig.add_subplot(111)
ring_patch2 = PolygonPatch(poly3, alpha=1)
ax.add_patch(ring_patch2)

ax.set_title('Shoreline Polygons')
xrange = [47, 58]
yrange = [23, 31]
ax.set_xlim(*xrange)
ax.set_xticks(range(*xrange) + [xrange[-1]])
ax.set_ylim(*yrange)
ax.set_yticks(range(*yrange) + [yrange[-1]])
ax.set_aspect(1)



my_line1= LineString(poly3.exterior.coords[:])
my_line2= LineString(poly3.interiors[0].coords[:])


           
offset=0
minim=[]
for r in range (len(my_line2.coords[:])):
    minim.append(Point(my_line2.coords[r][0],my_line2.coords[r][1]).distance(Point(my_line1.coords[0][0],my_line1.coords[0][1])))
    
index_min = np.argmin(minim)

offset=index_min.astype(int)
print offset , "offset"            
 
corrected_points=[] #for shifting
for k in range (len(my_line2.coords[:])):
    corrected_points.append(my_line2.coords[offset-k])
    
my_line2_corrected=LineString(corrected_points[:])
    
L1=my_line1.length
L2=my_line2_corrected.length


number_arcs=30 ###### ENTER AN APPROXIMATE NUMBER MAX 70

for i in range (100):
        
    point1=[]
    point2=[]            
    for j in range(number_arcs):

        point2.append(my_line2_corrected.interpolate(j*(L2/number_arcs)))
        nearest_point=my_line1.project(point2[j])
        point1.append(my_line1.interpolate(nearest_point))            

       
    result1 = snap(my_line1, LineString(point1[:]), 0.0001) # snaps adds the points to line/ for splitting the point should be part of line
    result2= snap(my_line2_corrected,LineString(point2[:]),0.0001)
    
    #for i in range(21):
    #    print result1.contains(point1[i]) #after snap it will contain
    ##    print my_line1.contains(point1[i])
    
    splitted1 = split(result1,MultiPoint(point1[1:]))
    splitted2 = split(result2,MultiPoint(point2[1:]))
    
    print len(list(splitted1)), "1"
    print len(list(splitted2)), "2"
    if len(list(splitted1))==len(list(splitted2)):  print "The number of arcs will be %i"%number_arcs; break
    else: number_arcs+=1    



plt.figure()
ax = plt.axes()
xrange = [47, 58]
yrange = [23, 31]
ax.set_xlim(*xrange)
ax.set_xticks(range(*xrange) + [xrange[-1]])
ax.set_ylim(*yrange)
ax.set_yticks(range(*yrange) + [yrange[-1]])
ax.set_aspect(1)



x_lon = []
y_lat = []
#for ip in range(40):#len(result2_corrected.coords[:])):
#     x_lon.append(result2.coords[ip][0])
#     y_lat.append(result2.coords[ip][1])

#for ip in range(len(result1.coords[:])):
#     x_lon.append(result1.coords[ip][0])
#     y_lat.append(result1.coords[ip][1])

#plt.plot(x_lon,y_lat)

#for j in range(number_arcs): 
#    print splitted2[j].length
#    for ip in range(len(splitted2[j].coords[:])):
#         x_lon.append(splitted2[j].coords[ip][0])
#         y_lat.append(splitted2[j].coords[ip][1])
#    plt.plot(x_lon,y_lat)



MY_POLYGONS=[]
q=0
p=np.min([len(list(splitted1)),len(list(splitted2))])
for i in range(q,p):
    a=list(reversed(splitted2[i].coords[:]))
    p=splitted1[i].coords[:]+a
    MY_POLYGONS.append(Polygon(p))
    ring_patch = PolygonPatch(MY_POLYGONS[i-q], fc=np.random.random(3), alpha=0.6) #fc = '#999999'
    ax.add_patch(ring_patch)



#fig.savefig('shoreline.png', dpi=90, bbox_inches='tight')


