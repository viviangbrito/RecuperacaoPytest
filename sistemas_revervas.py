"""
Módulo principal do Sistema de Reserva de Salas de Estudo.

Implementa os requisitos funcionais definidos no Documento de Requisitos:
    RF01 - Cadastro de um novo aluno
    RF02 - Consulta de salas disponíveis
    RF03 - Realização de reserva de sala por um aluno
    RF04 - Impedimento de reservas para horários já ocupados
    RF05 - Consulta do histórico de reservas realizadas

RNF02 - Esta classe contém SOMENTE a lógica de negócio (sem qualquer
        referência a pytest ou a frameworks de teste), garantindo a
        separação entre lógica e testes exigida pelos requisitos não
        funcionais. Os testes ficam isolados em tests/test_sistema_reservas.py.

RNF03 - As operações abaixo são todas em memória (O(n) sobre listas
        pequenas), portanto o tempo de resposta fica muito abaixo do
        limite de 3 segundos exigido. Essa característica é demonstrada
        de forma automatizada no teste `test_tempo_resposta_reserva`.
"""
from datetime import date, time
from typing import Dict, List, Optional

from .models import Aluno, Sala, Reserva
from .exceptions import (
    AlunoJaCadastradoError,
    AlunoNaoEncontradoError,
    SalaNaoEncontradaError,
    HorarioOcupadoError,
)


class SistemaReservas:
    """Centraliza as regras de negócio do sistema de reservas de salas."""

    def __init__(self, salas: Optional[List[Sala]] = None):
        self._alunos: Dict[str, Aluno] = {}
        self._salas: Dict[str, Sala] = {s.codigo: s for s in (salas or [])}
        self._reservas: List[Reserva] = []
        self._proximo_id: int = 1

    # ------------------------------------------------------------------ #
    # RF01 - Cadastro de aluno
    # ------------------------------------------------------------------ #
    def cadastrar_aluno(self, matricula: str, nome: str, email: str) -> Aluno:
        """
        Cadastra um novo aluno no sistema.

        Lança AlunoJaCadastradoError se a matrícula já estiver em uso.
        """
        if matricula in self._alunos:
            raise AlunoJaCadastradoError(
                f"Aluno com matrícula '{matricula}' já está cadastrado."
            )
        aluno = Aluno(matricula=matricula, nome=nome, email=email)
        self._alunos[matricula] = aluno
        return aluno

    # ------------------------------------------------------------------ #
    # RF02 - Consulta de salas disponíveis
    # ------------------------------------------------------------------ #
    def consultar_salas_disponiveis(self, data: date, horario: time) -> List[Sala]:
        """Retorna a lista de salas que NÃO possuem reserva na data/horário dados."""
        codigos_ocupados = {
            r.codigo_sala
            for r in self._reservas
            if r.data == data and r.horario == horario
        }
        return [
            sala for codigo, sala in self._salas.items()
            if codigo not in codigos_ocupados
        ]

    # ------------------------------------------------------------------ #
    # RF03 + RF04 - Realizar reserva / impedir conflito de horário
    # ------------------------------------------------------------------ #
    def realizar_reserva(
        self, matricula_aluno: str, codigo_sala: str, data: date, horario: time
    ) -> Reserva:
        """
        Realiza a reserva de uma sala para um aluno em uma data/horário.

        Regras aplicadas:
        - O aluno precisa estar cadastrado (senão: AlunoNaoEncontradoError).
        - A sala precisa existir (senão: SalaNaoEncontradaError).
        - RF04: não pode haver outra reserva para a MESMA sala na MESMA
          data e horário (senão: HorarioOcupadoError).
        """
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

    # ------------------------------------------------------------------ #
    # RF05 - Consulta de histórico de reservas
    # ------------------------------------------------------------------ #
    def consultar_historico(self, matricula_aluno: str) -> List[Reserva]:
        """Retorna todas as reservas já realizadas por um aluno cadastrado."""
        if matricula_aluno not in self._alunos:
            raise AlunoNaoEncontradoError(
                f"Aluno com matrícula '{matricula_aluno}' não encontrado."
            )
        return [
            r for r in self._reservas if r.matricula_aluno == matricula_aluno
        ]