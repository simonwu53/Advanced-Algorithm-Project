import heapq
from Queue import PriorityQueue
from heapq import *
from math import sqrt
import time

from ui.world import Point

class MyPriorityQueue(PriorityQueue):
    def _put(self, item):
        return super._put((self._get_priority(item), item))

    def _get(self):
        return super._get()[1]

    def _get_priority(self, item):
        return item[1]


class Astar:
    def __init__(self, map, x, y, start, goal):
        self.map = map
        self.x = x
        self.y = y
        self.start = start
        self.goal = goal
        self.restrict_area = self.map.world.restrict_area()  # to speed up the algorithm, calculate restrict area first
                                                             # function not completed yet
                                                             # change neighbor to use this area

    def get_neighbors(self, node):
        coords = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (-1, -1), (1, 1), (-1, 1), (1, -1)]
        neighbors = []

        for item in coords:
            x = node[0] + item[0]
            y = node[1] + item[1]

            if self.map.world.is_allowed(x, y):
                if 0 < x < self.x and 0 < y < self.y:
                    neighbors.append((x, y))

        return neighbors

    def get_distance(self, from_node, to_node):
        return sqrt((from_node[0] - to_node[0]) ** 2 + (from_node[1] - to_node[1]) ** 2)

    def build_path(self, goal, came_from, cost_so_far):
        current = goal
        path = []

        while current in came_from:
            path.append(current)
            current = came_from[current]

        return path

    def a_star(self):
        closed_set = set()
        closed_set_copy = []  # for plotting process, only new nodes will be plotted to make it faster
        open_set = PriorityQueue()
        open_set_copy = []  # for plotting process, the same as above
        came_from = {}
        cost_so_far = {}

        open_set.put((0, self.start))

        came_from[self.start] = None
        cost_so_far[self.start] = 0
        i = 0
        while not open_set.empty():
            current = open_set.get()[1]
            closed_set.add(current)
            closed_set_copy.append(current)

            i += 1
            #later refcator this to some drawing method
            if i % 5000 == 0:
                """uncomment if want to plot both sets"""
                # for node in open_set_copy:
                #     self.map.visualize_process(node, 'open')
                for node in closed_set_copy:
                    self.map.visualize_process(node, 'closed')
                closed_set_copy = []
                open_set_copy = []

            if current == self.goal:
                break

            for neighbor in self.get_neighbors(current):
                if neighbor in closed_set:
                    continue

                new_cost = cost_so_far[current] + self.get_distance(current, neighbor)

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heuristic_cost = self.get_distance(self.goal, neighbor)

                    priority = new_cost + heuristic_cost
                    open_set.put((priority, neighbor))
                    open_set_copy.append(neighbor)
                    came_from[neighbor] = current

        return came_from, cost_so_far


class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
