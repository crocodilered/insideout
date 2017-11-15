import cherrypy
import uuid
from webapp.libs.models.user import User


__all__ = ["AuthTool"]


class AuthTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, "before_handler", self._auth)

    def _auth(self):
        if not AuthTool.check_session():
            raise cherrypy.HTTPRedirect("/cms/?error=1")

    @staticmethod
    def _generate_token():
        return str(uuid.uuid4())

    @staticmethod
    def start_session(login, password):
        user = User.get_by_credentials(cherrypy.request.db, login, password)
        if user and user.enabled:
            cherrypy.session["token"] = user.token = AuthTool._generate_token()
            cherrypy.request.db.add(user)
            cherrypy.request.db.commit()
            return True
        else:
            return False

    @staticmethod
    def check_session():
        token = cherrypy.session.get("token", None)
        user = User.get_by_token(cherrypy.request.db, token)
        if user and user.enabled:
            return True
        else:
            return False

