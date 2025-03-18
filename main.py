import os
import sys
import shutil

import pandas as pd
from src.logo_fetch import scrape_website_logo
from src.image_processing import image_resizing, image_contour_processing, image_SIFT_processing, image_ORB_processing
sys.path.append('src')

if __name__ == '__main__':
	# websites scraping
	scrape_website_logo()
	print('Websites scraped')

	# process images
	image_resizing()
	image_contour_processing()
	image_SIFT_processing()
	image_ORB_processing()

	# remove logos folder
	if os.path.exists('src/logos'):
		print('Folder exists')
		shutil.rmtree('src/logos')
		print('Removing folder')

	if os.path.exists('src/resized_logos'):
		print('Folder exists')
		shutil.rmtree('src/resized_logos')
		print('Removing folder')
