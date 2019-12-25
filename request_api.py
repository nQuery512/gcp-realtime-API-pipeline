import requests

def retrieve_data_from_api(base_url, external_api_key):
	params= dict()
	params['$$app_token'] = external_api_key

	r = requests.get(base_url, params=params)

	return r.text
