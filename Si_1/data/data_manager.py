import pandas as pd

from structures.graph import Graph, calculate_time_diff


def read_connections(path):
    df = pd.read_csv(
        path,
        dtype=str,
        parse_dates=['departure_time', 'arrival_time'],
        date_parser=lambda x: pd.to_datetime(x, format='%H:%M:%S').time
    )
    return df


def dijkstra_fill_graph(df):
    graph = Graph()
    for row in df.values:
        start_stop = str(row[6]).upper()
        end_stop = str(row[7]).upper()

        if start_stop not in graph.vertices.keys():
            graph.vertices[start_stop] = [end_stop]
        else:
            graph.vertices[start_stop].append(end_stop)

        edge = row[4], calculate_time_diff(row[5], row[4]), row[3], row[5]

        if (start_stop, end_stop) not in graph.edges.keys():
            graph.edges[(start_stop, end_stop)] = [edge]
        else:
            graph.edges[(start_stop, end_stop)].append(edge)

    for r in graph.edges.values():
        r.sort(key=lambda x: x[0])

    return graph


def a_star_fill_graph(df):
    graph = Graph()
    for row in df.values:
        start_stop = str(row[6]).upper()
        from_w_h = row[8], row[9]

        end_stop = str(row[7]).upper()

        if start_stop in graph.vertices.keys():
            graph.vertices[start_stop].append(end_stop)
        else:
            graph.vertices[start_stop] = [end_stop]
            graph.width_height[start_stop] = from_w_h
        #  departure_time                  cost             line   arrival time
        edge = row[4], calculate_time_diff(row[5], row[4]), row[3], row[5]
        if (start_stop, end_stop) in graph.edges.keys():
            graph.edges[(start_stop, end_stop)].append(edge)
        else:
            graph.edges[(start_stop, end_stop)] = [edge]

    for r in graph.edges.values():
        r.sort(key=lambda x: x[0])

    return graph


def validate_test_data(graph, test_data):
    if test_data[0] in graph.vertices.keys() and test_data[1] in graph.vertices.keys():
        return True
