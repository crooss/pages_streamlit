import streamlit as st
from functions import grafica_conductancia, tuberias_largas, tuberias_distribucion
import numpy as np

def all_values_present(values):
    return all(value is not None and value != '' for value in values)

def page2():
    st.title("Calculo de conductancia específica de recubrimiento")
    # st.write("Welcome to the second page of the Streamlit application!")
    # st.write("Here you can add different components and functionalities tailored to this page.")

    st.header("1.-Resistividad de suelos")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        resistencia1, d1 = st.number_input("resistencia #1:", format="%.4f"), st.number_input("Distancia #1 [cm]:")
        km_1=st.number_input("Km #1 [m]:", step=1)
        if resistencia1 and d1:
            st.markdown(f"\nResistividad: {(2*np.pi*d1*resistencia1):,.0f} Ω-cm")
    with c2:
        resistencia2, d2 = st.number_input("resistencia #2:", format="%.4f"), st.number_input("Distancia #2 [cm]:")
        km_2=st.number_input("Km #2 [m]:", step=1)
        if resistencia2 and d2:
            st.markdown(f"\nResistividad: {(2*np.pi*d2*resistencia2):,.0f} Ω-cm")
    c1, c2 = st.columns([2, 1])
    with c1:
        if (2*np.pi*d1*resistencia1)>0 and (2*np.pi*d2*resistencia2)>0:
            resistividad_avg=round(((2*np.pi*d1*resistencia1)+(2*np.pi*d2*resistencia2))/2,0)
            st.markdown(f"\nResistividad promedio: {resistividad_avg:,.2f} Ω-cm",)


    
    
    
    
    st.divider()
    st.header("2.-Calibración de tramo en estación de 4 pines")
    
    st.subheader("Resistencia del tramo #1")
    c1, c2, c3 = st.columns([1, 1.3, 2])
    with c1:
        caida_1_on, caida_1_off = st.number_input("Caída IR en ON #1 [mV]:",format="%0.3f"), st.number_input("Caída IR en OFF #1 [mV]:")
    with c2:
        corriente_prueba_1_on, corriente_prueba_1_off = st.number_input("Corriente prueba ON #1 [mA]:"), st.number_input("Corriente prueba OFF #1 [mA]:")
    
    if caida_1_on and caida_1_off and corriente_prueba_1_on:
        R_tramo1=(caida_1_on-caida_1_off)/(corriente_prueba_1_on-corriente_prueba_1_off)
        st.markdown(f"Resistencia del tramo #1: {((R_tramo1)):,.6f} Ω")

    st.subheader("Resistencia del tramo #2")
    c1, c2, c3 = st.columns([1, 1.3, 2])
    with c1:
        caida_2_on, caida_2_off = st.number_input("Caída IR en ON #2 [mV]:",format="%0.3f"), st.number_input("Caída IR en OFF #2 [mV]:")
    with c2:
        corriente_prueba_2_on, corriente_prueba_2_off = st.number_input("Corriente prueba ON #2 [mA]:"), st.number_input("Corriente prueba OFF #2 [mA]:")
    
    if caida_2_on and caida_2_off and corriente_prueba_2_on:
        R_tramo2=(caida_2_on-caida_2_off)/(corriente_prueba_2_on-corriente_prueba_2_off)
        st.markdown(f"Resistencia del tramo #2: {((R_tramo2)):,.6f} Ω")
    
    st.divider()    
    st.header("3.-USANDO CORRIENTE DEL RPC")

    c1, c2, c3 = st.columns([1.4, 1.4, 1])
    with c1:
        st.subheader("Para tramo #1")
        Potencial_ON_1, Potencial_OFF_1 = st.number_input("Potencial ON #1 [V]:",format="%.4f"), st.number_input("Potencial OFF #1 [V]:",format="%0.3f")
        delta_pot_1=abs(Potencial_ON_1-Potencial_OFF_1)
        st.markdown(f"∆v [V]: {delta_pot_1:,.3f}")
    
    with c2:
        st.subheader("Para tramo #2")
        Potencial_ON_2, Potencial_OFF_2 = st.number_input("Potencial ON #2 [V]:",format="%0.3f"), st.number_input("Potencial OFF #2 [V]:",format="%0.3f")
        delta_pot_2=abs(Potencial_ON_2-Potencial_OFF_2)
        
    if Potencial_ON_1 and Potencial_OFF_1 and Potencial_ON_2 and Potencial_OFF_2:
        st.markdown(f"∆v [V]: {delta_pot_2:,.3f} V")
        ratio_deltas=delta_pot_1/delta_pot_2
    
        promedio_deltas=(delta_pot_1+delta_pot_2)/2
        st.markdown(f"Promedio de ∆v={round((delta_pot_1+delta_pot_2)/2,4)}")
        
        if ratio_deltas>0.625 or ratio_deltas<1.6:
            st.markdown(f"∆va/∆vb={round(ratio_deltas,3)}")
            st.markdown(f"NOTE 6: If the ratio of the ΔV potentials from each pair of adjacent test locations is between 1.6 and 0.625, then the arithmetic mean of the two can be taken as the average potential change in the section of pipeline between these test locations.1 However, if the ratio is outside this range, then one or more intermediate locations should be selected for the potential measurements until the ratio between two successive values is between 1.6 and 0.625. Alternatively, one of the attenuation methods outlined in Section 4 can be used.")
    
    st.subheader("Caída de Voltaje en el tramo usando la corriente del RPC")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        caida_rpc_1_on, caida_rpc_1_off = st.number_input("Caída de voltaje #1 ON [mV]:",format="%0.3f"), st.number_input("Caída de voltaje #1 OFF [mV]:",format="%0.3f")
    with c2:
        caida_rpc_2_on, caida_rpc_2_off = st.number_input("Caída de voltaje #2 ON [mV]::",format="%0.3f"), st.number_input("Caída de voltaje #2 OFF [mV]:",format="%0.3f")
    
    if caida_rpc_1_on and caida_rpc_1_off and caida_rpc_2_on and caida_rpc_2_off:
        delta1=abs(caida_rpc_1_on-caida_rpc_1_off)
        st.markdown(f"delta1 [V]: {delta1:,.3f}")
        delta2=abs(caida_rpc_2_on-caida_rpc_2_off)
        I_pick_1=abs(delta1/1000/R_tramo1)
        I_pick_2=abs(delta2/1000/R_tramo2)
        st.markdown(f"Corriente de Pickering #1: {I_pick_1:,.3f} A")
        st.markdown(f"Corriente de Pickering #2: {I_pick_2:,.3f} A")    
    st.divider()  
    st.header("4.-Conductancia de recubrimiento")
    
    st.subheader(f"Conductancia de recubrimiento g [S]: {(abs(I_pick_1-I_pick_2)/promedio_deltas):,.2f} S")
    diametro_in=st.number_input("Diametro [in]:",format="%0.3f", step=0.05)
    
    if diametro_in>0:
        diametro_m=diametro_in*0.0254
        Longitud_tramo=abs(km_1-km_2)
        area_coated=(np.pi*diametro_m)*Longitud_tramo
        st.markdown(f"Area del tramo: {area_coated:,.2f} m²")
    
        conducatancia_especifica=1000000*(abs(I_pick_1-I_pick_2)/promedio_deltas/area_coated)
        st.markdown(f"Conductancia especifica: {conducatancia_especifica:,.0f} μS/m² @ {resistividad_avg:,.2f} Ω-cm")
    
        st.subheader(f"Normalizacion de Conductancia especifica @ 1,000 Ω-cm")
    
        NORM_conductancia_especifica=conducatancia_especifica*resistividad_avg/1000
        st.subheader(f"Conductancia especifica normalizada: {NORM_conductancia_especifica:,.0f} μS/m²")
        # valor_conductancia=st.number_input("Conductancia:")
        valor_conductancia=conducatancia_especifica
    
        tipo_coating=st.selectbox('Tipo de Coating', 
                              ['','FBE', 'PE', 'Alquitrán de hulla','Tricapa','Visco-elastico', 'Otros'],
                              index=0)  # Set default value to the first option
        tipo=st.selectbox('Tipo de Tubería', 
        ['','Tuberías largas con pocas ramificaciones', 'Distribución de Gas o Agua, con muchas ramificaciones'], 
        index=0)  # Set default value to the first option
        st.header("5.-Resultados")
        if tipo and tipo_coating:
            grafica_conductancia(valor_conductancia, tipo)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image('images/barras_CP4.png', caption='Conductancia específica μS/m² y clasificación', width=300)
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
    print(all_values_present[1, 2, 3, '', 5])