import streamlit as st
from requests_oauthlib import OAuth2Session
from urllib.parse import urlparse, parse_qs

# Your LinkedIn credentials
client_id = '78nz3x6cxyj37h'
client_secret = 'UofXEjpk0jez4CfI'

# OAuth endpoints given in the LinkedIn API documentation
authorization_base_url = 'https://www.linkedin.com/oauth/v2/authorization'
token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
redirect_uri = 'https://kup7u2ixdrj2gdn6wmq3er.streamlit.app/'

# Initialize OAuth2 session with the correct scopes
oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=['r_liteprofile'])

# Generate the authorization URL and save the state
authorization_url, state = oauth.authorization_url(authorization_base_url)
st.session_state['oauth_state'] = state

# Streamlit app to display authorization URL
st.write('Please go to this URL and authorize:', authorization_url)

# Streamlit input for the callback URL
redirect_response = st.text_input('Paste the callback URL here: ')

if redirect_response:
    # Parse the state from the callback URL
    parsed_url = urlparse(redirect_response)
    callback_state = parse_qs(parsed_url.query)['state'][0] if 'state' in parse_qs(parsed_url.query) else 'No State in URL'

    # Compare the state in the callback URL to the saved state
    saved_state = st.session_state.get('oauth_state', 'No State in Session')

    # Check if states match and proceed if they do
    if callback_state == saved_state:
        try:
            # Exchange authorization code for access token
            token = oauth.fetch_token(token_url, client_secret=client_secret, 
                                      authorization_response=redirect_response,
                                      state=callback_state)

            # Output the token to the Streamlit app (for debugging purposes)
            st.write("Access token:", token)

            # Use token to make LinkedIn API calls
            linkedin = OAuth2Session(client_id, token=token)
            # Fetch the user's profile data
            response = linkedin.get('https://api.linkedin.com/v2/me')

            # Display user profile data in Streamlit
            st.json(response.json())

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        # If states don't match, output an error message
        st.error(f"State mismatch error: Callback state {callback_state} does not match saved state {saved_state}.")
