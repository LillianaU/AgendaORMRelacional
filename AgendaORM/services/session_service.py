from config.database import db_config

class SessionService:
    def __init__(self):
        self.db_config = db_config

    def get_session(self):
        """Retorna una nueva sesión de base de datos"""
        return self.db_config.get_session()