from math import sqrt

from game_message import Tick, Action, Spawn, Sail, directions, Position, Dock


class Bot:
    port_to_visit_index = 0
    not_visited_ports = []

    def __init__(self):
        print("Initializing your super mega duper bot")

    def get_next_move(self, tick: Tick) -> Action:
        """
        Here is where the magic happens, for now the move is random. I bet you can do better ;)
        """
        if tick.currentLocation is None:
            self.not_visited_ports = list(tick.map.ports)
            print(f"assigning value to array of not visited ports : {self.not_visited_ports}")
            self.not_visited_ports.remove(self.not_visited_ports[0])
            return Spawn(tick.map.ports[0])

        if tick.totalTicks == 2:
            return Dock()

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

    def get_distance(self, tick: Tick, port: Position):
        return sqrt((tick.currentLocation.row - port.row) ** 2 + (tick.currentLocation.column - port.column) ** 2)

    def get_nearest_port(self, tick: Tick):
        port_to_be_visited = tick.map.ports[0]
        nearest = 100000000000000
        for port in self.not_visited_ports:
            distance_to_port = self.get_distance(tick, port)
            if distance_to_port <= nearest:
                port_to_be_visited = port
                nearest = distance_to_port
        if (tick.currentLocation.row == port_to_be_visited.row) and (tick.currentLocation.column == port_to_be_visited.column):
            print(f"going to remove : {port_to_be_visited}")
            self.not_visited_ports.remove(port_to_be_visited)
        return port_to_be_visited

    def get_alternative_direction(self, direction):
        return

    def go_to_port(self, tick: Tick, destination: Position) -> Action:
        if tick.currentLocation.row < destination.row:
            if tick.currentLocation.column < destination.column:
                return Sail(directions[3])  # SE
            elif tick.currentLocation.column == destination.column:
                return Sail(directions[4])  # S
            else:
                return Sail(directions[5])  # SW
        elif tick.currentLocation.row == destination.row:
            if tick.currentLocation.column < destination.column:
                return Sail(directions[2])  # E
            elif tick.currentLocation.column == destination.column:
                print(f"liste des ports visités: {tick.visitedPortIndices}")
                self.port_to_visit_index += 1
                return Dock()  # Dock !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            else:
                return Sail(directions[6])  # W
        else:
            if tick.currentLocation.column < destination.column:
                return Sail(directions[1])  # NE
            elif tick.currentLocation.column == destination.column:
                return Sail(directions[0])  # N
            else:
                return Sail(directions[7])  # NW


