import json
import logging
import socket
from urllib.request import urlopen

from authlib.integrations.base_client import OAuthError
from authlib.integrations.flask_client import OAuth
from flask import session, jsonify, request, _request_ctx_stack, render_template, g
from jose import jwt
from six import wraps
from werkzeug.utils import redirect

from app import app


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


auth0 = OAuth(app).register(
    'auth0',
    client_id=app.config['AUTH0_CLIENT_ID'],
    client_secret=app.config['AUTH0_CLIENT_SECRET'],
    api_base_url=app.config['AUTH0_API_BASE_URL'],
    access_token_url=app.config['AUTH0_API_BASE_URL'] + '/oauth/token',
    authorize_url=app.config['AUTH0_API_BASE_URL'] + '/authorize',
    client_kwargs={
        'scope': 'openid profile email'
    },
)


@app.route('/callback')
def callback_handling():
    try:
        # Handles response from token endpoint
        tk = auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()
        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture'],
            'bearer_token': tk.get('access_token')
        }
        return redirect('/')
    except OAuthError as e:
        logging.info("User not authorized : " + e.args[0])
        return redirect('/not_allowed')


@app.route('/login')
def login():
    logging.info("PASSAGE  LOGIN")
    logging.info(app.config['AUTH0_REDIRECT_URL'])
    logging.info(app.config['AUTH0_AUDIENCE'])
    return auth0.authorize_redirect(redirect_uri=app.config['AUTH0_REDIRECT_URL'] + '/callback',
                                    audience=app.config['AUTH0_AUDIENCE'])


@app.route("/not_allowed")
def not_allowed():
    return render_template("not_allowed.html", title="GIREVE Testing Platform")


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logging.info("PASSAGE DECORATEUR")
        if 'profile' not in session:
            # Redirect to Login page here
            logging.info("PASSAGE REDIRECT LOGIN tstzt")
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


def get_api_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("X-OCPI-tester-token", None)
    if not auth:
        raise AuthError({"code": "X-OCPI-tester-token_header_missing",
                         "description":
                             "OCPI tester token header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                             "OCPI tester token header must start with"
                             " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                             "OCPI tester token header must be"
                             " Bearer token"}, 401)

    token = parts[1]
    return token


def requires_auth_api(f):
    """Determines if the Access Token is valid
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if len(request.headers.getlist("X-Forwarded-For")) > 0 and request.headers.getlist("X-Forwarded-For")[0] in ["185.11.188.193", "195.21.21.104"]:
            g.user_id = "IOP"
            return f(*args, **kwargs)
        API_AUDIENCE = app.config['AUTH0_AUDIENCE']
        ALGORITHMS = ["RS256"]
        token = get_api_token_auth_header()

        jsonurl = urlopen(app.config['AUTH0_API_BASE_URL'] + '/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=app.config['AUTH0_API_BASE_URL'] + "/"
                )
                g.user_id = payload['sub']
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                 "description": "OCPI tester token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                 "description":
                                     "incorrect claims,"
                                     "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                 "description":
                                     "Unable to parse authentication"
                                     " token."}, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)

    return decorated
