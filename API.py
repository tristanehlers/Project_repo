import streamlit as st
import requests

# Define the API key and headers
api_key = 'OQfhKnmj2k9bUHmlHH9Qbg'
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin/company/job'

# Country to geo_id mapping
country_geo_id_mapping = {
    'Germany': '101282230',
    'Switzerland': '106693272',
    'Austria': '103883259',
    'USA': '103644278',
    'France': '105015875',
    'Italy': '103350119'
}

# Function to capitalize labels
def capitalize_labels(options):
    return [option.replace('_', ' ').title() for option in options]

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

# Title and logo layout
col1, col2 = st.columns([8, 2])
with col1:
    st.write("")
with col2:
    st.image('https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png', width=60)

# Adjusting the title position
st.markdown("<h1 style='text-align: center; margin-bottom: -20px;'>Job Search</h1>", unsafe_allow_html=True)

# Create search fields for user input
country = st.selectbox('Country', list(country_geo_id_mapping.keys()))
job_type = st.selectbox('Job Type', capitalize_labels(['anything', 'full_time', 'part_time', 'internship', 'contract', 'temporary', 'volunteer']))
experience_level = st.selectbox('Experience Level', capitalize_labels(['anything', 'internship', 'entry_level', 'associate', 'mid_senior_level', 'director']))
when = st.selectbox('When', capitalize_labels(['anytime', 'yesterday', 'past-week', 'past-month']))
flexibility = st.selectbox('Flexibility', capitalize_labels(['anything', 'remote', 'on-site', 'hybrid']))
keyword = st.text_input('Keyword', '')

# Container for displaying jobs, placed in the right order
jobs_container = st.container()

# Button to perform the API call
if st.button('Search Jobs'):
    st.session_state['search_initiated'] = True
    st.session_state['jobs'] = []  # Clear previous jobs
    selected_geo_id = country_geo_id_mapping[country]
    params = {
        'job_type': job_type.lower().replace(' ', '_'),
        'experience_level': experience_level.lower().replace(' ', '_'),
        'when': when.lower().replace(' ', '_'),
        'flexibility': flexibility.lower().replace(' ', '_'),
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
