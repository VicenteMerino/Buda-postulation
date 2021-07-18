from sys import argv
import os
import json
from metro.metro import Metro

if __name__ == "__main__":
    if len(argv) < 4 or len(argv) > 5:
        raise Exception(
            (
                "The format to use the program is: "
                "python main.py <network_file> <origin_station> "
                "<end_station> <bus (optional)>"
            )
        )
    network_file = argv[1]
    origin_station = argv[2]
    end_station = argv[3]
    bus = argv[4] if len(argv) > 4 else None
    if bus not in ("red", "green", None):
        raise ValueError(
            "Bus color value incorrect (must be 'red', 'green', or None type)."
        )
    if not os.path.exists(network_file):
        raise Exception(f"Path {network_file} don't exist.")

    with open(network_file) as file:
        network_json = json.load(file)

    stations = network_json["stations"]
    edges = network_json["edges"]

    metro = Metro()

    for station in stations:
        station_name = station[0]
        station_color = station[1]
        metro.add_station(station_name, station_color)

    for edge in edges:
        station_1 = edge[0]
        station_2 = edge[1]
        metro.add_edge(station_1, station_2)

    if origin_station not in metro.stations:
        raise ValueError(
            (
                f"Station {origin_station} is not on "
                f"the network specified in {network_file}"
            )
        )

    if end_station not in metro.stations:
        raise ValueError(
            (
                f"Station {end_station} is not on "
                f"the network specified in {network_file}"
            )
        )

    (are_connected, path, path_length) = metro.solve_shortest_route(
        bus, origin_station, end_station
    )

    if are_connected:
        print(
            "The shortest path is:\n"
            f"{'->'.join(path)}\nWith length: {path_length}"
        )
    else:
        print(f"The nodes are not connected because of: '{path}'")
