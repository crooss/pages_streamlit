import streamlit as st
# streamlit run app.py


# Main entry point for the Streamlit application
def main():
    st.title("Web Application")
    # st.sidebar.title("Navigation")
    
    # Navigation options
    pages = {
        "Grafica Horaria": "pages/Grafica_horaria",
        "Conductancia específica": "pages/Conductancia_específica",
        "Geometry": "pages/page3"
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()), index=None)
    page = None

    # Load the selected page
    if selection == "Grafica Horaria":
        import pages.Grafica_horaria as page
        page.Grafica_horaria()
    elif selection == "Conductancia específica":
        import pages.Conductancia_específica as page
        page.Conductancia_específica()
    elif selection == "Geometry":
        import pages.page3 as page
        page.page3()
    
    # Execute the selected page's run function
    # page.run()

if __name__ == "__main__":
    main()