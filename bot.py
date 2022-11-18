import random
from math import sqrt

from game_message import Tick, Action, Spawn, Sail, directions, Position, Dock


class Bot:
    # port_to_visit_index = 0
    not_visited_ports = []
    port_1 = {"row": 0, "column": 0}

    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, tick: Tick) -> Action:
        """
        Here is where the magic happens, for now the move is random. I bet you can do better ;)
        """
        if tick.currentLocation is None:
            self.not_visited_ports = list(tick.map.ports)
            print(f"assigning value to array of not visited ports : {self.not_visited_ports}")
            # self.not_visited_ports.remove(self.not_visited_ports[0])
            return Spawn(tick.map.ports[0])

        # if tick.totalTicks == 2:
        #     self.port_1 = self.get_port_1(tick)
        #     print(f"PORT_1 :{self.port_1}")
        #     return Dock()

        print(f"presentement à la position: {tick.currentLocation}")
        # get nearest port TODO
        # solution temporaire: iterer dans l'array des ports
        # next_port = self.port_to_visit_index % len(tick.map.ports)
        next_port = self.get_nearest_port(tick)
        print(f"going to port: {next_port}")
        nearest_port: Position = next_port

        # go to nearest port
        return self.go_to_port(tick, nearest_port)
        # return Sail(directions[tick.currentTick % len(directions)])

    def get_distance(self, tick, port: Position):
        return sqrt((tick.currentLocation.row - port.row) ** 2 + (tick.currentLocation.column - port.column) ** 2)

    def get_port_1(self, tick: Tick):
        ports_list_copy = list(tick.map.ports)
        ports_list_copy.remove(ports_list_copy[0])
        port_1 = ports_list_copy[0]
        nearest = 100000000000000
        for port in ports_list_copy:
            distance_to_port = sqrt(
                (tick.spawnLocation.row - port.row) ** 2 + (tick.spawnLocation.column - port.column) ** 2)
            if distance_to_port <= nearest:
                port_1 = port
        return port_1

    def get_nearest_port(self, tick: Tick):
        port_1 = self.get_port_1(tick)
        print(f"PORT_1 IS : {port_1}")
        port_to_be_visited = tick.map.ports[0]
        nearest = 100000000000000
        for port in self.not_visited_ports:
            distance_to_port = self.get_distance(tick, port)
            if distance_to_port <= nearest:
                port_to_be_visited = port
                nearest = distance_to_port
        if (tick.currentLocation.row == port_to_be_visited.row) and (
                tick.currentLocation.column == port_to_be_visited.column):
            print(f"List of all non visited ports :{self.not_visited_ports}")
            print(f"going to remove : {port_to_be_visited}")
            if len(self.not_visited_ports) > 0:
                self.not_visited_ports.remove(port_to_be_visited)
            # elif (tick.currentLocation.row == port_to_be_visited.row) and (
            #         tick.currentLocation.column == port_to_be_visited.column):
            #     return self.port_1
        return port_to_be_visited

    def is_direction_available(self, tick, direction):
        if direction == "N":
            return tick.map.topology[tick.currentLocation.row - 1][tick.currentLocation.column] <= \
                   tick.tideSchedule[1]
        elif direction == "NE":
            return tick.map.topology[tick.currentLocation.row - 1][tick.currentLocation.column + 1] <= \
                   tick.tideSchedule[1]
        elif direction == "E":
            return tick.map.topology[tick.currentLocation.row][tick.currentLocation.column + 1] <= \
                   tick.tideSchedule[1]
        elif direction == "SE":
            return tick.map.topology[tick.currentLocation.row + 1][tick.currentLocation.column + 1] <= \
                   tick.tideSchedule[1]
        elif direction == "SE":
            return tick.map.topology[tick.currentLocation.row + 1][tick.currentLocation.column] <= \
                   tick.tideSchedule[1]
        elif direction == "SW":
            return tick.map.topology[tick.currentLocation.row + 1][tick.currentLocation.column - 1] <= \
                   tick.tideSchedule[1]
        elif direction == "W":
            return tick.map.topology[tick.currentLocation.row][tick.currentLocation.column - 1] <= \
                   tick.tideSchedule[1]
        else:  # NW
            return tick.map.topology[tick.currentLocation.row - 1][tick.currentLocation.column - 1] <= \
                   tick.tideSchedule[1]

    # def get_alternative_direction(self, tick: Tick, direction) -> Action:
    #     match direction:
    #         case "SE":
    #             alternative_directions = ["S", "E", "SW", "NE"]

    def go_to_port(self, tick: Tick, destination: Position) -> Action:
        if tick.currentLocation.row < destination.row:
            if tick.currentLocation.column < destination.column:
                if self.is_direction_available(tick, directions[3]):
                    return Sail(directions[3])  # SE
                return Sail(random.choice(directions))
            elif tick.currentLocation.column == destination.column:
                if self.is_direction_available(tick, directions[4]):
                    return Sail(directions[4])  # S
                return Sail(random.choice(directions))
            else:
                if self.is_direction_available(tick, directions[5]):
                    return Sail(directions[5])  # SW
                return Sail(random.choice(directions))
        elif tick.currentLocation.row == destination.row:
            if tick.currentLocation.column < destination.column:
                if self.is_direction_available(tick, directions[2]):
                    return Sail(directions[2])  # E
                return Sail(random.choice(directions))
            elif tick.currentLocation.column == destination.column:
                print(f"liste des ports visités: {tick.visitedPortIndices}")
                # self.port_to_visit_index += 1
                return Dock()  # Dock !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            else:
                if self.is_direction_available(tick, directions[6]):
                    return Sail(directions[6])  # W
                return Sail(random.choice(directions))
        else:
            if tick.currentLocation.column < destination.column:
                if self.is_direction_available(tick, directions[1]):
                    return Sail(directions[1])  # NE
                return Sail(random.choice(directions))
            elif tick.currentLocation.column == destination.column:
                if self.is_direction_available(tick, directions[0]):
                    return Sail(directions[0])  # N
                return Sail(random.choice(directions))
            else:
                if self.is_direction_available(tick, directions[7]):
                    return Sail(directions[7])  # NW
                return Sail(random.choice(directions))
