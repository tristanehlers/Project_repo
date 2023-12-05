import streamlit as st
import requests

# Define the API key and headers
api_key = 'OQfhKnmj2k9bUHmlHH9Qbg'  # Replace with your actual API key
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin/company/job'

# URL of the LinkedIn logo
logo_url = 'https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png'

# Country to geo_id mapping
country_geo_id_mapping = {
    'Germany': '101282230',
    'Switzerland': '106693272',
    'Austria': '103883259',
    'USA': '103644278',
    'France': '105015875',
    'Italy': '103350119'
}

# Function to display jobs
def display_jobs(jobs, container):
    for job in jobs:
        container.write(f"**{job['job_title']}** at **{job['company']}**")
        container.write(f"Location: {job['location']}")
        container.write(f"Listed on: {job['list_date']}")
        container.write(f"[Job Details]({job['job_url']})")
        container.write("---------")

# Initialize session state variables
if 'jobs' not in st.session_state:
    st.session_state['jobs'] = []
    st.session_state['next_page_url'] = None
    st.session_state['search_initiated'] = False

# Adjust layout for the title and logo
col1, col2 = st.columns([0.8, 0.2])
with col1:
    st.title("Job Search")

with col2:
    st.image(logo_url, width=40)  # Adjust width as needed to fit the end of the input boxes

# Create search fields for user input
country = st.selectbox('Country', list(country_geo_id_mapping.keys()))
job_type = st.selectbox('Job Type', ['Anything', 'Full Time', 'Part Time', 'Internship', 'Contract', 'Temporary', 'Volunteer'])
experience_level = st.selectbox('Experience Level', ['Anything', 'Internship', 'Entry Level', 'Associate', 'Mid-Senior Level', 'Director'])
when = st.selectbox('When', ['Anytime', 'Yesterday', 'Past-Week', 'Past-Month'])
flexibility = st.selectbox('Flexibility', ['Anything', 'Remote', 'On-Site', 'Hybrid'])
keyword = st.text_input('Keyword', '')

# Container to display jobs below the input fields
jobs_container = st.container()

# Button to perform the API call
if st.button('Search Jobs'):
    st.session_state['search_initiated'] = True
    st.session_state['jobs'] = []  # Clear previous jobs
    selected_geo_id = country_geo_id_mapping[country]  # Use the selected country's geo_id
    params = {
        'job_type': job_type.replace(' ', '_').lower(),
        'experience_level': experience_level.replace(' ', '_').lower(),
        'when': when.replace(' ', '_').lower(),
        'flexibility': flexibility.replace(' ', '_').lower(),
        'geo_id': selected_geo_id,
        'keyword': keyword
    }
    response = requests.get(api_endpoint, params=params, headers=headers)
    if response.status_code == 200:
        st.session_state['jobs'] = response.json().get('job', [])
        st.session_state['next_page_url'] = response.json().get('next_page_api_url')
        display_jobs(st.session_state['jobs'], jobs_container)
    else:
        st.error(f"Failed to retrieve jobs: {response.status_code}")

# Function to load more jobs
def load_more_jobs():
    next_page_url = st.session_state['next_page_url']
    if next_page_url:
        response = requests.get(next_page_url, headers=headers)
        if response.status_code == 200:
            new_jobs = response.json().get('job', [])
            st.session_state['jobs'].extend(new_jobs)
            st.session_state['next_page_url'] = response.json().get('next_page_api_url')
            display_jobs(st.session_state['jobs'], jobs_container)
        else:
            st.error(f"Failed to load more jobs: {response.status_code}")

# Show the 'Load More' button only if a search has been initiated and there's a next page URL
if st.session_state['search_initiated'] and st.session_state['next_page_url']:
    st.button('Load More', on_click=load_more_jobs)
