import json
import requests
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import time

class Doublemap:
    def __init__(self, system_name="iub"):
        self.root_url = "http://" + str(system_name) + ".doublemap.com/map/v2/"
        self.routes = self.pull("routes")
        self.stops = self.pull("stops")
        self.prev = self.get_state()
    
    def draw_route(self, short_name):
        route = None
        for r in self.routes:
            if r["short_name"] == short_name:
                route = r
                break
        
        assert route is not None and isinstance(route, dict)

        fig, ax = plt.subplots()

        r_y = np.zeros(len(route["path"])//2, dtype=np.float32)
        r_x = np.zeros_like(r_y)
        for i,j in enumerate(route["path"]):
            if i % 2 == 0:
                r_y[i//2] = j
            else:
                r_x[i//2] = j
        
        s_y = []
        s_x = []
        for i,j in enumerate(route["stops"]):
            st = None
            for row in self.stops:
                if row["id"] == j:
                    st = row
                    break
            if st is None:
                print("id {} not found".format(j))
            else:
                s_y.append(st["lat"])
                s_x.append(st["lon"])
        
        median_latitude = sorted(r_y)[len(r_y)//2]

        ax.set_aspect(1/np.cos(median_latitude * np.pi / 180))
        ax.plot(r_x, r_y, color='#'+route["color"])
        ax.plot(s_x, s_y, 'o', color="#000000")
        plt.show()


    def side_of_point(point):
        c = Doublemap.cutoff
        if point[0] == c[0]:
            return 1 if c[1] <= point[1] and point[1] <= c[3] else 0
        elif point[0] > c[0]:
            return 1 if c[1] <= point[1] else 0
        return -1 if point[1] <= c[3] else 0
    
    def pull(self, specific_api):
        api_url = self.root_url + specific_api
        response = requests.get(api_url)
        output = response.json()
        return output
    
    def get_state(self):
        return self.pull("buses")
    
    # def check_stops(self):
    #     curr = self.get_state()
    #     w_buses = [bus for bus in curr if bus["route"] == 819]
    #     w_bus_ids = [bus["id"] for bus in w_buses]
    #     for bus in self.prev:
    #         if bus["id"] in w_bus_ids:
                


if __name__ == '__main__':
    dm = Doublemap()
    route_shorts = [r["short_name"] for r in dm.routes]
    route_shorts.sort()
    listed = route_shorts[0]
    for each in route_shorts[1:]:
        listed += ', ' + each
    print("current services: " + listed)
    print()
    which = input("which one do you want to draw: ")
    dm.draw_route(which)