import streamlit as st
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
from funciones import graficar, texto, radianes_a_horas, Modelado_mitigación_UHLIG
matplotlib.use('agg')
from scipy.interpolate import RegularGridInterpolator # type: ignore
from matplotlib.ticker import MultipleLocator, FuncFormatter # type: ignore
import matplotlib.ticker as ticker
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator,FormatStrFormatter)
from scipy.optimize import curve_fit
import warnings
from scipy.optimize import OptimizeWarning
warnings.filterwarnings("ignore", category=OptimizeWarning)
# from mpy_UHLIG import mpy_UGLIH


def Modelado():
    st.title("Realizar predicción de velocidad de corrosión vs potencial de protección catódica")
    # nombre=st.text_input("Nombre de la anomalía", value="#1")
    
    
    
    resistividad=st.number_input(r"Resistividad [$\Omega$ cm]", min_value=0, max_value=500000, step=10)
    ph=st.number_input("pH",min_value=0.0, max_value=14.0, format="%.1f", step=0.1)
    pot_off=st.number_input("Potencial Off [V]", format="%.3f", step=0.001)
    
    if resistividad and ph and pot_off:
        modelo1=Modelado_mitigación_UHLIG(resistividad, ph, pot_off)
        # Display the saved figure in Streamlit
        st.write(modelo1)
        # st.image('images/Modelo.png', caption='Modelo', use_container_width=True)
        # st.pyplot(graficar(angulo_inicio,angulo_final,nombre,PM)[1])
if __name__ == "__main__":
    Modelado()