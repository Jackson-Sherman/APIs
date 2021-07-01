import googlemaps
import json

gm = googlemaps.Client(key='AIzaSyDIAv5PSciIzYg4B9edFs07hYGSXxiFd14')

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
		if has_not_function :
			existing_data[fun] = {}
		existing_data[fun][key] = result
	output = existing_data[fun][key]

	with open('results.json', 'w') as file:
		json.dump(existing_data, file, indent=4, sort_keys=True)
	print(json.dumps(output, indent=4, sort_keys=True))
	return output


def geocode(address):
	address = str(address)
	print('address: ' + address)
	print()
	result = gm.geocode(address)
	print('geocode: ' + json.dumps(result,indent=4))
	return result

def reverse_geocode(coord):
	print('coord: ' + str(coord))
	print()
	result = eval('gm.' + 'reverse_geocode' + '(' + str(coord) + ')')
	print('geocode: ' + json.dumps(result,indent=4))
	return result

if __name__ == '__main__':
	# reverse_geocode((39.934917146948614, -85.83684789098275))
	operation((39.934917146948614, -85.83684789098275), 'reverse_geocode')