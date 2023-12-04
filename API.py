import requests
from requests_oauthlib import OAuth2Session
from oauthlib import BackendApplicationClient

# Your LinkedIn credentials
client_id = '785jejrypgi7ks'
client_secret = '4ZwcgJ0s0ENgcVuA'

# Initialize OAuth2 client
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='https://www.linkedin.com/oauth/v2/accessToken',
                          client_id=client_id,
                          client_secret=client_secret)

# Make a request to LinkedIn API
response = oauth.get('API_ENDPOINT_HERE')

# Process the response
data = response.json()
print(data)
