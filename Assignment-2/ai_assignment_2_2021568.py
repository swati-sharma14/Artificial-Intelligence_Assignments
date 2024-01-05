# -*- coding: utf-8 -*-
"""AI_Assignment-2_2021568.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fP09Xq53OQsCiarCVlVsnwNtb4CzQA51
"""

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import LocalOutlierFactor
import pandas as pd
from sklearn.preprocessing import StandardScaler
import csv
import heapq
import math
from collections import defaultdict
import sys

def create_city_graph(filename):
    city_graph = {}

    # Read the CSV file
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        city_names = next(csv_reader)[1:]  # Get city names from the first row (excluding the first cell)

        # Initialize the dictionary with city names as keys
        for city_name in city_names:
            city_graph[city_name] = {}

        for row in csv_reader:
            city_graph[row[0]] = {}

    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        city_names = next(csv_reader)[1:]  # Get city names from the first row (excluding the first cell)

        # Read the rest of the file to extract distances and populate the graph
        for row in csv_reader:
            current_city = row[0]  # Get the name of the current city
            for i, distance in enumerate(row[1:]):
                if distance != '-':
                    other_city = city_names[i]  # Use city names from the first row directly
                    distance = int(distance)

                    # Check for already existing roads
                    if other_city in city_graph[current_city] and distance < city_graph[current_city][other_city]:
                        city_graph[current_city][other_city] = distance
                        city_graph[other_city][current_city] = distance

                    # Make it bidirectional (reverse direction)
                    if other_city not in city_graph[current_city]:
                        city_graph[current_city][other_city] = distance
                        city_graph[other_city][current_city] = distance

    return city_graph


def find_shortest_distance(graph, start, end):
    if start not in graph:
        return "Start city not found in the graph."
    if end not in graph:
        return "End city not found in the graph."

    visited_cities = set()
    queue = [(0, start)]

    while queue:
        queue.sort()
        current_cost, current_city = queue.pop(0)

        if current_city == end:
            return current_cost  # Found the shortest path

        if current_city in visited_cities:
            continue

        visited_cities.add(current_city)

        for neighbor, distance in graph[current_city].items():
            new_cost = current_cost + distance
            # Check if the neighbor is already in the queue and has a higher cost
            for i in range(len(queue)):
                cost, city = queue[i]
                if city == neighbor and cost > new_cost:
                    # Update the neighbor's cost in the queue
                    queue[i] = (new_cost, neighbor)
                    break
            else:
                # Neighbor is not in the queue or has a lower cost
                queue.append((new_cost, neighbor))

    return "No path found between the cities."

# Input file name containing the city distances data
csv_filename = 'Road_Distance.csv'  # Replace with your CSV filename

# Read the CSV file and create the graph of cities and distances
city_distance_graph = create_city_graph(csv_filename)
# Take user input for the starting and destination cities
start_city = input("Enter the starting city: ")
end_city = input("Enter the destination city: ")

# Find the shortest distance using Uniform Cost Search
distance_result = find_shortest_distance(city_distance_graph, start_city, end_city)
print(f"The shortest distance between {start_city} and {end_city} is {distance_result} units.")

def create_city_graph(filename):
    city_graph = {}

    # Read the CSV file
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        city_names = next(csv_reader)[1:]  # Get city names from the first row (excluding the first cell)

        # Initialize the dictionary with city names as keys
        for city_name in city_names:
            city_graph[city_name] = {}

        for row in csv_reader:
            city_graph[row[0]] = {}

    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        city_names = next(csv_reader)[1:]  # Get city names from the first row (excluding the first cell)

        # Read the rest of the file to extract distances and populate the graph
        for row in csv_reader:
            current_city = row[0]  # Get the name of the current city
            for i, distance in enumerate(row[1:]):
                if distance != '-':
                    other_city = city_names[i]  # Use city names from the first row directly
                    distance = int(distance)

                    # Check for already existing roads
                    if other_city in city_graph[current_city] and distance < city_graph[current_city][other_city]:
                        city_graph[current_city][other_city] = distance
                        city_graph[other_city][current_city] = distance

                    # Make it bidirectional (reverse direction)
                    if other_city not in city_graph[current_city]:
                        city_graph[current_city][other_city] = distance
                        city_graph[other_city][current_city] = distance

    return city_graph

def calculate_admissible_heuristic(graph):
    heuristic = {}

    for city in graph:
        heuristic[city] = float('inf')

        # Initialize the cost for the current city to infinity
        current_cost = float('inf')

        for neighbor, distance in graph[city].items():
          current_cost = min(current_cost, distance)

        heuristic[city] = current_cost

    return heuristic

def calculate_non_admissible_heuristic(graph):
    heuristic = {}

    for city in graph:
        heuristic[city] = 0

        # Initialize the cost for the current city to 0
        current_cost = 0

        for neighbor, distance in graph[city].items():
          current_cost = max(current_cost, distance)

        heuristic[city] = current_cost

    return heuristic

def find_shortest_distance_a_star(graph, start, end, heuristic_val):
    if start not in graph:
        return "Start city not found in the graph."
    if end not in graph:
        return "End city not found in the graph."

    visited_cities = set()
    frontier = [(heuristic_val[start], start)]
    g_costs = {city: float('inf') for city in graph}
    g_costs[start] = 0

    while frontier:
        frontier.sort()
        current_cost, current_city = frontier.pop(0)

        if current_city == end:
            return g_costs[end]  # Found the shortest path

        if current_city in visited_cities:
            continue

        visited_cities.add(current_city)

        for neighbor, distance in graph[current_city].items():
            if neighbor not in visited_cities:
                new_cost = g_costs[current_city] + distance
                if new_cost < g_costs[neighbor]:
                    g_costs[neighbor] = new_cost
                    h_costs = g_costs[current_city] + distance + heuristic_val[neighbor]
                    frontier.append((h_costs, neighbor))

    return "No path found between the cities."


csv_filename = 'Road_Distance.csv'
city_distance_graph = create_city_graph(csv_filename)

start_city = input("Enter the starting city: ")
end_city = input("Enter the destination city: ")

heuristic_choice = input("Choose a heuristic (1 for Admissible, 2 for Non-Admissible): ")

if heuristic_choice == "1":
    heuristic_val = calculate_admissible_heuristic(city_distance_graph)
elif heuristic_choice == "2":
    heuristic_val = calculate_non_admissible_heuristic(city_distance_graph)
else:
    print("Invalid heuristic choice.")
    exit()

# Find the shortest distance using A* search with the selected heuristic
distance_result = find_shortest_distance_a_star(city_distance_graph, start_city, end_city, heuristic_val)

print(f"The shortest distance between {start_city} and {end_city} is {distance_result} units.")