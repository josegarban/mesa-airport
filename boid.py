import mesa
import numpy as np
from random import random


class Boid(mesa.Agent):
    """
    A Boid-style flocker agent.
    The agent follows three behaviors to flock:
        - Cohesion: steering towards neighboring agents.
        - Separation: avoiding getting too close to any other agent.
        - Alignment: try to fly in the same direction as the neighbors.
    Boids have a vision that defines the radius in which they look for their
    neighbors to flock with. Their speed (a scalar) and velocity (a vector)
    define their movement. Separation is their desired minimum distance from
    any other Boid.
    """

    def __init__(
        self,
        unique_id,
        model,
        pos,
        speed,
        velocity,
        vision,
        separation,
        cohere=0.025,
        separate=0.25,
        match=0.04,
    ):
        """
        Create a new Boid flocker agent.
        Args:
            unique_id: Unique agent identifyer.
            pos: Starting position
            speed: Distance to move per step.
            heading: numpy vector for the Boid's direction of movement.
            vision: Radius to look around for nearby Boids.
            separation: Minimum distance to maintain from other Boids.
            cohere: the relative importance of matching neighbors' positions
            separate: the relative importance of avoiding close neighbors
            match: the relative importance of matching neighbors' headings
        """
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        self.separation = separation
        self.cohere_factor = cohere
        self.separate_factor = separate
        self.match_factor = match

    def cohere(self, neighbors):
        """
        Return the vector toward the center of mass of the local neighbors.
        """
        cohere = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                cohere += self.model.space.get_heading(self.pos, neighbor.pos)
            cohere /= len(neighbors)
        return cohere

    def separate(self, neighbors):
        """
        Return a vector away from any neighbors closer than separation dist.
        """
        me = self.pos
        them = (n.pos for n in neighbors)
        separation_vector = np.zeros(2)
        for other in them:
            if self.model.space.get_distance(me, other) < self.separation:
                separation_vector -= self.model.space.get_heading(me, other)
        return separation_vector

    def match_heading(self, neighbors):
        """
        Return a vector of the neighbors' average heading.
        """
        match_vector = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                match_vector += neighbor.velocity
            match_vector /= len(neighbors)
        return match_vector

    def step(self):
        """
        Get the Boid's neighbors, compute the new vector, and move accordingly.
        """

        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        self.velocity += (
            self.cohere(neighbors) * self.cohere_factor
            + self.separate(neighbors) * self.separate_factor
            + self.match_heading(neighbors) * self.match_factor
        ) / 2
        self.velocity /= np.linalg.norm(self.velocity)
        new_pos = self.pos + self.velocity * self.speed
        self.model.space.move_agent(self, new_pos)

    

class Airplane(mesa.Agent):
    """
    Class similar to Boid, with fewer features
    """
    def __init__(
        self,
        unique_id,
        model,
        pos,route,index,previ,direction
    ):
        super().__init__(unique_id, model)
        self.pos        = np.array(pos)
        self.route      = route
        self.index      = index
        self.previ      = previ
        self.direction  = 1
        self.type       = "airplane"

        print(self.pos)
    
    def step(self):
        """
        Move to another position
        """
        print("Plane {0} at position {1} ({2}) in direction {3}"\
            .format(self.unique_id, self.index, self.pos, self.direction))

        if self.direction == 1:
            if      self.index + 1 == len(self.route):
                next_idx = self.index
            elif    self.index + 1 <= len(self.route):
                next_idx = self.index + 1
            elif    self.index == 0:
                next_idx = self.index
        elif self.direction == -1: # Going backwards
            if      self.index == 0:
                next_idx = self.index
            elif    self.index - 1 >= -1:
                next_idx = self.index - 1
            elif    self.index == 0:
                next_idx = self.index

        # Reverse direction?
        if   self.index + 1 == len(self.route)  : self.direction = -1
        elif self.index - 1 == -1                : self.direction =  1

        next_pos    = self.route[next_idx]
        self.previ  = self.index
        self.index  = next_idx
        self.model.space.move_agent(self, next_pos)



class Airport(mesa.Agent):
    """
    An airport is an agent that doesn't move and that checks how many airplanes there are at its position
    """
    def __init__(
        self,
        unique_id,
        model,
        pos,
        grid,
        runways=1,
        runways_occupied=0,
        full=False,
        type="airport"
    ):
        """
        pos: position of the airport
        runways: amount of runways for airplanes
        Runways don't have a spatial location different from that of the airport
        """
        super().__init__(unique_id, model)
        self.pos                = np.array(pos)
        self.runways            = runways
        self.runways_occupied   = runways_occupied
        self.full               = full
        self.grid               = grid
        self.type               = type

    def step(self):
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        airplanes = [obj for obj in this_cell if isinstance(obj, Airplane)]
        
        if len(airplanes) == 0:
            self.runways_occupied=0
            self.full = False
        elif len(airplanes) < self.runways:
            self.runways_occupied = len(airplanes)
            self.full = False
        elif len(airplanes) == self.runways:
            self.runways_occupied = len(airplanes)
            self.full = True