from util import binary_search


class Graph:
    def __init__(self):
        self.edges = {}
        self.vertices = {}
        self.coordinates = {}

    def get_neighbors(self, id):
        return self.vertices[id]

    def calculate_time_cost(self, start, end, current_time):
        edges = self.edges[start, end]
        index = binary_search(edges, 0, len(edges) - 1, current_time)
        if index != -1:
            edge = edges[index]
            return edge[1] - calculate_time_diff(current_time, edge[0]),\
                   (edge[2], edge[0], edge[3])
        else:
            return None

    def calculate_line_cost(self, from_stop, to_stop, current_time, line,  LINE_CHANGE_HEURISTIC_VALUE):
        all_edges = self.edges[from_stop, to_stop]
        index = binary_search(all_edges, 0, len(all_edges) - 1, current_time)
        if index != -1:
            edge = all_edges[index]
            if edge[2] == line:
                return edge[1] - calculate_time_diff(current_time, edge[0]), (edge[2], edge[0], edge[3])
            else:
                return edge[1] - calculate_time_diff(current_time, edge[0]) + LINE_CHANGE_HEURISTIC_VALUE, (edge[2], edge[0], edge[3])
        else:
            return None


def calculate_time_diff(to_time, from_time):
        return (to_time.hour * 60 + to_time.minute) - (from_time.hour * 60 + from_time.minute)
