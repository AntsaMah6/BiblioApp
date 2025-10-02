from models.auth import Auth
import urllib.parse
import time
import secrets
from session_manager import sessions  # Note: set_session et delete_session ne sont pas définis, on utilise directement sessions

class AuthController(object):
    @staticmethod
    async def __load(send, filename, dico=None):
        with open(filename, "r", encoding="utf-8") as f:
            html = f.read()
        if dico:
            for key, value in dico.items():
                placeholder = "{{ " + str(key) + " }}"  # Correction: enlevé le double {
                html = html.replace(placeholder, str(value))
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [(b'content-type', b'text/html; charset=utf-8')]  # Correction: ajouté charset=utf-8
        })
        await send({
            'type': 'http.response.body',
            'body': html.encode('utf-8')  # Correction: encodage explicite en utf-8
        })

    @staticmethod
    async def login_page(scope, receive, send):
        await __class__.__load(send, "views/auth/login.html")

    @staticmethod
    async def login(scope, receive, send):
        event = await receive()
        body = event.get("body", b"")
        post_data = body.decode()
        dico = urllib.parse.parse_qs(post_data)
        username = dico.get('username', [''])[0]
        password = dico.get('password', [''])[0]

        user = Auth.getByUsernameAndPassword(username, password)

        if user:
            session_id = secrets.token_hex(16)
            sessions[session_id] = {"user": user, "last_active": time.time()}
            await send({
                'type': 'http.response.start',
                'status': 302,
                'headers': [
                    (b'Location', b'/dashboard'),
                    (b'Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly'.encode())
                ]
            })
            await send({'type': 'http.response.body', 'body': b''})
        else:
            error_html = "<p style='color:red'>Identifiants invalides</p>"
            await __class__.__load(send, "views/auth/login.html", {"error_message": error_html})

    @staticmethod
    async def logout(scope, receive, send):
        # Remove session
        session_id = None
        for k, v in scope.get('headers', []):
            if k == b'cookie':
                cookiestr = v.decode()
                for c in cookiestr.split(';'):
                    if c.strip().startswith('session_id='):
                        session_id = c.strip().split('=')[1]
        if session_id and session_id in sessions:
            del sessions[session_id]
        await send({
            'type': 'http.response.start',
            'status': 302,
            'headers': [
                (b'Location', b'/'),
                (b'Set-Cookie', b'session_id=; Path=/; Max-Age=0')
            ]
        })
        await send({'type': 'http.response.body', 'body': b''})