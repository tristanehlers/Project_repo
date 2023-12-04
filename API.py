import streamlit as st
from streamlit_oauth import OAuth2Component

# Constants
CLIENT_ID = '785jejrypgi7ks'
CLIENT_SECRET = '4ZwcgJ0s0ENgcVuA'
REDIRECT_URI = 'https://kup7u2ixdrj2gdn6wmq3er.streamlit.app/'
AUTHORIZATION_BASE_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
SCOPE = 'openid profile email'  # Updated scope format

# Create OAuth2Component instance
oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_BASE_URL, TOKEN_URL)

# Function to initiate OAuth process and handle token retrieval
def handle_oauth():
    if 'token' not in st.session_state:
        # If not, show authorize button
        result = oauth2.authorize_button("Authorize", REDIRECT_URI, SCOPE)
        if result and 'token' in result:
            # If authorization successful, save token in session state
            st.session_state['token'] = result['token']
            st.experimental_rerun()
    else:
        # If token exists in session state, show the token
        token = st.session_state['token']
        st.write("Your LinkedIn access token is:", token)
        # Add additional code to fetch user profile or email information using the token

# Main App
def main():
    st.title("LinkedIn OpenID Connect Authentication")
    handle_oauth()

if __name__ == "__main__":
    main()
