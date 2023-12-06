import streamlit as st
import requests

# Define your API key and headers
api_key = '_EIqMpWEbOnJLoQvNFz1CQ'  # Be sure to replace with your actual API key
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

# Streamlit app layout
st.set_page_config(layout="wide")  # Set the page layout to wide

# Create columns for the header and the LinkedIn logo
header_col, logo_col = st.columns([0.9, 0.1])

# Use the first column to display the app title
with header_col:
    st.title('LinkedIn Profile Filler')

# Use the second column to display the LinkedIn logo
with logo_col:
    linkedin_logo_url = 'https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png'
    st.image(linkedin_logo_url, width=50)

# Function to extract information from API response
def extract_info(jsondata):
    extracted_info = {
        'full_name': jsondata.get('full_name', 'Not available'),
        'city': jsondata.get('city', 'Not available'),
        'experiences': jsondata.get('experiences', [])
    }
    return extracted_info

# Function to retrieve information
def retrieve_info():
    params = {'linkedin_profile_url': linkedin_profile_url}
    response = requests.get(api_endpoint, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        info = extract_info(data)
        display_info(info)
    else:
        st.error(f"Failed to retrieve profile information: HTTP {response.status_code}")

# Function to display profile information
def display_info(info):
    st.subheader('Profile Information:')
    st.write('Full Name:', info['full_name'])
    st.write('City:', info['city'])
    
    st.subheader('Experiences:')
    for exp in info['experiences']:
        st.write('Title:', exp.get('title', 'Not available'))
        st.write('Company:', exp.get('company', 'Not available'))
        st.write('Description:', exp.get('description', 'Not available'))
        st.write('---')  # Separator line

# Input field for LinkedIn profile URL
linkedin_profile_url = st.text_input('Enter your LinkedIn profile URL')

# Button to trigger the information retrieval
if st.button('Retrieve Information'):
    retrieve_info()
