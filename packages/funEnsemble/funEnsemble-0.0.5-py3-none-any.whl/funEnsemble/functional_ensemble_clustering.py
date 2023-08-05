
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
from sklearn.cluster import SpectralClustering
import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy import spatial, interpolate

# First function which takes raw data and V as input arguments, and outputs the smooth functions, population mean, eigen functions and eigen vales
def functional_data_decomposition (data, V, b_spline_length):

    # Smooth the data
    data_smooth = np.zeros((len(data), b_spline_length))
    t = np.expand_dims(np.linspace(0, 10, len(data[0])), 1)

    for i in range(len(data)):
        tck = interpolate.splrep(t, data[i], s=0,k=3) 
        x_new = np.linspace(min(t), max(t), b_spline_length)
        y_fit = interpolate.BSpline(*tck)(x_new)
        y_fit = y_fit.reshape(len(y_fit,))
        data_smooth[i] = y_fit
        # plt.plot(x_new, data_smooth[i], '-m')

    # Get the population mean 
    mean = np.mean(data_smooth, axis=0)

    # plt.plot(x_new, mean, '-k', label='Mean')
    # plt.title((
    #     'Population Functions and Mean'))
    # plt.legend()
    # plt.show()

    # Subtract the mean from the data
    data_smooth_without_mean = data_smooth - mean
    
    # Get principal components of the data
    pca = PCA(n_components=V)
    pca.fit(data_smooth_without_mean)
    principal_componenets = pca.transform(data_smooth_without_mean)

    # Determine the eigen-functions of the population covariance function
    eigen_functions = pca.components_

    # Plot the eigen-functions
    # plt.plot(x_new, eigen_functions.T, '-m')
    # plt.title((
    #     'Eigen-functions of the population'))
    # plt.xlabel('$x$', fontsize=13)
    # plt.ylabel('$y = f(x)$', fontsize=13)
    # plt.show()
    
    return data_smooth, mean, principal_componenets, eigen_functions


# Second function which takes eigen values and clusters K and outputs probabilities and spectral clustering result
def functional_data_clustering (eigen_values, K):
    # Fit a Gaussian mixture model with K components
    membership_matrices = []
    n = len(eigen_values[0])
    for i in range(n):
        gmm = GaussianMixture(n_components=K, covariance_type='full')
        gmm.fit(eigen_values[:, i].reshape(-1, 1))
        labels = gmm.predict(eigen_values[:, i].reshape(-1, 1))
        #Create the membership probabilities for each component
        probability = gmm.predict_proba(eigen_values[:, i].reshape(-1,1))
        membership_matrices.append(probability)

    # Create binary membership matrices for each element in probabilities
    # for i in range(V):
    #     for j in range(n):
    #         for k in range(4):
    #             #Binary membership matrix based on max probability
    #             if probabilities[i][j][k] == max(probabilities[i][j]):
    #                 probabilities[i][j][k] = 1
    #             else:
    #                 probabilities[i][j][k] = 0

    # Affinity matrix A, which is the sum of the V cluster membership matrix M_v*M_v^T
    matrix_multiplication = []
    for i in range(n):
        matrix_multiplication.append(np.matmul(membership_matrices[i], membership_matrices[i].T))
    affinity_matrix = sum(matrix_multiplication)

    # Apply spectral clustering
    sc = SpectralClustering(n_clusters=K, affinity='precomputed', assign_labels='discretize')
    sc.fit(affinity_matrix)
    labels = sc.labels_

    return membership_matrices, labels