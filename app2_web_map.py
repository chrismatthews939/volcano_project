import folium
import pandas

# Read the data from the CSV file
data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

# Function to assign color based on elevation
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

# Initialize the map with attribution for Stamen Terrain
map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Stamen Terrain", 
                 attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.')

# Feature Group for Volcanoes
fgv = folium.FeatureGroup(name="Volcanoes")

# Add volcano markers with circle markers
for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=6, popup=str(el) + " m",
                                      fill_color=color_producer(el), fill=True, color='grey', fill_opacity=0.7))

# Feature Group for Population
fgp = folium.FeatureGroup(name="Population")

# Load GeoJSON data for population
try:
    with open('world.json', 'r', encoding='utf-8-sig') as file:
        geo_data = file.read()

    fgp.add_child(folium.GeoJson(data=geo_data,
                                 style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                                                           else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                                           else 'red'}))
except FileNotFoundError:
    print("Error: 'world.json' file not found.")
except Exception as e:
    print(f"Error reading 'world.json': {e}")

# Add feature groups and layer control to the map
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

# Save the map to an HTML file
map.save("Map1.html")
