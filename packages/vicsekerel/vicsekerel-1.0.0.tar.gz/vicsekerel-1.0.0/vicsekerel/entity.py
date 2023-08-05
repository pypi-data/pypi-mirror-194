

import numpy as np
import math


class Entity:
    def __init__(self, dimensions, velocity_mod, radius_perceived, noise):
        """Creates a new entity at a random location with a random steering direction.

        Args:
            dimensions (List): List containing the width and length of the model space.
            velocity_mod (Float): Module of the entity's velocity.
            radius_perceived (Float): Maximum radius looked at when defining neighbours.
            noise (Float): Parameter controlling the amount of turbulence in the entity's movement.
        """
        self.position = [dimensions[0]*np.random.rand(), dimensions[1]*np.random.rand()]
        self.velocity_mod = velocity_mod
        self.angle = 2*math.pi*np.random.rand()
        self.velocity = [self.velocity_mod*math.cos(self.angle), self.velocity_mod*math.sin(self.angle)]
        self.radius_perceived = radius_perceived
        self.noise=noise

    def get_distance(self, entity, model_dimensions):
        """Computes and returns the distance between the entity self and another entity passed as parameter.

        Args:
            entity (Object): object of the class Entity
            model_dimensions (List): Dimensions of the model space

        Returns:
            Float: Distance between the two entities.
        """
        effective_position_entity = self.get_effective_position(entity, model_dimensions)
        distance = math.sqrt(((effective_position_entity[0] - self.position[0])**2) + (
            (effective_position_entity[1] - self.position[1])**2))
        return distance

    def get_effective_position(self, entity, model_dimensions):
        """Calculates the actual spatial coordinates of entity self from another entity's viewpoint, passed as parameter.
        Given the periodic boundary conditions, entities on opposite sides of the model space appear distant, when they
        are actually very close. This function returns the actual position of self in those situations.

        Args:
            entity (Object): object of the class Entity
            model_dimensions (List): Dimensions of the model space

        Returns:
            List: List containing the actual spatial coordinates of entity self
        """
        effective_position_entity = [0, 0]
        for xy in range(0, len(effective_position_entity)):
            if self.position[xy] < self.radius_perceived and entity.position[xy] > model_dimensions[xy]-self.radius_perceived:
                effective_position_entity[xy] = entity.position[xy] - \
                    model_dimensions[xy]
            elif self.position[xy] > model_dimensions[xy]-self.radius_perceived and entity.position[xy] < self.radius_perceived:
                effective_position_entity[xy] = entity.position[xy] + \
                    model_dimensions[xy]
            else:
                effective_position_entity[xy] = entity.position[xy]
        return effective_position_entity

    def get_neighbours(self, entities, model_dimensions):
        """Identifies and returns the entities that are considered neighbours of the entity self. Only entities in the proximity of self that lile within a radius given
        by self.radius_perceived are considered neighbours.


        Args:
            entities (List): List of objects of the class Entity.
            model_dimensions (List): Dimensions of the model space

        Returns:
            List: List containing entities that are considered neighbours of self.
        """
        neighbour_entities = []
        for entity in entities:
            distance = self.get_distance(entity, model_dimensions)
            if distance < self.radius_perceived:
                neighbour_entities.append(entity)
            else:
                pass
        return neighbour_entities

    def get_mean_angle(self, neighbours):
        """ Computes and returns the average direction of movement of the neighbours of self, including itself.  

        Args:
            neighbours (List): List of entities considered neighbours of self.

        Returns:
            Float: Mean angle in radians.
        """
        sin_angle_sum = math.sin(self.angle)
        cos_angle_sum = math.cos(self.angle)
        n_neighbours = len(neighbours)
        if n_neighbours == 0:
            mean_sin_angle = sin_angle_sum
            mean_cos_angle = cos_angle_sum
        else:
            for neighbour in neighbours:
                sin_angle_sum = sin_angle_sum + math.sin(neighbour.angle)
                cos_angle_sum = cos_angle_sum + math.cos(neighbour.angle)
            mean_sin_angle = sin_angle_sum/n_neighbours
            mean_cos_angle = cos_angle_sum/n_neighbours
        angle_avg = self.get_angle_from_components(mean_sin_angle, mean_cos_angle)
        return angle_avg
        
    def get_angle_from_components(self, sin_angle, cos_angle):
        """ 
        get_angle_from_components returns an angle (in radians) from the values of its sine (pam:sin_angle) and cosine (pam:cos_angle).
        """
        angle = math.atan(sin_angle/cos_angle)
        if cos_angle<0 and sin_angle>=0:
            angle=angle+ math.pi
        elif cos_angle<0 and sin_angle<0:
            angle=angle - math.pi
        elif cos_angle==0 and sin_angle>0:
            angle=math.pi/2
        elif cos_angle==0 and sin_angle<0:
            angle=-math.pi/2  
        return angle

    def get_next_angle(self, angle_avg):
        """ Returns the next direction of movement of self. This is computed as a linear combination of the average angle of motion of the neighbours in 
        the previous iteration and a noise term accounting for fluctuations.  

        Args:
            angle_avg (Float): Average direction of neighbours in previous iteration.
            noise (Float): Limit for distribution range of a noise term affecting the direction of movement. 

        Returns:
            Float: Angle in radians.
        """
        random_noise = np.random.uniform(-self.noise/2, self.noise/2)
        next_angle = angle_avg + random_noise
        return next_angle

    def get_next_velocity(self, next_angle):
        """ Returns the vectorial components of the velocity of self on the next iteration. 

        Args:
            next_angle (Float): Direction of movement of self on the next iteration.

        Returns:
            List: Components of the velocity in the x and y directions.
        """
        next_velocity = [
            self.velocity_mod*math.cos(next_angle), self.velocity_mod*math.sin(next_angle)]
        return next_velocity

    def relocate_entity(self, next_position, model_dimensions):
        """ Returns the position of self after applying spatial transformations due to periodic boundary conditions at the borders of the model space. 
        When the next position of self is outside the confinements of the model, this function can restore them to the available area.


        Args:
            next_position (List): Spatial coordinates of self at the next iteration. 
            model_dimensions (List): Dimensions of the model space

        Returns:
            List: Spatial coordinates of self after applying periodic boundary conditions.
        """
        for xy in range(0, 2):
            if next_position[xy] < 0:
                next_position[xy] = model_dimensions[xy] + \
                    next_position[xy]
            if next_position[xy] > model_dimensions[xy]:
                next_position[xy] = - \
                    model_dimensions[xy] + next_position[xy]
        return next_position

    def get_next_position(self, next_velocity, model_dt_time):
        """Returns the next spatial coordinates of self at the next iteration given its velocity and the model discretization time.

        Args:
            next_velocity (List): Vectorial components of the velocity at the next iteration.
            model_dt_time (Float): Discretization time defining the interval between consecutive iterations

        Returns:
            List: Spatial coordinates of self at the next iteration.
        """
        next_position_x = self.position[0] + next_velocity[0]*model_dt_time
        next_position_y = self.position[1] + next_velocity[1]*model_dt_time
        next_position = [next_position_x, next_position_y]
        return next_position

    def update_entity(self, next_angle, next_velocity, next_position):
        """Updates the attributes of self: angle, velocity and position.


        Args:
            next_angle (Float): Angle of motion at the next iteration.
            next_velocity (List): Vectorial components of the velocity at the next iteration.
            next_position (List): Spatial coordinates of self at the next iteration.
        """
        self.angle = next_angle
        self.velocity = next_velocity
        self.position = next_position
