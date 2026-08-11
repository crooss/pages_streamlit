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
        km=st.number_input("Km [m]:", step=0.1, value=0) # type: ignore
        if km or km==0:
            st.markdown(f"\nKm: {km:,.0f} m")

    with c2:
        Voltaje_AC=st.number_input("Voltaje AC [V]:", format="%.4f")
        if Voltaje_AC:
            st.markdown(f"\nVoltaje AC: {Voltaje_AC:,.3f} V")
        
    with c3:
        RESISTIVIDAD=st.number_input("Resistividad [Ω-cm]:", format="%.2f")
        if RESISTIVIDAD:
            st.markdown(f"\nResistividad: {RESISTIVIDAD:,.0f} Ω-cm")
        # Voltaje_AC=st.number_input("Voltaje AC [V]:", format="%.4f")
        # if Voltaje_AC and km:
        #     st.markdown(f"\nVoltaje AC: {Voltaje_AC:,.0f} V")
    c1, c2 = st.columns([2, 1])
    
    st.divider()
    if Voltaje_AC and RESISTIVIDAD:
        ruta=Graficos_Densidad_AC_custom(Voltaje_AC, RESISTIVIDAD, km , 20) # type: ignore
        st.image(ruta, caption='AC Corrosion', use_container_width=True) # type: ignore
        # Display the saved figure in Streamlit
        # st.pyplot(fig)
        # st.image('images/AC_Corrosion.png', caption='AC Corrosion', use_container_width=True)
    # st.image('images/AC_Corrosion.png', caption='AC Corrosion', use_container_width=True)
    # with c1:
    #     if (RESISTIVIDAD_1)>0 and (RESISTIVIDAD_2)>0:
    #         resistividad_avg=round(((RESISTIVIDAD_1)+(RESISTIVIDAD_2))/2,0)
    #         st.markdown(f"\nResistividad promedio: {resistividad_avg:,.2f} Ω-cm",)


if __name__ == "__main__":
    AC_Corrosion()