import googlemaps
import json

gm = googlemaps.Client(key='AIzaSyDIAv5PSciIzYg4B9edFs07hYGSXxiFd14')

def geocode(address):
	address = str(address)
	print('address: ' + address)
	print()
	result = gm.geocode(address)
	print('geocode: ' + json.dumps(result,indent=4))
	return result

if __name__ == '__main__':
	with open('C:\\Users\\Laser 2\\Downloads\\location.json', 'w') as file:
		json.dump(geocode('289 Bus Park Dr 46040'), file, indent=4)