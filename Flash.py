# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 13:09:45 2020

@author: INTENTODEMUSICO
"""
from flask import Flask, request, render_template
from string import Template
import pandas as pd
from random import shuffle


data=pd.read_csv("Data/data.csv",sep=";")
amigos=data["code"].to_numpy()
data=data.set_index("code")

def ponerAmigos():
    shuffle(amigos)
    data["friend"]=amigos
    
ponerAmigos()
print(data)
print("")



def datos(obj):
    print(obj)
    return str("Nombre: "+str(obj[0])+". Detalles: "+str(obj[1])+". Alergias: "+str(obj[2])+". Dirección: "+str(obj[3])+".")
    
def datosDe(code):
    return datos(data.loc[code][:-2])

def llenarDatos(code,details,alergies,address,fun):
    data.loc[code,"details"]=details
    data.loc[code,"alergies"]=alergies
    data.loc[code,"address"]=address
    data.loc[code,"fun"]=fun
    data.to_csv("Data/dataF.csv",sep=";")
    return "Sus datos: \n"+datosDe(code)

def datosEntrantes(text):
    salida=text.split(";")
    if(len(salida))!=4:
        return "ERROR: No ingresó todo"
    return salida[0],salida[1],salida[2],salida[3]
    
#print(llenarDatos("bfcxlbvb"," sano","banano","ay","jaja")    )



HTML_TEMPLATE = Template("""

<form method="POST">
    <h1>Hola ${replace_name}!</h1>
    <p>Debe ingresar los datos que se le piden en la casilla y presionar el botón</p>
    <p>Recuerde poner <b>separados por punto y coma</b> " ; " los siguientes datos</p>
    <p>Detalles que quiera agregar(cosas que le gustan o lo que sea); alergias; dirección completa de entrega; su dato curioso</p>
    <h2>Ejemplo:</h2>   
    <p>detalles;alergias;dirección;dato curioso</p>          
    <p>pola, dulces, también me gustan los toxicombos de la UIS; soy alérgico a ser pobre;calle falsa #123;mi dato curioso: una vez me quedé dormido en el baño</p>
    <p><b>OJO:</b> si, por ejemplo, no tiene alergias, debe dejar el espacio vacío así -> datalles;;dirección;dato curioso</p>
    <input name="text">
    <input type="submit">
    <p>Si desea corregirlo, debe volver a esta página e ingresarlo todo nuevamente</p>
    <p>Puede consultar la información de su amigo <a href="/juego/${replace_code}/amigo">aquí</a></p>
    <p>Si no aparece la información de su amigo furtivo, vuelva más tarde</p>
</form>

""")

HTML_TEMPLATE1 = Template("""

<form method="POST">
    <h1>Saludos ${replace_name}!</h1>
</form>

""")


app = Flask(__name__)
@app.route('/')
def homepage():
    return """<h1>Debes poner tu código en el enlace después de / </h1>"""

@app.route('/admin/superadmin/restart')
def restart():
    ponerAmigos()
    return "reiniciao"

@app.route('/juego/<codigo>', methods=['GET'])
def codigo_page(codigo):
    #text = request.form['text']
    #print(text)
    return(HTML_TEMPLATE.substitute(replace_code=codigo,replace_name=data.loc[codigo,"name"]))

@app.route('/juego/<codigo>/amigo', methods=['GET'])
def codigo_page_amigo(codigo):
    codigoAmigo=data.loc[codigo,"friend"]
    return datosDe(codigoAmigo)

@app.route('/juego/<codigo>', methods=['POST'])
def codigo_page_post(codigo):
    text = request.form['text']
    a,b,c,d=datosEntrantes(text)
    return str(llenarDatos(codigo,a,b,c,d)+". Dato curioso: "+d+".")

# @app.route('/juego/<codigo>/data', methods=['POST','GET'])
# def codigo_page_data(codigo):
#     #text = request.form['text']
#     #print(text)
#     return render_template('my-form.html')
#     return(HTML_TEMPLATE1.substitute(replace_codigo=codigo,replace_name=codigo))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


# def ifA(text):
#     if(text=="a"):
#         return "ola"
#     else:
#         return "aaaa"
# @app.route('/')
# def my_form():
#     return render_template('my-form.html')

# @app.route('/')
# def my_form_post():
    
#     return ifA(text)

app.run()