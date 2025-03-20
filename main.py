import os
import sys
import shutil
from src.logo_fetch import scrape_website_logo
from src.logo_processing import image_resize, image_SIFT_processing, image_ORB_processing, hu_moments
from src.logo_similarity import compute_similarity, group_similar_logos

sys.path.append('src')

'''
	Provide a prettier display method
'''
def print_groups(title, groups):
	print("\n" + "=" * 50)
	print(f" {title} ")
	print("=" * 50)

	for idx, group in enumerate(groups, start=1):
		print(f"Group {idx}: {', '.join(group)} - {len(group)}\n")

	print("=" * 50 + "\n")

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
	scrape_website_logo()

	# process images
	image_resize()
	feature_hu_vector, valid_logos_hu = hu_moments()
	feature_SIFT_vector, valid_logos_SIFT = image_SIFT_processing()
	feature_ORB_vector, valid_logos_ORB = image_ORB_processing()

	# Compute similarities
	hu_similarities = compute_similarity(feature_hu_vector, valid_logos_hu)
	sift_similarities = compute_similarity(feature_SIFT_vector, valid_logos_SIFT)
	orb_similarities = compute_similarity(feature_ORB_vector, valid_logos_ORB)

	# Group similar logos
	hu_groups = group_similar_logos(hu_similarities)
	sift_groups = group_similar_logos(sift_similarities)
	orb_groups = group_similar_logos(orb_similarities)

	# Print groups
	print_groups("Hu Moments Groups:", hu_groups)
	print_groups("SIFT Groups:", sift_groups)
	print_groups("ORB Groups:", orb_groups)

	# remove unwanted folders
	remove_images_folder()

	# remove processed logos folder after visualization
	# uncomment line to delete processed folders after program run
	remove_processed_images_folder()
