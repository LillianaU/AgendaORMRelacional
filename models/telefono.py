from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Telefono(Base):
    __tablename__ = 'telefonos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    persona_id = Column(Integer, ForeignKey('personas.id'), nullable=False)
    telefono = Column(String(20), nullable=False)
    
    # Relación
    persona = relationship("Persona", back_populates="telefonos")
    
    def __repr__(self):
        return f"<Telefono(id={self.id}, telefono='{self.telefono}')>"