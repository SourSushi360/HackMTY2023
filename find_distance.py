import requests

# Replace 'YOUR_API_KEY' with your actual OpenRouteService API key
api_key = '5b3ce3597851110001cf6248fd138393e27e4ca89fe9a03a1770f507'

# Define the starting and ending addresses
start_address = '1600 Amphitheatre Parkway, Mountain View, CA'  # Example: Googleplex
end_address = '1 Infinite Loop, Cupertino, CA'  # Example: Apple Campus

# Geocode the starting and ending addresses to get their coordinates
geocode_url = f'https://api.openrouteservice.org/geocode/search?api_key={api_key}&text='
start_response = requests.get(geocode_url + start_address)
end_response = requests.get(geocode_url + end_address)

try:
    if start_response.status_code == 200 and end_response.status_code == 200:
        start_data = start_response.json()
        end_data = end_response.json()

        # Extract coordinates from the geocoding response
        start_coords = start_data['features'][0]['geometry']['coordinates']
        end_coords = end_data['features'][0]['geometry']['coordinates']

        # Define the API URL with the coordinates and API key
        api_url = f'https://api.openrouteservice.org/v2/directions/driving-car?start={start_coords[0]},{start_coords[1]}&end={end_coords[0]},{end_coords[1]}&api_key={api_key}'

        # Make the API request
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            # Extract the distance in meters from the response
            distance_meters = data['features'][0]['properties']['segments'][0]['distance']
            print(f"Distance in meters: {distance_meters} meters")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    else:
        print("Geocoding request failed.")
except Exception as e:
    print(f"An error occurred: {e}")
