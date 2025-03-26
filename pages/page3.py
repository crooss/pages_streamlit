import streamlit as st
from io import StringIO
import pandas as pd

def page3():
    st.title("Page 3")
    st.write("Welcome to the third page of the Streamlit application!")
    st.write("This page can be used to display additional features or information.")
    
    # Example of an interactive widget
    # user_input = st.text_input("Enter some text:")
    # if user_input:
    #     st.write(f"You entered: {user_input}")

    # Example of a chart
    # st.line_chart([1, 2, 3, 4, 5])
    
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # List all sheet names in the uploaded Excel file
        xl = pd.ExcelFile(uploaded_file)
        sheet_names = xl.sheet_names
        # st.write(sheet_names)
        option = st.selectbox('Seleccionar la Hoja de origen de datos',(sheet_names), index=None)
        if option:
            dataframe = pd.read_excel(uploaded_file, sheet_name=option)
            st.write(dataframe)
    #     # To read file as bytes:
    #     bytes_data = uploaded_file.getvalue()
    #     st.write(bytes_data)

    #     # To convert to a string based IO:
    #     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    #     st.write(stringio)

    #     # To read file as string:
    #     string_data = stringio.read()
    #     st.write(string_data)

    #     # Can be used wherever a "file-like" object is accepted:

    #     st.write(dataframe)

if __name__ == "__main__":
    page3()