import cv2, os
from itertools import combinations
from itertools import pairwise
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import polynomial_kernel, rbf_kernel, sigmoid_kernel, cosine_similarity
from sklearn.cluster import DBSCAN
from collections import defaultdict

'''
    RBF kernel - Gaussian Similarity:
        - Measures similarity using a Gaussian (radial basis function) kernel.
'''
def rbf_similarity(features, gamma=0.1):
    # compute RBF kernel similarity
    similarity_matrix = rbf_kernel(features, gamma=gamma)
    return similarity_matrix

'''
    Manhattan Similarity:
        - Measures the sum of absolute differences between feature vectors.
'''
def manhattan_similarity(features):
    # compute pairwise manhattan distances
    distances = pairwise_distances(features, metric='manhattan')

    # compute similarity matrix
    similarity_matrix = 1 / (1 + distances)
    return similarity_matrix

'''
    Euclidean Similarity:
        - Measures the straight-line distance between two feature vectors.
'''
def euclidean_similarity(features):
    # compute pairwise euclidean distances
    distances = pairwise_distances(features, metric='euclidean')

    # compute similarity matrix
    similarity_matrix = 1 / (1 + distances)
    return similarity_matrix

'''
     Similarity Computation:
        - Uses predefined functions from above for different results
        - Iterates through valid logos and stores those with similarity above 0.8 in a dictionary.
        - Returns a dictionary where each logo maps to a list of similar logos and their similarity scores.
'''
def compute_similarity(features, valid_logos):
    # change functions to be able to see results for each one
    #                 -> cosine_similarity, euclidean_similarity, manhattan_similarity, rbf_similarity
    similarity_matrix = euclidean_similarity(features)
    logo_similarity = {}

    for i, logo1 in enumerate(valid_logos):
        logo_similarity[logo1] = []

        for j, logo2 in enumerate(valid_logos):
            if i != j and similarity_matrix[i, j] > 0.8:
                logo_similarity[logo1].append((logo2, similarity_matrix[i, j]))

    return logo_similarity

'''
      Logo Grouping:
        - Iterates through the similarity dictionary created in `compute_similarity()`.
        - If a logo has not been visited, it starts a new group.
        - Adds similar logos to the group and marks them as visited to prevent duplication.
        - Returns a list of groups where each group contains similar logos.
'''
def group_similar_logos(logo_similarity):
    groups = []
    visited = set()

    for logo, similar_logos in logo_similarity.items():
        if logo not in visited:
            group = {logo}

            for similar_logo, _ in similar_logos:
                group.add(similar_logo)
                visited.add(similar_logo)

            visited.add(logo)
            groups.append(group)

    return groups

