from structures.graph import Graph
from structures.priority_queue import PriorityQueue


def dijkstra_search(graph: Graph, stopA, stopB, current_time):
    queue = PriorityQueue()
    queue.put(stopA, 0)

    source = {}
    summed_cost = {}
    stop_time = {}
    source[stopA] = None
    summed_cost[stopA] = 0
    stop_time[stopA] = current_time

    while not queue.empty():
        current = queue.get()

        if current == stopB:
            break

        try:
            graph.get_neighbors(current)
        except KeyError:
            continue

        for stop in graph.get_neighbors(current):
            next_cost = graph.calculate_time_cost(current, stop, stop_time[current])
            if next_cost is None:
                continue
            new_cost = summed_cost[current] + next_cost[0]

            if stop not in summed_cost or new_cost < summed_cost[stop]:
                summed_cost[stop] = new_cost
                priority = new_cost
                queue.put(stop, priority)
                source[stop] = current, next_cost[1]
                stop_time[stop] = next_cost[1][2]

    return source, summed_cost


def reconstruct_path(source, stopA, stopB):
    current = stopB
    stops = []
    lines = []
    if stopB not in source:
        return []

    while current != stopA:
        stops.append(current)
        current = source[current][0]
        if current != stopA:
            lines.append(source[current][1])

    stops.append(stopA)
    stops.reverse()
    stops.append(stopB)
    lines.reverse()
    lines.append(source[stopB][1])
    return stops, lines
