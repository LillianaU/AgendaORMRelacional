from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from models.base import Base

class Persona(Base):
    __tablename__ = 'personas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(200), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    
    # Relaciones con lazy='joined' para carga inmediata
    telefonos = relationship("Telefono", back_populates="persona", cascade="all, delete-orphan", lazy='joined')
    emails = relationship("Email", back_populates="persona", cascade="all, delete-orphan", lazy='joined')
    
    def __repr__(self):
        return f"<Persona(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}')>"