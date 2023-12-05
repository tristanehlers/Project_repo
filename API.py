import streamlit as st
import requests

# URL of the LinkedIn logo
logo_url = 'https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png'

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

# Initialize session state variables
if 'jobs' not in st.session_state:
    st.session_state['jobs'] = []
    st.session_state['next_page_url'] = None
    st.session_state['search_initiated'] = False

# Layout for the title and logo
header_col, logo_col = st.columns([8, 2])
with header_col:
    st.header("Job Search")
with logo_col:
    st.image(logo_url, width=60)

# Create search fields for user input
country = st.selectbox('Country', list(country_geo_id_mapping.keys()))
job_type = st.selectbox('Job Type', ['Anything', 'Full Time', 'Part Time', 'Internship', 'Contract', 'Temporary', 'Volunteer'])
experience_level = st.selectbox('Experience Level', ['Anything', 'Internship', 'Entry Level', 'Associate', 'Mid-Senior Level', 'Director'])
when = st.selectbox('When', ['Anytime', 'Yesterday', 'Past-Week', 'Past-Month'])
flexibility = st.selectbox('Flexibility', ['Anything', 'Remote', 'On-Site', 'Hybrid'])
keyword = st.text_input('Keyword', '')

# Function to display jobs
def display_jobs(jobs, container):
    for job in jobs:
        container.write(f"**{job['job_title']}** at **{job['company']}**")
        container.write(f"Location: {job['location']}")
        container.write(f"Listed on: {job['list_date']}")
        container.write(f"[Job Details]({job['job_url']})")
        container.write("---------")

# Container to hold the Search Jobs button
button_container = st.container()

# Container to display jobs below the input fields
jobs_container = st.container()

# Container to hold the Load More button
load_more_container = st.container()

# Inside the button_container, we place the Search Jobs button
with button_container:
    if st.button('Search Jobs'):
        st.session_state['search_initiated'] = True
        st.session_state['jobs'] = []  # Clear previous jobs
        selected_geo_id = country_geo_id_mapping[country]
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

# Inside the load_more_container, we place the Load More button
with load_more_container:
    if st.session_state['search_initiated'] and st.session_state['next_page_url']:
        if st.button('Load More'):
            load_more_jobs()
