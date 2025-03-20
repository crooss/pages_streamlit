import streamlit as st
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
from funciones import graficar, texto, radianes_a_horas
matplotlib.use('agg')


def Grafica_horaria():
    st.title("Realizar gráfico de posición horaria de una anomalía")
    nombre=st.text_input("Nombre de la anomalía", value="#1")
    angulo_inicio=st.number_input("Ángulo inicial [°]", min_value=0.0, max_value=360.0, format="%.4f")
    angulo_final=st.number_input("Ángulo final [°]",min_value=0.0, max_value=360.0, format="%.4f")
    PM=st.number_input("Pérdida de Metal [%]")/100
    if angulo_final and nombre and PM:
        graficar(angulo_inicio,angulo_final,nombre,PM)
        # Display the saved figure in Streamlit
        st.image('images/fig.png', caption='Generated Plot', use_container_width=True)

if __name__ == "__main__":
    Grafica_horaria()
