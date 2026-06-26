# Sistema de Reserva de Salas de Estudo

Projeto de exemplo que implementa um sistema em memória para cadastro de
alunos, consulta de salas disponíveis, realização de reservas e consulta do
histórico de reservas.

Conteúdo principal
- `src/` – código-fonte (modelos, exceções, `sistema_reservas`)
- `tests/` – testes em `pytest` cobrindo os casos funcionais
- `relatorio_final.md` / `relatorio_final.pdf` – relatório final com resultados

Requisitos cobertos
- RF01: cadastro de alunos
- RF02: consulta de salas disponíveis
- RF03: realização de reservas
- RF04: prevenção de conflito de horário
- RF05: consulta do histórico de reservas
- RNF02: separação entre lógica e testes
- RNF03: tempo de resposta da reserva abaixo de 3s

Resultados dos testes
- Total de testes: 11
- Cobertura de código: 100%
- Status: todos os testes aprovados

Pré-requisitos
- Python 3.8+ (testado em 3.13)
- Para execução completa (opcional): internet para instalar dependências

Instalação (com internet)

```powershell
python -m pip install -r requirements.txt
```

Executar testes (com cobertura)

```powershell
python -m pytest --cov=src --cov-report=term-missing
```

Gerar relatório em PDF (já incluso em `relatorio_final.pdf`)

```powershell
python gerar_relatorio_pdf.py
```

Executar tudo (Windows)

```powershell
./run_all.bat
```

Execução offline (sem `pytest`)

Se você estiver em um ambiente sem acesso à internet e sem `pytest`, pode
usar a ferramenta interna fornecida neste projeto (ou rodar manualmente os
casos de teste apontados em `tests/`). O autor usou um mini-executor + o
módulo `trace` para validação local antes da entrega.

Licença / Observações
- Código de exemplo para fins didáticos.
