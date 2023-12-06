import streamlit as st
import requests
import json

# Define your API key and headers
api_key = '_EIqMpWEbOnJLoQvNFz1CQ'  # Be sure to replace with your actual API key
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

# Function to extract information from API response
def extract_info(jsondata):
    extracted_info = {
        'full_name': jsondata.get('full_name', 'Not available'),
        'city': jsondata.get('city', 'Not available'),
        'experiences': jsondata.get('experiences', [])
    }
    return extracted_info

# Streamlit app layout
st.set_page_config(layout="wide")  # Set the page to wide layout

# Use columns to position the header and logo
col1, col2 = st.columns([5, 1])  # Adjust the ratio as needed for your layout

with col1:
    st.title('LinkedIn Profile Filler')

with col2:
    linkedin_logo_url = 'https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png'
    st.image(linkedin_logo_url, width=50)

# Input field for LinkedIn profile URL
linkedin_profile_url = st.text_input('Enter your LinkedIn profile URL', 'https://www.linkedin.com/in/...')

# Button to trigger the information retrieval
if st.button('Retrieve Information'):
    retrieve_info()

# Function to fetch and display profile information
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
