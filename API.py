import streamlit as st
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
import urllib.parse as urlparse
from urllib.parse import parse_qs

# Constants
CLIENT_ID = '785jejrypgi7ks'
CLIENT_SECRET = '4ZwcgJ0s0ENgcVuA'
REDIRECT_URI = 'https://kup7u2ixdrj2gdn6wmq3er.streamlit.app/'  # Your Streamlit app's address
AUTHORIZATION_BASE_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
SCOPE = ['openid', 'profile', 'email']  # Scopes for OpenID Connect

# Custom function to parse query string
def get_query_params(url):
    parsed_url = urlparse.urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return {k: v[0] for k, v in query_params.items()}

# Start the OAuth process
def start_oauth():
    linkedin = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = linkedin.authorization_url(AUTHORIZATION_BASE_URL)
    # Save the state in session for later use
    st.session_state['oauth_state'] = state
    # Redirect to LinkedIn for authorization
    st.markdown(f"[Log in with LinkedIn]({authorization_url})", unsafe_allow_html=True)

# Fetch token and user info
def fetch_token_and_user_info(code):
    try:
        linkedin = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
        token = linkedin.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, code=code)
        # Save the token in session and display it for debugging
        st.session_state['oauth_token'] = token
        st.write("OAuth Token Retrieved:", token)  # Debug statement

        # Fetch and display user info
        user_info = linkedin.get('https://api.linkedin.com/v2/me').json()
        st.session_state['user_info'] = user_info
        st.write("User Info:", user_info)  # Debug statement

        # Fetch and display user email
        email_info = linkedin.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))').json()
        st.session_state['email_info'] = email_info.get('elements', [])[0].get('handle~', {}).get('emailAddress', '')
        st.write("Email Info:", email_info)  # Debug statement

    except HTTPError as e:
        st.error(f'An HTTP error occurred: {e.response.status_code}')
        st.write(e.response.text)  # Debug statement
    except Exception as e:
        st.error(f'An error occurred: {e}')

# Main App
def main():
    st.title("LinkedIn OpenID Connect Authentication")

    # Get the current URL from Streamlit's query parameters
    current_url = st.experimental_get_query_params()
    query_params = get_query_params(str(current_url))
    code = query_params.get("code")

    if "oauth_token" not in st.session_state:
        if not code:
            start_oauth()
        else:
            fetch_token_and_user_info(code)
            st.success("Authentication successful!")

    if "user_info" in st.session_state:
        st.write("Your LinkedIn profile information:")
        st.json(st.session_state['user_info'])

        st.write("Your LinkedIn email information:")
        st.write(st.session_state['email_info'])

if __name__ == "__main__":
    main()
