import os
from urllib.parse import urlencode

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from authlib.integrations.flask_client import OAuth

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-this-secret")

KEYCLOAK_URL = os.environ.get("KEYCLOAK_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.environ.get("KEYCLOAK_REALM", "myrealm")
CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID", "hola-mundo-python")
CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET", "")

DISCOVERY_URL = (
    f"{KEYCLOAK_URL.rstrip('/')}/realms/{KEYCLOAK_REALM}"
    "/.well-known/openid-configuration"
)

oauth = OAuth(app)
oauth.register(
    name="keycloak",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=DISCOVERY_URL,
    client_kwargs={"scope": "openid profile email"},
)


@app.get("/")
def index():
    return render_template("index.html", user=session.get("user"))


@app.get("/login")
def login():
    # Esta URL debe coincidir exactamente con la registrada en Keycloak.
    callback_url = url_for("callback", _external=True)
    return oauth.keycloak.authorize_redirect(callback_url)


@app.get("/callback")
def callback():
    # Authlib intercambia el authorization code por tokens y valida el ID token.
    token = oauth.keycloak.authorize_access_token()
    userinfo = token.get("userinfo")

    if not userinfo:
        # En condiciones normales Authlib obtiene los claims del ID token.
        userinfo = oauth.keycloak.userinfo(token=token)

    session["user"] = {
        "id": userinfo.get("sub"),
        "username": userinfo.get("preferred_username"),
        "name": userinfo.get("name"),
        "email": userinfo.get("email"),
    }
    session["id_token"] = token.get("id_token")
    return redirect(url_for("index"))


@app.get("/logout")
def logout():
    id_token = session.get("id_token")
    session.clear()

    # Usamos el endpoint de cierre de sesión publicado por el discovery OIDC.
    metadata = oauth.keycloak.load_server_metadata()
    end_session_endpoint = metadata.get("end_session_endpoint")

    if not end_session_endpoint:
        return redirect(url_for("logged_out"))

    params = {
        "client_id": CLIENT_ID,
        "post_logout_redirect_uri": url_for("logged_out", _external=True),
    }
    if id_token:
        params["id_token_hint"] = id_token

    return redirect(f"{end_session_endpoint}?{urlencode(params)}")


@app.get("/logged-out")
def logged_out():
    session.clear()
    return render_template("logged_out.html")


if __name__ == "__main__":
    # Solo para desarrollo local. No usar el servidor integrado de Flask en producción.
    app.run(host="127.0.0.1", port=5000, debug=True)
