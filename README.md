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

Con esos 4 datos se completa la participación del usuario. Luego a partir del valor obtenido al realizar el scraping se llenarán los demás espacios, y una vez llenados todos los espacios todos los valores de dicho items se enviarán a la base de datos y una vez que los valores estén guardados la entrada del json es eliminada permanentemente.

## Scraping y procesamiento de datos:

La parte del scraping tomará del json el valor "crypto" y con esto formará la dirección de la página web para ir a buscar el valor del precio de la moneda en ese momento, traerá el precio y lo formateará para que se un float y con él se harán comparaciones sencillas: si el precio es igual o inferior al precio de compra del json entonces se comprará la cantidad de monedas equivalentes al monto del json y se actualizarán dos cosas en ese momento, el precio de compra (pues podría ser menor al ingresado) y la fecha de compra. Entonces es cuestión de esperar y ver si el precio sube hasta el precio deseado de venta. El precio de venta puede ser modificado dependiendo de la situación, por ejemplo que el precio de la cryptomoneda empiece a bajar más allá de lo tolerable, por lo que se puede modificar el precio para tomar pérdidas menores. Sea lo que sea en cuanto el precio producto del scraping es mayor o igual al precio de venta del json se ejecuta la venta, cambiando el valor "venta", calculando el "beneficio", ingresando "fecha_compra" y creando el "id" de la transacción para dar por completo el ciclo para la entrada del json.

## Base de datos y gráficación:

Como se dijo anteriormente cuando la entrada del json cumple su ciclo de vida los datos que hay en él son enviados a la base de datos creando una nueva entrada, estos datos quedan almacenados aunque el programa se detenido, por lo que los datos de las transacciones quedan disponibles para su análisis, utilización o bien para servir como registro contable. En la parte de graficación primero se obtienen los valores directamente de la base de datos, con estos datos en bruto se trabaja para crear un archivo .csv donde se agrupan los valores que se quieren graficar, luego apartir de este archivo se crea una gráfica que muestra los beneficios que han dado las monedas con las que se ha comerciado. Con lo que se da por concluido el ciclo del programa.


# Forma en que se ejecuta el programa

Primero que nada se deben escribir las entradas del programa, en otras palabras agregar entradas al json, como ya se explicó anteriormente.

Una vez se tienen las órdenes de compra-venta en el json, para correr el programa se debe abrir una terminal bash en la carpeta donde se encuentran los archivos fuente y escribir lo siguiente:

* python3 scrape.py

Este programa es un loop que seguirá comprobando si hay una nueva entrada en el json.

Para obtener la gráfica se debe abrir otra terminal en la misma carpeta del código fuente y escribir:

* python3 graficar.py