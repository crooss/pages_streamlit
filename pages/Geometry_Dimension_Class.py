import streamlit as st
# from io import StringIO
import pandas as pd
from funct_geometry import Plot_geometry
def Geometry_Dimension_Class():
    st.title("Anomaly Dimesion Class")
    st.subheader("Esta aplicacion ayuda a la creacion de un grafico de clasificaciones de dimensiones de corridas instrumentadas")
    st.write("Los datos necesarios para la creacion del grafico son:")
    st.markdown(''':orange[Longitud de anomalia en mm]  
                   :orange[Ancho de anomalia en mm]  
                   :orange[Espesor nominal en mm]''')
    
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # List all sheet names in the uploaded Excel file
        xl = pd.ExcelFile(uploaded_file)
        sheet_names = xl.sheet_names
        # st.write(sheet_names)
        option = st.selectbox('Seleccionar la Hoja de origen de datos',(sheet_names), index=None, placeholder="Seleccione la hoja de datos")
        if option:
            dataframe = pd.read_excel(uploaded_file, sheet_name=option)
            df=pd.DataFrame(dataframe)
            with st.expander("Ver datos de entrada"):
                st.write(dataframe)
            
            option_columns_L = st.selectbox('Seleccionar la columna que contiene la longitud del defecto en mm', dataframe.columns, index=None, placeholder="Seleccione Longitud en mm")
            if option_columns_L:
                option_columns_W=st.selectbox('Seleccionar la columna que contiene el ancho del defecto en mm', dataframe.columns, index=None, placeholder="Seleccione Ancho en mm")
                if option_columns_W:
                    option_columns_t=st.selectbox('Seleccionar la columna que contiene el espesor nominal en mm', dataframe.columns, index=None, placeholder="Seleccione Espesor en mm")
                    if option_columns_t and option_columns_L and option_columns_W:
                        extent_xy=st.radio("Extensión del eje x y eje y", [10,20,30], index=None)
                        if extent_xy:
                            Plot_geometry(df, option_columns_W, option_columns_L, option_columns_t, extent_xy)
                            # Display the saved figure in Streamlit
                            st.image('images/Plot_geometry.png', caption='Anomaly dimesion class', use_container_width=True)

if __name__ == "__main__":
    Geometry_Dimension_Class()