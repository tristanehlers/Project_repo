import streamlit as st
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth

# Constants
CLIENT_ID = '785jejrypgi7ks'
CLIENT_SECRET = '4ZwcgJ0s0ENgcVuA'
REDIRECT_URI = 'https://kup7u2ixdrj2gdn6wmq3er.streamlit.app/'
AUTHORIZATION_BASE_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
SCOPE = 'openid', 'profile', 'email'

# Function to parse query string
def get_query_params():
    params = st.experimental_get_query_params()
    return {k: v[0] for k, v in params.items() if v}

# Start the OAuth process
def start_oauth():
    # Using BackendApplicationClient does not require a redirect_uri
    client = BackendApplicationClient(client_id=CLIENT_ID)
    linkedin = OAuth2Session(client=client, scope=SCOPE)
    authorization_url, state = linkedin.authorization_url(AUTHORIZATION_BASE_URL)
    st.session_state['oauth_state'] = state
    st.markdown(f"[Log in with LinkedIn]({authorization_url})", unsafe_allow_html=True)

# Fetch token and user info
def fetch_token_and_user_info(code):
    try:
        linkedin = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
        # Fetch the token using the authorization code
        token = linkedin.fetch_token(
            TOKEN_URL,
            authorization_response=st.session_state['authorization_response'],
            # Use HTTPBasicAuth to include the client_id and client_secret
            auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
            # No need to include the client_secret as a separate parameter
            # since auth parameter takes care of it
            code=code
        )
        st.session_state['oauth_token'] = token

        user_info = linkedin.get('https://api.linkedin.com/v2/me').json()
        st.session_state['user_info'] = user_info

        email_info = linkedin.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))').json()
        st.session_state['email_info'] = email_info.get('elements', [])[0].get('handle~', {}).get('emailAddress', '')

    except HTTPError as e:
        st.error(f'An HTTP error occurred: {e.response.status_code}')
        st.write(e.response.text)
    except Exception as e:
        st.error(f'An error occurred: {e}')
        st.write(str(e))

# Main App
def main():
    st.title("LinkedIn OpenID Connect Authentication")

    query_params = get_query_params()
    code = query_params.get("code")

    if "oauth_token" not in st.session_state:
        if not code:
            start_oauth()
        else:
            # Save the full authorization response URL
            st.session_state['authorization_response'] = st.url
            fetch_token_and_user_info(code)
            st.success("Authentication successful!")

    if "user_info" in st.session_state:
        st.write("Your LinkedIn profile information:")
        st.json(st.session_state['user_info'])

        st.write("Your LinkedIn email information:")
        st.write(st.session_state['email_info'])

if __name__ == "__main__":
    main()
