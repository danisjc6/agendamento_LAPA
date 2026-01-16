from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base

class Reserva(Base):
    __tablename__ = "Reserva"

    id_agendamento = Column(
        Integer,
        ForeignKey("Agendamento.id"),
        primary_key=True
    )

    id_sala = Column(
        Integer,
        ForeignKey("Sala.id_sala"),
        nullable=False
    )
