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
    # Store the data from the response
    data = response.read()
    # Try to JSONify the result
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't read server response")


# This Function uses the data supplied to it to display it in a readable output
def disply_neo_data(neo_data):
    # Amount of NEO's today
    neo_amount = neo_data["element_count"]

    # Display how many NEO's there are TODAY
    print(colored("🔭Amount of NEO'S TODAY:", "cyan", "on_black"))
    print(colored(f"{neo_amount}\n", "light_red"))

    # 'neos' variable is the stage before having to iterate over each NEO 
    neos = neo_data["near_earth_objects"][f"{DATE}"]

    # Store how many are potentially hazardous asteroids and their details
    hazardous_neo_amount = 0
    hazardous_neo_names = []
    hazardous_neo_diameters = []
    hazardous_neo_miss_distance = []

    # Loop over each NEO and append details to the lists
    x = 0
    while x < neo_amount:
        if neos[x]["is_potentially_hazardous_asteroid"] == True:
            hazardous_neo_amount += 1
            hazardous_neo_names.append(neos[x]["name"])
            hazardous_neo_diameters.append(neos[x]["estimated_diameter"]["meters"]["estimated_diameter_max"])
            hazardous_neo_miss_distance.append(neos[x]["close_approach_data"][0]["miss_distance"]["kilometers"])
        x += 1

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
            print(f"\tMax Est. Diameter (meters): {hazardous_neo_diameters[y]}")
            print(f"\tMiss Distance (kilometers): {hazardous_neo_miss_distance[y]}")
            y += 1
    else:
        print(colored("👌No Potentially Hazardous NEO's", "green", "on_black"))

    

print("Displays Todays Near Earth Objects\nAlso shows a bit of data about the ones that come a little close!\n")


# Give get_neo_data() the API URL and store the results in neo_data
neo_data = get_neo_data(API_URL)
# Display the results from neo_data
disply_neo_data(neo_data)