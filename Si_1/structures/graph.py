class Graph:
    def __init__(self):
        self.edges = {}
        self.vertices = {}
        self.width_height = {}

    def get_neighbors(self, id):
        return self.vertices[id]

    def calculate_time_cost(self, start_stop, end_stop, current_time):

        all_edges = self.edges[start_stop, end_stop]
        index = binary_search(all_edges, 0, len(all_edges) - 1, current_time)
        if index != -1:
            edge = all_edges[index]
                        # cost                            line, departure_time, arrival_time
            return edge[1] - calculate_time_diff(current_time, edge[0]), (edge[2], edge[0], edge[3])
        else:
            return None
        #
        # for edge in self.edges[(start_stop, end_stop)]:
        #     if edge[0] >= current_time:
        #         return edge[1] + calculate_time_diff(edge[0], current_time), (edge[2], edge[0], edge[3])
        # return None

    def calculate_line_cost(self, from_stop, to_stop, current_time, line):
        all_edges = self.edges[from_stop, to_stop]
        index = binary_search(all_edges, 0, len(all_edges) - 1, current_time)
        if index != -1:
            e = all_edges[index]
            if e[2] == line:
                return e[1] - calculate_time_diff(current_time, e[0]), (e[2], e[0], e[3])
            else:
                return e[1] - calculate_time_diff(current_time, e[0]) + 10, (e[2], e[0], e[3])
        else:
            return None

        # for e in self.edges[(from_stop, to_stop)]:
        #     if e[0] >= current_time:
        #         if e[2] == line:
        #             return e[1] + calculate_time_diff(e[0], current_time), (e[2], e[0], e[3])
        #         else:
        #             return e[1] + calculate_time_diff(e[0], current_time) + 10, (e[2], e[0], e[3])
        # return None


def calculate_time_diff(to_time, from_time):
    return (to_time.hour * 60 + to_time.minute) - (from_time.hour * 60 + from_time.minute)


def binary_search(arr, low, high, x):
    if high >= low:
        mid = (high + low) // 2
        if arr[mid][0] == x:
            return mid
        elif arr[mid][0] > x:
            return binary_search(arr, low, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, high, x)
    else:
        if low >= len(arr):
            return -1
        if arr[low][0] > x:
            return low
        else:
            return -1