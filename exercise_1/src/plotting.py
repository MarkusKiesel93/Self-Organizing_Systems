import math

import matplotlib.pyplot as plt


## https://gist.github.com/Mizux/cbc48733e0c1d8cb9171bb6828811341
def plot_location(location, axes, color, location_number):
  axes.scatter(
      location[0],
      location[1],
      s=500,
      facecolors='white',
      edgecolors=color,
      linewidths=2)
  axes.scatter(
      location[0],
      location[1],
      s=200,
      marker=f'${location_number}$',
      edgecolors=color,
      facecolors=color)



def plot_locations(coordinates, height):
    fig, axes = plt.subplots(figsize=(1.7 * height, height))
    axes.grid(True)
    axes.set_xticks(list(set([x for (x, y) in coordinates])))
    axes.set_xticklabels([])
    axes.set_yticks(list(set([y for (x, y) in coordinates])))
    axes.set_yticklabels([])
    axes.set_axisbelow(True)
    for (i, location) in enumerate(coordinates):
        color = 'blue' if i else 'black'
        plot_location(location, axes, color, i)
    return fig, axes

def plot_solution(coordinates, solution, marker_size=0.1, height=12):
    
    fig, axes = plot_locations(coordinates, height)
    google_colors = [
        r'#4285F4', r'#EA4335', r'#FBBC05', r'#34A853', r'#101010', r'#FFFFFF'
    ]
    
    for current_node_ind in range(1, len(solution)):
        start_node = solution[current_node_ind - 1]
        end_node = solution[current_node_ind]
        start = coordinates[start_node]
        end = coordinates[end_node]
        delta_x = end[0] - start[0]
        delta_y = end[1] - start[1]
        delta_length = math.sqrt(delta_x**2 + delta_y**2)
        unit_delta_x = delta_x / delta_length
        unit_delta_y = delta_y / delta_length
        axes.arrow(
            start[0] + (marker_size / 2) * unit_delta_x,
            start[1] + (marker_size / 2) * unit_delta_y,
            (delta_length - marker_size) * unit_delta_x,
            (delta_length - marker_size) * unit_delta_y,
            width=0.2,
            head_width=2,
            head_length=2,
            facecolor=google_colors[0],
            edgecolor=google_colors[0],
            length_includes_head=True)
        
    return fig