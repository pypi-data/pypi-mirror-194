
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
from matplotlib.animation import FuncAnimation, writers
from IPython import display
import colorsys
import os
import numpy as np


class Animation:
    def __init__(self, model, entity_screen_size):
        """Initializes animation. 
        Input the results of the model run, define the speed rate of the animation and the output movie file name.

        Args:
            model (Object): Object of the class Model
            entity_screen_size (Int): Markersize of entities in the animation.
        """
        self.model = model
        self.ms_frame = model.dt_time*1000 # Delay between frames of the animation in miliseconds
        self.entity_screen_size=entity_screen_size
        self.video_name = "Vicsek_"+str(self.model.dimensions[0])+"X"+str(self.model.dimensions[1])+"_entities"+str(
            self.model.n_entities)+"_velocity"+str(self.model.velocity_mod)+"_radius-perceived"+str(self.model.radius_perceived)+"_noise" +str(self.model.noise)+"_entity-screen-size"+str(self.entity_screen_size)+"_dt"+str(self.model.dt_time)+"_time"+str(self.model.time)+".mp4"
        self.get_animation()

    def get_animation(self):
        """Generate animation and save in movie file
        """
        fig = plt.figure(figsize=(16, 16), dpi=1920/16)
        fig.patch.set_facecolor('xkcd:black')
        axis = plt.axes(xlim=(0, self.model.dimensions[0]), ylim=(
            0, self.model.dimensions[1]))

        def animate(frame_number):
            fig.clear()
            axis = plt.axes(xlim=(0, self.model.dimensions[0]), ylim=(
                0, self.model.dimensions[1]))
            xy = self.model.iterations_data[frame_number]
            for i in xy:
                plt.plot(i[0], i[1], marker=self.get_arrow(i[2]), ms=self.entity_screen_size, c=self.get_colour_rgba(i[2]))
        anim = FuncAnimation(fig, animate, frames=len(np.arange(
            0, self.model.time, self.model.dt_time)), interval=self.ms_frame, blit=False)
        filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),  self.video_name)
        anim.save(filepath)

    def get_arrow(self, angle):
        """Define shape of entities in the model space.
         The geometry of each entity is a triangle pointing in the direction of movement.

        Args:
            angle (Float): Steering direction of entity in a given iteration.

        Returns:
            List: Vectorial representation of the entity's shape.
        """
        a = angle + (3*np.pi/2)
        ar = np.array([[-.25, -.5], [.25, -.5], [0, .5], [-.25, -.5]]).T
        rot = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
        return np.dot(rot, ar).T

    def get_colour_rgba(self, angle):
        """Returns an rgba colour code based on the steering angle of the entity. 

        Args:
            angle (Float): Steering direction of entity in a given iteration.

        Returns:
            List: RGB components.
        """
        if angle < 0:
            angle = angle + (2*np.pi)
        angle = angle/8
        col = colorsys.hsv_to_rgb(angle, 1, 1)
        colors = [col[0], col[1], col[2], 1]
        return colors
