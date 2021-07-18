import pytest
from metro import Metro


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
        assert new_color == None

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
            "Station color value incorrect (must be 'red', 'green', or None type)."
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
    pass