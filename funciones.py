#Alojaremos las funciones principales en un script a parte, siguiendo buenas prácticas de ingeniería de software
#Agregamos este parámetro para que sólo se hace la 'recomputation' cuando hayan cambios
@st.cache_data(persist=True)
def load_data(nrows):
    colisiones = pd.read_csv('colisiones_Cleaned.csv', nrows = nrows)
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