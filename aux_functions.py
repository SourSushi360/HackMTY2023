import pandas as pd
import requests

def guardar_nuevo_usuario(name, email, user_type, address, csv_file_path):
    # Create a dictionary with the new data
    if user_type == 'D':
        user_type = 'Donante'
    elif user_type == 'C':
        user_type = 'Beneficiario'
        
    new_data = {
        'Name': [name],
        'Email': [email],
        'User_Type': [user_type],
        'Address': [address]
    }

    # Read the existing CSV file into a DataFrame
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame
        df = pd.DataFrame(columns=['Name', 'Email', 'User_Type', 'Address'])

    # Append the new data to the DataFrame
    new_df = pd.concat([df, pd.DataFrame(new_data)])

    # Save the updated DataFrame to the CSV file
    new_df.to_csv(csv_file_path, index=False)

def buscar_distancia(address, distMax, df, api_key):
    df = df.drop(df[df['User_Type'] == 'Beneficiario'].index)
    provCercanos = pd.DataFrame(columns = ['datosUsuario','distancia'])
    cont = int(0)
    
    while(df.shape[0]-1>cont):
            direccion = df.loc[cont]["Address"]
            # Define the starting and ending addresses
            start_address = address
            end_address = direccion

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
                        provCercanos.loc[cont] = [df.loc[cont]["Name"], distance_meters/1000]

                        print(f"Distance in meters: {distance_meters} meters")
                    else:
                        print(f"Error: {response.status_code} - {response.text}")
                else:
                    print("Geocoding request failed.")

            except Exception as e:
                print(f"An error occurred: {e}")

            provCercanos.drop(provCercanos[provCercanos['distancia'] > distMax].index, inplace = True)
                
            cont += 1
    provCercanos.sort_values(by = ['distancia'], inplace = True)
    provCercanos.to_csv('provTemp.csv', sep='\t')
    return provCercanos.to_string()

def generar_id(name, address):
    result = name[0:4:1]+address[0:4:1]
    return result
