import time

sessions = {}
SESSION_TIMEOUT = 1800  # 30 minutes en secondes

def is_session_valid(session_id):
    if session_id in sessions:
        session = sessions[session_id]
        # Vérifier si la session a expiré
        if time.time() - session["last_active"] > SESSION_TIMEOUT:
            # Supprimer la session expirée
            del sessions[session_id]
            return False
        return True
    return False

def update_session_activity(session_id):
    if session_id in sessions:
        sessions[session_id]["last_active"] = time.time()

def delete_session(session_id):
    if session_id in sessions:
        del sessions[session_id]