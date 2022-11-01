"""
Visualize geodesics in landmarks space with kernel metric
"""

import geomstats.backend as gs
from geomstats.geometry.euclidean import Euclidean
from geomstats.geometry.landmarks import Landmarks, L2LandmarksMetric, KernelLandmarksMetric
import numpy as np
import matplotlib.pyplot as plt
import time

gs.random.seed(1234)

step = "euler" # step rule for numerical integration
n_steps = 10 # number of integration steps

# Setting : 2 landmarks in 2D
n_points = 2
landmark_set_a = gs.array([[0., 0.],[1., .1]])
landmark_set_b = gs.array([[1., 0.],[0., .1]])
print("Experiment 1 : 2 landmarks in 2D")

# set the space and metrics
r2 = Euclidean(dim=2)
gaussian_1 = lambda d: gs.exp(-d)
gaussian_2 = lambda d: gs.exp(-d/.25**2)

metrics = { 
    "Kernel metric (gaussian kernel, sigma=1)" : 
            KernelLandmarksMetric(ambient_dimension=2, k_landmarks=n_points, kernel=gaussian_1),
    "Kernel metric (gaussian kernel, sigma=.25)" : 
            KernelLandmarksMetric(ambient_dimension=2, k_landmarks=n_points, kernel=gaussian_2)
}

# set parameters for geodesics computation and plotting
n_sampling_geod = 100
times = gs.linspace(0., 1., n_sampling_geod)
atol = 1e-6

# main loop
for key in metrics:
    print(key)
    metric = metrics[key]
    space_landmarks_in_euclidean_2d = Landmarks(
        ambient_manifold=r2, k_landmarks=n_points, metric=metric)
    landmarks_a = landmark_set_a
    landmarks_b = landmark_set_b

    # testing exp
    print("Testing exponential map")
    initial_cotangent_vec = gs.array([[1., 0.],[-1., 0.]])
    start = time.time()
    landmarks_ab = metric.geodesic(landmarks_a, initial_cotangent_vec=initial_cotangent_vec, step=step, n_steps=n_steps)
    geod = gs.to_numpy(landmarks_ab(times))
    end = time.time()
    print("elapsed=", end-start)
    plt.figure()
    plt.plot(landmark_set_a[:,0], landmark_set_a[:,1], 'o')
    plt.quiver(landmark_set_a[:,0], landmark_set_a[:,1], 
                initial_cotangent_vec[:,0], initial_cotangent_vec[:,1])
    plt.plot(geod[:,:,0], geod[:,:,1])
    plt.title(f"{key},\n geodesic (exp from cotangent vector)")
    plt.axis("equal")

    # testing log
    print("Testing geodesics computation")
    start = time.time()
    landmarks_ab = metric.geodesic(landmarks_a, landmarks_b, step=step, n_steps=n_steps)
    geod = gs.to_numpy(landmarks_ab(times))
    end = time.time()
    print("elapsed=", end-start)
    plt.figure()
    plt.plot(landmark_set_a[:,0], landmark_set_a[:,1], 'o')
    plt.plot(landmark_set_b[:,0], landmark_set_b[:,1], 'x')
    plt.plot(geod[:,:,0], geod[:,:,1])
    plt.title(f"{key},\n geodesic (computing log)")
    plt.axis("equal")


# exp map with a large number of landmarks
print("Experiment 2 : 100 landmarks in 2D")

N = 100
# Setting : 100 points in 2D
n_points = 2
landmark_set_a = 2*gs.random.rand(N,2)
landmark_set_b = landmark_set_a + .5*(gs.random.rand(N,2)-.5)

metrics = { 
       "Kernel metric (gaussian kernel, sigma=.25)" : 
            KernelLandmarksMetric(ambient_dimension=2, k_landmarks=n_points, kernel=gaussian_2)
}

# main loop
for key in metrics:
    print(key)
    metric = metrics[key]
    space_landmarks_in_euclidean_2d = Landmarks(
        ambient_manifold=r2, k_landmarks=n_points, metric=metric)
    landmarks_a = landmark_set_a
    landmarks_b = landmark_set_b

    # testing exp
    print("Testing exponential map")
    initial_cotangent_vec = 50*(gs.random.rand(N,2)-.5)/N
    start = time.time()
    landmarks_ab = metric.geodesic(landmarks_a, initial_cotangent_vec=initial_cotangent_vec, step=step, n_steps=n_steps)
    geod = gs.to_numpy(landmarks_ab(times))
    end = time.time()
    print("elapsed=", end-start)
    plt.figure()
    plt.plot(landmark_set_a[:,0], landmark_set_a[:,1], 'o')
    plt.plot(geod[:,:,0], geod[:,:,1])
    plt.title(f"{key},\n geodesic (exp from cotangent vector)")
    plt.axis("equal")

plt.show()