"""
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""

import mesa
import numpy as np

from boid import Boid, Airplane, Airport


class BoidFlockers(mesa.Model):
    """
    Flocker model class. Handles agent creation, placement and scheduling.
    """

    def __init__(
        self,
        population=100,
        width=100,
        height=100,
        speed=1,
        vision=10,
        separation=2,
        cohere=0.025,
        separate=0.25,
        match=0.04,
    ):
        """
        Create a new Flockers model.
        Args:
            population: Number of Boids
            width, height: Size of the space.
            speed: How fast should the Boids move.
            vision: How far around should each Boid look for its neighbors
            separation: What's the minimum distance each Boid will attempt to
                    keep from any other
            cohere, separate, match: factors for the relative importance of
                    the three drives."""
        self.population = population
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.schedule = mesa.time.RandomActivation(self)
        self.space = mesa.space.ContinuousSpace(width, height, True)
        self.factors = dict(cohere=cohere, separate=separate, match=match)
        self.make_agents()
        self.running = True

    def make_agents(self):
        """
        Create self.population agents, with random positions and starting headings.
        """
        for i in range(self.population):
            x = self.random.random() * self.space.x_max
            y = self.random.random() * self.space.y_max
            pos = np.array((x, y))
            velocity = np.random.random(2) * 2 - 1
            boid = Boid(
                i,
                self,
                pos,
                self.speed,
                velocity,
                self.vision,
                self.separation,
                **self.factors
            )
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)

    def step(self):
        self.schedule.step()

class AirplaneFlockers(BoidFlockers):
    def __init__(
                self, population, width, height, routes):
        self.routes = routes

        self.index = 0 #Position in route where the agent finds itself
        self.route_extremes = [ [r[0], r[-1]] for r in routes ]
        self.airport_locations = [x for x in {s for s in [a[0] for a in self.route_extremes]+[a[1] for a in self.route_extremes]}]
        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        super().__init__(population, width, height)        

    def make_agents(self):
        """
        Create self.population agents, starting at an airport.
        """
        for i in range(len(self.routes)):
            x = self.routes[i][0][0]
            y = self.routes[i][0][1]
            pos = np.array((x, y))
            route = self.routes[i]
            index = self.index
            
            previ = 0
            direction = 1
            
            airplane = Airplane(
                    i,
                    self,
                    pos,route,index,previ,direction
                    )
            self.space.place_agent(airplane, pos)
            self.schedule.add(airplane)
        
        """
        Create airports.
        """
        for i in range(len(self.airport_locations)):
            x, y = self.airport_locations[i][0], self.airport_locations[i][1]
            pos = np.array((x, y))
            runways = 1
            runways_occupied = 1
            grid = self.grid

            airport = Airport(
                i+len(self.routes),
                self,
                pos,
                runways,runways_occupied,grid
            )
            self.space.place_agent(airport, pos)
            self.schedule.add(airport)

    def step(self):
        self.schedule.step()