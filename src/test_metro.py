import json
import pytest
from metro.metro import Metro


class TestStationAddition:
    @pytest.mark.parametrize(
        "station,color",
        [
            ("A", "green"),
            ("Baquedano", "red"),
            ("Irarrázaval", None),
        ],
    )
    def test_simple_addition(self, station, color):
        metro = Metro()
        initial_stations_count = len(metro.stations)
        initial_colors_count = len(metro.colors)
        metro.add_station(station, color)
        new_station = metro.stations[0]
        new_color = metro.colors[0]
        assert len(metro.stations) == initial_stations_count + 1
        assert len(metro.colors) == initial_colors_count + 1
        assert new_station == station
        assert new_color == color

    @pytest.mark.parametrize(
        "station",
        [
            ("Santa Isabel"),
        ],
    )
    def test_hidden_color_addition(self, station):
        metro = Metro()
        initial_stations_count = len(metro.stations)
        initial_colors_count = len(metro.colors)
        metro.add_station(station)
        new_station = metro.stations[0]
        new_color = metro.colors[0]
        assert len(metro.stations) == initial_stations_count + 1
        assert len(metro.colors) == initial_colors_count + 1
        assert new_station == station
        assert new_color is None

    @pytest.mark.parametrize(
        "station,color",
        [
            ("San Pablo", "blue"),
            ("La Moneda", 43),
            ("Franklin", {}),
        ],
    )
    def test_color_exception(self, station, color):
        metro = Metro()
        with pytest.raises(ValueError) as exc:
            metro.add_station(station, color)
        assert (
            "Station color value incorrect (must"
            " be 'red', 'green', or None type)."
        ) == str(exc.value)

    @pytest.mark.parametrize(
        "station,color",
        [
            ({}, "green"),
            (52454, "red"),
            (None, None),
        ],
    )
    def test_station_type_exception(self, station, color):
        metro = Metro()
        with pytest.raises(TypeError) as exc:
            metro.add_station(station, color)
        assert "Station must be a string." == str(exc.value)

    @pytest.mark.parametrize(
        "station,color",
        [
            ("A", "green"),
            ("Baquedano", "red"),
            ("Irarrázaval", None),
        ],
    )
    def test_repeated_station_addition(self, station, color):
        metro = Metro()
        metro.add_station(station, color)
        with pytest.raises(ValueError) as exc:
            metro.add_station(station, color)
        assert "Station already in the network" == str(exc.value)


class TestEdgeAddition:
    @pytest.mark.parametrize(
        "station_1, station_2",
        [
            ("Escuela Militar", "Los Dominicos"),
            ("Simón Bolívar", "Plaza Egaña"),
        ],
    )
    def test_add_edge(self, station_1, station_2):
        metro = Metro()
        metro.add_station(station_1)
        metro.add_station(station_2)
        metro.add_edge(station_1, station_2)
        assert station_1 in metro.edges[station_2]
        assert station_2 in metro.edges[station_1]

    @pytest.mark.parametrize(
        "station_1,station_2",
        [
            ("A", "B"),
            ("Los Leones", "Tobalaba"),
            ("Ñuñoa", "Chile España"),
        ],
    )
    def test_unexistance_of_station(self, station_1, station_2):
        metro = Metro()
        metro.add_station(station_1)
        with pytest.raises(ValueError) as exc:
            metro.add_edge(station_1, station_2)
        assert f"Station {station_2} has not been added" == str(exc.value)


