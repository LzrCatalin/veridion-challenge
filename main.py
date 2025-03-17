import os
import sys
import shutil

import pandas as pd
from src.logo_fetch import scrape_website_logo
sys.path.append('src')

if __name__ == '__main__':
	# read .parquet file
	df = pd.read_parquet('src/dataset/logos.snappy.parquet', engine='pyarrow')
	print(df.values)

	# store websites into a list
	websites = df.values.tolist()

	# iterate list of websites
	for website in websites[:20]:
		scrape_website_logo(website[0])
	print('Websites scraped')

	# remove logos folder
	if os.path.exists('src/logos'):
		print('Folder exists')
		shutil.rmtree('src/logos')
		print('Removing folder')
