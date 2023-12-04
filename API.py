import streamlit as st
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import MobileApplicationClient

# OAuth 2.0 Client ID and Secret
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
REDIRECT_URI = 'YOUR_REDIRECT_URI'

# OAuth endpoints given in the XING API documentation
authorization_base_url = 'https://api.xing.com/auth'
token_url = 'https://api.xing.com/token'

# Using OAuth2Session for OAuth 2.0
client = MobileApplicationClient(CLIENT_ID)
oauth = OAuth2Session(client=client, redirect_uri=REDIRECT_URI)

# Redirect user to XING for authorization
authorization_url, state = oauth.authorization_url(authorization_base_url)
st.write(f'Please go here and authorize: {authorization_url}')

# Get the authorization verifier code from the callback URL
redirect_response = input('Paste the full redirect URL here: ')
oauth.fetch_token(token_url, client_secret=CLIENT_SECRET,
                  authorization_response=redirect_response)

# Fetch a protected resource, i.e., user profile
r = oauth.get('https://api.xing.com/v1/users/me')

# Display in Streamlit
st.json(r.json())
