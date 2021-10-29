import streamlit as st
import pandas as pd

# Plotly imports
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px


def plot(las_file, well_data):
    st.title('Visualizacion del contenido del LAS')
    
    if not las_file:
        st.warning('No file has been uploaded')
    
    else:
        columns = list(well_data.columns)
        st.write('Expandir para visualizar los datos')

        with st.expander('Log Plot'):
            
            curves = st.multiselect('Seleccione las curvas a graficar', columns)
            if len(curves) <= 1:
                st.warning('Selecciones al menos dos curvas.')
            else:
                curve_index = 1
                fig = make_subplots(rows=1, cols= len(curves), subplot_titles=curves, shared_yaxes=True)

                for curve in curves:
                    fig.add_trace(go.Scatter(x=well_data[curve], y=well_data['DEPTH']), row=1, col=curve_index)
                    curve_index+=1
                
                fig.update_layout(height=1000, showlegend=False, yaxis={'title':'DEPTH','autorange':'reversed'})
                fig.layout.template='seaborn'
                st.plotly_chart(fig, use_container_width=True)
        
        with st.expander('Histogramas'):
            col1_h, col2_h = st.columns(2)
            col1_h.header('Options')

            hist_curve = col1_h.selectbox('Seleccione una curva', columns)
            log_option = col1_h.radio('Seleccione escala lineal o logaritmica', ('Linear', 'Logarithmic'))
            
            if log_option == 'Linear':
                log_bool = False
            elif log_option == 'Logarithmic':
                log_bool = True
            
            
            histogram = px.histogram(well_data, x=hist_curve, log_x=log_bool)
            #print(hist_curve)
            histogram.layout.template='seaborn'
            col2_h.plotly_chart(histogram, use_container_width=True)

        with st.expander('Crossplot'):
            col1, col2 = st.columns(2)
            col1.write('Opciones')

            xplot_x = col1.selectbox('Eje X', columns)
            xplot_y = col1.selectbox('Eje Y', columns)
            xplot_col = col1.selectbox('Colorear usando', columns)
            xplot_x_log = col1.radio('Eje X - Lineal o Logaritmica', ('Linear', 'Logarithmic'))
            xplot_y_log = col1.radio('Eje Y - Lineal o Logaritmica', ('Linear', 'Logarithmic'))

            if xplot_x_log == 'Linear':
                xplot_x_bool = False
            elif xplot_x_log == 'Logarithmic':
                xplot_x_bool = True
            
            if xplot_y_log == 'Linear':
                xplot_y_bool = False
            elif xplot_y_log == 'Logarithmic':
                xplot_y_bool = True

            col2.write('Crossplot')

            xplot = px.scatter(well_data, x=xplot_x, y=xplot_y, color=xplot_col, log_x=xplot_x_bool, log_y=xplot_y_bool)
            xplot.layout.template='seaborn'
            col2.plotly_chart(xplot, use_container_width=True)
