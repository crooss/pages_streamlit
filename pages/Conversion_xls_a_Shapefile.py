import streamlit as st
import pandas as pd
import matplotlib
from funciones import df_to_shp
matplotlib.use('agg')


def xls_a_shp():
    st.title("Convertir xls a shapefile")
    
    # Widget para subir el archivo .xls o .xlsx
    uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xls", "xlsx"])

    if uploaded_file is not None:
        try:
            hojas=pd.ExcelFile(uploaded_file).sheet_names
            st.write("Hojas disponibles en el archivo:")
            hoja_seleccionada = st.selectbox("Selecciona la hoja de datos", hojas)
            # Leemos el archivo cargado
            df = pd.read_excel(uploaded_file, sheet_name=hoja_seleccionada)
            
            st.success(f"¡Archivo cargado con éxito! {uploaded_file.name}")
            
            # # Mostramos los datos en una tabla interactiva
            # st.write("Vista previa de los datos:")
            # st.dataframe(df)
            
        except Exception as e:
            st.error(f"Hubo un error al procesar el archivo: {e}")
    
    if uploaded_file and df is not None:
        c1, c2= st.columns([1, 1])
        with c1:
            # st.write("coordenadas X")
            opciones_X = df.columns.tolist() if uploaded_file is not None else ["Opción 1", "Opción 2", "Opción 3"]
            seleccion_X = st.selectbox("coordenadas X:", opciones_X)
        with c2:
            # st.write("coordenadas Y")
            opciones_Y = df.columns.tolist() if uploaded_file is not None else ["Opción 1", "Opción 2", "Opción 3"]
            seleccion_Y = st.selectbox("coordenadas Y:", opciones_Y)

        if seleccion_X and seleccion_Y:
            st.write(f"Coordenada X: {seleccion_X}")
            st.write(f"Coordenada Y: {seleccion_Y}")
            
            diccionario_crs = {"WGS 84": "EPSG:4326",
                                "UTM Zona 12N": "EPSG:32612",
                                "UTM Zona 13N": "EPSG:32613",
                                "UTM Zona 14N": "EPSG:32614",
                                "UTM Zona 15N": "EPSG:32615"
                                }
            
            opc_CRS= st.selectbox("Selecciona el sistema de referencia de coordenadas (CRS)", list(diccionario_crs.keys()))
        
            st.write(f"CRS: {diccionario_crs[opc_CRS]}")
    
    if uploaded_file is not None and seleccion_X and seleccion_Y and opc_CRS:
        creado=""
        st.button("Convertir a Shapefile")

        try:
            shape_name=f"{opc_CRS}_{uploaded_file.name.split('.xlsx')[0]}"
            shapefile_path = df_to_shp(df, lat_col=seleccion_Y, lon_col=seleccion_X, EPSG_code=diccionario_crs[opc_CRS], shape_name=shape_name)
            creado=1
            st.success("¡Archivo convertido a Shapefile con éxito!")   
        except Exception as e:
            st.error(f"Hubo un error al convertir el archivo: {e}")
    else:
        st.warning("Por favor, sube un archivo Excel antes de intentar convertirlo.")
    
    # st.divider()
    
        if creado==1: # type: ignore
            nombre_archivo =f'images/{shape_name}.shp.zip'

            with open(nombre_archivo, "rb") as archivo:
                st.download_button(
                    label="Descargar archivo",
                    data=archivo,
                    file_name=nombre_archivo.split('images/')[1],
                    mime="application/zip"
                )

            
    
    # st.write(f"Path del shapefile generado: {shapefile_path}")
if __name__ == "__main__":
    xls_a_shp()
