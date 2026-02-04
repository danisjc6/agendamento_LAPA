from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base

class Reserva(Base):
    __tablename__ = "reservas"

    id_agendamento = Column(
        Integer,
        ForeignKey("agendamentos.id_agendamento"),
        primary_key=True
    )

    id_sala = Column(
        Integer,
        ForeignKey("salas.id_sala"),
        nullable=False
    )
