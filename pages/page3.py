import streamlit as st
# from io import StringIO
import pandas as pd
from funct_geometry import Plot_geometry
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
            df=pd.DataFrame(dataframe)
            st.write(dataframe)
            
            option_columns_L = st.selectbox('Seleccionar la columna que contiene la longitud del defecto en mm', dataframe.columns, index=None)
            if option_columns_L:
                option_columns_W=st.selectbox('Seleccionar la columna que contiene el ancho del defecto en mm', dataframe.columns, index=None)
                if option_columns_W:
                    option_columns_t=st.selectbox('Seleccionar la columna que contiene el espesor nominal en mm', dataframe.columns, index=None)
                    if option_columns_t and option_columns_L and option_columns_W:
                        Plot_geometry(df, option_columns_W, option_columns_L, option_columns_t)
                        # Display the saved figure in Streamlit
                        st.image('images/Plot_geometry.png', caption='Anomaly dimesion class', use_container_width=True)
            
            


if __name__ == "__main__":
    page3()