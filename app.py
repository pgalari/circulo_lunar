from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
from astroquery.jplhorizons import Horizons
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    fecha = request.form['fecha']
    lugar = request.form['lugar']
    datos_luna = obtener_datos_luna(fecha, lugar)
    generar_circulo_lunar(datos_luna)
    return render_template('index.html', message="Círculo lunar generado con éxito")

def obtener_datos_luna(fecha, lugar):
    # Aquí usamos JPL Horizons para obtener los datos de la Luna
    obj = Horizons(id='301', location=lugar, epochs=fecha, id_type='majorbody')
    eph = obj.ephemerides()
    datos_luna = {
        'fase': eph['illumination'][0],  # Porcentaje de iluminación de la Luna
        'signo': obtener_signo_zodiacal(eph['RA'][0])
    }
    return datos_luna

def obtener_signo_zodiacal(ra):
    # Función simplificada para obtener el signo zodiacal basado en la Ascensión Recta (RA)
    signos = ['Aries', 'Tauro', 'Géminis', 'Cáncer', 'Leo', 'Virgo', 'Libra', 'Escorpio', 'Sagitario', 'Capricornio', 'Acuario', 'Piscis']
    indice = int((ra / 30) % 12)
    return signos[indice]

def generar_circulo_lunar(datos_luna):
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    
    fases = ['Nueva', 'Creciente', 'Llena', 'Menguante']
    colores = ['black', 'gray', 'white', 'gray']
    
    for i, fase in enumerate(fases):
        theta = np.linspace(i * np.pi / 2, (i + 1) * np.pi / 2, 100)
        r = 1 + 0.1 * np.sin(4 * theta)
        ax.plot(theta, r, color=colores[i], lw=2)
        ax.fill_between(theta, 0, r, color=colores[i], alpha=0.5)
    
    theta = np.deg2rad(datos_luna['fase'] * 360 / 100)
    r = 1.2
    ax.text(theta, r, f"{datos_luna['signo']} {datos_luna['fase']}%", ha='center', va='center')
    
    ax.set_rticks([])
    ax.set_yticklabels([])
    
    os.makedirs('static', exist_ok=True)
    plt.savefig('static/circulo_lunar.png')

if __name__ == '__main__':
    app.run(debug=True)
