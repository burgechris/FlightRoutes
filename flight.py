import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

ap_col = ['Airport ID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Lat', 'Log', 'Alt', 'Timezone', 'DST', 'TZ Database', 'Type', 'Source']
airports = pd.read_csv('./data/airports.dat.txt', header=None, names=ap_col)
print(airports.head())


routes = pd.read_csv('./data/routes.dat.txt')
