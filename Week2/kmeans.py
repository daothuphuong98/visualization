import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.spatial import ConvexHull
np.random.seed(11)

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

def kmeans_display(X, label, centroid):

    color = ['b','g','r','c','m', 'y', 'k','w']
    unique_label = np.unique(label)
    for i in range(len(unique_label)):
        cluster = X[label == unique_label[i]]
        plt.plot(cluster[:, 0], cluster[:, 1], color[i] + 'o', markersize=4, alpha=.8)

        hull = ConvexHull(cluster)
        x_hull = np.append(cluster[hull.vertices, 0],
                           cluster[hull.vertices, 0][0])
        y_hull = np.append(cluster[hull.vertices, 1],
                           cluster[hull.vertices, 1][0])
        plt.fill(x_hull, y_hull, alpha=0.3, c=color[i])

    plt.plot(centroid[:, 0], centroid[:, 1], 'y^', markersize=7, alpha=1)

    x = np.arange(-3, 10, 1)
    for c in combinations(centroid, 2):
        u = c[0] - c[1]
        m = (c[0] + c[1])/2
        y = m[1] + u[0]/u[1]*(m[0]-x)
        plt.plot(x,y, 'k:')

    plt.axis('equal')
    plt.xlim(left = -1, right = 10)
    plt.ylim((-1,10))
    plt.show()

K = 3
data, original_label = random_data()
l, c = kmeans(data, K)
kmeans_display(data, l, c)




