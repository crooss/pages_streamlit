import streamlit as st
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
from functions import graficar, texto, radianes_a_horas
matplotlib.use('agg')
# plt.rcParams['font.family'] = 'Century Gothic'

def Grafica_horaria():
    st.title("Welcome to Page 1")
    st.write("This is the first page of the Streamlit application.")
    
    # Example of an interactive widget
    nombre=st.text_input("Nombre de la anomalia", value="#1")
    angulo_inicio=st.number_input("Angulo inicial", min_value=0.0, max_value=360.0, format="%.2f")
    angulo_final=st.number_input("Angulo final",min_value=0.0, max_value=360.0, format="%.2f")
    PM=st.number_input("PM")/100

    # if name:
    st.write(f"El texto es, {texto('arturo')}!")
    
    if angulo_final and nombre and PM:
        graficar(angulo_inicio,angulo_final,nombre,PM)
        # Display the saved figure in Streamlit
        st.image('images/fig.png', caption='Generated Plot', use_container_width=True)
    
    # Example of a chart
    # st.line_chart([1, 2, 3, 4, 5])

if __name__ == "__main__":
    Grafica_horaria()
