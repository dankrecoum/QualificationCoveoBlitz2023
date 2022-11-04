from typing import List
from game_message import Tick, Action, Spawn, Sail, Dock, Anchor, directions, Position
import numpy as np
import math


def next_path_to_port(tick, position):
    # if tick.currentLocation.row < position.row and tick.currentLocation.column < position.column:
    #     x = 1
    #     y = 1
    #     a = "SE"
    # if tick.currentLocation.row < position.row and tick.currentLocation.column > position.column:
    #     x = 1
    #     y = -1
    #     a = "NW"
    # if tick.currentLocation.row > position.row and tick.currentLocation.column > position.column:
    #     x = -1
    #     y = -1
    #     a = "NE"
    # if tick.currentLocation.row > position.row and tick.currentLocation.column < position.column:
    #     a = "SW"
    #     x = -1
    #     y = 1
    # if tick.currentLocation.row < position.row and tick.currentLocation.column == position.column:
    #     x = 1
    #     a = "E"
    # if tick.currentLocation.row > position.row and tick.currentLocation.column == position.column:
    #     x = -1
    #     a = "W"
    # if tick.currentLocation.row == position.row and tick.currentLocation.column > position.column:
    #     y = 1
    #     a = "N"
    # if tick.currentLocation.row == position.row and tick.currentLocation.column < position.column:
    #     y = -1
    #     a = "S"
    if tick.currentLocation.column > position.column:
        return "N"

    elif tick.currentLocation.column < position.column:
        return "S"

    if tick.currentLocation.row > position.row:
        return "W"
    elif tick.currentLocation.row < position.row:
        return "E"


class Bot:
    def __init__(self):
        self.graph = None
        self.ports = []
        print("Initializing your super mega duper bot")

    def get_next_move(self, tick: Tick) -> Action:
        """
        Here is where the magic happens, for now the move is random. I bet you can do better ;)
        """
        if tick.currentLocation is None:
            print(tick.tideSchedule)
            self.ports.append(tick.map.ports[0])
            return Spawn(tick.map.ports[0])
        # if tick.currentTick % len(tick.tideSchedule) == 0:
        #     self.graph = self.create_graph(tick)
        nearest_port = tick.map.ports[self.find_nearest_port(tick)]

        next_move = next_path_to_port(tick, nearest_port)
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

    def create_graph(self, tick: Tick) -> List[List[int]]:
        graph = np.array(tick.map.topology)
        for indexl, ligne in tick.map.topology:
            for indexc, colonne in ligne:
                distance = abs(tick.currentLocation.row - indexl) + abs(tick.currentLocation.column - indexc)
