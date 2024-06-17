from datetime import datetime
import time

from algorithms.a_star import a_star_time, a_star_lines
from algorithms.dijkstra import dijkstra_search, reconstruct_path
from data.data_manager import dijkstra_fill_graph, read_connections, validate_test_data, a_star_fill_graph
from data.tests import my_data

if __name__ == '__main__':

    print("Wczytywanie grafu...")
    start = time.time()

    path = "connection_graph.csv"
    df = read_connections(path)

    graph = dijkstra_fill_graph(df)

    end = time.time()
    print(f"Czas wczytania grafu: {round(end - start, 2)}s\n")

    test_data = (my_data[0].upper(), my_data[1].upper(), datetime.strptime(my_data[2], '%H:%M').time())

    if validate_test_data(graph, test_data):

        #####################
        # ALGORYTM DIJSKRTY #
        #####################

        print("Szukanie najlepszego połączenia algorytmem Dijkstry...")
        start = time.time()
        graph = dijkstra_fill_graph(df)

        source, cost = dijkstra_search(graph, test_data[0], test_data[1], test_data[2])
        stops, lines = reconstruct_path(source, test_data[0], test_data[1])

        end = time.time()

        result = zip(stops, lines)
        print("\nZnaleziona trasa:")
        for route_part in result:
            print(f"{route_part[1][1]} - linia: {route_part[1][0]}, z przystanku: {route_part[0]}")
            # print(f"      - {route_part[0][0]} - {route_part[1]} - {route_part[0][1]} ")

        print(f"Czas przejazdu: {cost[test_data[1]]}min")
        print(f"Czas obliczeń: {(round(end - start, 2))}s")

        ###################
        # KRYTERIUM CZASU #
        ###################

        print("\nSzukanie najlepszego połączenia algorytmem A* w oparciu o kryterium czasu ...")
        start = time.time()
        graph = a_star_fill_graph(df)

        source, cost = a_star_time(graph, test_data[0], test_data[1], test_data[2])
        stops, lines = reconstruct_path(source, test_data[0], test_data[1])

        end = time.time()

        result = zip(stops, lines)
        print("\nZnaleziona trasa:")
        for route_part in result:
            print(f"{route_part[1][1]} - linia: {route_part[1][0]}, z przystanku: {route_part[0]}")

        print(f"Czas przejazdu: {cost[test_data[1]]}min")
        print(f"Czas obliczeń: {(round(end - start, 2))}s")

        ########################
        # KRYTERIUM PRZESIADEK #
        ########################

        print("\nSzukanie najlepszego połączenia algorytmem A* w oparciu o kryterium przesiadek ...")
        start = time.time()
        graph = a_star_fill_graph(df)

        source, cost = a_star_lines(graph, test_data[0], test_data[1], test_data[2])
        stops, lines = reconstruct_path(source, test_data[0], test_data[1])

        line_list = []
        for line in lines:
            line_list.append(line[0])
        amount_of_lines = len(set(line_list))

        end = time.time()

        result = zip(stops, lines)
        print("\nZnaleziona trasa:")
        for route_part in result:
            print(f"{route_part[1][1]} - linia: {route_part[1][0]}, z przystanku: {route_part[0]}")

        print(f"Czas przejazdu: {cost[test_data[1]] - 10 * amount_of_lines}min")
        print(f"Czas obliczeń: {(round(end - start, 2))}s")
        print(f"Ilość przesiadek: {amount_of_lines - 1}")

    else:
        print("Błąd w nazwie przystanku!")
