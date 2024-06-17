import pandas as pd



def read_connections(path):
    df = pd.read_csv(
        path,
        dtype=str,
        parse_dates=['departure_time', 'arrival_time'],
        date_parser=lambda x: pd.to_datetime(x, format='%H:%M:%S').time
    )
    return df


def reconstruct_path(previous, start, end):
    current = end
    stops = []
    lines = []
    if end not in previous:
        return []

    while current != start:
        stops.append(current)
        current = previous[current][0]
        if current != start:
            lines.append(previous[current][1])

    stops.append(start)
    stops.reverse()
    stops.append(end)
    lines.reverse()
    lines.append(previous[end][1])
    return stops, lines

def  print_end(stop,line):
    print(f"Z przystanku: {stop[len(stop)-1]:<28} {line[len(line)-1][2]}  linia - {line[len(line)-1][0]}")
def  print_start(start,end,time):
    print(f"Z przystanku: {start} do {end}  start - {time}")
    print()



def  print_route(route):
    print(f"Z przystanku: {route[0]:<28} {route[1][1]}  linia - {route[1][0]}")

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

