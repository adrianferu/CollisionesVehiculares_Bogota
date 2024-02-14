import streamlit as st 
import pandas as pd 
import numpy as np
import pydeck as pdk #Debemos importar esta librería
#from streamlit_deckgl import st_deckgl #Debemos importar esta libnrería
import plotly.express as px

# "-------------------------------------------"
#URL del dataset
URL = 'https://datosabiertos.bogota.gov.co/dataset/8624f916-1db2-4c17-b669-19a19b35d1ca/resource/f5862aaa-4e1c-463e-94d5-f04db8164360/download/historico_siniestros_bogota_d.c_-.csv'
st.title('Registro de siniestros viales en la ciudad de Bogotá, Colombias')

st.markdown('Esta aplicación de Streamlit tiene como objetivo mostrar información acerca de las colisiones de vehículos en la ciudad de Bogotá')
# "-------------------------------------------"
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
    colisiones = pd.read_csv(URL, nrows=nrows, parse_dates=['FECHA_HORA_ACC', 'FECHA_OCURRENCIA_ACC'])
    lowercase = lambda x: str(x).lower()
    colisiones.rename(lowercase, axis='columns', inplace=True)#Pasamos los nombres de columnas a minúsculas
    colisiones.drop(columns=['x','y','objectid'],inplace=True)#Borramos columnas innecesarias
    colisiones['pk_calzada'] = colisiones['pk_calzada'].fillna('sin calzada') #Tratamos valores nulos
    colisiones['civ'] = colisiones['civ'].fillna(0) #trata,ps valores nulos
    colisiones['localidad'] = colisiones['localidad'].fillna('sin informacion') #tratamos valores nulos
    #colisiones['FECHA_HORA_ACC'] = pd.to_datetime(colisiones['FECHA_HORA_ACC'])
    colisiones.rename(columns={'latitud':'latitude', 'longitud':'longitude'}, inplace=True) #Cambio de nombre: lectura de streamlit

   

    return colisiones
# "-------------------------------------------"
#Cargue de la data
data = load_data2(199145) #Hagamos la prueba con los primeros 20.000 registros
original_data = data #Creamos esto para, más adelante, poder hacer la selección por localicadaes. Aparentemente la data es modificada abajo
# "-------------------------------------------"

# Filtro de accidentes por hora: st.slider()
st.header("Consulta la información relacionada a acidentes dependiendo de la hora: ")
# A a sidebar st.sidebar.slider
hour = st.slider("Selecciona la hora entre", 0, 23)
data = data[data['fecha_hora_acc'].dt.hour == hour]

# "-------------------------------------------"
#FILTRO POR AÑO Y FILTRO POR FECHA DE OCURRENCIA
# Filtro por año de ocurrencia del accidente
st.header("Consulta la información relacionada a acidentes dependiendo del año de ocurrencia: ")
rango_anos = st.slider("Selecciona un rango de años", min_value=int(data['ano_ocurrencia_acc'].min()), max_value=int(data['ano_ocurrencia_acc'].max()))
data = data[data['ano_ocurrencia_acc'] == rango_anos]
# "--------------------------"
#Visualicacion de mapa: uso de st.slider(); st.map() y query
st.header('Consulta la concentración de accidentes de tránsito por categoría: ')
# Crear un slider para seleccionar la categoría de gravedad
gravedad_seleccionada = st.select_slider('Seleccione la categoría de gravedad:',
                                             options=data['gravedad'].unique())
#Ahora, el mapa
st.map(data.query("gravedad == @gravedad_seleccionada")[["latitude","longitude"]])
# ------------------------------------------------------
#C
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

# "--------------------------"
#Creacion de histogramas
st.subheader('Separación, por minutos entre  %i:00 and %i:00' % (hour,(hour+1) %24))
filtered = data[(data['fecha_hora_acc'].dt.hour >= hour) & (data['fecha_hora_acc'].dt.hour < (hour+1))]
hist = np.histogram(filtered['fecha_hora_acc'].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({'minute':range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minute', y= 'crashes', hover_data = ['minute','crashes'], height=400)
st.write(fig) #La visualización NO se hace efectiva hasta que haces st.write()
# "--------------------------"
#Filtro por Localidad: Cuáles son las localidades con más accidentes?
st.header('Las 5 localidades con más siniestros vehiculares')
#Necesitamos conocer los valores únicos de las localidades
# Crear el diccionario con las condiciones para cada opción
condiciones = {
    "choque": "clase_acc = 'choque'",
    "otro": "clase_acc = 'otro'",
    "atropello": "clase_acc = 'atropello",
    "volcamiento": "clase_acc = 'volcamiento'",
    "caida de ocupante": "clase_acc = 'caida de ocupante'",
    "autolesion": "clase_acc = 'autolesion'",
    "incendio": "clase_acc = 'incendio'"
}
#--
# Obtener los valores únicos de la columna CLASE_ACC
valores_clase_acc = data['clase_acc'].unique()
# Crear el diccionario con las condiciones para cada opción
condiciones = {valor: f"clase_acc == '{valor}'" for valor in valores_clase_acc}

#-
# Obtener la opción seleccionada por el usuario
opcion_seleccionada = st.selectbox("Selecciona una opción", list(condiciones.keys()))
# Evaluar la condición correspondiente a la opción seleccionada
if opcion_seleccionada in condiciones:
    condicion_evaluar = condiciones[opcion_seleccionada]
    # Filtrar la DataFrame utilizando la condición
    df_filtrado = data.query(condicion_evaluar)[['localidad', 'clase_acc']].groupby('localidad').size().reset_index(name='Cantidad de Accidentes')
    # Ordenar el DataFrame por la columna 'Cantidad de Registros' de forma descendente
    df_filtrado = df_filtrado.sort_values(by='Cantidad de Accidentes', ascending=False)
    # Mostrar solo los 10 primeros valores
    df_filtrado = df_filtrado.head(10)
    st.write("DataFrame filtrado:")
    st.write(df_filtrado)
else:
    st.write("Opción no válida")
# "--------------------------"

#Visualicemos la data en la pap
#Podemos usar checkbox para que, por default, al usuario le de la opción de clickear si queire ver la data:
if st.checkbox('Muéstrame la data procesada', False):
    st.subheader('Data Cruda y preprocesada')
    st.write(data)







