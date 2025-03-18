import streamlit as st

# Main entry point for the Streamlit application
def main():
    st.title("Streamlit Web Application")
    st.sidebar.title("Navigation")
    
    # Navigation options
    pages = {
        "Grafica Horaria": "pages/Grafica_horaria",
        "Pagina 2": "pages/page2.py",
        "Pagina 3": "pages/page3.py"
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = None
    print(list(pages.keys()))
    # Load the selected page
    if selection == "Grafica Horaria":
        import pages.Grafica_horaria as page
        print(page)
        page.Grafica_horaria()
    elif selection == "Page 2":
        import pages.page2 as page
    elif selection == "Page 3":
        import pages.page3 as page
    
    # Execute the selected page's run function
    # page.run()

if __name__ == "__main__":
    main()