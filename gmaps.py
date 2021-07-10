import googlemaps
import json
import numpy as np
import colorsys
from PIL import Image
from datetime import datetime

beginning = datetime.now()

gm = googlemaps.Client(key='AIzaSyDIAv5PSciIzYg4B9edFs07hYGSXxiFd14')

def stateFromCoord(latitude, longitude):
	with open('states.json', 'r') as file:
		existing_data = json.load(file)
	latitude, longitude = round(latitude, 3), round(longitude, 3)
	latkey = str(latitude)
	lngkey = str(longitude)

	def getState(result):
		if result:
			state = None
			for component in result[0]["address_components"]:
				if "country" in component["types"]:
					if component["short_name"] != "US":
						return component["short_name"]
				elif "administrative_area_level_1" in component["types"]:
					state = component["short_name"]
			return state
		else:
			return None
					
	if latkey not in existing_data:
		existing_data[latkey] = {}
	
	if lngkey not in existing_data[latkey]:
		existing_data[latkey][lngkey] = getState(gm.reverse_geocode((latitude, longitude)))
		with open('states.json', 'w') as file:
			json.dump(existing_data, file, indent=4)
	
	return existing_data[latkey][lngkey]

def operation(inp, fun):
	function_options = {'geocode', 'reverse_geocode'}
	assert fun in function_options
	with open('results.json', 'r') as file:
		existing_data = json.load(file)

	if isinstance(inp,(tuple,list)):
		key = str(inp)[1:-1]
	else:
		key = inp

	has_not_function = fun not in existing_data

	if has_not_function or key not in existing_data[fun]:
		result = eval('gm.' + fun + '(' + str(inp) + ')')
		if has_not_function:
			existing_data[fun] = {}
		if fun == 'reverse_geocode':
			existing_data[fun][key] = result[0]
		else:
			existing_data[fun][key] = result
	output = existing_data[fun][key]

	with open('results.json', 'w') as file:
		json.dump(existing_data, file, indent=4, sort_keys=True)
	
	return output


def geocode(address):
	address = str(address)
	result = gm.geocode(address)
	return result

def reverse_geocode(coord):
	result = eval('gm.' + 'reverse_geocode' + '(' + str(coord) + ')')
	return result

def reverse_result_to_state(result):
	try:
		components = result[0]["address_components"] #type is list
		def get_entry_with_type(cual):
			for each in components:
				if cual in each["types"]:
					return each
			return None
		country = get_entry_with_type("country")["short_name"]
		if country == "US":
			state = get_entry_with_type("administrative_area_level_1")["short_name"]
			return state
		else:
			return country
	except:
		return None

def coord_range(coord0, coord1, min_side_length):
	bl = tuple([min(coord0[i], coord1[i]) for i in (0,1)])
	tr = tuple([max(coord0[i], coord1[i]) for i in (0,1)])
	lat_array, lon_array = None, None
	dif = min(tr[0] - bl[0], tr[1] - bl[1])
	step = dif / min_side_length
	lat_array = np.arange(bl[0], tr[0], step)
	lon_array = np.arange(bl[1], tr[1], step)
	lat_array -= (tr[0] - lat_array[-1] + 1) / 2
	lon_array -= (tr[1] - lon_array[-1] + 1) / 2
	return tuple(np.round(lat_array, 3)), tuple(np.round(lon_array, 3))

def state_array(lats, lons):
	return np.full((len(lats), len(lons)), '', dtype=str)

def makeStateMap(coord0, coord1, min_side_length):
	lats, lons = coord_range(coord0, coord1, min_side_length)
	colors = np.zeros((len(lats), len(lons), 3),dtype=int)
	state_colors = {}
	def printDif(start_time):
		now = datetime.now()
		print(now - start_time)
		return now
	def string_to_color(string):
		result = np.zeros(3,dtype=int)
		if string is None:
			return result
		if string not in state_colors:
			try:
				val = 0
				for char in string.upper()[::-1]:
					val += "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(char) + 1
					val /= 27
				result = np.array([int(255 * i) for i in colorsys.hsv_to_rgb(val, 1.0, 1.0)], dtype=int)
			except:
				pass
			state_colors[string] = result
		return state_colors[string]
	form = '{:>' + str(len(str(len(lats)))) + '} / ' + str(len(lats))
	start = datetime.now()
	for yi,y in enumerate(lats):
		print(form.format(yi), end=' time: ')
		start = printDif(start)
		for xi,x in enumerate(lons):
			state = stateFromCoord(y,x)
			colors[yi][xi] = string_to_color(state)
	
	return Image.fromarray(colors.astype(np.uint8)[::-1])

if __name__ == '__main__':
	img = makeStateMap((49.0, -125.0), (25.0, -66.0), 50)
	img.show()
	img.save('test_complete.png')
	print("total time: " + str(datetime.now() - beginning))