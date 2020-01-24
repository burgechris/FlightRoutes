import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ap_col = ['Airport ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Lat', 'Log', 'Alt', 'Timezone', 'DST', 'TZ Database', 'Type', 'Source']
airports = pd.read_csv('./data/airports.dat.txt', header=None, names=ap_col)


rt_col = ['Airline', 'Airline ID', 'Source Airport', 'Src Airport ID', 'Dest Airport', 'Dest Airport ID', 'Codeshare', 'Stops', 'Equipment']
routes = pd.read_csv('./data/routes.dat.txt', header=None, names=rt_col)
print(routes.head())