import streamlit as st

def page3():
    st.title("Page 3")
    st.write("Welcome to the third page of the Streamlit application!")
    st.write("This page can be used to display additional features or information.")
    
    # Example of an interactive widget
    user_input = st.text_input("Enter some text:")
    if user_input:
        st.write(f"You entered: {user_input}")

    # Example of a chart
    st.line_chart([1, 2, 3, 4, 5])

if __name__ == "__main__":
    page3()