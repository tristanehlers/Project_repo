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
    'Global': '92000000',
    'Austria': '103883259',
    'France': '105015875',
    'Germany': '101282230',
    'Italy': '103350119',
    'Switzerland': '106693272',
    'USA': '103644278'
}

# Initialize session state variables
if 'jobs' not in st.session_state:
    st.session_state['jobs'] = []
    st.session_state['next_page_url'] = None
    st.session_state['search_initiated'] = False

# Title and logo layout
header_col, logo_col = st.columns([0.85, 0.15])
with header_col:
    st.header("Job Search")
with logo_col:
    st.image(logo_url, width=60)  # Adjust width as needed

# Create search fields for user input
country = st.selectbox('Country', list(country_geo_id_mapping.keys()))
job_type = st.selectbox('Employment type', ['Anything', 'Full Time', 'Part Time', 'Internship', 'Contract', 'Temporary', 'Volunteer'])
experience_level = st.selectbox('Experience level', ['Anything', 'Internship', 'Entry Level', 'Associate', 'Mid-Senior Level', 'Director'])
when = st.selectbox('Job posted on', ['Anytime', 'Yesterday', 'Past-Week', 'Past-Month'])
flexibility = st.selectbox('Flexibility', ['Anything', 'Remote', 'On-Site', 'Hybrid'])
keyword = st.text_input('Keywords', '')

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
    else:
        st.error(f"Failed to retrieve jobs: {response.status_code}")

# Container to display jobs below the button
jobs_container = st.container()

# Function to display jobs
def display_jobs(jobs, container):
    for job in jobs:
        container.write(f"**{job['job_title']}** at **{job['company']}**")
        container.write(f"Location: {job['location']}")
        container.write(f"Listed on: {job['list_date']}")
        container.write(f"[Job Details]({job['job_url']})")
        container.write("---------")

# Display jobs if any
if st.session_state['jobs']:
    display_jobs(st.session_state['jobs'], jobs_container)

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
