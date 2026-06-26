from pathlib import Path
p = Path('relatorio_final.pdf')
print('path:', p.resolve())
print('exists:', p.exists())
if not p.exists():
    raise SystemExit(1)

b = p.read_bytes()
checks = {
    'title': 'Relatório Final - Sistema de Reserva de Salas de Estudo',
    'coverage': 'Cobertura total do pacote `src`: 100%'
}
for k, v in checks.items():
    found = v.encode('utf-8') in b
    print(f"{k}_found: {found}")
print('size:', p.stat().st_size)
