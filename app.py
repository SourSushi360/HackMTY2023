from flask import Flask, render_template, request
import pandas as pd
#import requests
from aux_functions import guardar_nuevo_usuario, buscar_distancia, generar_id
#from find_distance import find_distance

api_key = '5b3ce3597851110001cf6248fd138393e27e4ca89fe9a03a1770f507'

df = pd.read_csv('test_usuarios.csv')
distMax = float(30)
dist = float(0)

app = Flask(__name__, static_folder='static')

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
        
        '''
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Type: {tipo}")
        print(f"Address: {address}")
        '''
        
        if not name or not email or not tipo or not address:
            return "Por favor, llena todos los campos."
        
        #Actualiza la información de la base de datos
        guardar_nuevo_usuario(name, email, tipo, address, "test_usuarios.csv")
                
        # Busca los proveedores cercanos
        if tipo == 'D':
            donantes_cercanos = buscar_distancia(address, distMax, df, api_key)
            return mostrar_output(tipo, donantes_cercanos)
        elif tipo == 'C':
            id=generar_id(name, address)
            return mostrar_output(tipo, id)
        
        
@app.route('/output')
def mostrar_output(tipo, infoImprimir):
    if tipo == 'D':
        return render_template('output.html', id=infoImprimir)
    elif tipo == 'C':
        return render_template('output2.html', donantes_cercanos=infoImprimir)

if __name__ == '__main__':
    app.run(debug=True)

