import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from shapely.geometry import LineString, Polygon, Point
from shapely.ops import split
np.random.seed(11)

LEFT_TOP = (-3, 12)
RIGHT_TOP = (12, 12)
LEFT_BOTTOM = (-3, -3)
RIGHT_BOTTOM = (12, -3)

BOTTOM_LINE = LineString((LEFT_BOTTOM, RIGHT_BOTTOM))
TOP_LINE = LineString((LEFT_TOP, RIGHT_TOP))
LEFT_LINE = LineString((LEFT_TOP, LEFT_BOTTOM))
RIGHT_LINE = LineString((RIGHT_TOP, RIGHT_BOTTOM))

PLANE = Polygon((LEFT_TOP, RIGHT_TOP, RIGHT_BOTTOM, LEFT_BOTTOM))

def random_data():
    means = [[2, 2], [8, 3], [3, 6]]
    cov = [[1, 0], [0, 1]]
    N = 500
    X0 = np.random.multivariate_normal(means[0], cov, N)
    X1 = np.random.multivariate_normal(means[1], cov, N)
    X2 = np.random.multivariate_normal(means[2], cov, N)

    X = np.concatenate((X0, X1, X2), axis = 0)
    original_label = np.asarray([0] * N + [1] * N + [2] * N).T
    return X, original_label

def get_centroid(x, centroid):
    result = np.sqrt((centroid[:, 0] - x[0])**2 + (centroid[:, 1] - x[1])**2)
    res = result.argmin()
    return res

def kmeans(X, k):
    random_row = np.random.choice(X.shape[0], size=k, replace=False)
    centroid = X[random_row, :]
    new_centroid = np.zeros([k, 2])

    while True:
        label = np.apply_along_axis(get_centroid, 1, X, centroid)
        for c in range(k):
            new_centroid[c] = X[label == c].mean(axis=0)
        if np.all(new_centroid == centroid):
            label = np.apply_along_axis(get_centroid, 1, X, centroid)
            break
        centroid = new_centroid
    return label, centroid

def kmeans_display(X, k, label, centroid):

    color = ['b','g','r','c','m', 'y', 'k','w']
    unique_label = np.unique(label)
    for i in range(k):
        cluster = X[label == unique_label[i]]
        plt.plot(cluster[:, 0], cluster[:, 1], color[i] + 'o', markersize=4, alpha=.8)

    plt.plot(centroid[:, 0], centroid[:, 1], 'y^', markersize=7, alpha=1)

    x = np.arange(-3, 15, 1)
    polygons = {x:[] for x in range(k)}
    for c1, c2 in combinations(range(k), 2):
        u = centroid[c1] - centroid[c2]
        m = (centroid[c1]+ centroid[c2])/2
        y = m[1] + u[0]/u[1]*(m[0]-x)
        p1, p2 = make_polygon(Point(centroid[c1]), Point(centroid[c2]),
                  LineString(((x[0], y[0]), (x[-1], y[-1]))))
        polygons[c1].append(p1)
        polygons[c2].append(p2)
    for centroid, polygon_list in polygons.items():
        pol = get_intersect_polygon(polygon_list)
        x, y = pol.exterior.xy
        plt.fill(x, y, c=color[centroid], alpha = 0.2)

    plt.axis('equal')
    plt.xlim(left = -1, right = 10)
    plt.ylim((-1,10))
    plt.show()

def make_polygon(centroid1, centroid2, line):
    polygons = split(PLANE, line)
    if polygons[0].contains(centroid1):
        return polygons[0], polygons[1]
    else:
        return polygons[1], polygons[0]

def get_intersect_polygon(polygons):
    p = polygons[0]
    for pol in polygons[1:]:
        p = pol.intersection(p)
    return p

K = 5
data, original_label = random_data()
l, c = kmeans(data, K)
kmeans_display(data, K, l, c)




