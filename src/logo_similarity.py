from itertools import pairwise
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import polynomial_kernel, rbf_kernel, sigmoid_kernel
from sklearn.cluster import DBSCAN
from collections import defaultdict


'''
    Similarity Computation and Clustering:
        - Computes the pairwise Euclidean distance matrix for the extracted feature vectors.
        - Applies DBSCAN (Density-Based Spatial Clustering of Applications with Noise) 
          to group similar logos based on distance.
        - Uses "precomputed" distance metric for efficient clustering.
        - Groups logos into clusters based on the DBSCAN results.
        - Prints out the logos belonging to each identified cluster along with their associated website URLs.
'''
def similarity(feature_vector, valid_logos, logo_url_mapping):
	# compute pairwise distance matrix
	distance_matrix = pairwise_distances(feature_vector, metric='euclidean')

	# perform DBSCAN clustering
	clustering = DBSCAN(metric="precomputed", eps=0.5, min_samples=2).fit(distance_matrix)
	labels = clustering.labels_

	# group logos
	logo_group = defaultdict(list)
	for i, label in enumerate(labels):
		logo_group[label].append(i)

	# print
	for group, logo_indices in logo_group.items():
		print(f'\nCluster {group}: {len(logo_indices)} logos')

		for idx in logo_indices:
			if idx < len(valid_logos):

				logo_filename = valid_logos[idx]
				website_url = logo_url_mapping.get(logo_filename)
				print(f'- {website_url}')


