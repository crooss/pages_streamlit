import streamlit as st
# streamlit run app.py


# Main entry point for the Streamlit application
def main():
    st.title("Streamlit Web Application")
    st.sidebar.title("Navigation")
    
    # Navigation options
    pages = {
        "Grafica Horaria": "pages/Grafica_horaria",
        "Conductancia específica": "pages/Conductancia_específica",
        "page3": "pages/page3"
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = None
    # print(list(pages.keys()))
    # Load the selected page
    if selection == "Grafica Horaria":
        import pages.Grafica_horaria as page
        print(page)
        page.Grafica_horaria()
    elif selection == "Conductancia específica":
        import pages.Conductancia_específica as page
        page.Conductancia_específica()
    elif selection == "page3":
        import pages.page3 as page
        page.page3()
    
    # Execute the selected page's run function
    # page.run()

if __name__ == "__main__":
    main()