import numpy as np
import skimage
from pprint import pprint

# First, let's determine fixed positions for the airports

AIRPORTS = ( (2,2), (3,8), (0,0) )


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

# Airplanes will move between airports following an "L"-shaped path.
def pointsetter(map=mapmaker(), airports=AIRPORTS, width=10, height=10):
    output = map
    for a in airports:
        y_pos, x_pos = a
        for y in range(height):
            for x in range(width):
                if (x+1 == width-x_pos) and (y+1 == height-y_pos):
                    output[x_pos-width][y_pos-height] = False
    return output

def pathmaker(map=pointsetter(), airports=AIRPORTS, width=10, height=10):
    start, end = airports[0:2]
    array = np.asarray(map)
    costs = np.where(array, 100, 0)
    path, cost = skimage.graph.route_through_array(costs, start=start, end=end, fully_connected=False)
    return array, path, cost

if __name__ == "__main__":
    # Test function
    #print(np.asarray(pointsetter()))
    for x in pathmaker(): print(x)