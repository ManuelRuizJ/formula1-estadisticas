import pandas as pd

dfp = pd.read_csv('clasificacion_pilotos_acumulado.csv')
dfc = pd.read_csv('clasificacion_constructores_acumulado.csv')

with open('cols_report.txt', 'w', encoding='utf-8') as f:
    f.write('PILOTOS cols count: ' + str(len(dfp.columns)) + '\n')
    f.write('PILOTOS cols: ' + str(list(dfp.columns)) + '\n\n')
    f.write('CONSTRUCTORES cols count: ' + str(len(dfc.columns)) + '\n')
    f.write('CONSTRUCTORES cols: ' + str(list(dfc.columns)) + '\n')

print('Report written to cols_report.txt')
