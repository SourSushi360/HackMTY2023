from flask import Flask, render_template, request
import pandas as pd
#import requests
from aux_functions import guardar_nuevo_usuario, buscar_distancia, generar_ID_beneficiario, generar_ID_empresa
#from find_distance import find_distance

api_key = '5b3ce3597851110001cf6248fd138393e27e4ca89fe9a03a1770f507'

df = pd.read_csv('test_usuarios.csv')
distMax = float(30)
dist = float(0)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])

###Funciones para el formulario###
def submit():
    if request.method == 'POST':
        name = request.form['nombre']
        email = request.form['email']
        tipo = request.form['tipo']
        address = request.form['address']
        
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Type: {tipo}")
        print(f"Address: {address}")

        if not name or not email or not tipo or not address:
            return "Por favor, llena todos los campos."
        
        #Actualiza la información de la base de datos
        guardar_nuevo_usuario(name, email, tipo, address, "test_usuarios.csv")
        
        # Genera un id para el usuario
        if tipo == 'D':
            id = generar_ID_empresa(name, email, tipo, address)
        elif tipo == 'C':
            id = generar_ID_beneficiario(name, email, tipo, address)
        else:
            return "Tipo de usuario no válido."
        
        # Busca los proveedores cercanos
        buscar_distancia(address, distMax, df, api_key)
        
        return "Formato enviado correctamente."

def mostrar_output():
    proveImp = pd.read_csv('provTemp.csv')
    cont = int(0)
    output = " "
    while(proveImp.shape[0]>cont):
        output += proveImp.loc[cont][0] + "\t" + proveImp.loc[cont][1] + "\n"
        cont += 1
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)

