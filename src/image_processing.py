import os
import cv2

'''
	Images Processing;
		1. Open each image from logos folder in grey scale, so there be no difference
		and resize all of them to a similar size
		2. Implementing algorithms that helps to extract images characteristics
			-> findContours() -> SIFT alg -> ORB alg
'''

# folder paths
images_path = 'src/logos'
resized_images_path = 'src/resized_logos'
contour_images_path = 'src/logos_contour'
SIFT_images_path = 'src/logos_SIFT'
ORB_images_path = 'src/logos_ORB'

# create if it doesn't exist folder location for images
if not os.path.exists(resized_images_path):
	print('Save directory not found, creating it')
	os.mkdir(resized_images_path)

if not os.path.exists(contour_images_path):
	print('Contour directory not found, creating it')
	os.mkdir(contour_images_path)

if not os.path.exists(SIFT_images_path):
	print('SIFT directory not found, creating it')
	os.mkdir(SIFT_images_path)

if not os.path.exists(ORB_images_path):
	print('SURF directory not found, creating it')
	os.mkdir(ORB_images_path)

'''
	Resize images into a common size
'''
def image_resizing():
	# iterate files from folder
	for file in os.listdir(images_path):
		# each file from the folder has the .jpg extension
		# retrieve full path of the file
		file_path = os.path.join(images_path, file)

		# open the file / image
		img = cv2.imread(file_path)

		# check if the image was loaded successfully
		if img is None:
			print(f"Failed to load image: {file_path}")
			continue

		# resize the image to a common size (e.g., 100x100)
		resized_img = cv2.resize(img, (100, 100))

		# save resized images
		cv2.imwrite(os.path.join(resized_images_path, file), resized_img)

'''
	Open resized images and get contours
'''
def image_contour_processing():
	for file in os.listdir(resized_images_path):
		file_path = os.path.join(resized_images_path, file)

		# load image in gray scale
		resized_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
		if resized_image is None:
			continue

		# find contours
		contours, _ = cv2.findContours(resized_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		# convert grayscale to BGR for contour drawing
		image_with_contours = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2BGR)

		# draw contours
		cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)

		# save contour img
		cv2.imwrite(os.path.join(contour_images_path, file), image_with_contours)

'''
	Applying SIFT (Scale-Invariant Fourier Transform) on resized images
	Algorithm based on Difference of Gaussians for keypoint detection.
		-> Accurate but slower, known for its robustness to scale, rotation
		and illumination changes
'''
def image_SIFT_processing():
	# iterate resized images folder
	for file in os.listdir(resized_images_path):
		file_path = os.path.join(resized_images_path, file)

		# load image in gray scale
		resized_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

		# init SIFT detector
		sift = cv2.SIFT_create()

		# detect
		keypoints, descriptors = sift.detectAndCompute(resized_image, None)

		# draw keypoints on the image
		image_sift = cv2.drawKeypoints(resized_image, keypoints, None,
									   flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

		# save sift process image
		cv2.imwrite(os.path.join(SIFT_images_path, file), image_sift)

'''
	ORB algorithm, an efficient alternative to SIFT and SURF.
	Fusion of FAST keypoints and BRIEF descriptors
		-> improve version of SIFT
'''
def image_ORB_processing():
	for file in os.listdir(resized_images_path):
		file_path = os.path.join(resized_images_path, file)

		# load image
		resized_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

		# init SURF detector
		orb = cv2.ORB_create(400)

		# detect
		keypoints, descriptors = orb.detectAndCompute(resized_image, None)

		# draw
		image_ORB = cv2.drawKeypoints(resized_image, keypoints, None, flags=0)

		# save surf process image
		cv2.imwrite(os.path.join(ORB_images_path, file), image_ORB)


