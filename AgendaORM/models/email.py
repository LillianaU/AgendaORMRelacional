from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Email(Base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    persona_id = Column(Integer, ForeignKey('personas.id'), nullable=False)
    email = Column(String(100), nullable=False)
    
    # Relación
    persona = relationship("Persona", back_populates="emails")
    
    def __repr__(self):
        return f"<Email(id={self.id}, email='{self.email}')>"