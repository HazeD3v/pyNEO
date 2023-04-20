import sys
import json
from datetime import date
from termcolor import colored
from urllib import error, request

API_URL = "http://www.neowsapp.com/rest/v1/feed/today"
DATE = date.today()

# Function that attempts to contact the api and retrieve data 
def get_neo_data(url):
    # Try to contact the api
    try:
        response = request.urlopen(url)
    except error.HTTPError as http_error:
        sys.exit(f"Something went wrong! ({http_error.code})")
    data = response.read()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't read server response")


# This Function uses the data supplied to it to display it in a readable output
def disply_neo_data(neo_data):
    # Amount of NEO's today
    neo_amount = neo_data["element_count"]
    # 'neos' variable is the stage before having to iterate over each NEO 
    neos = neo_data["near_earth_objects"][f"{DATE}"]

    # Store data about the NEO's
    fast_neo = []
    big_neo = []
    miss_neo = []

    # Loop over each NEO and append data
    i = 0
    while i < neo_amount:
        big_neo.append(neos[i]["estimated_diameter"]["kilometers"]["estimated_diameter_max"])
        miss_neo.append(neos[i]["close_approach_data"][0]["miss_distance"]["kilometers"])
        fast_neo.append(neos[i]["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
        i += 1

    # Store how many are potentially hazardous asteroids and their details
    hazardous_neo_amount = 0
    hazardous_neo_names = []
    hazardous_neo_diameters = []
    hazardous_neo_miss_distance = []
    hazardous_neo_velocity = []

    # Loop over each NEO and append details
    x = 0
    while x < neo_amount:
        if neos[x]["is_potentially_hazardous_asteroid"] == True:
            hazardous_neo_amount += 1
            hazardous_neo_names.append(neos[x]["name"])
            hazardous_neo_diameters.append(neos[x]["estimated_diameter"]["meters"]["estimated_diameter_max"])
            hazardous_neo_miss_distance.append(neos[x]["close_approach_data"][0]["miss_distance"]["kilometers"])
            hazardous_neo_velocity.append(neos[x]["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
        x += 1
    
    # Display how many NEO's there are TODAY
    print(colored("🔭Amount of NEO'S TODAY:", "cyan", "on_black"))
    print(colored(f"{neo_amount}\n", "light_red"))

    # Check to see if there were any that are potentially hazardous Asteroids
    if hazardous_neo_amount > 0: 
        print(colored("💥Amount of Potentially Hazardous NEO's:", "red", "on_black"))
        print(colored(f"{hazardous_neo_amount}\n", "light_red"))
        print(colored("Hazardous NEO Details:", "yellow", "on_black"))
        y = 0
        # Loop over each hazardous NEO and display the data
        while y < hazardous_neo_amount:
            print(f"{y+1}.")
            print(f"\tName: {hazardous_neo_names[y]}")
            print(f"\tMax Est. Diameter: {hazardous_neo_diameters[y]} km")
            print(f"\tMiss Distance: {hazardous_neo_miss_distance[y]} km")
            print(f"\Velocity: {hazardous_neo_velocity[y]} kph\n")
            y += 1
    # If there is no Hazardous NEO's display some stats along with the okay symbol
    else:
        # Display NEO Stats
        print(f"Largest Estimated Maximum Diameter: {max(big_neo)} km\n")
        print(f"Miss Distance of the nearest NEO : {max(miss_neo)} km\n")
        print(f"Highest Velocity: {max(fast_neo)} km/h\n")
        # Give it the okay
        print(colored("👌No Potentially Hazardous NEO's", "green", "on_black"))


# Loads before data. Gives the user something to stare at I guess
print("Displays Todays Near Earth Objects\n")
# Give get_neo_data() the API URL and store the results in neo_data
neo_data = get_neo_data(API_URL)
# Display the results from neo_data
disply_neo_data(neo_data)
