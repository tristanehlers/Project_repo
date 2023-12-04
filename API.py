import streamlit as st
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

# Constants
CLIENT_ID = '785jejrypgi7ks'
CLIENT_SECRET = '4ZwcgJ0s0ENgcVuA'
REDIRECT_URI = 'https://kup7u2ixdrj2gdn6wmq3er.streamlit.app/'
AUTHORIZATION_BASE_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
SCOPE = 'r_liteprofile r_emailaddress'

# Function to initiate OAuth process and handle token retrieval
def handle_oauth():
    linkedin = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE.split())
    if "code" not in st.experimental_get_query_params():
        authorization_url, state = linkedin.authorization_url(AUTHORIZATION_BASE_URL)
        st.session_state['oauth_state'] = state
        st.markdown(f"[Log in with LinkedIn]({authorization_url})", unsafe_allow_html=True)
    else:
        try:
            token = linkedin.fetch_token(
                TOKEN_URL,
                client_secret=CLIENT_SECRET,
                authorization_response=st.experimental_get_query_params()["code"][0]
            )
            st.session_state['oauth_token'] = token
            st.write("Received token:", token)  # Display token

            # Fetch user profile information
            profile_info = linkedin.get('https://api.linkedin.com/v2/me').json()
            st.write("Your LinkedIn profile information:", profile_info)

            # Fetch user email address
            email_info = linkedin.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))').json()
            st.write("Your LinkedIn email address:", email_info.get('elements', [])[0].get('handle~', {}).get('emailAddress', ''))

        except HTTPError as e:
            st.error(f'HTTP error occurred: {e.response.status_code}')
            st.error(e.response.text)
        except Exception as e:
            st.error(f'An error occurred: {e}')

# Main App
def main():
    st.title("LinkedIn OpenID Connect Authentication")
    if 'oauth_token' not in st.session_state:
        handle_oauth()
    else:
        # If token exists in session state, show user information
        st.write("You are already authenticated")
        st.json(st.session_state['oauth_token'])

if __name__ == "__main__":
    main()
