import streamlit as st
from careerjet_api_client import CareerjetAPIClient

def search_jobs(location, keyword):
    cj  = CareerjetAPIClient("en_GB")  # Use the appropriate locale here

    result = cj.search({
        'location'    : location,
        'keywords'    : keyword,
        'affid'       : 'your_affiliate_id',  # Replace with your affiliate ID
        'user_ip'     : '11.22.33.44',        # Replace with the user's IP
        'url'         : 'http://www.example.com/jobsearch', # Replace with your URL
        'pagesize'    : 10,
    })

    return result['jobs']

# Streamlit UI
st.title("Job Search with Careerjet")

location = st.text_input("Location")
keyword = st.text_input("Keyword")

if st.button("Search"):
    if location and keyword:
        jobs = search_jobs(location, keyword)
        for job in jobs:
            st.write(job['title'], "-", job['company'])
            st.write(job['description'])
            st.write("Location:", job['locations'])
            st.write("URL:", job['url'])
            st.write("--------")
    else:
        st.warning("Please enter both location and keyword")
