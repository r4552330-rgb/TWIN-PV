import streamlit as st

# Title of the application
st.title('My Sample Streamlit Dashboard')

# Sidebar navigation
st.sidebar.title('Navigation')
option = st.sidebar.selectbox('Select Section', ['Home', 'Data', 'Visualizations'])

# Sample sections
if option == 'Home':
    st.subheader('Welcome to the Home Page!')
    st.write('This is a simple Streamlit dashboard.')
elif option == 'Data':
    st.subheader('Data Section')
    st.write('Here you can include your data analysis.')
elif option == 'Visualizations':
    st.subheader('Visualizations Section')
    st.write('Here you can include your visualizations.')