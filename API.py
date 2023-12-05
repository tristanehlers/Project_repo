import streamlit as st
import requests

st.title("Job Search")

# Define the API key and headers
api_key = 'OQfhKnmj2k9bUHmlHH9Qbg'  # Replace with your actual API key
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin/company/job'

# Create search fields for user input
job_type = st.selectbox('Job Type', ['', 'full_time', 'part_time', 'internship', 'contract', 'temporary', 'volunteer', 'anything'])
experience_level = st.selectbox('Experience Level', ['', 'internship', 'entry_level', 'associate', 'mid_senior_level', 'director', 'executive'])
when = st.selectbox('When', ['', 'past-day', 'past-week', 'past-month'])
flexibility = st.selectbox('Flexibility', ['', 'remote', 'in-person'])
geo_id = st.text_input('Geo ID', '92000000')
keyword = st.text_input('Keyword', 'software engineer')
search_id = st.text_input('Search ID', '1035')

# Button to perform the API call
if st.button('Search Jobs'):
    # Make the API call with the user input
    params = {
        'job_type': job_type,
        'experience_level': experience_level,
        'when': when,
        'flexibility': flexibility,
        'geo_id': geo_id,
        'keyword': keyword,
        'search_id': search_id,
    }
    
    response = requests.get(api_endpoint, params=params, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        jobs = response.json()
        # Display the job results - you may need to adjust this based on the actual response structure
        for job in jobs.get('data', []):
            st.write(job['title'])
            st.write(job['companyName'])
            st.write(job['location'])
            st.write(job['description'])
            st.write(job['listingUrl'])
            st.write("---------")
    else:
        st.error(f"Failed to retrieve jobs: {response.status_code}")
