#LinkedIn API

import streamlit as st
import requests
from requests_oauthlib import OAuth2Session
from urllib.parse import urlparse, parse_qs

# Constants
CLIENT_ID = '785jejrypgi7ks'
CLIENT_SECRET = '4ZwcgJ0s0ENgcVuA'
REDIRECT_URI = 'https://cz5daz6qukdskgv9cj6h4t.streamlit.app/'  # Your Streamlit app's address
AUTHORIZATION_BASE_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
SCOPE = ['r_liteprofile']  # Scope for basic profile information

# Function to parse query string
def get_query_params():
    query_params = st.experimental_get_query_params()
    return query_params

# Start the OAuth process
def start_oauth():
    linkedin = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = linkedin.authorization_url(AUTHORIZATION_BASE_URL)

    # Save the state in session for later use
    st.session_state['oauth_state'] = state

    # Redirect to LinkedIn for authorization
    st.markdown(f"[Log in with LinkedIn to prefill your CV]({authorization_url})", unsafe_allow_html=True)

# Fetch token
def fetch_token(code):
    linkedin = OAuth2Session(CLIENT_ID, state=st.session_state['oauth_state'], redirect_uri=REDIRECT_URI)
    token = linkedin.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, code=code)

    # Save the token in session
    st.session_state['oauth_token'] = token

    # Fetch basic profile information
    fetch_profile_info(token)

def fetch_profile_info(token):
    linkedin = OAuth2Session(CLIENT_ID, token=token)
    profile_response = linkedin.get('https://api.linkedin.com/v2/me')
    profile_data = profile_response.json()
    st.session_state['profile_data'] = profile_data

# Main App
def main():
    st.title("LinkedIn Profile Information")

    # Check if the code is returned in the query string
    query_params = get_query_params()
    code = query_params.get("code")

    if "oauth_token" not in st.session_state:
        # If we don't have an oauth token, and the code is not in the query string, start the OAuth process
        if not code:
            start_oauth()
        else:
            # If we have the code, fetch the token
            fetch_token(code[0])
            st.write("Authentication successful!")

    if "profile_data" in st.session_state:
        # If we have the profile data, display it
        st.write("Your profile data:", st.session_state['profile_data'])

if __name__ == "__main__":
    main()
