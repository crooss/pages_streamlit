import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import math
from modulos import num2station
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from funciones import Graficos_Densidad_AC_custom

def AC_Corrosion():
    st.title("Calculo de conductancia específica de recubrimiento")
    # st.write("Welcome to the second page of the Streamlit application!")
    # st.write("Here you can add different components and functionalities tailored to this page.")

    st.header("1.-Datos de entrada")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        # resistencia1, d1 = st.number_input("resistencia #1:", format="%.4f"), st.number_input("Distancia #1 [cm]:")
        km=st.number_input("Km [m]:", step=1)
    with c2:
        Voltaje_AC=st.number_input("Voltaje AC [V]:", format="%.4f")
        if Voltaje_AC and km:
            st.markdown(f"\nVoltaje AC: {Voltaje_AC:,.0f} V")
        
    with c3:
        RESISTIVIDAD=st.number_input("Resistividad [Ω-cm]:", format="%.2f")
        if RESISTIVIDAD and km:
            st.markdown(f"\nResistividad: {RESISTIVIDAD:,.0f} Ω-cm")
        # Voltaje_AC=st.number_input("Voltaje AC [V]:", format="%.4f")
        # if Voltaje_AC and km:
        #     st.markdown(f"\nVoltaje AC: {Voltaje_AC:,.0f} V")
    c1, c2 = st.columns([2, 1])
    
    st.divider()
    
    st.write(Graficos_Densidad_AC_custom(Voltaje_AC,RESISTIVIDAD, km , 20), use_container_width=True) # type: ignore
    # with c1:
    #     if (RESISTIVIDAD_1)>0 and (RESISTIVIDAD_2)>0:
    #         resistividad_avg=round(((RESISTIVIDAD_1)+(RESISTIVIDAD_2))/2,0)
    #         st.markdown(f"\nResistividad promedio: {resistividad_avg:,.2f} Ω-cm",)


if __name__ == "__main__":
    AC_Corrosion()