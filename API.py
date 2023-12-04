import streamlit as st
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

# Constants
CLIENT_ID = '785jejrypgi7ks'
CLIENT_SECRET = '4ZwcgJ0s0ENgcVuA'
REDIRECT_URI = 'https://kup7u2ixdrj2gdn6wmq3er.streamlit.app/'
AUTHORIZATION_BASE_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
SCOPE = 'openid profile email'

# Function to initiate OAuth process and handle token retrieval
def handle_oauth():
    linkedin = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    if "code" not in st.experimental_get_query_params():
        authorization_url, state = linkedin.authorization_url(AUTHORIZATION_BASE_URL)
        st.markdown(f"[Log in with LinkedIn]({authorization_url})", unsafe_allow_html=True)
        return

    try:
        token = linkedin.fetch_token(
            TOKEN_URL,
            client_secret=CLIENT_SECRET,
            code=st.experimental_get_query_params()["code"][0]
        )
        st.write("Received token:", token)  # Display token

        user_info = linkedin.get('https://api.linkedin.com/v2/me', headers={
            'Authorization': f'Bearer {token["access_token"]}'
        }).json()
        email_info = linkedin.get(
            'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))', 
            headers={'Authorization': f'Bearer {token["access_token"]}'}
        ).json()

        st.write("Your LinkedIn profile information:", user_info)
        st.write("Your LinkedIn email information:", email_info.get('elements', [])[0].get('handle~', {}).get('emailAddress', ''))

    except HTTPError as e:
        st.error(f'HTTP error occurred: {e.response.status_code}')
    except Exception as e:
        st.error(f'Error occurred: {e}')

# Main App
def main():
    st.title("LinkedIn OpenID Connect Authentication")
    handle_oauth()

if __name__ == "__main__":
    main()
