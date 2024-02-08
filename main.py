import streamlit as st 
import pandas as pd 


#URL del dataset
URL = 'https://datosabiertos.bogota.gov.co/dataset/8624f916-1db2-4c17-b669-19a19b35d1ca/resource/f5862aaa-4e1c-463e-94d5-f04db8164360/download/historico_siniestros_bogota_d.c_-.csv'
st.title('Registro de siniestros viales en la ciudad de Bogotá, Colombias')

st.markdown('Esta aplicación de Streamlit tiene como objetivo mostrar las colisiones de veh´´ículos en la ciuidad de Bogotá')

#Función para cargar dataset en función del número de registros
#Agregamos este parámetro para que sólo se hace la 'recomputation' cuando hayan cambios
@st.cache_data(persist=True)
def load_data(nrows):
    colisiones = pd.read_csv('colisiones_Cleaned.csv', nrows = nrows)
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

#Visualicemos la data en la pap
#Podemos usar checkbox para que, por default, al usuario le de la opción de clickear si queire ver la data:
if st.checkbox('Muéstrame la data procesada', False):
    st.subheader('Data Cruda y preprocesada')
    st.write(data)


#Visualicacion de mapa: Se debe hacer con una query
st.header('En qué sector de Bogotá está la mayor parte de los heridos por colisiones vehiculares?')
#con_heridos = st.slider("Numero de personas heridas en colisiones vehiculares",3,9605) #Revisar: el valor maximo de accidentes es 15009
# Crear un slider para seleccionar la categoría de gravedad
gravedad_seleccionada = st.select_slider('Seleccione la categoría de gravedad:',
                                             options=data['gravedad'].unique())
#Ahora, el mapa
st.map(data.query("gravedad == @gravedad_seleccionada")[["latitude","longitude"]])



