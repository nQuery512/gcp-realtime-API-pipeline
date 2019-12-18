import requests

#base_url = "https://data.cityofchicago.org/resource/kf7e-cur8.json/"

def retrieve_data_from_api(base_url, external_api_key):
	params= dict()
	params['$$app_token'] = external_api_key

	r = requests.get(base_url, params=params)
	#if(r.status_code != 200)
	#print(r.status_code)
	#print(r.headers['content-type'])
	#print(r.encoding)
	#print(r.text)
	#print(r.json())
	return r.text
