from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from models.base import Base

class Agendamento(Base):
    __tablename__ = "Agendamento"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(Integer, ForeignKey("Usuario.matricula"), nullable=False)

    data = Column(Date)
    hora_inicio = Column(Time)
    hora_fim = Column(Time)
    finalidade = Column(String(100))
    status = Column(String(20))
