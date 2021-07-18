#!/bin/bash

for station_a in {A..V}
do  
    for station_b in {A..V}
    do
        echo "Running main.py with metro.json between station $station_a and $station_b with bus of no color..."
        python ../main.py ../json/metro.json "$station_a" "$station_b"
        echo " "
        echo "Running main.py with metro.json between station $station_a and $station_b with bus of color red..."
        python ../main.py ../json/metro.json "$station_a" "$station_b" red
        echo " "
        echo "Running main.py with metro.json between station $station_a and $station_b with bus of color red..."
        python ../main.py ../json/metro.json "$station_a" "$station_b" green
        echo " "
    done
done