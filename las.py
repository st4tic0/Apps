import streamlit as st
st.set_page_config(layout="wide", page_title='LAS Explorer v.0.1')

#from load_css import local_css
import lasio
#import missingno as mno
import pandas as pd
import petropy as ptr
# Local Imports
import home
import raw_data
import plotting
import header
import ooip
import plotly.figure_factory as ff

# import debugpy
# debugpy.listen(5677)
# debugpy.wait_for_client()  # blocks execution until client is attached

#local_css("style.css")

@st.cache(allow_output_mutation=True)
def load_data(uploadedfile):
    if uploadedfile:
        string = uploadedfile.read().decode()
        las_file =  lasio.read(string)

        # Create the dataframe
        well_data = las_file.df()

        #Assign the dataframe index to a curve
        well_data['DEPTH'] = well_data.index
    else:
        las_file=None
        well_data=None
    
    return las_file, well_data

#TODO
def missing_data():
    st.title('Missing Data')
    missing_data = well_data.copy()
    missing = px.area(well_data, x='DEPTH', y='DT')
    st.plotly_chart(missing)

# Sidebar Options & File Uplaod
las_file=None
st.sidebar.write('# LAS Data Explorer')
st.sidebar.write('Elige el archivo que se cargara')

uploadedfile = st.sidebar.file_uploader(' ', type=['las'])
las_file, well_data = load_data(uploadedfile)

if las_file:
    st.sidebar.success('Archivo cargado satisfactoriamente')
    st.sidebar.write(f'<b>Nombre del Pozo</b>: {las_file.well.WELL.value}',unsafe_allow_html=True)


# Sidebar Navigation
st.sidebar.title('Navegacion')
options = st.sidebar.radio('Selecciona:', ['Home', 'Informacion del Encabezado', 'Datos de las curvas', 'Visualizacion', 'Net Pay'])

if options == 'Home':
    home.home()
elif options == 'Informacion del Encabezado':
    header.header(las_file)
elif options == 'Datos de las curvas':
    raw_data.raw_data(las_file, well_data)
elif options == 'Visualizacion':
    plotting.plot(las_file, well_data)
elif options == 'OIIP':
    oiip.oiip(las_file, well_data)

