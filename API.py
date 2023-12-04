import requests
import streamlit as st
from requests_oauthlib import OAuth2Session

# Your LinkedIn credentials
client_id = '785jejrypgi7ks'
client_secret = '4ZwcgJ0s0ENgcVuA'

# OAuth endpoints given in the LinkedIn API documentation
authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
redirect_uri = 'https://kup7u2ixdrj2gdn6wmq3er.streamlit.app/'

# Initialize OAuth2 session
oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=['openid profile email'])
authorization_url, state = oauth.authorization_url(authorization_base_url)

# Streamlit app to display authorization URL
st.write(f'Please go to this URL and authorize: {authorization_url}')

# Streamlit input for the callback URL
redirect_response = st.text_input('Paste the callback URL here: ')

if redirect_response:
    # Exchange authorization code for access token
    token = oauth.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

    # Use token to make LinkedIn API calls
    linkedin = OAuth2Session(client_id, token=token)
    response = linkedin.get('https://api.linkedin.com/v2/me')

    # Display user profile data in Streamlit
    st.json(response.json())
