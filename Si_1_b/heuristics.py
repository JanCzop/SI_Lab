from cmath import sqrt


def a_b_distance_heuristic(graph, a_stop, b_stop):
    try:
        MAGIC_NUMBER = 1000
        x1, y1 = graph.coordinates[a_stop]
        x2, y2 = graph.coordinates[b_stop]
        distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return MAGIC_NUMBER*distance.real if isinstance(distance, complex) else distance

    except KeyError:
        return 0.0

def line_change_heuristic():
    MAGIC_NUMBER = 25
    return MAGIC_NUMBER