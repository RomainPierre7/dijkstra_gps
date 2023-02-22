import pandas as pd
from enum import Enum, auto
import tkinter as tk
from tkinter import ttk

# Cities (30 french cities)
class Cities(Enum):
    Marseille = 0
    Nice = auto()
    Gap = auto()
    Montpellier = auto()
    Perpignan = auto()
    Toulouse = auto()
    Pau = auto()
    Bordeaux = auto()
    Brive = auto()
    Clermont_Ferrand = auto()
    Lyon = auto()
    Grenoble = auto()
    La_Rochelle = auto()
    Limoges = auto()
    Poitiers = auto()
    Nantes = auto()
    Rennes = auto()
    Caen = auto()
    Rouen = auto()
    Amiens = auto()
    Calais = auto()
    Lille = auto()
    Metz = auto()
    Nancy = auto()
    Strasbourg = auto()
    Dijon = auto()
    Nevers = auto()
    Besançon = auto()
    Paris = auto()
    Genève = auto()

number_cities = 30

list_cities = []
for name, member in Cities.__members__.items():
    list_cities.append(name)

# Graph of distances from cities by direct highways
data = pd.read_csv(r"matrice_autoroutes.csv",encoding = 'ISO-8859-1', index_col=0)
G = data.to_numpy()

# 1 explored, 0 unexplored (for cities)
explored = []
for i in  range(number_cities):
    explored.append(0)

# -1 = no previous
previous_city = []
for i in  range(number_cities):
    previous_city.append(-1)

# Distances of each city from the start
distances_to_start = []
inf = float('inf')
for i in  range(30):
    distances_to_start.append(inf)

# Set Itinerary
start = 0
destination = 0

# ---------- Program ----------

# Auxiliary functions
def closest_unexplored_city():
    closest = 0
    while explored[closest] == 1:
        closest += 1
    for i in range(closest + 1, number_cities):
        if (explored[i] == 0) and (distances_to_start[i] < distances_to_start[closest]):
            closest = i
    return closest

def itinerary_name(T):
    travel = []
    for i in range(len(T)):
        for name, member in Cities.__members__.items():
            if (member.value == T[i]):
                travel.append(name)
    travel.reverse()
    return travel

def value_city(name_city):
    for name, member in Cities.__members__.items():
        if name_city == name:
            return member.value

# Dijkstra algorithm
def find_travel():
    distances_to_start[start] = 0

    while (explored[destination] == 0):
        current_city = closest_unexplored_city()
        explored[current_city] = 1
        for i in range(number_cities):
            if G[current_city][i] > 0:
                if distances_to_start[current_city] + G[current_city][i] < distances_to_start[i]:
                    distances_to_start[i] = distances_to_start[current_city] + G[current_city][i]
                    previous_city[i] = current_city

    back = destination
    itinerary = [back]
    while(back != start):
        itinerary.append(previous_city[back])
        back = previous_city[back]

    return itinerary_name(itinerary)

# Tkinter
root = tk.Tk() 
root.geometry('1000x500')

def start_action(event):
    global start
    choosen_number = start_combo.get()
    start = value_city(choosen_number)
    print(find_travel())

label_start = tk.Label(root, text = "Start ?")
label_start.pack()

start_combo = ttk.Combobox(root, values=list_cities)
 
start_combo.current(0)

start_combo.pack()
start_combo.bind("<<ComboboxSelected>>", start_action)

def destination_action(event):
    global destination
    choosen_number = destination_combo.get()
    destination = value_city(choosen_number)
    print(find_travel())

label_destination = tk.Label(root, text = "destination ?")
label_destination.pack()

destination_combo = ttk.Combobox(root, values=list_cities)
 
destination_combo.current(0)

destination_combo.pack()
destination_combo.bind("<<ComboboxSelected>>", destination_action)

root.mainloop()