# investigate the sensitivity of clustering results w.r.t. V (namely, the percentage of variation explained)
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.cluster import adjusted_mutual_info_score, adjusted_rand_score
from ensemble_clustering import functional_data_decomposition, functional_data_clustering

# Create function for percentage of variation and AMI/ARI scores, with eigen_dimension, data, splines, and labels as inputs
def percentage_variation_ami_ari(eigen_dimension, data, spline_length, simulation_labels, K):
    # eigen_dimension = 50
    v_range = np.arange(1, eigen_dimension+1, 1)
    ami_scores = []
    ari_scores = []

    data_smooth, mean, principal_components, eigen_functions = functional_data_decomposition (data, eigen_dimension, spline_length)

    # Investigate the percentage of variation explained by the first 5 eigen dimensions based on the principal components
    variance_explained = np.zeros(eigen_dimension)
    total_variance = 0

    # Determine the total variance
    for i in range(eigen_dimension):
        total_variance += np.var(principal_components[:, i])

    for i in range(eigen_dimension):
        variance_explained[i] = np.var(principal_components[:, i])/total_variance

    print('Percentage of variation explained by each eigen dimensions: ', variance_explained)

    # Determine the ari and ami scores for each eigen dimension
    for i in (v_range):
        # Apply functional data clustering on the principal components until the ith eigen dimension
        membership_matrices, labels = functional_data_clustering(principal_components[:, :i], K)

        ami_scores.append(adjusted_mutual_info_score(simulation_labels, labels))
        ari_scores.append(adjusted_rand_score(simulation_labels, labels))
        
    return variance_explained, ami_scores, ari_scores, v_range

# Function which plots the percentage of variation explained, ami and ari scores against the number of eigen dimensions
def plot_percentage_variation_ami_ari(variance_explained, ari, ami, v_range, simulation_labels, data):

    # Plot the plots on a 2x2 grid
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    # Plot the simulated data
    for i in range(len(data)):
        if simulation_labels[i] == 0:
            axs[0, 0].plot(data[i], linestyle='--', color='b')
        elif simulation_labels[i] == 1:
            axs[0, 0].plot(data[i], linestyle='--', color='r')
        elif simulation_labels[i] == 2:
            axs[0, 0].plot(data[i], linestyle='--', color='g')
        elif simulation_labels[i] == 3:
            axs[0, 0].plot(data[i], linestyle='--', color='c')
        elif simulation_labels[i] == 4:
            axs[0, 0].plot(data[i], linestyle='--', color='y')
        elif simulation_labels[i] == 5:
            axs[0, 0].plot(data[i], linestyle='--', color='k')
        else:
            axs[0, 0].plot(data[i], linestyle='--', color='m')
    axs[0, 0].set_title('Simulated data')
    axs[0, 0].set_xlabel('Time')
    axs[0, 0].set_ylabel('Y')
    axs[0, 1].plot(v_range, np.cumsum(variance_explained)*100, linestyle='-', marker='o', color='b')
    axs[0, 1].set_title('Total Variation % '+'Explained per Eigen Dimension')
    axs[0, 1].set_xlabel('Dimension')
    axs[0, 1].set_ylabel('Percentage Explained')
    
    axs[1, 0].plot(v_range, ari, linestyle='-', marker='o', color='b')
    axs[1, 0].set_title('ARI Score Copared to the Eigen Dimension')
    axs[1, 0].set_xlabel('Dimension')
    axs[1, 0].set_ylabel('ARI Score')

    axs[1, 1].plot(v_range, ami, linestyle='-', marker='o', color='b')
    axs[1, 1].set_title('AMI Score Copared to the Eigen Dimension')
    axs[1, 1].set_xlabel('Dimension')
    axs[1, 1].set_ylabel('AMI Score')


