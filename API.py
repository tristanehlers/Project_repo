import streamlit as st

try:
    from careerjet_api_client import CareerjetAPIClient
except ImportError as e:
    st.error(f"An error occurred while importing CareerjetAPIClient: {e}")
    # Add any necessary logic to handle the import error here
    raise

# Initialize the Careerjet API client with your locale
cj = CareerjetAPIClient("en_GB")  # or any other locale code

# Streamlit app layout
st.title("Job Search with Careerjet")

# Input fields for the search criteria
location = st.text_input("Location", "london")
keywords = st.text_input("Keywords", "python")

# Button to perform the search
if st.button("Search Jobs"):
    try:
        # Using the Careerjet API client to search for jobs
        result_json = cj.search({
            'location': location,
            'keywords': keywords,
            'affid': '213e213hd12344552',  # Replace with your affiliate ID
            'user_ip': '192.168.1.29',  # Replace with the user's IP
            'url': 'http://www.example.com/jobsearch',  # Replace with the URL where the results will be displayed
            'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
            'pagesize': 10,
        })
    except Exception as e:
        st.error(f"An error occurred while searching for jobs: {e}")
        # Add any necessary logic to handle the search error here
        raise

    # Displaying the search results
    if result_json and 'jobs' in result_json:
        for job in result_json['jobs']:
            st.write(job['title'])
            st.write(job['company'])
            st.write(job['description'])
            st.write(job['url'])
            st.write("---------")
    else:
        st.error("No jobs found")
