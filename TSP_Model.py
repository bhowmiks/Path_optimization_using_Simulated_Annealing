import json
import copy
import math


class TravelingSalesmanProblem:
    """Representation of a traveling salesman optimization problem.  The goal
    is to find the shortest path that visits every city in a closed loop path.



    Parameters
    ----------
    cities : list
        A list of cities specified by a tuple containing the name and the x, y
        location of the city on a grid. e.g., ("Atlanta", (585.6, 376.8))

    Attributes
    ----------
    names
    coords
    path : list
        The current path between cities as specified by the order of the city
        tuples in the list.
    """

    def __init__(self, cities):
        self.path = copy.deepcopy(cities)

    def copy(self):
        """Return a copy of the current board state."""
        new_tsp = TravelingSalesmanProblem(self.path)
        return new_tsp

    @property
    def names(self):
        """Strip and return only the city name from each element of the
        path list. For example,
            [("Atlanta", (585.6, 376.8)), ...] -> ["Atlanta", ...]
        """
        names, _ = zip(*self.path)

        return names

    @property
    def coords(self):
        """Strip the city name from each element of the path list and return
        a list of tuples containing only pairs of xy coordinates for the
        cities. For example,
            [("Atlanta", (585.6, 376.8)), ...] -> [(585.6, 376.8), ...]
        """
        _, coords = zip(*self.path)
        return coords

    def successors(self):
        """Return a list of states in the neighborhood of the current state by
        switching the order in which any adjacent pair of cities is visited.

        For example, if the current list of cities (i.e., the path) is [A, B, C, D]
        then the neighbors will include [A, B, D, C], [A, C, B, D], [B, A, C, D],
        and [D, B, C, A]. (The order of successors does not matter.)

        """
        n = self.path.__len__() - 1
        tsp_list = []
        while n >= 0:
            f = self.path[n]
            g = self.path.copy()
            g[n] = self.path[n - 1]
            g[n - 1] = f
            newtsp=TravelingSalesmanProblem(g)
            tsp_list.append(newtsp)
            n -= 1

        return tsp_list

    def get_value(self):
        """Calculate the total length of the closed-circuit path of the current
        state by summing the distance between every pair of adjacent cities.

        Returns
        -------
        float
            A floating point value with the total cost of the path given by visiting
            the cities in the order according to the self.cities list ((Multiplying by -1 makes the smallest
        path the smallest negative number, which is the maximum value.)

        """

        total_distance = 0
        for n in range(self.path.__len__() - 1, -1, -1):
            distance = math.hypot(self.path[n][1][0] - self.path[n - 1][1][0], self.path[n][1][1] - self.path[n - 1][1][1])
            total_distance += distance
        return float(-1 * total_distance)

