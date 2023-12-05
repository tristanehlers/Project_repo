import streamlit as st
import requests

# Define the API key and headers
api_key = 'OQfhKnmj2k9bUHmlHH9Qbg'  # Replace with your actual API key
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin/company/job'

# URL of the LinkedIn logo
logo_url = 'https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png'

# Set the geo_id parameter which the user cannot change
geo_id = '101282230'

# Function to capitalize labels
def capitalize_labels(options):
    return [option.replace('_', ' ').title() for option in options]

# Function to display jobs
def display_jobs(jobs):
    for job in jobs:
        st.write(f"**{job['job_title']}** at **{job['company']}**")
        st.write(f"Location: {job['location']}")
        st.write(f"Listed on: {job['list_date']}")
        st.write(f"[Job Details]({job['job_url']})")
        st.write("---------")

# Initialize session state variables
if 'jobs' not in st.session_state:
    st.session_state['jobs'] = []
    st.session_state['next_page_url'] = None
    st.session_state['search_initiated'] = False

# Adjust the column widths to align the logo with the end of the input fields
col1, col2 = st.columns([0.8, 0.2])

# Display the title in the first column
with col1:
    st.title("Job Search")

# Display the logo in the second column, adjusted to align with the inputs
with col2:
    st.image(logo_url, width=int(200 * 0.4))  # Adjust the size to 40% of the original

# Mapping of countries to their respective geo IDs
geo_ids = {
    'Germany': '101282230',
    'Switzerland': '106693272',
    'Austria': '103883259',
    'USA': '103644278',
    'France': '105015875',
    'Italy': '103350119'
}

# Create search fields for user input
country = st.selectbox('Country', list(geo_ids.keys()))
job_type = st.selectbox('Job Type', capitalize_labels(job_type_options))
experience_level = st.selectbox('Experience Level', capitalize_labels(experience_level_options))
when = st.selectbox('When', capitalize_labels(when_options))
flexibility = st.selectbox('Flexibility', capitalize_labels(flexibility_options))
keyword = st.text_input('Keyword', '')

# Container to display jobs below the input fields
jobs_container = st.container()

# Button to perform the API call
if st.button('Search Jobs'):
    st.session_state['search_initiated'] = True
    st.session_state['jobs'] = []  # Clear previous jobs
    selected_geo_id = geo_ids[country]  # Get the geo ID for the selected country
    # ... rest of the code for making the API call ...

# Function to load more jobs
# ... rest of the code for the load_more_jobs function ...

# Show the 'Load More' button only if a search has been initiated and there's a next page URL
if st.session_state['search_initiated'] and st.session_state['next_page_url']:
    st.button('Load More', on_click=load_more_jobs)
