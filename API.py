import streamlit as st
from requests_oauthlib import OAuth2Session, TokenUpdated

# Constants
CLIENT_ID = '785jejrypgi7ks'
CLIENT_SECRET = '4ZwcgJ0s0ENgcVuA'
REDIRECT_URI = 'https://kup7u2ixdrj2gdn6wmq3er.streamlit.app/'
AUTHORIZATION_BASE_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
SCOPE = 'openid profile email'

# Function to start the OAuth process
def start_oauth():
    linkedin = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = linkedin.authorization_url(AUTHORIZATION_BASE_URL)
    st.session_state.oauth_state = state
    st.markdown(f"[Log in with LinkedIn]({authorization_url})", unsafe_allow_html=True)

# Function to fetch token and user info
def fetch_token_and_user_info(code):
    linkedin = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    token = linkedin.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, code=code)
    st.session_state.oauth_token = token
    user_info = linkedin.get('https://api.linkedin.com/v2/me', headers={'Authorization': f'Bearer {token["access_token"]}'}).json()
    st.session_state.user_info = user_info
    email_info = linkedin.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))', headers={'Authorization': f'Bearer {token["access_token"]}'}).json()
    st.session_state.email_info = email_info.get('elements', [])[0].get('handle~', {}).get('emailAddress', '')

# Main App
def main():
    st.title("LinkedIn OpenID Connect Authentication")

    code = st.experimental_get_query_params().get("code")

    if "oauth_token" not in st.session_state:
        if not code:
            start_oauth()
        else:
            try:
                fetch_token_and_user_info(code)
                st.success("Authentication successful!")
            except TokenUpdated:
                st.error("Authentication failed. Please try again.")

    if "user_info" in st.session_state:
        st.write("Your LinkedIn profile information:")
        st.json(st.session_state.user_info)

        st.write("Your LinkedIn email information:")
        st.write(st.session_state.email_info)

if __name__ == "__main__":
    main()
