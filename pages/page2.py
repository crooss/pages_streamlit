import streamlit as st
from functions import grafica_conductancia, tuberias_largas, tuberias_distribucion
import numpy as np
def page2():
    st.title("Page 2: graficos y calculos")
    st.write("Welcome to the second page of the Streamlit application!")
    st.write("Here you can add different components and functionalities tailored to this page.")
    
    # Example components
    st.header("Interactive Widget Ejemplo")
    user_input = st.text_input("Enter some text:")
    if user_input:
        st.write(f"You entered: {user_input}")

    st.header("Resistividad de suelos")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        resistencia1, d1 = st.number_input("resistencia #1:"), st.number_input("Distancia #1 [cm]:")
        if resistencia1 and d1:
            st.markdown(f"\nResistividad: {(2*np.pi*d1*resistencia1):,.2f} Ω-cm")
    with c2:
        resistencia2, d2 = st.number_input("resistencia #2:"), st.number_input("Distancia #2 [cm]:")
        if resistencia2 and d2:
            st.markdown(f"\nResistividad: {(2*np.pi*d2*resistencia2):,.2f} Ω-cm")
    c1, c2 = st.columns([2, 1])
    with c1:
        if (2*np.pi*d1*resistencia1)>0 and (2*np.pi*d2*resistencia2)>0:
            resistividad_avg=((2*np.pi*d1*resistencia1)+(2*np.pi*d2*resistencia2))/2
            st.markdown(f"\nResistividad promedio: {resistividad_avg:,.2f} Ω-cm",)
       
    st.divider()
    st.header("Conductancia de recubrimiento")
    valor_conductancia=st.number_input("Conductancia:")
    
    tipo_coating=st.selectbox('Tipo de Coating', 
                              ['','FBE', 'PE', 'Alquitrán de hulla','Tricapa','Visco-elastico', 'Otros'],
                              index=0)  # Set default value to the first option
    tipo=st.selectbox('Tipo de Tubería', 
        ['','Tuberías largas con pocas ramificaciones', 'Distribución de Gas o Agua, con muchas ramificaciones'], 
        index=0)  # Set default value to the first option
    if tipo and tipo_coating:
        grafica_conductancia(valor_conductancia, tipo)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image('images/barras_CP4.png', caption='Grafico de barras CP4', width=300)
    if tipo_coating=='FBE':
        if tipo=='Tuberías largas con pocas ramificaciones':
            tuberias_largas(valor_conductancia)
            st.image('images/tuberias_largas.png', caption='Tuberías largas con pocas ramificaciones', use_container_width=True)
        elif tipo=='Distribución de Gas o Agua, con muchas ramificaciones':
            tuberias_distribucion(valor_conductancia)
            st.image('images/tuberias_distribucion.png', caption='Tuberías largas con pocas ramificaciones', use_container_width=True)
        
    
    
    # st.header("Data Visualization Example")
    # st.line_chart([1, 2, 3, 4, 5])  # Simple line chart

if __name__ == "__main__":
    page2()