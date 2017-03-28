import TSP_Model
import json

import numpy.random as random  # see numpy.random module


import matplotlib.pyplot as plt
import matplotlib.image as mpimg

"""Read input data and define helper functions for visualization."""

# Map services and data available from U.S. Geological Survey, National Geospatial Program.

map = mpimg.imread("map.png")  # US States & Capitals map

# List of 30 US state capitals and corresponding coordinates on the map
with open('capitals.json', 'r') as capitals_file:
    capitals = json.load(capitals_file)
capitals_list = list(capitals.items())


def show_path(path, starting_city, w=12, h=8, msg=""):
    """Plot a TSP Model path overlaid on a map of the US States & their capitals."""
    x, y = list(zip(*path))
    _, (x0, y0) = starting_city
    plt.imshow(map)
    plt.plot(x0, y0, 'y*', markersize=15)  # y* = yellow star for starting point
    plt.plot(x + x[:1], y + y[:1])  # include the starting point at the end of path
    plt.axis("off")
    fig = plt.gcf()
    fig.set_size_inches([w, h])
    fig.suptitle(msg)
    plt.show()


def simulated_annealing(problem):
    """The simulated annealing algorithm, a version of stochastic hill climbing
    where some downhill moves are allowed. Downhill moves are accepted readily
    early in the annealing schedule and then less often as time goes on.

    Parameters
    ----------
    problem : Problem
        An optimization problem, already initialized to a random starting state.


    Returns
    -------
    Problem
        An approximate solution state of the optimization problem

    """
    current= problem
    alpha = 0.99
    T = 1e4   # define a temperature

    while T > .00001:
        next_cities= random.choice(current.successors()).path
        new_cities= TSP_Model.TravelingSalesmanProblem(next_cities)
        if new_cities.get_value() > current.get_value():
            current = new_cities

        else:
            E0= new_cities.get_value() - current.get_value()
            probability = 2.71828**(E0/T)
            if probability > random.uniform(0, 1):
                current = new_cities
        if T==1e4:
             best_result= current
        if current.get_value() > best_result.get_value():
             best_result = current
        T= T*alpha

    return best_result



num_cities = 15 # enter the number of cities to be used for the problem
capitals_tsp = TSP_Model.TravelingSalesmanProblem(capitals_list[:num_cities])  # Construct an instance of the TravelingSalesmanProblem
starting_city = capitals_list[0]
print("Initial path value: {:.2f}".format(-capitals_tsp.get_value()))
print(capitals_list[:num_cities])  # The start/end point is indicated with a yellow star
show_path(capitals_tsp.coords, starting_city)
print(str(-1*capitals_tsp.get_value()) +  " Miles before optimization")
msg_string= str(-1*capitals_tsp.get_value()) +  " Miles before optimization"
result = simulated_annealing(capitals_tsp)
print("Final path length: {:.2f}".format(-result.get_value()))
print(result.path)
print(str(-1*result.get_value())+ " Miles after optimization")
msg_string= str(int(-1*result.get_value()))+ " Miles after optimization"
show_path(result.coords, starting_city, msg=msg_string)  #  plot results on the figure
