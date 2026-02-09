import requests
from bs4 import BeautifulSoup
import csv

URL_2025 = "https://www.caranddriver.com/es/formula-1/clasificacion/a63305490/clasificacion-mundial-f1-2025/"
headers = {"User-Agent": "Mozilla/5.0"}


def obtener_tablas_f1():
    response = requests.get(URL_2025, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    tablas = soup.find_all("table")
    return tablas


def extraer_pilotos_completo(tabla_pilotos):
    filas = tabla_pilotos.find_all("tr")
    
    # Encabezado: extraer nombres de Tot. y GP
    header = filas[0]
    columnas_header = header.find_all(["th", "td"])
    gp_names = [col.get_text(strip=True) for col in columnas_header[1:]]  # Pil. + Tot. + GPs

    datos_pilotos = []
    for fila in filas[1:]:
        columnas = fila.find_all("td")
        if len(columnas) < 3:
            continue
        nombre = columnas[1].get_text(strip=True)       # Piloto
        puntos_totales = columnas[2].get_text(strip=True)  # Totales
        if puntos_totales == "-" or puntos_totales == "":
            puntos_totales = "0"

        # Puntos por GP
        puntos_gps = []
        for td in columnas[3:]:
            valor = td.get_text(strip=True)
            if valor == "-" or valor == "":
                valor = "0"
            puntos_gps.append(valor)

        datos_pilotos.append([nombre, puntos_totales] + puntos_gps)

    return gp_names, datos_pilotos


def extraer_constructores_completo(tabla_constructores):
    filas = tabla_constructores.find_all("tr")

    # Encabezado: Tot. y GP
    header = filas[0]
    columnas_header = header.find_all(["th", "td"])
    gp_names = [col.get_text(strip=True) for col in columnas_header[1:]]  # Equ. + Tot. + GPs

    datos_constructores = []
    for fila in filas[1:]:
        columnas = fila.find_all("td")
        if len(columnas) < 3:
            continue
        nombre = columnas[1].get_text(strip=True)       # Equ.
        puntos_totales = columnas[2].get_text(strip=True)  # Totales
        if puntos_totales == "-" or puntos_totales == "":
            puntos_totales = "0"

        # Puntos por GP
        puntos_gps = []
        for td in columnas[3:]:
            valor = td.get_text(strip=True)
            if valor == "-" or valor == "":
                valor = "0"
            puntos_gps.append(valor)

        datos_constructores.append([nombre, puntos_totales] + puntos_gps)

    return gp_names, datos_constructores


def guardar_csv(filename, encabezados, datos):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(encabezados)
        writer.writerows(datos)


if __name__ == "__main__":
    tablas = obtener_tablas_f1()
    if len(tablas) < 2:
        print("❌ No se encontraron suficientes tablas en el HTML.")
        exit()

    # Pilotos
    gp_names_pilotos, pilotos_completo = extraer_pilotos_completo(tablas[0])
    encabezados_pilotos = ["Piloto", "Totales"] + gp_names_pilotos[1:]  # ignoramos "Pil." inicial
    guardar_csv("clasificacion_pilotos_2025.csv", encabezados_pilotos, pilotos_completo)
    print("➡ Archivo 'clasificacion_pilotos_2025.csv' generado")

    # Constructores
    gp_names_constructores, constructores_completo = extraer_constructores_completo(tablas[1])
    encabezados_constructores = ["Escudería", "Totales"] + gp_names_constructores[1:]  # ignoramos "Equ." inicial
    guardar_csv("clasificacion_constructores_2025.csv", encabezados_constructores, constructores_completo)
    print("➡ Archivo 'clasificacion_constructores_2025.csv' generado")
