import streamlit as st
from streamlit_server_state import server_state, server_state_access

@server_state_access
def get_client_ip():
    if server_state.client_ip is None:
        raise ValueError("Client IP is not set on the server state!")
    return server_state.client_ip

# Somewhere in your server initialization code
# This is pseudo-code and would need to be adapted to your specific server setup
@server.route("/streamlit_app")
def streamlit_app_route():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    server_state.client_ip = client_ip
    return render_streamlit_app()

# In your Streamlit app
st.title('User IP Address')
try:
    user_ip = get_client_ip()
    st.write(f"Your IP address is {user_ip}")
except ValueError as e:
    st.error(str(e))
