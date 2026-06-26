@echo off
REM Instala dependências (se houver internet)
python -m pip install -r requirements.txt

REM Executa testes com cobertura
python -m pytest --cov=src --cov-report=term-missing

REM Gera relatório PDF a partir do markdown
python gerar_relatorio_pdf.py

pause
