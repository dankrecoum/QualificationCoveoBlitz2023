from typing import List, Tuple

import tcod.path

from game_message import Tick, Action, Spawn, Sail, Dock, Anchor, directions, Position
import numpy as np
import math


def next_path_to_port(tick, position: Tuple):

    if tick.currentLocation.column > position[0]:
        return "N"

    elif tick.currentLocation.column < position[0]:
        return "S"

    if tick.currentLocation.row > position[1]:
        return "W"
    elif tick.currentLocation.row < position[1]:
        return "E"


def create_graph(tick: Tick):
    graph = np.array(tick.map.topology)
    for indexl, ligne in tick.map.topology:
        for indexc, colonne in ligne:
            distance = abs(tick.currentLocation.row - indexl) + abs(tick.currentLocation.column - indexc)
            if tick.tideSchedule[distance % len(tick.tideSchedule)] > colonne:
                graph[indexl][indexc] = 1
            else:
                graph[indexl][indexc] = 0
    return graph.tolist()


class Bot:
    def __init__(self):
        self.graph = None
        self.ports = []
        self.path = None
        print("Initializing your super mega duper bot")

    def get_next_move(self, tick: Tick) -> Action:
        """
        Here is where the magic happens, for now the move is random. I bet you can do better ;)
        """
        if tick.currentLocation is None:
            print(tick.tideSchedule)
            self.ports.append(tick.map.ports[0])
            return Spawn(tick.map.ports[0])

        """
        vérifier si on a atteint le port puis recréer le graph et le chemin
        """
        self.graph = tcod.path.AStar(create_graph(tick), 0)
        nearest_port = tick.map.ports[self.find_nearest_port(tick)]
        self.path = self.graph.get_path(tick.currentLocation.row, tick.currentLocation.column, nearest_port.row,
                                        nearest_port.column)
        next_move = next_path_to_port(tick, self.path[0])
        self.path = self.path[1:]

        if tick.currentLocation.row == nearest_port.row and tick.currentLocation.column == nearest_port.column:
            self.ports.append(nearest_port)
            return Dock()
        return Sail(next_move)

    def find_nearest_port(self, tick) -> int:
        min_distance = math.inf
        index_port = 0
        for port in tick.map.ports:
            if not self.is_in_ports(port.row, port.column):
                distance = abs(tick.currentLocation.row - port.row) + abs(tick.currentLocation.column - port.column)
                if distance < min_distance:
                    min_distance = distance
                    index_port = tick.map.ports.index(port)
        return index_port

    def is_in_ports(self, row, column):
        for port in self.ports:
            if port.row == row and port.column == column:
                return True
        return False
