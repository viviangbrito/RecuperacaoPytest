"""
Módulo principal do Sistema de Reserva de Salas de Estudo.
"""
from datetime import date, time
from typing import Dict, List, Optional

from .exceptions import (
    AlunoJaCadastradoError,
    AlunoNaoEncontradoError,
    SalaNaoEncontradaError,
    HorarioOcupadoError,
)
from .models import Aluno, Reserva, Sala


class SistemaReservas:
    """Centraliza as regras de negócio do sistema de reservas de salas."""

    def __init__(self, salas: Optional[List[Sala]] = None):
        self._alunos: Dict[str, Aluno] = {}
        self._salas: Dict[str, Sala] = {s.codigo: s for s in (salas or [])}
        self._reservas: List[Reserva] = []
        self._proximo_id: int = 1

    def cadastrar_aluno(self, matricula: str, nome: str, email: str) -> Aluno:
        """Cadastra um novo aluno no sistema."""
        if matricula in self._alunos:
            raise AlunoJaCadastradoError(
                f"Aluno com matrícula '{matricula}' já está cadastrado."
            )
        aluno = Aluno(matricula=matricula, nome=nome, email=email)
        self._alunos[matricula] = aluno
        return aluno

    def consultar_salas_disponiveis(self, data: date, horario: time) -> List[Sala]:
        """Retorna a lista de salas que NÃO possuem reserva na data/horário dados."""
        codigos_ocupados = {
            r.codigo_sala
            for r in self._reservas
            if r.data == data and r.horario == horario
        }
        return [
            sala
            for codigo, sala in self._salas.items()
            if codigo not in codigos_ocupados
        ]

    def realizar_reserva(
        self, matricula_aluno: str, codigo_sala: str, data: date, horario: time
    ) -> Reserva:
        """Realiza a reserva de uma sala para um aluno em uma data/horário."""
        if matricula_aluno not in self._alunos:
            raise AlunoNaoEncontradoError(
                f"Aluno com matrícula '{matricula_aluno}' não encontrado."
            )
        if codigo_sala not in self._salas:
            raise SalaNaoEncontradaError(f"Sala '{codigo_sala}' não encontrada.")

        for reserva_existente in self._reservas:
            if (
                reserva_existente.codigo_sala == codigo_sala
                and reserva_existente.data == data
                and reserva_existente.horario == horario
            ):
                raise HorarioOcupadoError(
                    f"Sala '{codigo_sala}' já está reservada em "
                    f"{data} às {horario}."
                )

        nova_reserva = Reserva(
            id_reserva=self._proximo_id,
            matricula_aluno=matricula_aluno,
            codigo_sala=codigo_sala,
            data=data,
            horario=horario,
        )
        self._reservas.append(nova_reserva)
        self._proximo_id += 1
        return nova_reserva

    def consultar_historico(self, matricula_aluno: str) -> List[Reserva]:
        """Retorna todas as reservas já realizadas por um aluno cadastrado."""
        if matricula_aluno not in self._alunos:
            raise AlunoNaoEncontradoError(
                f"Aluno com matrícula '{matricula_aluno}' não encontrado."
            )
        return [r for r in self._reservas if r.matricula_aluno == matricula_aluno]
