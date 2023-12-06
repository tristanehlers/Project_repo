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
st.title('LinkedIn Profile Filler')

# Input field for LinkedIn profile URL
linkedin_profile_url = st.text_input('Enter your LinkedIn profile URL', 'https://www.linkedin.com/in/...')

# Display the clickable image
if st.button('Retrieve Information'):
    retrieve_info()

def retrieve_info():
    params = {'linkedin_profile_url': linkedin_profile_url}
    
    # Make a request to the API
    response = requests.get(api_endpoint, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        info = extract_info(data)
        
        # Display the extracted information
        st.subheader('Profile Information:')
        st.write('Full Name:', info['full_name'])
        st.write('City:', info['city'])
        
        st.subheader('Experiences:')
        for exp in info['experiences']:
            st.write('Title:', exp.get('title', 'Not available'))
            st.write('Company:', exp.get('company', 'Not available'))
            st.write('Description:', exp.get('description', 'Not available'))
            st.write('---')  # Separator line
    else:
        st.error(f"Failed to retrieve profile information: HTTP {response.status_code}")

# Load the image from the
