"""
Testes automatizados do Sistema de Reserva de Salas de Estudo.
"""
from datetime import date, time

import pytest

from src.models import Sala
from src.sistema_reservas import SistemaReservas
from src.exceptions import (
    AlunoJaCadastradoError,
    AlunoNaoEncontradoError,
    SalaNaoEncontradaError,
    HorarioOcupadoError,
)


@pytest.fixture
def sistema():
    """Cria uma instância limpa do SistemaReservas para cada teste."""
    salas = [
        Sala(codigo="S01", nome="Sala de Estudo 1", capacidade=4),
        Sala(codigo="S02", nome="Sala de Estudo 2", capacidade=6),
    ]
    return SistemaReservas(salas=salas)


def test_cadastrar_aluno_com_sucesso(sistema):
    """TC01: um aluno novo deve ser cadastrado com os dados corretos."""
    aluno = sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")

    assert aluno.matricula == "2025001"
    assert aluno.nome == "Vívian Silva"
    assert "2025001" in sistema._alunos


def test_cadastrar_aluno_duplicado_lanca_erro(sistema):
    """TC02: a mesma matrícula não pode ser cadastrada duas vezes."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")

    with pytest.raises(AlunoJaCadastradoError):
        sistema.cadastrar_aluno("2025001", "Outro Nome", "outro@email.com")


def test_consultar_salas_disponiveis_sem_reservas(sistema):
    """TC03: sem reservas no horário, todas as salas devem aparecer como livres."""
    disponiveis = sistema.consultar_salas_disponiveis(date(2026, 7, 1), time(14, 0))
    codigos = {s.codigo for s in disponiveis}

    assert codigos == {"S01", "S02"}


def test_sala_reservada_nao_aparece_como_disponivel(sistema):
    """TC04: depois de reservada, a sala some da lista de salas disponíveis."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")
    sistema.realizar_reserva("2025001", "S01", date(2026, 7, 1), time(14, 0))

    disponiveis_mesmo_horario = sistema.consultar_salas_disponiveis(
        date(2026, 7, 1), time(14, 0)
    )
    disponiveis_outro_horario = sistema.consultar_salas_disponiveis(
        date(2026, 7, 1), time(16, 0)
    )

    assert {s.codigo for s in disponiveis_mesmo_horario} == {"S02"}
    assert {s.codigo for s in disponiveis_outro_horario} == {"S01", "S02"}


def test_realizar_reserva_com_sucesso(sistema):
    """TC05: aluno cadastrado consegue reservar uma sala livre."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")
    reserva = sistema.realizar_reserva("2025001", "S01", date(2026, 7, 1), time(14, 0))

    assert reserva.codigo_sala == "S01"
    assert reserva.matricula_aluno == "2025001"
    assert reserva.id_reserva == 1


def test_reserva_horario_ocupado_lanca_erro(sistema):
    """TC06: uma segunda reserva na mesma sala/horário deve ser rejeitada."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")
    sistema.cadastrar_aluno("2025002", "Outro Aluno", "outro@email.com")
    sistema.realizar_reserva("2025001", "S01", date(2026, 7, 1), time(14, 0))

    with pytest.raises(HorarioOcupadoError):
        sistema.realizar_reserva("2025002", "S01", date(2026, 7, 1), time(14, 0))


def test_consultar_historico_de_reservas(sistema):
    """TC07: o histórico deve retornar exatamente as reservas feitas pelo aluno."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")
    sistema.realizar_reserva("2025001", "S01", date(2026, 7, 1), time(14, 0))
    sistema.realizar_reserva("2025001", "S02", date(2026, 7, 2), time(10, 0))

    historico = sistema.consultar_historico("2025001")

    assert len(historico) == 2
    assert historico[0].codigo_sala == "S01"
    assert historico[1].codigo_sala == "S02"


def test_reserva_aluno_nao_cadastrado_lanca_erro(sistema):
    """TC08: aluno não cadastrado não pode realizar reservas."""
    with pytest.raises(AlunoNaoEncontradoError):
        sistema.realizar_reserva("9999999", "S01", date(2026, 7, 1), time(14, 0))


def test_reserva_sala_inexistente_lanca_erro(sistema):
    """TC09: usar uma sala inexistente deve falhar."""
    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")

    with pytest.raises(SalaNaoEncontradaError):
        sistema.realizar_reserva("2025001", "S99", date(2026, 7, 1), time(14, 0))


def test_tempo_resposta_reserva_abaixo_de_3_segundos(sistema):
    """TC10: a reserva deve responder em menos de 3 segundos."""
    import time as time_module

    sistema.cadastrar_aluno("2025001", "Vívian Silva", "vivian@email.com")

    inicio = time_module.perf_counter()
    sistema.realizar_reserva("2025001", "S01", date(2026, 7, 1), time(14, 0))
    duracao = time_module.perf_counter() - inicio

    assert duracao < 3.0
