import matplotlib.pyplot as plt
import pandas as pd
import math
import networkx as nx
from networkx import drawing
from networkx import graph
import heapq

ap_col = ['Airport ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Lat',
          'Log', 'Alt', 'Timezone', 'DST', 'TZ Database', 'Type', 'Source']
airports = pd.read_csv('./data/airports.dat.txt', header=None, names=ap_col)


rt_col = ['Airline', 'Airline ID', 'Source Airport', 'Src Airport ID',
          'Dest Airport', 'Dest Airport ID', 'Codeshare', 'Stops', 'Equipment']
routes = pd.read_csv('./data/routes.dat.txt', header=None, names=rt_col)


def toRadians(degrees):
    return (degrees * math.pi)/180.0

def distance(lat1, lon1, lat2, lon2):
    # R radius of Earth
    R = 6371e3  # metres
    #phi is latitude
    lat1_rad = toRadians(lat1)
    lat2_rad = toRadians(lat2)
    # difference lat
    delta_lat = toRadians((lat2-lat1))
    # difference lon
    delta_lon = toRadians((lon2-lon1))

    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.cos(lat1_rad) * \
        math.cos(lat2_rad) * math.sin(delta_lon/2) * math.sin(delta_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c
    return math.trunc(d/1000)


def flightplanner(source, destination):
    G = nx.Graph()
    newDF = routes[(routes.Airline == 'AS') | (routes.Airline == 'AA')]
    for index, airport in airports.iterrows():
        G.add_node(airport['IATA'])
    for i, route in newDF.iterrows():
        route_dest = route["Dest Airport"]
        route_src = route["Source Airport"]
        if (route_dest in airports['IATA'].array) and (route_src in airports['IATA'].array):
            src_lat = airports[airports.IATA == route_src].iloc[0]['Lat']
            src_log = airports[airports.IATA == route_src].iloc[0]['Log']

            dest_lat = airports[airports.IATA == route_dest].iloc[0]['Lat']
            dest_log = airports[airports.IATA == route_dest].iloc[0]['Log']

            route_dist = distance(src_lat, src_log, dest_lat, dest_log)

            G.add_edge(route_src, route_dest, weight=route_dist)

    return G


def path_distance(G, array_of_stops):
    distance = 0
    for index in range(0, len(array_of_stops)-1):
        distance = distance + G.edges[array_of_stops[index], array_of_stops[index + 1]]['weight']

    return distance


def weighted(G, paths):
    h = []
    for path in paths:
        distance = path_distance(G, path)
        t = (distance, path)
        heapq.heappush(h, t)

    return [heapq.heappop(h) for index in range(len(h))]


def drawG(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    plt.show()

G = flightplanner('SFO', 'PDX')

coolflight = nx.all_simple_paths(G, source='SFO', target='PDX', cutoff=3)

paths = list(coolflight)

distance_route_sorted = weighted(G, paths)

df = pd.DataFrame(distance_route_sorted, columns=['Distance', 'Stops'])

print(df)
