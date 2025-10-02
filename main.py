import os
from router import Router
from controllers.livre import LivreController
from controllers.membre import MembreController
import uvicorn
from models.livre import Livre
from models.membre import Membre
from controllers.auth import AuthController
import time
from session_manager import sessions, SESSION_TIMEOUT, is_session_valid, update_session_activity
from controllers.dashboard import DashboardController
from controllers.emprunt import EmpruntController

router = Router()
router.add("/", AuthController.login_page)
router.add("/login", AuthController.login)
router.add("/logout", AuthController.logout)

router.add("/livre/list", LivreController.pageList)
router.add("/livre/insert", LivreController.pageInsert)
router.add("/livre/update/\d+", LivreController.pageUpdate)
router.add("/livre/insert/opinsert", LivreController.opInsert)
router.add("/livre/update/opupdate", LivreController.opUpdate)
router.add("/livre/delete/\d+", LivreController.opDelete)
router.add("/api/livres/search", LivreController.searchLivres)

router.add("/membre/list", MembreController.pageList)
router.add("/membre/insert", MembreController.pageInsert)
router.add("/membre/update/\d+", MembreController.pageUpdate)
router.add("/membre/insert/opinsert", MembreController.opInsert)
router.add("/membre/update/opupdate", MembreController.opUpdate)
router.add("/membre/delete/\d+", MembreController.opDelete)
router.add("/api/membres/search", MembreController.searchMembres)


router.add("/dashboard", DashboardController.pageDashboard)	
router.add("/dashboard/stats", DashboardController.getStats)
router.add("/api/stats", DashboardController.getStats)

router.add("/emprunt/list", EmpruntController.pageEmprunts)
router.add("/emprunt/nouvel", EmpruntController.pageNouvelEmprunt)
router.add("/emprunt/emprunter", EmpruntController.opEmprunter)
router.add("/emprunt/retourner/\d+", EmpruntController.opRetourner)
router.add("/emprunt/retards", EmpruntController.pageRetards)

router.add("/api/livres/disponibles", LivreController.apiLivresDisponibles)
router.add("/api/membres", MembreController.apiMembres)



async def app(scope, receive, send):
    assert scope['type'] == 'http'
    path = scope["path"]

    # Gestion des assets statiques
    if path.startswith("/assets/"):
        file_path = "." + path
        
        if os.path.exists(file_path):
            if file_path.endswith(".css"):
                content_type = b"text/css"
            elif file_path.endswith(".js"):
                content_type = b"application/javascript"
            elif file_path.endswith(".png"):
                content_type = b"image/png"
            elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
                content_type = b"image/jpeg"
            else:
                content_type = b"application/octet-stream"

            with open(file_path, "rb") as f:
                body = f.read()

            await send({
                "type" : "http.response.start",
                "status" : 200,
                "headers" : [[b"content-type", content_type]]
            })
            await send({
                "type" : "http.response.body",
                "body" : body
            })
            return
        else:
            body = "<h1>404 - Fichier non trouvé</h1>".encode("utf-8")
            await send({
                "type" : "http.response.start",
                "status" : 404,
                "headers" : [[b"content-type", content_type]]
            })
            await send({
                "type" : "http.response.body",
                "body" : body
            })
            return
    
    # Gestion de la session
    session_id = None
    for k, v in scope.get('headers', []):
        if k == b'cookie':
            cookiestr = v.decode()
            for c in cookiestr.split(';'):
                if c.strip().startswith('session_id='):
                    session_id = c.strip().split('=')[1]

    # Si pas de session ou session expirée, rediriger vers login sauf pour / et /login
    if path not in ["/", "/login"]:
        if not session_id or session_id not in sessions:
            await send({
                'type': 'http.response.start',
                'status': 302,
                'headers': [(b'Location', b'/')]
            })
            await send({'type': 'http.response.body', 'body': b''})
            return
        else:
            # Vérifier si la session a expiré
            session = sessions[session_id]
            if time.time() - session["last_active"] > SESSION_TIMEOUT:
                del sessions[session_id]  # Supprimer la session expirée
                await send({
                    'type': 'http.response.start',
                    'status': 302,
                    'headers': [(b'Location', b'/')]
                })
                await send({'type': 'http.response.body', 'body': b''})
                return
            else:
                # Mettre à jour le timestamp d'activité
                sessions[session_id]["last_active"] = time.time()                                                                                                                                                     

    handler = router.resolve(path)
    if handler:
        await handler(scope, receive, send)
    else:
        await LivreController.error404(scope, receive, send)


if __name__ == '__main__':
    uvicorn.run("main:app", port = 8001, reload = True)