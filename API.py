# Fetch token and user info
def fetch_token_and_user_info(code):
    try:
        linkedin = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
        token = linkedin.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, code=code)
        
        # Save the token in session
        st.session_state['oauth_token'] = token

        # Fetch user info
        user_info = linkedin.get('https://api.linkedin.com/v2/me').json()
        st.session_state['user_info'] = user_info
        
        # Fetch user email
        email_info = linkedin.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))').json()
        st.session_state['email_info'] = email_info.get('elements', [])[0].get('handle~', {}).get('emailAddress', '')
        
        st.success("Authentication successful!")  # Only show this if all steps are successful
    except HTTPError as e:
        st.error(f'An HTTP error occurred: {e.response.status_code}')
        return  # Return early if an error occurs
    except Exception as e:
        st.error(f'An error occurred: {e}')
        return  # Return early if an error occurs
# Fetch token and user info
def fetch_token_and_user_info(code):
    try:
        linkedin = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
        token = linkedin.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, code=code)
        
        # Save the token in session
        st.session_state['oauth_token'] = token

        # Fetch user info
        user_info = linkedin.get('https://api.linkedin.com/v2/me').json()
        st.session_state['user_info'] = user_info
        
        # Fetch user email
        email_info = linkedin.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))').json()
        st.session_state['email_info'] = email_info.get('elements', [])[0].get('handle~', {}).get('emailAddress', '')
        
        st.success("Authentication successful!")  # Only show this if all steps are successful
    except HTTPError as e:
        st.error(f'An HTTP error occurred: {e.response.status_code}')
        return  # Return early if an error occurs
    except Exception as e:
        st.error(f'An error occurred: {e}')
        return  # Return early if an error occurs
