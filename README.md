# s2026q4d-kc-andres-jimenez
This repo contains the information from the KeyCloak dummy practice

In the present screenshots the process of the key cloak activity can be observed:

1. Put up KeyCloak with docker `01_Docker-Up-KC.png`
2. Creating a new realm `02_KC-Realm-MyRealm.png`
3. Create a new user `03_KC-user-config.png`
4. Registering and getting credentials from GCC `04_GCC-OAuth-Client.png`
5. Configuring google as an IdP in KC `05_KC-IdP-Google.png`
6. Using Google for Authorization `06_Try-Auth-Google.png`
7. Create the web app `keycloak_flask_demo/`
- To execute the app, include the .env with KeyCloak Client Secret
- Create an .venv `python3 -m venv .venv`
- Install dependencies `pip install -r requirements.txt`
- Execute on console `python app.py`
- Go to `http://127.0.0.1:5000`

8. Finally, registered the application on KeyCloak `07_KC_AppRegister.png`
9. Watch the app before authenticating `08_before_login.png`
10. And used Google as the IdP `09_Used-IdP`