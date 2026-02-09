import pandas as pd
import sys

try:
    from app import get_gp_cols
except Exception as e:
    print('Error importing get_gp_cols from app.py:', e)
    sys.exit(1)

try:
    dfp = pd.read_csv("clasificacion_pilotos_acumulado.csv")
    dfc = pd.read_csv("clasificacion_constructores_acumulado.csv")
except Exception as e:
    print('Error leyendo CSV:', e)
    sys.exit(1)

gp_p = get_gp_cols(dfp)
gp_c = get_gp_cols(dfc)

print('GP columns pilotos (count):', len(gp_p))
print('Last GP columns pilotos:', gp_p[-6:])
print('GP columns constructores (count):', len(gp_c))
print('Last GP columns constructores:', gp_c[-6:])

# Mostrar últimos 6 valores para filas representativas
for name in ['L. Norris', 'M. Verstappen', 'O. Piastri']:
    if name in dfp['Piloto'].values:
        s = dfp.set_index('Piloto').loc[name, gp_p].tail(6)
        print(name, 'last 6 GP values:', s.to_dict())

for esc in ['McLaren', 'Mercedes', 'Red Bull']:
    if esc in dfc['Escudería'].values:
        s = dfc.set_index('Escudería').loc[esc, gp_c].tail(6)
        print(esc, 'last 6 GP values:', s.to_dict())
