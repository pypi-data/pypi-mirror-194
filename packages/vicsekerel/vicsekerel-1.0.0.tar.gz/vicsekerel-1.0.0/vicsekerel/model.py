
import numpy as np
from .entity import Entity
from .animation import Animation


class Model:
    def __init__(self, dimensions=[30,30], n_entities=300, velocity_mod=4, radius_perceived=1, noise=0.4, dt_time=0.01, time=4):
        """Initialize model.

        Args:
            dimensions (List): Size and width of the model space.
            n_entities (Int): Number of entities that will populate the model.
            velocity_mod (Float): Module of the entities' velocity
            radius_perceived (Float): Maximum distance looked at when defining neighbours.
            noise (Float): Parameter controlling the amount of turbulence in the entities' movement.
            dt_time (Int): Discretization time used in the simulation runs (in seconds).
            time (Int): Total simulation time (in seconds)
        """
        self.dimensions = dimensions
        self.n_entities = n_entities
        self.velocity_mod=velocity_mod
        self.radius_perceived= radius_perceived
        self.entities = [Entity(dimensions, velocity_mod, radius_perceived,noise ) for x in range(n_entities)]
        self.time = time
        self.dt_time = dt_time
        self.noise = noise
        self.iterations_data = []

    def run_iteration(self):
        """Runs one iteration of the simulation.
        On each iteration, this function computes the neighbours for all the entities of the model. Then it calculates
        the average angle of movement and combines this with some noise to define the angle to steer at the next iteration.
        The angle is used to calculate the vectorial components of the velocity. The velocity is used together with the discretization
        time of the model to get the position of all the entities at the next iteration. Periodic boundary conditions are applied if entities
        happen to lie outside the model space. Finally, the attributes of each entity are updated according to the previous calculations.
        """

        for entity in self.entities:
            neighbours = entity.get_neighbours(
                entities=self.entities, model_dimensions=self.dimensions)
            angle_avg = entity.get_mean_angle(neighbours)
            next_angle = entity.get_next_angle(angle_avg)
            next_velocity = entity.get_next_velocity(next_angle)
            next_position = entity.get_next_position(next_velocity, self.dt_time)
            next_position = entity.relocate_entity(next_position, self.dimensions)
            entity.update_entity(next_angle, next_velocity, next_position)

    def save_iteration_data(self):
        """Arrange and save all entity positions and asteering angles for a given iteration.
        """
        x_entities = [x.position[0] for x in self.entities]
        y_entities = [y.position[1] for y in self.entities]
        angle_entities = [a.angle for a in self.entities]
        xya = np.vstack((x_entities, y_entities, angle_entities)).T
        self.iterations_data.append(xya)

    def run_simulation(self):
        """Run all iterations of the model run and save the data.
        """
        n_dts = int(self.time/self.dt_time)
        for dt in range(n_dts):
            self.run_iteration()
            self.save_iteration_data()

    def get_animation(self,entity_screen_size=25):
        Animation(self, entity_screen_size)
