import requests
import time
from bs4 import BeautifulSoup as bs
from datetime import datetime
import json
import sqlite3
import os

def crear_db():
    conex = sqlite3.connect('crypto.db')
    c = conex.cursor()

    c.execute('''CREATE TABLE crypto
         (ID text, 
          CRYPTO text, 
          COMPRA float,
          VENTA float,
          MONTO float, 
          BENEFICIO float, 
          FECHA_COMPRA text,
          FECHA_VENTA text)''')
    conex.close()

def insertar_data(data):
    conex = sqlite3.connect('crypto.db')
    c = conex.cursor()
    string = 'INSERT INTO crypto VALUES('
    number = len(data) - 1
    j = 0
    for k in data:
        if j < number:
            string += k + ', '
        else:
            string += k
        j += 1
    string += ')'
    print(string)
### inserta valores en la base de datos
    c.execute(string)

    conex.commit()
    conex.close()

    
def obtener_fecha():
    # datetime object containing current date and time
    actual = datetime.now()

    # dd/mm/YY H:M:S
    fecha = actual.strftime("%Y/%m/%d %H:%M:%S")
    return fecha

def obtener_id(fecha_venta):
    id = 'RE'
    for k in fecha_venta:
        if k == '/' or k == ':':
            id += ''
        elif k == ' ':
            id += '_'
        else:
            id += k
    return id

def scrape(crypto = 'bitcoin'):
    url = "https://coinmarketcap.com/currencies/" + crypto + '/'
    respuesta = requests.get(url)
    datos = bs(respuesta.content,'html.parser')
    contenido = datos.find('div',{'class':'priceValue'})
    precio = contenido.select_one('span')
    precio = precio.text

    value = ''
    for k in precio:
        cond = (k == "$" or k == ",")
        if not cond:
            value += k

    value = float(value)
    return value


def borrar_entrada_json():
    with open('file.json', 'r') as file:
        json_data = json.load(file)

        num = 0
        for k in json_data:
            if k["id"] != "0":
                num += 1


        for k in range(num):        
            for i in range(len(json_data)):
                if json_data[i]["id"] != "0":
                    json_data.pop(i)
                    open("file.json", "w").write(json.dumps(json_data, indent = 4))
                    break

            
def json_update(archivo_json):
    with open(archivo_json, 'r') as file:
        json_data = json.load(file)
        size = len(json_data)
        num = 0
        for item in json_data:
            if item['id'] != '0':
                # crear data para la base de datos
                data = []
                for k in item:
                    if type(item[k]) == str:
                        val = "'" + item[k] + "'"
                    else:
                        val = str(item[k])
                    data.append(val)
                # enviar data a la base de datos
                insertar_data(data)
        #borrar data de json
    borrar_entrada_json()
        
    with open(archivo_json, 'r') as file:
        json_data = json.load(file)
        for item in json_data:
            if item['fecha_venta'] == '0':
                #obtener el precio
                precio = scrape(item['crypto'])
                print("precio crypto: ", precio)
                if item['fecha_compra'] == '0':
                    if precio <= float(item['compra']):
                        item['compra'] = precio
                        item['fecha_compra'] = obtener_fecha()
                else:
                    if precio >= float(item['venta']):
                        item['venta'] = precio
                        item['fecha_venta'] = obtener_fecha()
                        item['beneficio'] = item['monto'] * (item['venta'] / item['compra'] - 1)
                        item['id'] = obtener_id(item['fecha_venta'])
            else:
                num += 1

        if num == size:
            print("TODAS LAS OPERACIONES SE COMPLETARON")

    with open(archivo_json, 'w') as file:
        json.dump(json_data, file, indent=4)


file_name = r"crypto.db"
bool = os.path.exists(file_name)

if not bool:
    crear_db()
    
while 1:
    json_update('file.json')
    time.sleep(60)
    
