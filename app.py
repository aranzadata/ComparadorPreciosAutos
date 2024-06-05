#paquetes
import pandas as pd
import plotly_express as px
import streamlit as st


#datos
car_data = pd.read_csv('vehicles_us.csv')

#correción de datos

#cambia el tipo de dato de la columna 'date_posted' a datetime
car_data['date_posted'] = pd.to_datetime(car_data['date_posted'], format='%Y-%m-%d')

#separa la columna 'model' en columnas 'manufacturer' y 'model'
car_data[['manufacturer', 'model']] = car_data['model'].str.split(' ', n=1, expand=True)
car_data['model'] = car_data['model'].str.strip()

#diccionario para los nombres de las columnas en español
col = list(car_data.columns)
col_names = ['Precio (dólares)', 'Año del modelo', 'Modelo', 'Condición', 'Cilindros', 'Tipo de combustible', 'Millas recorridas', 'Transmisión', 'Tipo de vehículo', 'Color', 'Es 4x4', 'Fecha de publicación', 'Días publicado', 'Marca']
dic = dict(zip(col_names, col))


#Contenido de la página

st.title('Comparador de vehículos') #título

st.write('En esta página encontrará información reelevante sobre los precios y características de vehículos publicados para venta.')

st.header('Comparador de precios')

#despliega lista de tipos de vehículo
vehicle_type = st.selectbox('Seleccione un tipo de vehículo', list(car_data['type'].unique()))

#filtra por el tipo deseado
cars_filtered_by_type = car_data[car_data['type'] == vehicle_type]

#despliega lista de marcas y guarda las seleccionadas
manufacturers = st.multiselect('Seleccione las marcas de vehículo de su interés',
                               list(cars_filtered_by_type['manufacturer'].unique()))

#filtra por marcas deseadas
cars_filtered_by_man = cars_filtered_by_type[cars_filtered_by_type['manufacturer'].isin(manufacturers)]

st.write('Seleccione todos los modelos de su interés.')

#crea una lista de modelos por marca 1
models = list(cars_filtered_by_man['model'].unique())

#crea una casilla por cada modelo y si está marcada la añade a la lista modelos de interés.
models_of_interest=[] 

for model in models:
    check = st.checkbox(model)
    if check:
        models_of_interest.append(model)
        
button1 = st.button('Ver distribución de precios')

#filtra car_data por la lista de modelos de interés.
df= car_data[car_data['model'].isin(models_of_interest)]


if button1:
    #crea histograma de precios con los modelos seleccionados.
    fig1 = px.histogram(df,
                        x='price',
                        color='model',
                        title ='Distribución de precios por modelo.',
                        labels= dict(zip(col, col_names)))
    
    st.plotly_chart(fig1, use_container_width=True)

#comparador de millas
st.header('Precio por millas recorridas')

button2 = st.button('Ver precio en función de las millas recorridas')

if button2:
    
    fig2 = px.scatter(df,
                      x='odometer',
                      y='price',
                      color='manufacturer',
                      symbol='model',
                     title='Precio contra millaje.',
                     labels= dict(zip(col, col_names)))
    
    st.plotly_chart(fig2, use_container_width=True)

st.header('Precio por año del modelo')

button3 = st.button('Ver precio en función del año del modelo')

if button3:
    
    fig3 = px.scatter(df,
                      x='model_year',
                      y='price',
                      color='manufacturer',
                      symbol='model',
                      title ='Precio contra año de modelo.',
                      labels= dict(zip(col, col_names)))
    
    
    st.plotly_chart(fig3, use_container_width=True)
    
st.header('Gráfico personalizado')

st.write('En esta sección puede visualizar un gráfico del precio en función de cualquier característica de interés')

dependent_var = st.selectbox('Seleccione la característica de interés', col_names)

button4 = st.button(f'Ver precio en función de {dependent_var}.')

if button4:
    
    fig4 = px.scatter(df,
                      x=dic[dependent_var],
                      y='price',
                      color='manufacturer',
                      symbol='model',
                      title =f'Precio en función de {dependent_var}.',
                      labels= dict(zip(col, col_names)))
    
    st.plotly_chart(fig4, use_container_width=True)

    
