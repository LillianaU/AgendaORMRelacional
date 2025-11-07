class Telefono:
    """ASOCIACIÓN: Esta clase está asociada a Persona"""
    def __init__(self, numero: str, persona_id: int = None):
        self.id = None
        self.numero = numero          # ← Debe recibir número
        self.persona_id = persona_id  # ← Debe recibir persona_id
    
    def __str__(self):
        return f"Teléfono({self.id}, {self.numero})"