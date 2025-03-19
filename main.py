import os
import sys
import shutil
import pandas as pd
from src.logo_fetch import scrape_website_logo
from src.logo_processing import image_resize, image_SIFT_processing, image_ORB_processing, hu_moments
from src.logo_similarity import similarity

sys.path.append('src')

'''
	Remove folders of downloaded images after scrape and
	resized folder of the images
'''
def remove_images_folder():
	print('Removing images folder')
	if os.path.exists('src/logos'):
		shutil.rmtree('src/logos')

	if os.path.exists('src/resized_logos'):
		shutil.rmtree('src/resized_logos')

'''
	Remove folders of processed images after applying SIFT and ORB
	and contours from HuMoments
'''
def remove_processed_images_folder():
	print('Removing processed images folder')
	if os.path.exists('src/logos_contour'):
		shutil.rmtree('src/logos_contour')

	if os.path.exists('src/logos_SIFT'):
		shutil.rmtree('src/logos_SIFT')

	if os.path.exists('src/logos_ORB'):
		shutil.rmtree('src/logos_ORB')

if __name__ == '__main__':
	# return a mapping of the stored images to their corresponding URLs
	logo_url_mapping = scrape_website_logo()

	# process images
	image_resize()
	feature_hu_vector, valid_logos_hu = hu_moments()
	feature_SIFT_vector, valid_logos_SIFT = image_SIFT_processing()
	feature_ORB_vector, valid_logos_ORB = image_ORB_processing()

	# verify similarity
	print("Similarity for HuMoments:")
	similarity(feature_hu_vector, valid_logos_hu, logo_url_mapping)

	print("Similarity for SIFT:")
	similarity(feature_SIFT_vector, valid_logos_SIFT, logo_url_mapping)

	print("Similarity for ORB:")
	similarity(feature_ORB_vector, valid_logos_ORB, logo_url_mapping)

	# remove unwanted folders
	remove_images_folder()

	# remove processed logos folder after visualization
	# uncomment line to delete processed folders after program run
	# remove_processed_images_folder()
