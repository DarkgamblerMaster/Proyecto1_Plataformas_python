import matplotlib.pyplot as plt 
import pylab as p
import pandas as pd 
import sqlite3
import os


# abrir la base de datos para extraer cryptos:
def extraer_cryptos_db():
    cryptos = []
    conex = sqlite3.connect('crypto.db')
    c = conex.cursor()
    for row in c.execute('SELECT * FROM crypto'):
        if row[1] not in cryptos:
            cryptos.append(row[1])
            
    return cryptos

# abrir la base de datos para extraer beneficios:
def extraer_beneficios_db(cryptos):
    tamano = len(cryptos)
    beneficios = []
    # inicializa los beneficios en 0
    for k in range(tamano):
        beneficios.append(0)
        
    conex = sqlite3.connect('crypto.db')
    c = conex.cursor()
    
    for row in c.execute('SELECT * FROM crypto'):
        for k in range(tamano):
            if row[1] == cryptos[k]:
                beneficios[k] += float(row[5])
                
    return beneficios

# abrir la base de datos para extraer transacciones:
def extraer_transacciones_db(cryptos):
    tamano = len(cryptos)
    transacciones = []
    # inicializa los beneficios en 0
    for k in range(tamano):
        transacciones.append(0)
        
    conex = sqlite3.connect('crypto.db')
    c = conex.cursor()
    
    for row in c.execute('SELECT * FROM crypto'):
        for k in range(tamano):
            if row[1] == cryptos[k]:
                transacciones[k] += 1
                
    return transacciones


def crear_csv():
    cryptos = extraer_cryptos_db()    
    beneficios = extraer_beneficios_db(cryptos)
    transacciones = extraer_transacciones_db(cryptos)
    csv_archivo = open("cryptos.csv", "w")
    string = "CRYPTOS, BENEFICIOS, TRANSACCIONES\n"
    total_beneficios = 0
    total_transacciones = 0
    for k in range(len(beneficios)):
        total_beneficios += beneficios[k]
        total_transacciones += transacciones[k]
        
    for k in range(len(cryptos)):
        string += cryptos[k] + ', ' + str(beneficios[k]) + ', ' \
            + str(transacciones[k]) + '\n'

    string += "total, " + str(total_beneficios) + ", " \
        + str(total_transacciones)

    csv_archivo.write(string)
    csv_archivo.close()

# grafica los beneficios para cada cryptomoneda
# en un grafico de barras.
def graficar_beneficios():
    # crea el archivo csv a partir de la base de datos
    crear_csv()
    # datos se toman del csv
    data = pd.read_csv('cryptos.csv')
    # se crea el data frame con los datos del csv
    df = pd.DataFrame(data)

    # se asocian los ejes con las columnas del csv
    X = list(df.iloc[:, 0])
    Y = list(df.iloc[:, 1])

    # algunos atributos de los graficos de barras
    plt.grid(axis = 'y', color='gray', linestyle='dashed')
    plt.bar(X, Y, color='r')
    plt.title("BENEFICIOS POR CRYPTOMONEDA")
    plt.xlabel("CRYPTOMONEDAS")
    plt.ylabel("BENEFICIOS")
    # mostrar grafico terminado
    plt.show()
    p.show()

graficar_beneficios()
