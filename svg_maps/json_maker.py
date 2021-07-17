import json
import random

with open('svg_maps/states.json', 'r') as file:
    states = json.load(file)

output = {}
def randomize(vals):
    if not isinstance(vals,tuple):
        return randomize(tuple(vals))
    l = len(vals)
    if l < 2:
        return vals
    i = int(l * random.random())
    return vals[i:i+1] + randomize(vals[:i] + vals[i+1:])

for state, number in zip(states, randomize(range(len(states)))):
    output[state] = number

with open('svg_maps/random.json', 'w') as file:
    json.dump(output, file, indent=4)