import streamlit as st
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

# Constants
CLIENT_ID = '785jejrypgi7ks'
CLIENT_SECRET = '4ZwcgJ0s0ENgcVuA'
REDIRECT_URI = 'https://cz5daz6qukdskgv9cj6h4t.streamlit.app/'  # Your Streamlit app's address
AUTHORIZATION_BASE_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
SCOPE = ['openid', 'profile', 'email']  # Scopes for OpenID Connect

# Function to parse query string
def get_query_params():
    return st.experimental_get_query_params()

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
        # Add the client_secret parameter to the fetch_token() method call
        token = linkedin.fetch_token(TOKEN_URL, client_secret='4ZwcgJ0s0ENgcVuA', code=code)
        # Save the token in session
        st.session_state['oauth_token'] = token

        # Fetch user info
        user_info = linkedin.get('https://api.linkedin.com/v2/userinfo').json()
        st.session_state['user_info'] = user_info

        # Fetch user email
        email_info = linkedin.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))').json()
        st.session_state['email_info'] = email_info.get('elements', [])[0].get('handle~', {}).get('emailAddress', '')

    except HTTPError as e:
        st.error(f'An HTTP error occurred: {e.response.status_code}')
    except Exception as e:
        st.error(f'An error occurred: {e}')

# Main App
def main():
    st.title("LinkedIn OpenID Connect Authentication")

    query_params = get_query_params()
    code = query_params.get("code")

    if "oauth_token" not in st.session_state:
        if not code:
            start_oauth()
        else:
            fetch_token_and_user_info(code[0])
            st.success("Authentication successful!")

    if "user_info" in st.session_state:
        st.write("Your LinkedIn profile information:")
        st.json(st.session_state['user_info'])

        st.write("Your LinkedIn email information:")
        st.write(st.session_state['email_info'])

if __name__ == "__main__":
    main()
