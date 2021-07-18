class Metro:
    def __init__(self):
        self.stations = []
        self.colors = []
        self.edges = dict()

    def add_station(self, station, color=None):
        if color not in (None, "red", "green"):
            raise ValueError(
                "Station color value incorrect "
                "(must be 'red', 'green', or None type)."
            )
        if not isinstance(station, str):
            raise TypeError("Station must be a string.")

        if station in self.stations:
            raise ValueError("Station already in the network")

        self.stations.append(station)
        self.colors.append(color)

    def add_edge(self, station_1, station_2):
        if station_1 not in self.stations:
            raise ValueError(f"Station {station_1} has not been added")
        if station_2 not in self.stations:
            raise ValueError(f"Station {station_2} has not been added")
        if station_1 not in self.edges:
            self.edges[station_1] = []
        self.edges[station_1].append(station_2)
        if station_2 not in self.edges:
            self.edges[station_2] = []
        self.edges[station_2].append(station_1)

    def solve_shortest_route(self, bus, origin, end):
        origin_index = self.stations.index(origin)
        end_index = self.stations.index(end)

        if (
            self.colors[origin_index] == "green"
            and self.colors[end_index] == "red"
        ) or (
            self.colors[origin_index] == "red"
            and self.colors[end_index] == "green"
        ):
            return (
                False,
                (
                    "origin and end stations of different"
                    f" color ({self.colors[origin_index]} "
                    f"& {self.colors[end_index]})"
                ),
                None,
            )
        if (
            bus
            and self.colors[origin_index]
            and bus != self.colors[origin_index]
        ):
            return (
                False,
                (
                    "the origin station and the bus has dif"
                    f"ferent colors ({self.colors[origin_index]} & {bus})"
                ),
                None,
            )
        if bus and self.colors[end_index] and bus != self.colors[end_index]:
            return (
                False,
                (
                    "the end station and the bus has dif"
                    f"ferent colors ({self.colors[end_index]} & {bus})"
                ),
                None,
            )

        if origin == end:
            return (True, [origin], 0)

        # Now we are ready to execute bfs
        N = len(self.stations)
        queue = []
        visited = [False for _ in range(N)]
        visited[self.stations.index(origin)] = True
        distance = [10000000 for _ in range(N)]
        distance[self.stations.index(origin)] = 0
        pred = [-1 for _ in range(N)]
        queue.append(origin)

        while len(queue):
            current_station = queue.pop(0)
            current_station_index = self.stations.index(current_station)
            for i in range(len(self.edges[current_station])):
                next_station_index = self.stations.index(
                    self.edges[current_station][i]
                )
                next_station = self.stations[next_station_index]

                if not visited[next_station_index]:
                    visited[next_station_index] = True
                    if (
                        self.colors[next_station_index] == "green"
                        and bus == "red"
                    ) or (
                        self.colors[next_station_index] == "red"
                        and bus == "green"
                    ):
                        distance[next_station_index] = distance[
                            current_station_index
                        ]
                        while (
                            distance[next_station_index]
                            < distance[current_station_index] + 1
                        ):
                            all_visited = True
                            for j in range(len(self.edges[next_station])):
                                subsequent_station_index = self.stations.index(
                                    self.edges[next_station][j]
                                )
                                if not visited[subsequent_station_index]:
                                    visited[subsequent_station_index] = True
                                    all_visited = False
                                    if (
                                        self.colors[subsequent_station_index]
                                        == "green"
                                        and bus == "red"
                                    ) or (
                                        self.colors[subsequent_station_index]
                                        == "red"
                                        and bus == "green"
                                    ):
                                        distance[
                                            subsequent_station_index
                                        ] = distance[next_station_index]
                                    else:
                                        distance[subsequent_station_index] = (
                                            distance[next_station_index] + 1
                                        )
                                    subsequent_station = self.stations[
                                        subsequent_station_index
                                    ]
                                    pred[
                                        subsequent_station_index
                                    ] = current_station
                                    queue.append(subsequent_station)
                                    if subsequent_station == end:
                                        path = []
                                        prev_station = end
                                        prev_station_index = (
                                            self.stations.index(end)
                                        )
                                        path.append(prev_station)
                                        path_built = False
                                        while not path_built:
                                            prev_station = pred[
                                                prev_station_index
                                            ]
                                            prev_station_index = (
                                                self.stations.index(
                                                    prev_station
                                                )
                                            )
                                            if (
                                                not self.colors[
                                                    prev_station_index
                                                ]
                                                or not bus
                                                or self.colors[
                                                    prev_station_index
                                                ]
                                                == bus
                                            ):
                                                path.append(prev_station)

                                            if origin == prev_station:
                                                path_built = True

                                        return (
                                            True,
                                            list(reversed(path)),
                                            len(path) - 1,
                                        )
                            if all_visited:
                                break

                    else:
                        distance[next_station_index] = (
                            distance[current_station_index]
                        ) + 1

                        pred[next_station_index] = current_station
                        queue.append(self.edges[current_station][i])

                    if self.edges[current_station][i] == end:
                        path = []
                        prev_station = end
                        prev_station_index = self.stations.index(end)
                        path.append(prev_station)

                        path_built = False

                        while not path_built:
                            prev_station = pred[prev_station_index]
                            prev_station_index = self.stations.index(
                                prev_station
                            )
                            if (
                                not self.colors[prev_station_index]
                                or not bus
                                or self.colors[prev_station_index] == bus
                            ):
                                path.append(prev_station)

                            if origin == prev_station:
                                path_built = True

                        return True, list(reversed(path)), len(path) - 1
        return False, "Network architecture", None