class TestShortestRouteSolver:
    @pytest.mark.parametrize(
        "network_file,origin,end,bus,expected_path",
        [
            (
                "json/metro_buda.json",
                "A",
                "F",
                None,
                ["A", "B", "C", "D", "E", "F"],
            ),
            (
                "json/metro_buda.json",
                "A",
                "F",
                "green",
                ["A", "B", "C", "D", "E", "F"],
            ),
            (
                "json/metro_buda.json",
                "A",
                "F",
                "red",
                ["A", "B", "C", "H", "F"],
            ),
            (
                "json/metro.json",
                "U",
                "G",
                "red",
                ["U", "T", "M", "O", "E", "G"],
            ),
            (
                "json/metro.json",
                "U",
                "G",
                "green",
                ["U", "V", "Q", "M", "N", "O", "F", "G"],
            ),
            (
                "json/metro.json",
                "U",
                "G",
                None,
                ["U", "V", "T", "Q", "M", "B", "C", "I", "H", "G"],
            ),
        ],
    )
    def test_expected_shortest_route(
        self, network_file, origin, end, bus, expected_path
    ):
        metro = Metro()
        with open(network_file) as file:
            network_json = json.load(file)
        stations = network_json["stations"]
        edges = network_json["edges"]

        for station in stations:
            station_name = station[0]
            station_color = station[1]
            metro.add_station(station_name, station_color)

        for edge in edges:
            station_1 = edge[0]
            station_2 = edge[1]
            metro.add_edge(station_1, station_2)

        (are_connected, path, path_length) = metro.solve_shortest_route(
            bus, origin, end
        )

        assert are_connected
        assert path == expected_path
        assert path_length == len(path) - 1

    @pytest.mark.parametrize(
        "network_file,origin,end,bus",
        [
            ("json/metro_buda.json", "G", "H", None),
            ("json/metro.json", "T", "F", "green"),
            ("json/metro.json", "Q", "T", "red"),
        ],
    )
    def test_different_stations_color(self, network_file, origin, end, bus):
        metro = Metro()
        with open(network_file) as file:
            network_json = json.load(file)
        stations = network_json["stations"]
        edges = network_json["edges"]

        for station in stations:
            station_name = station[0]
            station_color = station[1]
            metro.add_station(station_name, station_color)

        for edge in edges:
            station_1 = edge[0]
            station_2 = edge[1]
            metro.add_edge(station_1, station_2)

        (are_connected, path, path_length) = metro.solve_shortest_route(
            bus, origin, end
        )
        origin_index = metro.stations.index(origin)
        end_index = metro.stations.index(end)
        assert not are_connected
        assert (
            path == "origin and end stations of different color "
            f"({metro.colors[origin_index]} & {metro.colors[end_index]})"
        )
        assert path_length is None

    @pytest.mark.parametrize(
        "network_file,origin,end,bus",
        [
            ("json/metro_buda.json", "G", "A", "red"),
            ("json/metro.json", "F", "B", "red"),
            ("json/metro.json", "T", "U", "green"),
        ],
    )
    def test_different_origin_station_bus_color(
        self, network_file, origin, end, bus
    ):
        metro = Metro()
        with open(network_file) as file:
            network_json = json.load(file)
        stations = network_json["stations"]
        edges = network_json["edges"]

        for station in stations:
            station_name = station[0]
            station_color = station[1]
            metro.add_station(station_name, station_color)

        for edge in edges:
            station_1 = edge[0]
            station_2 = edge[1]
            metro.add_edge(station_1, station_2)

        (are_connected, path, path_length) = metro.solve_shortest_route(
            bus, origin, end
        )
        origin_index = metro.stations.index(origin)
        assert not are_connected
        assert (
            path == "the origin station and the bus "
            f"has different colors ({metro.colors[origin_index]} & {bus})"
        )
        assert path_length is None

    @pytest.mark.parametrize(
        "network_file,origin,end,bus",
        [
            ("json/metro_buda.json", "A", "G", "red"),
            ("json/metro.json", "B", "F", "red"),
            ("json/metro.json", "U", "T", "green"),
        ],
    )
    def test_different_end_station_bus_color(
        self, network_file, origin, end, bus
    ):
        metro = Metro()
        with open(network_file) as file:
            network_json = json.load(file)
        stations = network_json["stations"]
        edges = network_json["edges"]

        for station in stations:
            station_name = station[0]
            station_color = station[1]
            metro.add_station(station_name, station_color)

        for edge in edges:
            station_1 = edge[0]
            station_2 = edge[1]
            metro.add_edge(station_1, station_2)

        (are_connected, path, path_length) = metro.solve_shortest_route(
            bus, origin, end
        )
        end_index = metro.stations.index(end)
        assert not are_connected
        assert (
            path == "the end station and the bus"
            f" has different colors ({metro.colors[end_index]} & {bus})"
        )
        assert path_length is None

    @pytest.mark.parametrize(
        "network_file,origin,end,bus",
        [
            ("json/metro_buda.json", "A", "Z", "red"),
            ("json/metro.json", "B", "Z", "red"),
            ("json/metro.json", "U", "Z", "green"),
        ],
    )
    def test_unconnected_stations(self, network_file, origin, end, bus):
        metro = Metro()
        with open(network_file) as file:
            network_json = json.load(file)
        stations = network_json["stations"]
        edges = network_json["edges"]

        for station in stations:
            station_name = station[0]
            station_color = station[1]
            metro.add_station(station_name, station_color)

        for edge in edges:
            station_1 = edge[0]
            station_2 = edge[1]
            metro.add_edge(station_1, station_2)

        metro.add_station(end)

        (are_connected, path, path_length) = metro.solve_shortest_route(
            bus, origin, end
        )
        assert not are_connected
        assert path == "Network architecture"
        assert path_length is None
