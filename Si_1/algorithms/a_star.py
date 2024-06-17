from structures.graph import Graph
from structures.priority_queue import PriorityQueue


def a_star_time(graph: Graph, stopA, stopB, current_stop_time):
    queue = PriorityQueue()
    queue.put(stopA, 0)

    source = {}
    summed_cost = {}
    stop_time = {}
    source[stopA] = None
    summed_cost[stopA] = 0
    stop_time[stopA] = current_stop_time

    while not queue.empty():
        current_stop = queue.get()

        if current_stop == stopB:
            break

        try:
            graph.get_neighbors(current_stop)
        except KeyError:
            continue

        for next_stop in graph.get_neighbors(current_stop):
            next_cost = graph.calculate_time_cost(current_stop, next_stop, stop_time[current_stop])
            if next_cost is None:
                continue
            new_cost = summed_cost[current_stop] + next_cost[0]

            if next_stop not in summed_cost or new_cost < summed_cost[next_stop]:
                summed_cost[next_stop] = new_cost
                priority = new_cost + heuristic(graph, current_stop, stopB)  # doliczanie do kosztu odległości od celu
                queue.put(next_stop, priority)
                source[next_stop] = current_stop, next_cost[1]
                stop_time[next_stop] = next_cost[1][2]

    return source, summed_cost


def a_star_2(graph: Graph, stopA, stopB, current_stop_time):
    queue = PriorityQueue()
    queue.put(stopA, 0)

    source = {}
    summed_cost = {}
    stop_time = {}
    lines = {}
    source[stopA] = None
    summed_cost[stopA] = 0
    stop_time[stopA] = current_stop_time
    lines[stopA] = ""

    while not queue.empty():
        current_stop = queue.get()

        if current_stop == stopB:
            break

        try:
            graph.get_neighbors(current_stop)
        except KeyError:
            continue

        for next_stop in graph.get_neighbors(current_stop):
            next_cost = graph.calculate_line_cost(current_stop, next_stop, stop_time[current_stop],
                                                  lines[current_stop])
            if next_cost is None:
                continue
            new_cost = summed_cost[current_stop] + next_cost[0]

            if next_stop not in summed_cost or new_cost < summed_cost[next_stop]:
                summed_cost[next_stop] = new_cost
                priority = new_cost + heuristic(graph, current_stop, stopB)
                queue.put(next_stop, priority)
                source[next_stop] = current_stop, next_cost[1]
                stop_time[next_stop] = next_cost[1][2]
                lines[next_stop] = next_cost[1][0]

    return source, summed_cost

def a_star_lines(graph: Graph, stopA, stopB, current_stop_time):
    queue = PriorityQueue()
    queue.put(stopA, 0)

    source = {}
    summed_cost = {}
    stop_time = {}
    lines = {}
    source[stopA] = None
    summed_cost[stopA] = 0
    stop_time[stopA] = current_stop_time
    lines[stopA] = ""  # dodatkowa tablica na linie

    while not queue.empty():
        current_stop = queue.get()

        if current_stop == stopB:
            break

        try:
            graph.get_neighbors(current_stop)
        except KeyError:
            continue

        for next_stop in graph.get_neighbors(current_stop):
            next_cost = graph.calculate_line_cost(current_stop, next_stop, stop_time[current_stop],
                                                  lines[current_stop])
            if next_cost is None:
                continue
            new_cost = summed_cost[current_stop] + next_cost[0]

            if next_stop not in summed_cost or new_cost < summed_cost[next_stop]:
                summed_cost[next_stop] = new_cost
                priority = new_cost + heuristic(graph, current_stop, stopB)
                queue.put(next_stop, priority)
                source[next_stop] = current_stop, next_cost[1]
                stop_time[next_stop] = next_cost[1][2]
                lines[next_stop] = next_cost[1][0]

    return source, summed_cost


def heuristic(graph, current_stop, stopB):
    try:
        return 400 * (abs(float(graph.width_height[current_stop][0]) - float(graph.width_height[stopB][0]))
                       + abs(float(graph.width_height[current_stop][1]) - float(graph.width_height[stopB][1])))
    except KeyError:
        return 0.0
