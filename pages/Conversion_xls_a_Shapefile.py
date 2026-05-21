import streamlit as st
import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
from funciones import graficar, texto, radianes_a_horas
matplotlib.use('agg')


def xls_a_shp():
    st.title("Convertir xls a shapefile")
    
    # Widget para subir el archivo .xls o .xlsx
    uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xls", "xlsx"])

    if uploaded_file is not None:
        try:
            # Leemos el archivo cargado
            df = pd.read_excel(uploaded_file)
            
            st.success("¡Archivo cargado con éxito!")
            
            # Mostramos los datos en una tabla interactiva
            st.write("Vista previa de los datos:")
            st.dataframe(df)
            
        except Exception as e:
            st.error(f"Hubo un error al procesar el archivo: {e}")
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.write("coordenadas X")
        opciones_X = df.columns.tolist() if uploaded_file is not None else ["Opción 1", "Opción 2", "Opción 3"]
    with c2:
        st.write("coordenadas Y")
        opciones_Y = df.columns.tolist() if uploaded_file is not None else ["Opción 1", "Opción 2", "Opción 3"]

    # Crear el combobox
    seleccion = st.selectbox("Elige una opción:", opciones)
    
    nombre=st.text_input("Nombre de la anomalía", value="#1")
    angulo_inicio=st.number_input("Ángulo inicial [°]", min_value=0.0, max_value=360.0, format="%.4f", step=0.0001)
    angulo_final=st.number_input("Ángulo final [°]",min_value=0.0, max_value=360.0, format="%.4f", step=0.0001)
    PM=st.number_input("Pérdida de Metal [%]")/100
    if angulo_final and nombre and PM:
        graficar(angulo_inicio,angulo_final,nombre,PM)
        # Display the saved figure in Streamlit
        st.image('images/fig.png', caption='Generated Plot', use_container_width=True)
        # st.pyplot(graficar(angulo_inicio,angulo_final,nombre,PM)[1])
if __name__ == "__main__":
    xls_a_shp()
