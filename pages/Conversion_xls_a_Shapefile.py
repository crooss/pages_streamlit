import streamlit as st
import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
from funciones import graficar, texto, radianes_a_horas, df_to_shp
matplotlib.use('agg')


def xls_a_shp():
    st.title("Convertir xls a shapefile")
    
    # Widget para subir el archivo .xls o .xlsx
    uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xls", "xlsx"])

    if uploaded_file is not None:
        try:
            hojas=pd.ExcelFile(uploaded_file).sheet_names
            st.write("Hojas disponibles en el archivo:")
            hoja_seleccionada = st.selectbox("Selecciona la hoja de datos", hojas)
            # Leemos el archivo cargado
            df = pd.read_excel(uploaded_file, sheet_name=hoja_seleccionada)
            
            st.success(f"¡Archivo cargado con éxito! {uploaded_file.name}")
            
            # # Mostramos los datos en una tabla interactiva
            # st.write("Vista previa de los datos:")
            # st.dataframe(df)
            
        except Exception as e:
            st.error(f"Hubo un error al procesar el archivo: {e}")
    
    c1, c2= st.columns([1, 1])
    with c1:
        # st.write("coordenadas X")
        opciones_X = df.columns.tolist() if uploaded_file is not None else ["Opción 1", "Opción 2", "Opción 3"]
        seleccion_X = st.selectbox("coordenadas X:", opciones_X)
    with c2:
        # st.write("coordenadas Y")
        opciones_Y = df.columns.tolist() if uploaded_file is not None else ["Opción 1", "Opción 2", "Opción 3"]
        seleccion_Y = st.selectbox("coordenadas Y:", opciones_Y)

    opc_CRS= st.selectbox("Selecciona el sistema de referencia de coordenadas (CRS)", {"WGS 84": "EPSG:4326",
                                                                                       "UTM Zona 12N": "EPSG:32612",
                                                                                       "UTM Zona 13N": "EPSG:32613", 
                                                                                       "UTM Zona 14N": "EPSG:32614", 
                                                                                       "UTM Zona 15N": "EPSG:32615"})
    
    st.write(f"Has seleccionado: {seleccion_X} para X, {"\n"} {seleccion_Y} para Y, y el CRS: {opc_CRS}")
    
    if st.button("Convertir a Shapefile"):
        if uploaded_file is not None:
            try:
                df_to_shp(df, "shapefile_output", lat_col=seleccion_Y, lon_col=seleccion_X)
                st.success("¡Archivo convertido a Shapefile con éxito!")
            except Exception as e:
                st.error(f"Hubo un error al convertir el archivo: {e}")
        else:
            st.warning("Por favor, sube un archivo Excel antes de intentar convertirlo.")
            
            
    # seleccion_X = st.selectbox("Elige una opción:", opciones_X)
    # seleccion_Y = st.selectbox("Elige una opción:", opciones_Y)
   
    # nombre=st.text_input("Nombre de la anomalía", value="#1")
    # angulo_inicio=st.number_input("Ángulo inicial [°]", min_value=0.0, max_value=360.0, format="%.4f", step=0.0001)
    # angulo_final=st.number_input("Ángulo final [°]",min_value=0.0, max_value=360.0, format="%.4f", step=0.0001)
    # PM=st.number_input("Pérdida de Metal [%]")/100
    # if angulo_final and nombre and PM:
    #     graficar(angulo_inicio,angulo_final,nombre,PM)
    #     # Display the saved figure in Streamlit
    #     st.image('images/fig.png', caption='Generated Plot', use_container_width=True)
    #     # st.pyplot(graficar(angulo_inicio,angulo_final,nombre,PM)[1])
if __name__ == "__main__":
    xls_a_shp()
