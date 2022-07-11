# Proyecto1_Plataformas_python
Este proyecto trata de un programa de scraping, que usa un archivo de configuración JSON, una base de datos sqlite3 para almacenar los datos y pandas junto con matplotlib para graficar datos correspondientes a los beneficios de las operaciones de compra y venta de cryptomonedas.

Es necesario instalar las siguientes librerías y se hace de la siguiente manera (Válido para Ubuntu 20.04):

* pip install BautifulSoup
* pip install requests
* pip install pandas
* pip install matplotlib
* pip install sqlite3
* pip install json


# Partes fundamentales del proyecto:
Las siguientes son las partes fundamentales del proyecto.

## Archivo JSON: file.json
Este archivo tiene una doble función pues define completamente la entrada de datos y además de este archivo depende la salida que irá a la base de datoscada entrada del file.json tiene la siguiente forma:

    {
        "id": "0",
        "crypto": "bnb",
        "compra": 230.26,
        "venta": 231.65,
        "monto": 1000,
        "beneficio": 0,
        "fecha_compra": "0",
        "fecha_venta": "0"
    }

Lo que el usuario debe modificar es "crypto", puesto que es necesario saber que moneda se desea negociar, "compra" que es el precio de compra que está dispuesto a pagar por la cryptomoneda, "venta" que es el precio de venta al que el inversor quiere vender sus monedas una vez que es dueño de ellas y "monto" que es la cantidad de dólares que desea invertir en esa compra.

Con esos 4 datos se completa la participación del usuario.



Para correr el programa se debe abrir una terminal bash en la carpeta donde se encuentran los archivos fuente y escribir lo siguiente:



* python3 scrape.py