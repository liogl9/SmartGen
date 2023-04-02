# SmartGen

Este repositorio consiste en el sistema de gestión eficiente propuesto por Socket Team.
Consta de los siguientes microservicios y sus localizaciones.

## Base de datos del sistema (influxDB)

Este servicio consta de una base de datos construida en InfluxDB por su capacidad de almacenar series temporales.

Se basa en la imagen oficial expuesta en docker hub y en este repositorio existen archivos para la escritura de datos en la misma como para su lectura.

Actualmente, el servicio se puede inicializar y cargar un número de datos para la demo del sistema.

## Predicción del consumo de agua (waterpred)

Este servicio consta de un sistema de consultas a la base de datos así como de un modelo de predicción del consumo de agua.

Actualmente el modelo no ha sido entrenado pero es operable.

## Consulta de los datos de REE (reedata)

Este servicio consta de un sistema de consultas a la API externa de REE para procesar la situación del balance de generación y demanda en tiempo real.

Actualmente el servicio se puede inicializar y ejecutar las consultas de forma periódica.

## Consulta de datos de AEMET (Aemet_API)

Este servicio constará de otro sistema de consultas a la api externa de AEMET y el procesado de las respuestas.

Actualmente está en desarrollo.

## Sistema de gestión de generación eficiente (smartgen)

Este servicio consta del sistema de control de la situación actual y futura de las centrales hidroeléctricas.
Para ello, interactua con el resto de sistemas y almacenará la predicción de los niveles de los embalses en la base de datos.

Actualmente, interactua con el sistema de predicción de consumo con los archivos del directorio water_cons para obtener el consumo de agua, con el sistema de consulta de la API de REE a través de los archivos del directorio gen_dem y con el sistema de monitorización a través del archivo monitor.

Como el sistema de consulta de precipitaciones no está operativo se simula como igual al consumo.

## Sistema de monitorización (app)

Este servicio consta de un servidor web que exponga los resultados del servicio SmartGen, los cuales se almacenan en el directorio monitor en forma de archivo JSON.

## DEmo

Leer readme de influxdb

Ejecutar el archivo docker compose

Ejecutar en writeinfluxdb.py del contenedor de waterpred.

Comprobar que en el contenedor smartgen se ha generado el archivo de centrales.json con que central genera y cual no.

Actualmente no está disponible el servicio de monitorización.
