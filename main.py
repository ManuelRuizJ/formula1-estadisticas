import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Archivos CSV
PILOTOS_CSV = "clasificacion_pilotos_2025.csv"
CONSTRUCTORES_CSV = "clasificacion_constructores_2025.csv"

# Crear carpetas para gráficas
os.makedirs("graficas", exist_ok=True)
os.makedirs("graficas_acumuladas", exist_ok=True)

# --- Cargar datos ---
df_pilotos = pd.read_csv(PILOTOS_CSV)
df_constructores = pd.read_csv(CONSTRUCTORES_CSV)

# --- Convertir todas las columnas de GP a números ---
gp_cols_pilotos = df_pilotos.columns[2:]  # Totales + GP
for col in gp_cols_pilotos:
    df_pilotos[col] = pd.to_numeric(df_pilotos[col], errors='coerce').fillna(0).astype(int)

gp_cols_constructores = df_constructores.columns[2:]
for col in gp_cols_constructores:
    df_constructores[col] = pd.to_numeric(df_constructores[col], errors='coerce').fillna(0).astype(int)

# --- Tablas básicas ---
df_pilotos['Promedio_GP'] = df_pilotos[gp_cols_pilotos].mean(axis=1)
df_pilotos['STD_GP'] = df_pilotos[gp_cols_pilotos].std(axis=1)
df_constructores['Promedio_GP'] = df_constructores[gp_cols_constructores].mean(axis=1)
df_constructores['STD_GP'] = df_constructores[gp_cols_constructores].std(axis=1)

# Top 10 Pilotos y Constructores
df_pilotos.sort_values("Totales", ascending=False).head(10).to_csv("top10_pilotos.csv", index=False)
df_constructores.sort_values("Totales", ascending=False).head(10).to_csv("top10_constructores.csv", index=False)

# Pilotos con más victorias (25 pts)
df_pilotos['Victorias'] = (df_pilotos[gp_cols_pilotos] == 25).sum(axis=1)
df_pilotos.sort_values("Victorias", ascending=False)[['Piloto','Victorias']].to_csv("pilotos_mas_victorias.csv", index=False)

# Pilotos con más podios (>=18 pts)
df_pilotos['Podios'] = (df_pilotos[gp_cols_pilotos] >= 18).sum(axis=1)
df_pilotos.sort_values("Podios", ascending=False)[['Piloto','Podios']].to_csv("pilotos_mas_podios.csv", index=False)

# --- Gráficas originales ---
sns.set(style="whitegrid")

# Barras puntos totales
plt.figure(figsize=(12,6))
sns.barplot(x='Piloto', y='Totales', data=df_pilotos.sort_values("Totales", ascending=False))
plt.xticks(rotation=90)
plt.title("Puntos Totales por Piloto")
plt.tight_layout()
plt.savefig("graficas/puntos_totales_pilotos.png")
plt.close()

plt.figure(figsize=(10,5))
sns.barplot(x='Escudería', y='Totales', data=df_constructores.sort_values("Totales", ascending=False))
plt.xticks(rotation=45)
plt.title("Puntos Totales por Constructor")
plt.tight_layout()
plt.savefig("graficas/puntos_totales_constructores.png")
plt.close()

# Heatmaps
plt.figure(figsize=(20,10))
sns.heatmap(df_pilotos.set_index('Piloto')[gp_cols_pilotos], annot=True, fmt="d", cmap="YlGnBu")
plt.title("Puntos por GP - Pilotos")
plt.tight_layout()
plt.savefig("graficas/heatmap_pilotos.png")
plt.close()

plt.figure(figsize=(15,8))
sns.heatmap(df_constructores.set_index('Escudería')[gp_cols_constructores], annot=True, fmt="d", cmap="YlOrRd")
plt.title("Puntos por GP - Constructores")
plt.tight_layout()
plt.savefig("graficas/heatmap_constructores.png")
plt.close()

# Boxplots
plt.figure(figsize=(15,6))
sns.boxplot(data=df_pilotos[gp_cols_pilotos])
plt.xticks(rotation=90)
plt.title("Distribución de Puntos por GP - Pilotos")
plt.tight_layout()
plt.savefig("graficas/boxplot_pilotos.png")
plt.close()

plt.figure(figsize=(12,6))
sns.boxplot(data=df_constructores[gp_cols_constructores])
plt.xticks(rotation=90)
plt.title("Distribución de Puntos por GP - Constructores")
plt.tight_layout()
plt.savefig("graficas/boxplot_constructores.png")
plt.close()

# Evolución puntos GP (line plot)
plt.figure(figsize=(12,6))
for i, row in df_pilotos.iterrows():
    plt.plot(gp_cols_pilotos, row[gp_cols_pilotos], marker='o', label=row['Piloto'])
plt.xticks(rotation=90)
plt.title("Evolución de puntos por GP - Pilotos")
plt.ylabel("Puntos")
plt.legend(bbox_to_anchor=(1.05,1), loc='upper left')
plt.tight_layout()
plt.savefig("graficas/evolucion_puntos_pilotos.png")
plt.close()

plt.figure(figsize=(12,6))
for i, row in df_constructores.iterrows():
    plt.plot(gp_cols_constructores, row[gp_cols_constructores], marker='o', label=row['Escudería'])
plt.xticks(rotation=90)
plt.title("Evolución de puntos por GP - Constructores")
plt.ylabel("Puntos")
plt.legend(bbox_to_anchor=(1.05,1), loc='upper left')
plt.tight_layout()
plt.savefig("graficas/evolucion_puntos_constructores.png")
plt.close()

# --- 6. Acumulado ---
df_pilotos_acum = df_pilotos.copy()
df_pilotos_acum[gp_cols_pilotos] = df_pilotos_acum[gp_cols_pilotos].cumsum(axis=1)
df_constructores_acum = df_constructores.copy()
df_constructores_acum[gp_cols_constructores] = df_constructores_acum[gp_cols_constructores].cumsum(axis=1)

# Guardar CSV acumulativo
df_pilotos_acum.to_csv("clasificacion_pilotos_acumulado.csv", index=False)
df_constructores_acum.to_csv("clasificacion_constructores_acumulado.csv", index=False)

# Gráficas acumuladas
plt.figure(figsize=(12,6))
for i, row in df_pilotos_acum.iterrows():
    plt.plot(gp_cols_pilotos, row[gp_cols_pilotos], marker='o', label=row['Piloto'])
plt.xticks(rotation=90)
plt.title("Puntos acumulados por GP - Pilotos")
plt.ylabel("Puntos acumulados")
plt.legend(bbox_to_anchor=(1.05,1), loc='upper left')
plt.tight_layout()
plt.savefig("graficas_acumuladas/pilotos_acumulado.png")
plt.close()

plt.figure(figsize=(12,6))
for i, row in df_constructores_acum.iterrows():
    plt.plot(gp_cols_constructores, row[gp_cols_constructores], marker='o', label=row['Escudería'])
plt.xticks(rotation=90)
plt.title("Puntos acumulados por GP - Constructores")
plt.ylabel("Puntos acumulados")
plt.legend(bbox_to_anchor=(1.05,1), loc='upper left')
plt.tight_layout()
plt.savefig("graficas_acumuladas/constructores_acumulado.png")
plt.close()

print("✔ Todas las tablas y gráficas (normales y acumuladas) generadas")
