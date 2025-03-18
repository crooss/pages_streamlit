import streamlit as st

def page2():
    st.title("Page 2")
    st.write("Welcome to the second page of the Streamlit application!")
    st.write("Here you can add different components and functionalities tailored to this page.")
    
    # Example components
    st.header("Interactive Widget Ejemplo")
    user_input = st.text_input("Enter some text:")
    if user_input:
        st.write(f"You entered: {user_input}")

    st.header("Data Visualization Example")
    st.line_chart([1, 2, 3, 4, 5])  # Simple line chart

if __name__ == "__main__":
    page2()