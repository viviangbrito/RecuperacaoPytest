"""
Exceções customizadas do Sistema de Reserva de Salas de Estudo.

Usar exceções específicas (em vez de Exception genérica) facilita tanto
a leitura do código quanto a escrita de testes automatizados, pois cada
caso de erro previsto nos requisitos tem um tipo próprio para ser
verificado com `pytest.raises(...)`.
"""


class AlunoJaCadastradoError(Exception):
    """Levantada ao tentar cadastrar uma matrícula que já existe (RF01)."""


class AlunoNaoEncontradoError(Exception):
    """Levantada quando a matrícula informada não corresponde a nenhum aluno."""


class SalaNaoEncontradaError(Exception):
    """Levantada quando o código de sala informado não existe no sistema."""


class HorarioOcupadoError(Exception):
    """Levantada ao tentar reservar uma sala em horário já reservado (RF04)."""