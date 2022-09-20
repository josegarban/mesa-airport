import numpy as np
import skimage
from pprint import pprint

# First, let's determine fixed positions for the airports

AIRPORTS = ( (2,2), (3,8), (1,0), (1,10), (8,1), (7,5) )

def destinations(airports=AIRPORTS):
    """
    Match airport i to airport i+1
    """
    alldestinations = [ (airports[i], airports[i+1]) for i in list(range(len(airports))) if i%2 == 0 ]
    print(alldestinations)
    return alldestinations


def mapmaker(width=10, height=10):
    output = []
    # Draw empty grid
    for y in range(height):
        row = []
        for x in range(width):
            # There will be a cost in that point
            value = True
            row.append(value)
        output.append(row)
    return output

def pointsetter(map=mapmaker(), airports=AIRPORTS, width=10, height=10):
    output = map
    for a in airports:
        y_pos, x_pos = a
        for y in range(height):
            for x in range(width):
                if (x+1 == width-x_pos) and (y+1 == height-y_pos):
                    output[x_pos-width][y_pos-height] = False
    return output

def pathmaker(map=pointsetter(), route_extremes=AIRPORTS[0:2], width=10, height=10):
    start, end = route_extremes
    array = np.asarray(map)
    costs = np.where(array, 100, 0)
    
    # Airplanes will move between airports in straight lines.
    path, cost = skimage.graph.route_through_array(costs, start=start, end=end, fully_connected=False)
    return route_extremes, array, path, cost

if __name__ == "__main__":
    # Test function
    #print(np.asarray(pointsetter()))
    #for x in pathmaker(): print(x)
    destinations()