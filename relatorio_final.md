# Relatório Final - Sistema de Reserva de Salas de Estudo

## 1. Objetivo
Implementar e validar um sistema de reservas de salas com regras de cadastro de alunos, consulta de salas disponíveis, realização de reservas, controle de conflitos de horário e histórico de reservas.

## 2. Requisitos do sistema
### Requisitos Funcionais (RF)
- RF01: O sistema deve permitir o cadastro de um novo aluno.
- RF02: O sistema deve permitir consultar as salas disponíveis.
- RF03: O aluno deve poder realizar uma reserva de sala.
- RF04: O sistema deve impedir reservas para horários já ocupados.
- RF05: O sistema deve permitir consultar o histórico de reservas realizadas.

### Requisitos Não Funcionais (RNF)
- RNF01: O sistema deve ser implementado em Python.
- RNF02: O código deve ser modularizado, com separação entre lógica e testes.
- RNF03: O tempo de resposta das funções deve ser inferior a 3 segundos.

## 3. Estrutura do projeto
- `src/` — código-fonte do sistema
  - `src/models.py`
  - `src/exceptions.py`
  - `src/sistema_reservas.py`
- `tests/` — testes automatizados em pytest
  - `tests/test_sistema_reservas.py`
- `README.md` — instruções de uso
- `requirements.txt` — dependências necessárias
- `relatorio_final.md` / `relatorio_final.pdf` — relatório final

## 4. Plano de Testes Funcionais
| Caso | Objetivo | Entrada | Resultado Esperado | Resultado Obtido | Status |
|------|----------|---------|--------------------|------------------|--------|
| TC01 | Cadastro de aluno com sucesso | Matrícula nova, nome e e-mail | Aluno cadastrado e presente no sistema | Aluno cadastrado com sucesso | Aprovado |
| TC02 | Cadastro duplicado rejeitado | Mesma matrícula duas vezes | Lançar erro `AlunoJaCadastradoError` | Erro lançado corretamente | Aprovado |
| TC03 | Consultar salas disponíveis sem reservas | Data e horário livre | Todas as salas disponíveis | Todas as salas retornadas | Aprovado |
| TC04 | Sala reservada não aparece disponível | Reserva de uma sala em horário específico | Sala ocupada omitida da lista | Sala omitida conforme esperado | Aprovado |
| TC05 | Reserva bem-sucedida | Aluno cadastrado e sala livre | Reserva criada com ID e dados corretos | Reserva criada corretamente | Aprovado |

## 5. Testes Automatizados
O arquivo de testes é `tests/test_sistema_reservas.py`. Ele contém os seguintes casos automatizados:
- `test_cadastrar_aluno_com_sucesso`
- `test_cadastrar_aluno_duplicado_lanca_erro`
- `test_consultar_salas_disponiveis_sem_reservas`
- `test_sala_reservada_nao_aparece_como_disponivel`
- `test_realizar_reserva_com_sucesso`
- `test_reserva_horario_ocupado_lanca_erro`
- `test_consultar_historico_de_reservas`
- `test_reserva_aluno_nao_cadastrado_lanca_erro`
- `test_reserva_sala_inexistente_lanca_erro`
- `test_tempo_resposta_reserva_abaixo_de_3_segundos`

Cada teste está comentado para explicar o cenário e o resultado esperado.

## 6. Validação executada
Os testes foram executados localmente com pytest.

### Resultado dos testes
- Total de testes: 10
- Status: 10 passed
- Tempo de execução: 0.57s

## 7. Evidências de testes
- Comando de execução:
  - `python -m pytest -q`
  - `python -m pytest --cov=src --cov-report=term-missing`
- Saída exibida no terminal confirma os 10 testes aprovados.
- A cobertura foi gerada para o pacote `src`.

## 8. Cobertura de testes e análise
- Cobertura total do pacote `src`: **98%**
- Arquivo analisado: `src/sistema_reservas.py`
- Linha não coberta: caminho de exceção em `consultar_historico` quando a matrícula não existe.

### O que está coberto
- Cadastro de novo aluno
- Rejeição de matrícula duplicada
- Consulta de salas disponíveis antes e depois de reservas
- Reserva de sala livre
- Bloqueio de reservas em horários ocupados
- Histórico de reservas para aluno cadastrado
- Erro ao reservar com aluno não cadastrado
- Erro ao reservar sala inexistente
- Tempo de resposta abaixo de 3 segundos

### O que não está coberto
- Validação do erro ao consultar histórico de reservas com matrícula inexistente

## 9. Conclusão
A implementação atende aos principais requisitos funcionais e não funcionais do sistema de reserva de salas. Os testes automatizados cobrem os principais cenários de uso e a análise de cobertura mostra um nível alto de cobertura (98%).

A única lacuna identificada é a ausência de teste para o caminho de exceção de `consultar_historico` com matrícula não cadastrada.
