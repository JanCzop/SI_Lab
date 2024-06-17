import heuristics
from graph import Graph
from priority_queue import PriorityQueue



def a_star_time(graph, start, end, current_time):
    queue = PriorityQueue()
    queue.push(start, 0)

    previous = {}
    cost = {}
    time = {}
    previous[start] = None
    cost[start] = 0
    time[start] = current_time

    while not queue.is_empty():
        current_stop = queue.pop()

        if current_stop == end:
            break

        try:
            neighbors = graph.get_neighbors(current_stop)
        except KeyError:
            continue

        for neighbor in neighbors:
            cost_val = graph.calculate_time_cost(current_stop, neighbor, time[current_stop])
            if cost_val is None:
                continue
            new_cost = cost[current_stop] + cost_val[0]

            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                priority = new_cost + heuristics.a_b_distance_heuristic(graph, current_stop, end)
                queue.push(neighbor, priority)
                previous[neighbor] = current_stop, cost_val[1]
                time[neighbor] = cost_val[1][2]

    return previous, cost


def a_star_changes(graph, start, end, current_time):
    queue = PriorityQueue()
    queue.push(start, 0)

    source = {}
    summed_cost = {}
    stop_time = {}
    lines = {}
    source[start] = None
    summed_cost[start] = 0
    stop_time[start] = current_time
    lines[start] = ""
    LINE_CHANGE_HEURISTIC_VALUE = heuristics.line_change_heuristic()

    while not queue.is_empty():
        current_stop = queue.pop()

        if current_stop == end:
            break

        try:
            neighbors = graph.get_neighbors(current_stop)
        except KeyError:
            continue

        for neighbor in neighbors:
            cost_val = graph.calculate_line_cost(current_stop, neighbor, stop_time[current_stop], lines[current_stop], LINE_CHANGE_HEURISTIC_VALUE)
            if cost_val is None:
                continue
            new_cost = summed_cost[current_stop] + cost_val[0]

            if neighbor not in summed_cost or new_cost < summed_cost[neighbor]:
                summed_cost[neighbor] = new_cost
                priority = new_cost + heuristics.a_b_distance_heuristic(graph, current_stop, end)
                queue.push(neighbor, priority)
                source[neighbor] = current_stop, cost_val[1]
                stop_time[neighbor] = cost_val[1][2]
                lines[neighbor] = cost_val[1][0]

    return source, summed_cost
