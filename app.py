from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import py_astrolab as astrolab
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
    al = astrolab.Astrolab(fecha, lugar)
    datos_luna = al.get_lunar_data()
    return datos_luna

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
    
    for dato in datos_luna:
        theta = np.deg2rad(dato['grado'])
        r = 1.2
        ax.text(theta, r, f"{dato['signo']} {dato['grado']}°", ha='center', va='center')
    
    ax.set_rticks([])
    ax.set_yticklabels([])
    
    os.makedirs('static', exist_ok=True)
    plt.savefig('static/circulo_lunar.png')

if __name__ == '__main__':
    app.run(debug=True)
    
    