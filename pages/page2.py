import streamlit as st
from functions import grafica_conductancia
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
    grafica_conductancia(200)
    st.image('images/barras_CP4.png', caption='Grafico de barras CP4', use_container_width=True)
    
    st.header("Data Visualization Example")
    st.line_chart([1, 2, 3, 4, 5])  # Simple line chart

if __name__ == "__main__":
    page2()