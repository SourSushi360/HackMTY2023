import pandas as pd
import requests


def save_data(name, email, type, address):
    # Guarda la información en una base de datos .csv
    data_to_add = [[name, email, type, address]]
    columns = ['Name', 'Email', 'Type', 'Address']

    try:
        existing_data = pd.read_csv('your_existing_file.csv')
    except FileNotFoundError:
        existing_data = pd.DataFrame(columns=columns)
        
    # Concatenate the existing data and the new data
    combined_data = pd.concat([existing_data, data_to_add], ignore_index=True)

    # Save the combined data back to the CSV file
    combined_data.to_csv('test_usuarios.csv', index=False)

def buscar_distancia(address, distMax, df):
    api_key = '5b3ce3597851110001cf6248fd138393e27e4ca89fe9a03a1770f507'
    df = df.drop(df[df['tipo'] == 'ESR'].index)
    provCercanos = pd.DataFrame(columns = ['datosUsuario','distancia'])
    cont = int(0)
    while(df.shape[0]>cont):
            direccion = df.loc[cont][3]
            # Define the starting and ending addresses
            start_address = address
            end_address = direccion  # Example: Apple Campus

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
                        guardado = distance_meters

                        print(f"Distance in meters: {distance_meters} meters")
                    else:
                        print(f"Error: {response.status_code} - {response.text}")
                else:
                    print("Geocoding request failed.")

            except Exception as e:
                print(f"An error occurred: {e}")

            dist = distance_meters/1000
            if(dist < distMax):
                textUsu =  df.loc[cont][0] + ", " + df.loc[cont][1] + ", " + df.loc[cont][3]
                new_row = {'datosUsuario': textUsu, 'distancia': dist}
                provCercanos.append(new_row, ignore_index=True)
                
            cont += 1
    provCercanos.sort_values(by = ['distancia'], inplace = True)
    provCercanos.to_csv('provTemp.csv', sep='\t')
