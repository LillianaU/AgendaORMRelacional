class Email:
    """ASOCIACIÓN: Esta clase está asociada a Persona"""
    def __init__(self, direccion: str, persona_id: int = None):
        self.id = None
        self.direccion = direccion     # ← Debe recibir dirección
        self.persona_id = persona_id   # ← Debe recibir persona_id
    
    def __str__(self):
        return f"Email({self.id}, {self.direccion})"