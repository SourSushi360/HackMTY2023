import pandas as pd

def add_to_dataframe_and_save_csv(name, email, user_type, address, csv_file_path):
    # Create a dictionary with the new data
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

# Example usage:
add_to_dataframe_and_save_csv("Juan Perez", "juan@example.com", "Donante", "Paseo de los Leones 3201, Cumbres 6o. Sector Secc a, 64610 Monterrey, N.L.", "test_usuarios.csv")
add_to_dataframe_and_save_csv("Maria Lopez", "maria@gmail.com", "Donante", "Calle Alejandro de Rodas 6767, Pedregal Cumbres, 64340 Monterrey, N.L.", "test_usuarios.csv")
add_to_dataframe_and_save_csv("Pedro Sanchez", "pedro@outlook.com", "Beneficiario", "C. Santos Cantú Salinas 3025, Altamira, 64750 Monterrey, N.L.", "test_usuarios.csv")
add_to_dataframe_and_save_csv("Ana Garcia", "ana@icloud.com", "Beneficiario", "Chiapas 2061, Roma, 64700 Monterrey, N.L.", "test_usuarios.csv")