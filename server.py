import mesa
from mesa.visualization.ModularVisualization import ModularServer

from model import BoidFlockers
from SimpleContinuousModule import SimpleCanvas

def draw(agent):
    portrayal = {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Red", "Layer":0}
    return portrayal

canvas_element = SimpleCanvas(draw, 500, 500)

model_params = {
    "population": 10,
    "width": 100,
    "height": 100,
    "speed": 5,
    "vision": 10,
    "separation": 2
}

server = ModularServer( BoidFlockers, 
                        [canvas_element], 
                        "Boids", model_params)