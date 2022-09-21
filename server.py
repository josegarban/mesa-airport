# Code based in MESA's own examples

import mesa
from mesa.visualization.ModularVisualization import ModularServer
import paths
from model import AirplaneFlockers
from SimpleContinuousModule import SimpleCanvas

def draw(agent):
    portrayal = {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Red", "Layer":0}
    return portrayal

canvas_element = SimpleCanvas(draw, 10, 10)

routes = paths.AIRPORTS
worldmap, route_solutions = paths.main(routes, width=10, height=10)


model_params = {
    "population": 0,
    "width": 10,
    "height": 10,
    "routes": route_solutions
}


server = ModularServer( AirplaneFlockers, 
                        [canvas_element], 
                        "Planes", model_params)