# Relatório Final - Sistema de Reserva de Salas de Estudo

## 1. Objetivo
Implementar e validar um sistema de reservas de salas com regras de cadastro de alunos, consulta de salas disponíveis, realização de reservas, controle de conflitos de horário e histórico de reservas.

## 2. Estrutura do projeto
- Pacote principal: src/
- Módulos principais:
  - src/models.py
  - src/exceptions.py
  - src/sistema_reservas.py
- Testes automatizados: tests/test_sistema_reservas.py
- Arquivo de dependências: requirements.txt

## 3. Requisitos cobertos
- RF01: cadastro de alunos
- RF02: consulta de salas disponíveis
- RF03: realização de reservas
- RF04: prevenção de conflito de horário
- RF05: consulta de histórico de reservas
- RNF02: separação entre lógica de negócio e testes
- RNF03: tempo de resposta da reserva abaixo de 3 segundos

## 4. Validação executada
Os testes foram executados com pytest no ambiente local.

### Resultado dos testes
- Total de testes: 10
- Status: 10 passed
- Tempo de execução: 0.57s

### Cobertura de código
- Arquivo principal: src/sistema_reservas.py
- Cobertura total do pacote src: 98%

## 5. Conclusão
A implementação foi validada com sucesso, com todos os testes automatizados aprovados e cobertura elevada do código principal.
