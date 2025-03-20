import os
import cv2
import numpy as np

'''
    Image Resizing:
        - Resizes all images in the 'src/logos' folder to a fixed size (100x100).
        - Ensures consistency in image dimensions to improve feature extraction performance.
'''

# folder paths
images_path = 'src/logos'
resized_images_path = 'src/resized_logos'
contour_images_path = 'src/logos_contour'
SIFT_images_path = 'src/logos_SIFT'
ORB_images_path = 'src/logos_ORB'

# create if it doesn't exist folder location for processed images
for folder in [images_path, resized_images_path, contour_images_path, SIFT_images_path, ORB_images_path]:
	if not os.path.exists(folder):
		os.makedirs(folder)


'''
	Image Resizing:
		- Resize images to a common size (100x100).
		- Save resized images to 'src/resized_logos' folder.
'''
def image_resize():
	# iterate files from folder
	for file in os.listdir(images_path):
		# each file from the folder has the .jpg extension
		# retrieve full path of the file
		file_path = os.path.join(images_path, file)

		# open the file / image
		img = cv2.imread(file_path)

		# check if the image was loaded successfully
		if img is not None:
			# resize the image to a common size (e.g., 100x100)
			resized_img = cv2.resize(img, (100, 100))

			# save resized images
			cv2.imwrite(os.path.join(resized_images_path, file), resized_img)


'''
    Hu Moments Feature Extraction:
        - Converts images to grayscale and applies a binary threshold to highlight shapes.
        - Extracts contours from each image and computes the seven Hu invariant moments.
        - Stores processed images with contours drawn for visualization.
        - Returns an array of Hu moments descriptors and the corresponding valid logos.
'''
def hu_moments():
	hu_moments_list = []
	valid_logos = []

	for file in os.listdir(resized_images_path):
		# fetch image path
		file_path = os.path.join(resized_images_path, file)

		# load color image
		img = cv2.imread(file_path)

		if img is not None:
			# load image in gray scale
			gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			# apply threshold
			ret, thresh = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY_INV)

			# find contours
			contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

			if contours:
				cnt = contours[0]
				M = cv2.moments(cnt)
				hu = cv2.HuMoments(M).flatten()

				hu_moments_list.append(hu)
				valid_logos.append(file)

				cv2.drawContours(img, [cnt], -1, (150, 0, 255), 3)
				cv2.imwrite(os.path.join(contour_images_path, file), img)

	return np.array(hu_moments_list), valid_logos


'''
    SIFT (Scale-Invariant Feature Transform) Feature Extraction:
        - Converts images to grayscale and detects keypoints using SIFT.
        - Computes feature descriptors based on detected keypoints.
        - Averages the descriptors for each image to create a feature vector.
        - Saves images with keypoints drawn for visualization.
        - Returns an array of SIFT descriptors and the corresponding valid logos.
'''
def image_SIFT_processing():
	feature_SIFT_vector = []
	valid_logos = []

	# init SIFT detector
	sift = cv2.SIFT_create()

	for file in os.listdir(resized_images_path):
		file_path = os.path.join(resized_images_path, file)

		# load image in gray scale
		resized_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
		keypoints, descriptors = sift.detectAndCompute(resized_image, None)

		# verify descriptors
		if descriptors is not None:
			mean_descriptor = np.mean(descriptors, axis=0)
			feature_SIFT_vector.append(mean_descriptor)
			# append the valid file
			valid_logos.append(file)

		image_sift = cv2.drawKeypoints(resized_image, keypoints, None,
									   flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
		cv2.imwrite(os.path.join(SIFT_images_path, file), image_sift)

	return np.array(feature_SIFT_vector), valid_logos


'''
    ORB (Oriented FAST and Rotated BRIEF) Feature Extraction:
        - Uses ORB, a fast alternative to SIFT, combining FAST keypoint detection and BRIEF descriptors.
        - Extracts keypoints and computes binary feature descriptors.
        - Averages the descriptors to generate a feature vector for each image.
        - Saves images with detected keypoints drawn for visualization.
        - Returns an array of ORB descriptors and the corresponding valid logos.
'''
def image_ORB_processing():
	feature_ORB_vector = []
	valid_logos = []

	# init SURF detector
	orb = cv2.ORB_create(400)

	for file in os.listdir(resized_images_path):
		file_path = os.path.join(resized_images_path, file)

		# load image
		resized_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
		keypoints, descriptors = orb.detectAndCompute(resized_image, None)

		# verify descriptors
		if descriptors is not None:
			mean_descriptor = np.mean(descriptors, axis=0)
			feature_ORB_vector.append(mean_descriptor)
			# append the valid file
			valid_logos.append(file)


		image_ORB = cv2.drawKeypoints(resized_image, keypoints, None, flags=0)
		cv2.imwrite(os.path.join(ORB_images_path, file), image_ORB)

	return np.array(feature_ORB_vector), valid_logos