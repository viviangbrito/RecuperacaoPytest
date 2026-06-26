"""
Exceções customizadas do Sistema de Reserva de Salas de Estudo.
"""


class AlunoJaCadastradoError(Exception):
    """Levantada ao tentar cadastrar uma matrícula que já existe."""


class AlunoNaoEncontradoError(Exception):
    """Levantada quando a matrícula informada não corresponde a nenhum aluno."""


class SalaNaoEncontradaError(Exception):
    """Levantada quando o código de sala informado não existe no sistema."""


class HorarioOcupadoError(Exception):
    """Levantada ao tentar reservar uma sala em horário já reservado."""
