import os
import urllib3
import pandas as pd
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as bs

# create if it doesn't exist folder location for logos
if not os.path.exists('src/logos'):
	os.mkdir('src/logos')

http = urllib3.PoolManager()

# defined list of most common used words for logo finding
COMMON_WORDS = ['logo', 'brand', 'site-logo']


'''
    Ensure HTTP/HTTPS in URL:
        - Takes a URL as input and ensures it has either "http://" or "https://".
        - Attempts a GET request to verify which protocol (HTTP or HTTPS) is supported.
        - Returns the tuple of website response data with the website url.
'''
def ensure_http_request(url):
	# print(f'Verifying {url}')

	if not url.startswith(('http://', 'https://')):
		#
		#	Verify both protocols
		#
		try:
			response_http = http.request('GET', 'http://' + url, timeout=1)
			if response_http.status == 200:
				# print(f'  -> http://{url}')
				return response_http.data, 'http://' + url

		except urllib3.exceptions.MaxRetryError:
			pass

		try:
			response_https = http.request('GET', 'https://' + url, timeout=1)
			if response_https.status == 200:
				# print(f'  -> https://{url}')
				return response_https.data, 'https://' + url

		except urllib3.exceptions.MaxRetryError:
			pass

		# If neither protocol works, return None
		return None, url

	else:
		# If the URL already has a protocol, fetch it directly
		response = http.request('GET', url, timeout=5)
		if response.status == 200:
			return response.data, url

		else:
			return None, url


'''
    Retrieve Websites from Parquet File:
        - Reads a .snappy.parquet file containing website URLs using pandas.
        - Ensures each URL is properly formatted with "https://" if missing.
        - Returns a list of valid website URLs.
'''
def retrieve_websites_data():
	# read .parquet file
	df = pd.read_parquet('src/dataset/logos.snappy.parquet', engine='pyarrow')

	# store websites into a list
	# 	-> df.values.tolist()[:x] 	=> set x as the maximum number of websites to verify
	#	-> df.values.tolist() 		=> verify the whole dataset of websites
	websites_data = [ensure_http_request(w[0]) for w in df.values.tolist()[:200] if w[0]]
	websites_data = [data_url for data_url in websites_data if data_url[0] is not None]

	return websites_data


'''
    Scrape Website for Logos:
        - Iterates through a list of website URLs to extract logos.
        - Fetches the website's HTML using urllib3.
        - Parses the HTML using BeautifulSoup to find `<img>` tags.
        - Identifies potential logos by checking:
            - The `src` attribute.
            - The `class` or `id` attributes for common keywords (e.g., "logo", "brand").
        - Constructs the full logo URL and downloads the image if available.
        - Saves each logo in the "src/logos" folder with a filename based on the website name.
        - Handles various exceptions, including timeouts, connection errors, and invalid responses.
        - Returns a dictionary mapping logo filenames to their corresponding website URLs.
'''
def scrape_website_logo():
	# map with image and url as key-value pair
	logo_url_mapping = {}

	# iterate
	for data, url in retrieve_websites_data():
		if data is None:
			continue

		# split url to get website name
		website_name = urlparse(url).netloc.split('.')[0]

		try:
			# html parse
			soup = bs(data, 'html.parser')

			# look-up for logo in html parse data
			for img in soup.find_all('img'):
				# print(img)

				'''
				Search for attributes: src, class or id
				and check for each of the common keywords
				'''
				try:
					src = img.get('src', '')
					if src:
						if any(keyword in src.lower() for keyword in COMMON_WORDS) or \
								any(keyword in img.get('class', []) for keyword in COMMON_WORDS) or \
								any(keyword in img.get('id', '') for keyword in COMMON_WORDS):

							logo_url = urljoin(url, src)

							# download the logo
							try:
								# fetch response about image url
								logo_response = http.request('GET', logo_url, timeout=1)
								# verify response
								if logo_response.status == 200:
									# give file path
									file_path = os.path.join('src/logos', f'{website_name}.jpg')
									# save file
									with open(file_path, 'wb') as logo_file:
										logo_file.write(logo_response.data)

									# store the website that has successfully been saved
									logo_url_mapping[f'{website_name}.jpg'] = url

								else:
									print('Failed to download logo')

							except Exception as e:
								print(f'Failed to download logo: {e}')
							break

				except Exception as e:
					print(f'Failed to parse img: {e}')

		except urllib3.exceptions.TimeoutError as e:
			print(f"TimeoutError for {url}: {e}")
		except urllib3.exceptions.ConnectionError as e:
			print(f"ConnectionError for {url}: {e}")
		except urllib3.exceptions.HTTPError as e:
			print(f"HTTPError for {url}: {e}")
		except Exception as e:
			print(f"Unexpected error for {url}: {e}")

	return logo_url_mapping
