#!/usr/bin/python
 
import cv2
import numpy as np
import random
from scipy.spatial import Delaunay
import pickle as pickle
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
from matplotlib import cm

#############################################

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    return resized


img = cv2.imread('input.jpg',-1)
img_bw = cv2.imread('input.jpg',0)

#split into chanels
b,g,r = cv2.split(img);

#resize splits
resized_image_b = cv2.flip(image_resize(b, 400),0)
resized_image_g = cv2.flip(image_resize(g, 400),0)
resized_image_r = cv2.flip(image_resize(r, 400),0)

#resize
resized_image = cv2.flip(image_resize(img_bw, 400),0)
edge = cv2.Canny(resized_image,100,200)

#ans will be an array to store points
ans = []
for y in range(0, edge.shape[0]):
     for x in range(0, edge.shape[1]):
            if edge[y, x] != 0:
                ans = ans + [[x, y]]

height, width = resized_image.shape

#append corners
ans.append([0,0])
ans.append([0,height])
ans.append([width, height])
ans.append([width, 0])

#append noise to array
n=int(2000)

for j in range(n):
       ans.append([random.randint(1,width),random.randint(1,height)])

points = np.array(ans)
 
tri = Delaunay(points)

triangle_ = points[tri.simplices];

##print triangle_

center = []

print resized_image[0]

for ttt in range(len(triangle_)):
    centerX =  int((triangle_[ttt][0][0] + triangle_[ttt][1][0] + triangle_[ttt][2][0]) / 3.0)
    centerY =  int((triangle_[ttt][0][1] + triangle_[ttt][1][1] + triangle_[ttt][2][1]) / 3.0)
    center.append(int(resized_image_b[centerY][centerX]) + int(resized_image_g[centerY][centerX]) + int(resized_image_r[centerY][centerX]))

print len(center)
print center[0]

cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ['blue','violet','white','white','yellow'])

plt.tripcolor(points[:,0], points[:,1], tri.simplices.copy(), facecolors=np.array(center), edgecolors='k', lw=0, cmap=cmap)

##plt.colorbar()

plt.axis('equal')

plt.show()
