import streamlit as st
import requests

st.title("Job Search")

# Define the API key and headers
api_key = 'OQfhKnmj2k9bUHmlHH9Qbg'  # Replace with your actual API key
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin/company/job'

# Set the geo_id parameter which the user cannot change
geo_id = '101282230'

# Function to display jobs
def display_jobs(jobs):
    for job in jobs:
        st.write(f"**{job['job_title']}** at **{job['company']}**")
        st.write(f"Location: {job['location']}")
        st.write(f"Listed on: {job['list_date']}")
        st.write(f"[Job Details]({job['job_url']})")
        st.write("---------")

# Create search fields for user input
job_type = st.selectbox('Job Type', ['anything', 'full_time', 'part_time', 'internship', 'contract', 'temporary', 'volunteer'])
experience_level = st.selectbox('Experience Level', ['anything', 'internship', 'entry_level', 'associate', 'mid_senior_level', 'director'])
when = st.selectbox('When', ['anytime', 'yesterday', 'past-week', 'past-month'])
flexibility = st.selectbox('Flexibility', ['anything', 'remote', 'on-site', 'hybrid'])
keyword = st.text_input('Keyword', '')

# Container to display jobs below the input fields
jobs_container = st.container()

# Button to perform the API call
if st.button('Search Jobs'):
    st.session_state['next_page_url'] = None  # Reset the next page URL

    # Make the API call with the user input, including the geo_id parameter
    params = {
        'job_type': job_type,
        'experience_level': experience_level,
        'when': when,
        'flexibility': flexibility,
        'geo_id': geo_id,
        'keyword': keyword
    }
    
    response = requests.get(api_endpoint, params=params, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        jobs = response.json().get('job', [])
        with jobs_container:
            display_jobs(jobs)
        
        # Handle pagination if there are more pages
        next_page_url = response.json().get('next_page_api_url')
        if next_page_url:
            st.session_state['next_page_url'] = next_page_url

    else:
        st.error(f"Failed to retrieve jobs: {response.status_code}")

# Function to load more jobs
def load_more_jobs():
    next_page_url = st.session_state.get('next_page_url')
    if next_page_url:
        response = requests.get(next_page_url, headers=headers)
        if response.status_code == 200:
            jobs = response.json().get('job', [])
            with jobs_container:
                display_jobs(jobs)
            st.session_state['next_page_url'] = response.json().get('next_page_api_url')
        else:
            st.error(f"Failed to load more jobs: {response.status_code}")

# Button to load more jobs, if there is a next page URL available
if st.session_state.get('next_page_url'):
    st.button('Load More', on_click=load_more_jobs)
