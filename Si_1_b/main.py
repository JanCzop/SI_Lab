from datetime import datetime
import time

import a
import dijkstra
import heuristics
import util
from util import read_connections, reconstruct_path

if __name__ == '__main__':

    path = "connection_graph.csv"
    df = read_connections(path)
   # print(df)
    print("\n\n")

    data_ = ('PERZOWA', 'JAWOROWA', '17:34')
    data = ('ZIMOWA', 'DWORZEC GŁÓWNY', '22:34')

    test_data = (data[0].upper(), data[1].upper(), datetime.strptime(data[2], '%H:%M').time())

    print("Dijkstra")
    start = time.time()
    graph = dijkstra.create_graph(df)

    source, cost = dijkstra. dijkstra(graph, test_data[0], test_data[1], test_data[2])

    stops, lines = reconstruct_path(source, test_data[0], test_data[1])

    end = time.time()

    line_list = []
    for line in lines:
        line_list.append(line[0])
    amount_of_lines = len(set(line_list))

    result = zip(stops, lines)
    print("\nTrasa:")
    util.print_start(data[0],data[1],data[2])
    for route_part in result:
        util.print_route(route_part)
    util.print_end(stops,lines)
    print()
    print(f"Czas przejazdu: {cost[test_data[1]]}min")
    print(f"Czas obliczeń: {(round(end - start, 2))}s")
    print(f"Ilość przesiadek: {amount_of_lines - 1}")

    print()
    print("Kryterium czasowe")
    start = time.time()
    graph = dijkstra.create_graph(df)

    source, cost = a.a_star_time(graph, test_data[0], test_data[1], test_data[2])
    stops, lines = reconstruct_path(source, test_data[0], test_data[1])

    end = time.time()

    line_list = []
    for line in lines:
        line_list.append(line[0])
    amount_of_lines = len(set(line_list))

    result = zip(stops, lines)
    print("\nTrasa:")
    util.print_start(data[0],data[1],data[2])
    for route_part in result:
        util.print_route(route_part)

    util.print_end(stops, lines)
    print()
    print(f"Czas przejazdu: {cost[test_data[1]]}min")
    print(f"Czas obliczeń: {(round(end - start, 2))}s")
    print(f"Ilość przesiadek: {amount_of_lines - 1}")

    print()
    print("A*  kryterium przesiadkowe")
    start = time.time()
    graph = dijkstra.create_graph(df)

    source, cost = a.a_star_changes(graph, test_data[0], test_data[1], test_data[2])
    stops, lines = reconstruct_path(source, test_data[0], test_data[1])

    end = time.time()

    line_list = []
    for line in lines:
        line_list.append(line[0])
    amount_of_lines = len(set(line_list))


    result = zip(stops, lines)
    print("\nTrasa:")
    util.print_start(data[0],data[1],data[2])
    for route_part in result:
        util.print_route(route_part)
    util.print_end(stops, lines)
    print()
    ERROR_HANDLED_TIME = cost[test_data[1]]-(amount_of_lines*heuristics.line_change_heuristic())

    print(f"Czas przejazdu: {ERROR_HANDLED_TIME}min")
    print(f"Czas obliczeń: {(round(end - start, 2))}s")
    print(f"Ilość przesiadek: {amount_of_lines - 1}")