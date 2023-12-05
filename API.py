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

# Function to capitalize labels
def capitalize_labels(options):
    return [option.replace('_', ' ').title() for option in options]

# Initialize session state variables
if 'jobs' not in st.session_state:
    st.session_state['jobs'] = []
    st.session_state['next_page_url'] = None
    st.session_state['search_initiated'] = False

# Title and logo layout
st.title("Job Search")
col1, col2 = st.columns([0.85, 0.15])
with col1:
    st.write("")  # Spacer to align title with the input fields
with col2:
    st.image(logo_url, width=int(200 * 0.4))  # Adjust the size to 40% of the original

# Create search fields for user input
country = st.selectbox('Country', list(country_geo_id_mapping.keys()))
job_type_options = ['anything', 'full_time', 'part_time', 'internship', 'contract', 'temporary', 'volunteer']
experience_level_options = ['anything', 'internship', 'entry_level', 'associate', 'mid_senior_level', 'director']
when_options = ['anytime', 'yesterday', 'past-week', 'past-month']
flexibility_options = ['anything', 'remote', 'on-site', 'hybrid']

job_type = st.selectbox('Job Type', capitalize_labels(job_type_options))
experience_level = st.selectbox('Experience Level', capitalize_labels(experience_level_options))
when = st.selectbox('When', capitalize_labels(when_options))
flexibility = st.selectbox('Flexibility', capitalize_labels(flexibility_options))
keyword = st.text_input('Keyword', '')

# Button to perform the API call
if st.button('Search Jobs'):
    st.session_state['search_initiated'] = True
    st.session_state['jobs'] = []  # Clear previous jobs
    selected_geo_id = country_geo_id_mapping[country]  # Use the selected country's geo_id
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
        with st.container():
            display_jobs(st.session_state['jobs'])
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
            with st.container():
                display_jobs(st.session_state['jobs'])
        else:
            st.error(f"Failed to load more jobs: {response.status_code}")

# Function to display jobs
def display_jobs(jobs):
    for job in jobs:
        st.write(f"**{job['job_title']}** at **{job['company']}**")
        st.write(f"Location: {job['location']}")
        st.write(f"Listed on: {job['list_date']}")
        st.write(f"[Job Details]({job['job_url']})")
        st.write("---------")

# Show the 'Load More' button only if a search has been initiated and there's a next page URL
if st.session_state['search_initiated'] and st.session_state['next_page_url']:
    st.button('Load More', on_click=load_more_jobs)
