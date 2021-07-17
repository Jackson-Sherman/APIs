import xml.etree.ElementTree as ET
from PIL import Image
import colorsys
import numpy as np
import json



def dataToColorFunction(vals, invert=False, option=None):
    maximum = max(vals)
    minimum = min(vals)
    dif = maximum - minimum
    add_me = - minimum / dif
    mul_me = 1 / dif
    scale = lambda x: mul_me * x + add_me
    if invert:
        scale = lambda x: 1 - (mul_me * x + add_me)
    if option:
        def color(value):
            value = scale(value)
            if value == 0:
                return (0,0,0)
            elif value < 0.5:
                return tuple([int(255 * i) for i in colorsys.hsv_to_rgb(0,1,2*value)])
            else:
                return tuple([int(255 * i) for i in colorsys.hsv_to_rgb((value - 0.5) / 3, 1 - 2 * scale(option) * (value - 0.5), 1)])

        return color
    else:
        def color(val):
            def compute(value):
                if value < 1/3:
                    return colorsys.hsv_to_rgb(0, 1, 1.5 * value + 0.25)
                elif value < 1/2:
                    return colorsys.hsv_to_rgb((value - 1/3) / 4, 1, 1.5 * value + 0.25)
                elif value < 1:
                    return colorsys.hsv_to_rgb((value - 1/3) / 4, 1, 1)
                else:
                    return (1,1,0)
            return tuple([int(255 * i) for i in compute(scale(val))])
        return color

def to_hex(tup):
    return '#' + ('{:02x}' * 3).format(*tup)

states = (
    "AL",
    "AK",
    "AR",
    "AZ",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "IA",
    "ID",
    "IL",
    "IN",
    "KS",
    "KY",
    "LA",
    "MA",
    "MD",
    "ME",
    "MI",
    "MN",
    "MO",
    "MS",
    "MT",
    "NC",
    "ND",
    "NE",
    "NH",
    "NJ",
    "NM",
    "NV",
    "NY",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VA",
    "VT",
    "WA",
    "WI",
    "WV",
    "WY",
    "DC"
)

def create(jsonpath,outputpath=None,invert=False):
    with open(jsonpath, "r") as file:
        data = json.load(file)

    zero_color = '#b0b0b0'
    
    fun = dataToColorFunction(data.values(), invert=invert)
    tree = ET.parse('svg_maps/original.svg')
    root = tree.getroot()
    # root.find('.//title').text = jsonpath.split('/')[-1][:-5]

    root.find(".//*[@id='outlines']").set('fill', zero_color)
    root.find(".//*[@id='label0']").text = '0'
    root.find(".//*[@id='box0']").set('fill', zero_color)
    minmax = min(data.values()), max(data.values())
    d = (minmax[1] - minmax[0]) / 3
    vals = 0, minmax[0], int(0.5 + d), int(0.5 + 2 * d), minmax[1]
    for i in range(1,5):
        root.find(".//*[@id='label" + str(i) + "']").text = str(vals[i])
        root.find(".//*[@id='box" + str(i) + "']").set('fill', to_hex(fun(vals[i])))

    # root.find('./svg/defs/style').text = '.state{fill:#b0b0b0;}'

    for state in states:
        elem = root.find(".//*[@id='" + state + "n']")
        if state in data:
            val = data[state]
            elem.text = str(val)
            color = fun(val)
            if colorsys.rgb_to_hsv(*[i/255 for i in color])[2] < 0.5:
                elem.set('fill','#ffffff')
            root.find(".//*[@id='" + state + "']").set('fill', to_hex(color))
        else:
            elem.text = '0'
        
    if outputpath is None:
        tree.write(jsonpath[:-4] + 'svg')
    else:
        tree.write(outputpath)
    
    

if __name__ == '__main__':
    create("svg_maps/random.json",invert=False)
    # img = Image.new('RGB',(100,100))
    # px = img.load()
    # fun = dataToColorFunction(range(img.size[0]), invert=True)
    # for y in range(img.size[0]):
    #     if y % 10 == 0:
    #         print('{:>3}%'.format(y))
    #     for x in range(img.size[1]):
    #         c = fun(x)
    #         px[x, y] = c
    
    # print('{:>3}%'.format(100))
    # img.show()