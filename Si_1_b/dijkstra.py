import heapq

from graph import Graph, calculate_time_diff
from priority_queue import PriorityQueue

def create_graph(df):
    graph = Graph()
    for row in df.values:
        start_stop = str(row[6]).upper()
        end_stop = str(row[7]).upper()
        xy = float(row[8]), float(row[9])

        if start_stop in graph.vertices.keys():
            graph.vertices[start_stop].append(end_stop)
        else:
            graph.vertices[start_stop] = [end_stop]
            graph.coordinates[start_stop] = xy

        edge = row[4], calculate_time_diff(row[5], row[4]), row[3], row[5]
        if (start_stop, end_stop) not in graph.edges.keys():
            graph.edges[(start_stop, end_stop)] = [edge]
        else:
            graph.edges[(start_stop, end_stop)].append(edge)

    for r in graph.edges.values():
        r.sort(key=lambda x: x[0])

    return graph




def dijkstra(graph: Graph, start, end, current_time):
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
            time_cost = graph.calculate_time_cost(current_stop, neighbor, time[current_stop])
            if time_cost is None:
                continue

            new_cost = cost[current_stop] + time_cost[0]

            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                priority = new_cost
                queue.push(neighbor, priority)
                previous[neighbor] = current_stop, time_cost[1]
                time[neighbor] = time_cost[1][2]

    return previous, cost


