import os
from functools import wraps
from flask import request, Response
from dotenv import load_dotenv
load_dotenv()

USER = os.getenv("DASH_USER", "admin")
PASS = os.getenv("DASH_PASS", "admin")

def _ok(a): return a and a.username == USER and a.password == PASS

def require_auth(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth = request.authorization
        if not _ok(auth):
            return Response("Auth required", 401, {"WWW-Authenticate": 'Basic realm="dashboard"'})
        return f(*args, **kwargs)
    return wrap



