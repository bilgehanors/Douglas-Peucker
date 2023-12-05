import json
from math import sqrt
import geopandas as gdp
import matplotlib.pyplot as plt

def douglas_peucker(coords, tolerance):
    if len(coords) < 3:
        return coords

    dmax = 0
    index = 0
    end = len(coords) - 1

    for i in range(1, end):
        d = perpendicular_distance(coords[i], coords[0], coords[end])
        if d > dmax:
            index = i
            dmax = d

    result = []
    if dmax > tolerance:
        rec_results1 = douglas_peucker(coords[:index + 1], tolerance)
        rec_results2 = douglas_peucker(coords[index:], tolerance)

        result = rec_results1[:-1] + rec_results2

    else:
        result = [coords[0], coords[end]]

    return result

def perpendicular_distance(point, line_start, line_end):
    x, y = point
    x1, y1 = line_start
    x2, y2 = line_end

    A = x - x1
    B = y - y1
    C = x2 - x1
    D = y2 - y1

    dot = A * C + B * D
    len_sq = C * C + D * D
    param = -1
    if len_sq != 0:
        param = dot / len_sq

    xx, yy = 0, 0
    if param < 0:
        xx, yy = x1, y1
    elif param > 1:
        xx, yy = x2, y2
    else:
        xx, yy = x1 + param * C, y1 + param * D

    dx = x - xx
    dy = y - yy

    return sqrt(dx * dx + dy * dy)

def simplify_geojson(input_geojson_path, output_geojson_path, tolerance=0.001):
    with open(input_geojson_path, 'r') as f:
        geojson_data = json.load(f)

    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'MultiLineString':
            for i, line_string in enumerate(feature['geometry']['coordinates']):
                feature['geometry']['coordinates'][i] = douglas_peucker(line_string, tolerance)

    with open(output_geojson_path, 'w') as f:
        json.dump(geojson_data, f)

if __name__ == "__main__":
    input_file_name = '/Users/bilgehanors/Desktop/PA_Douglas_Peucker/bodrum.geojson'
    output_file_name = '/Users/bilgehanors/Desktop/output2.geojson'
    tolerance = 0.005  # Düzeltme toleransını değiştirebilirsiniz

    simplify_geojson(input_file_name, output_file_name, tolerance)

def plot_geojson(file_path):
    gdf =gdp.read_file(file_path)
    gdf.plot()
    plt.show()
plot_geojson(output_file_name)