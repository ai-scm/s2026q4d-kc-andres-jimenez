# Hola Mundo: Flask + Keycloak

Aplicación web mínima que demuestra el inicio de sesión con Keycloak mediante OpenID Connect Authorization Code Flow.

## Requisitos

- Python 3.10 o superior.
- Keycloak en ejecución y accesible desde el navegador y desde Python.
- Realm: `myrealm`.

## Instalación en Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edita `.env` y configura `KEYCLOAK_URL`, `KEYCLOAK_CLIENT_ID` y `KEYCLOAK_CLIENT_SECRET`.

## Ejecutar

```powershell
python app.py
```

Abre http://127.0.0.1:5000.

## Configuración requerida en Keycloak

- Client type: OpenID Connect.
- Client ID: `hola-mundo-python`.
- Client authentication: ON (cliente confidencial).
- Standard flow: ON.
- Valid redirect URIs: `http://127.0.0.1:5000/callback`.
- Valid post logout redirect URIs: `http://127.0.0.1:5000/logged-out`.
- Web origins: `http://127.0.0.1:5000` (o configura el origen según tu versión/política CORS).

Copia el Client Secret desde la pestaña Credentials del cliente y pégalo en `.env`.

## Notas

- El secreto de Flask y el secreto del cliente son distintos.
- No subas `.env` al repositorio.
- `debug=True` es exclusivamente para desarrollo.
- Para producción usa HTTPS, un secreto robusto, cookies seguras y un servidor WSGI.
- La aplicación no implementa autorización por roles; solo demuestra autenticación.
