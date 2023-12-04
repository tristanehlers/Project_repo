from starlette.requests import Request
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
import streamlit as st

# Custom middleware to capture the client's IP address
class CaptureIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        client_ip = request.client.host
        response = await call_next(request)
        request.state.ip = client_ip  # Storing the IP in the request state
        return response

# Register the middleware with Streamlit
middleware = [Middleware(CaptureIPMiddleware)]
st.set_page_config(page_title='My Streamlit App', page_icon=':tada:', layout='wide', initial_sidebar_state='auto', menu_items=None, middleware=middleware)

# Access the client IP from within a Streamlit app
def get_client_ip():
    ctx = st.report_thread.get_report_ctx()
    session_info = st.server.server.Server.get_current()._get_session_info(ctx.session_id)
    if session_info is None:
        return None
    request = session_info.ws.request
    return request['client'][0] if 'client' in request else None

# Use the function in your app
client_ip = get_client_ip()
st.write(f"Client IP: {client_ip}")
