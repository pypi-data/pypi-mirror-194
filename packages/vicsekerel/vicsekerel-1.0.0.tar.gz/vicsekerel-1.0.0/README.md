# **Vicsekerel**

Implemetation of the Vicsek model in Python. It allows users to edit the parameters dominating the dynamics of the system and to generate a video of the resulting simulation.

## **Project Description**

Details of the model can be found in the original paper published in 1995 under the title: "Novel Type of Phase Transition in a System of Self-Driven Particles". https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.75.1226

The system consists of moving agents that are initially located at random within a 2D space. The movement of agents is dictated by the average direction of other agents in their vicinity plus some noise. Depending on the parameter selection, agents can end up displaying different collective behaviour. For small densities and noise the system may well remind of schools of fish and other swarms.


## **Dependencies**

Download ffmpeg build and add path to the local environment variables of your machine. Details for this can be found in the following post: https://suryadayn.medium.com/error-requested-moviewriter-ffmpeg-not-available-easy-fix-9d1890a487d3


## **Installation** 

``` pip install vicsekerel ```

## **Import Library**

```import vicsekerel as vkl ```

## **Initialize Model**

Initialize model by providing values for its parameters.

 - **dimensions** (List): Size and width of the model space.
- **n_entities** (Int): Number of entities that will populate the model.
- **velocity_mod** (Float): Module of the entities' velocity
- **radius_perceived** (Float): Maximum distance looked at when defining neighbours.
- **noise** (Float): Parameter controlling the amount of turbulence in the entities' movement.
- **dt_time** (Int): Discretization time used in the simulation runs (in seconds).
- **time** (Int): Total simulation time (in seconds)

See an example below:

```my_model = vkl.Model(dimensions=[30, 30], n_entities=300, velocity_mod=4, radius_perceived=1, noise=0.4, dt_time=0.01, time=5) ```

## **Run simulation**

Run the simulation as follows:

```my_model.run_simulation()```

The coordinates and steering angles of all the entities on each of the iterations of the model run are stored in the object attribute "iterations_data". You can retrieve this data by simply typing "my_model.iterations_data" once the simulation has run.

## **Create Video**

The following line will produce a video of the simulation. Use the parameter "entity_screen_size" to define the markersize of the agents in the output video.

```my_model.get_animation(entity_screen_size=15)```

![alt text](snapshots_animation_examples.png "Title")

## **Note...**

The computational time increases rapidily as the number of entities is increased!