import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

airports = pd.read_csv('./data/airports.dat.txt')

airport = pd.read_csv('./data/routes.dat.txt')
print(airports.head())