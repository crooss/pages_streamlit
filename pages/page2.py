import streamlit as st
from functions import grafica_conductancia, tuberias_largas, tuberias_distribucion
def page2():
    st.title("Page 2")
    st.write("Welcome to the second page of the Streamlit application!")
    st.write("Here you can add different components and functionalities tailored to this page.")
    
    # Example components
    st.header("Interactive Widget Ejemplo")
    user_input = st.text_input("Enter some text:")
    if user_input:
        st.write(f"You entered: {user_input}")

    resistencia1, d1 = st.number_input("resistencia #1:"), st.number_input("Distancia #1 [cm]:")
    
    tipo_coating=st.selectbox('Tipo de Coating', ['FBE', 'PE', 'Epoxy'])
    tipo=st.selectbox('Tipo de Tubería', ['Tuberías largas con pocas ramificaciones', 'Distribución de Gas o Agua, con muchas ramificaciones'])
    valor_conductancia=200
    # tipo='Tuberías largas con pocas ramificaciones'
    # tipo='Distribución de Gas o Agua, con muchas ramificaciones'
    
    grafica_conductancia(valor_conductancia)
        
    
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
        
    
    
    st.header("Data Visualization Example")
    st.line_chart([1, 2, 3, 4, 5])  # Simple line chart

if __name__ == "__main__":
    page2()