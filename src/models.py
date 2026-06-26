"""
Módulo de modelos de dados do Sistema de Reserva de Salas de Estudo.

Define as entidades principais utilizadas pela lógica de negócio:
Aluno, Sala e Reserva.
"""
from dataclasses import dataclass
from datetime import date, time


@dataclass
class Aluno:
    """Representa um aluno cadastrado no sistema."""

    matricula: str
    nome: str
    email: str


@dataclass
class Sala:
    """Representa uma sala de estudo disponível na instituição."""

    codigo: str
    nome: str
    capacidade: int


@dataclass
class Reserva:
    """Representa uma reserva de sala feita por um aluno."""

    id_reserva: int
    matricula_aluno: str
    codigo_sala: str
    data: date
    horario: time
