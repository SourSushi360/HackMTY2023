from flask import Flask, render_template, request
import pandas as pd
#from find_distance import find_distance

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])

###Funciones para el formulario###
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['type']
        address = request.form['address']

        if not name or not email or not message or not address:
            return "Por favor, llena todos los campos."
        
        if type == "Empresa Socialmente Responsable": #Empresa Solicitante de Responsable
            type = "ESR"
        elif type == "Caridad/ONG": #Caridad/ONG
            type = "ONG"
        else:
            return "Por favor, selecciona un tipo de organización."
        
        #Actualiza la información de la base de datos
        save_data(name, email, type, address)
        
        
        
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Type: {type}")
        print(f"Address: {address}")

        return "Formato enviado correctamente."

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


if __name__ == '__main__':
    app.run(debug=True)
