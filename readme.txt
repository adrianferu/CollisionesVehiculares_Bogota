Fecha de inicio: DOmingo 04 de febrero de 2024

NOMBRE DE PROYECTO:		APLICACIÓN DE GEORREFERENCIACIÓN DE CHOQUES VIALES EN LA CIUDAD DE BOGOTÁ


El objetivo de este proyecto es el de crear una aplicación en streamit-folium, con el fin de que le usuario pueda visualizar los accidentes de tr´qansito acontecidos
en la ciudad de Bogotá, y filtrar por atributos como fecha, año de ocurrencia y localización.


Nombre del archivo original:		historico_siniestros_bogota_d.c_-

Fuente del archivo original:		https://datosabiertos.bogota.gov.co/dataset/8624f916-1db2-4c17-b669-19a19b35d1ca?_external=True

Para futura guía:                   https://github.com/LAMDAMielgo/WebApp_Streamlit_for_DataScience/blob/master/app.py

                                    https://github.com/streamlit/streamlit/issues/7627  onsulta de conflicto entre pydeck and ipywidgets.

                                    https://github.com/pyenv/pyenv: Diferentes versiones de python en WSL2

Dividiremos el proyecto en varios pasos:

1. El primero será un EDA: Análisis Exploratorio de los datos de colsiiones en un Jupyter Notebook..

Hice un pequeño cambio

1.a.Para esto, recuerda que deberemos crear un ambiente virtual: En mi caso, se llama geoPortfolioUbuntu
1.b. Los packages necesarios para este trabajo se encuentran en el archivo requirements.txt



2. 





3. Debido a que tuvimos confliuctos para visualizar la app con el ambiente de Conda, decidimos hacelro con un ambiente virutal venv:

Usamos la versión de python: Python 3.7.9

Clonamos este repo en el pc de mesa. Comprobemos si están bien sincronizados

