import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import networkx as nx
from networkx import drawing 
from networkx import graph

ap_col = ['Airport ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Lat', 'Log', 'Alt', 'Timezone', 'DST', 'TZ Database', 'Type', 'Source']
airports = pd.read_csv('./data/airports.dat.txt', header=None, names=ap_col)


rt_col = ['Airline', 'Airline ID', 'Source Airport', 'Src Airport ID', 'Dest Airport', 'Dest Airport ID', 'Codeshare', 'Stops', 'Equipment']
routes = pd.read_csv('./data/routes.dat.txt', header=None, names=rt_col)

def toRadians(degrees):
    return (degrees * math.pi)/180.0

def distance (lat1,lon1,lat2,lon2) :
    #R radius of Earth
    R = 6371e3; # metres
    #phi is latitude
    lat1_rad = toRadians(lat1)
    lat2_rad = toRadians(lat2)
    #difference lat
    delta_lat = toRadians((lat2-lat1))
    #difference lon
    delta_lon = toRadians((lon2-lon1))

    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2) * math.sin(delta_lon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    d = R * c
    return d
 
def flightplanner(source,destination):
    G = nx.Graph()
    # dest_airport = routes['Dest Airport'] == destination
    # src_airport = routes['Source Airport'] == source
    # condition = dest_airport | src_airport
    # newDF = routes[condition]
    for index, airport in airports.iterrows():
        print(index, 'airport')
        G.add_node(airport['IATA'])
    for i, route in routes.iterrows():
        print(i, 'route')
        route_dest = route["Dest Airport"]
        route_src = route["Source Airport"]
        if (route_dest in airports['IATA'].array) and (route_src in airports['IATA'].array):
            src_lat = airports[airports.IATA == route_src].iloc[0]['Lat']
            src_log = airports[airports.IATA == route_src].iloc[0]['Log']

          
            dest_lat = airports[airports.IATA == route_dest].iloc[0]['Lat']
            dest_log = airports[airports.IATA == route_dest].iloc[0]['Log']

            route_dist = distance(src_lat,src_log,dest_lat,dest_log) 

            G.add_edge(route_src,route_dest,weight=route_dist)

    path_array = []
    for path in nx.all_simple_paths(G, source=source, target=destination):
      print('path')
      path_array.append(path)    

    return path_array

def drawG(G) :
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, width=len(G.edges))
    nx.draw_networkx_edges(G, pos, width=len(G.edges))
    plt.show()

coolflight = flightplanner('SFO','PDX')

print(coolflight)
