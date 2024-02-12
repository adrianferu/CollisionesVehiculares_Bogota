import streamlit as st 
import pandas as pd 
import numpy as np
import pydeck as pdk #Debemos importar esta librería
from streamlit_deckgl import st_deckgl #Debemos importar esta libnrería
import plotly.express as px


#URL del dataset
URL = 'https://datosabiertos.bogota.gov.co/dataset/8624f916-1db2-4c17-b669-19a19b35d1ca/resource/f5862aaa-4e1c-463e-94d5-f04db8164360/download/historico_siniestros_bogota_d.c_-.csv'
st.title('Registro de siniestros viales en la ciudad de Bogotá, Colombias')

st.markdown('Esta aplicación de Streamlit tiene como objetivo mostrar las colisiones de veh´´ículos en la ciuidad de Bogotá')

#Función para cargar dataset en función del número de registros
#Agregamos este parámetro para que sólo se hace la 'recomputation' cuando hayan cambios
@st.cache_data(persist=True)
def load_data(nrows):
    colisiones = pd.read_csv('colisiones_Cleaned.csv', nrows = nrows, parse_dates=['FECHA_HORA_ACC', 'FECHA_OCURRENCIA_ACC'])
    #Nos dimos cuenta también que debemos pasar a minúscula las columnas de latitud y longitud
    #Entonces mejor pasamos todas las columnas a minusculas
    lowercase = lambda x: str(x).lower()
    colisiones.rename(lowercase, axis='columns', inplace=True)
    return colisiones

#PRUEBA: ALTERNATIVA A SI LO HACEMOS DIORECTAMENTE DESDE EL ENLACE:
def load_data2(nrows):
    colisiones = pd.read_csv(URL, nrows=nrows)
    colisiones.drop(columns=['X','Y','OBJECTID'],inplace=True)
    colisiones['PK_CALZADA'] = colisiones['PK_CALZADA'].fillna('SIN CALZADA')
    colisiones['FECHA_HORA_ACC'] = pd.to_datetime(colisiones['FECHA_HORA_ACC'])
    colisiones['FECHA_ACC'] = colisiones['FECHA_HORA_ACC'].dt.date
    colisiones['HORA_ACC'] = colisiones['FECHA_HORA_ACC'].dt.time

    return colisiones

#Cargamos la data
data = load_data(20000) #Hagamos la prueba con los primeros 20.000 registros
#data = load_data2(30000) #Por ahora nos sirve, pero se demora bastante en cargar

# "--------------------------"
''' 
try:
    #Cuántas accidentes hubo  para cada periodo de tiempo
    st.header('Cuantos accidentes hubo por periodo de tiempo')
    hour = st.slider('Hora en formato hh:mm ',0, 20)
    data = data[data['fecha_hora_acc'].dt.hour == hour]
except:
    st.write('Aun no hemos podido rsolver el filtro por accidentes y hora')

'''
# Using filtering options in streamlit to show a specific hour
st.header("How many collisions occur during a given time of day")
# A a sidebar st.sidebar.slider
hour = st.slider("Hour to look at", 0, 23)
data = data[data['fecha_hora_acc'].dt.hour == hour]

# "--------------------------"
#Visualicacion de mapa: Se debe hacer con una query
st.header('En qué sector de Bogotá está la mayor parte de los heridos por colisiones vehiculares?')
#con_heridos = st.slider("Numero de personas heridas en colisiones vehiculares",3,9605) #Revisar: el valor maximo de accidentes es 15009
# Crear un slider para seleccionar la categoría de gravedad
gravedad_seleccionada = st.select_slider('Seleccione la categoría de gravedad:',
                                             options=data['gravedad'].unique())
#Ahora, el mapa
st.map(data.query("gravedad == @gravedad_seleccionada")[["latitude","longitude"]])



# "--------------------------"

# ------------------------------------------------------
st.markdown(f"Vehicle collisions between {hour}:00 and {hour + 1}:00")
map_midpoint = (np.average(data['latitude']), np.average(data['longitude']))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={"latitude": map_midpoint[0],
                        "longitude": map_midpoint[1],
                        "zoom": 10,
                        "pitch": 50,
                        },
    # see pydeck documentation for more layers
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data[['fecha_hora_acc', 'latitude', 'longitude']],
            get_position=['longitude', 'latitude'],
            radius=100,
            extruded=True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0, 1000],
        ),
    ],
))

#Creacion de histogramas
st.subheader('Separación, por minutos, ')

# "--------------------------"
#Visualicemos la data en la pap
#Podemos usar checkbox para que, por default, al usuario le de la opción de clickear si queire ver la data:
if st.checkbox('Muéstrame la data procesada', False):
    st.subheader('Data Cruda y preprocesada')
    st.write(data)







