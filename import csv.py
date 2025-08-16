import csv

from pathlib import Path

from datetime import datetime



DATA_PATH = Path("datos/ventas.csv") # se espera: fecha, categoria, producto, precio, cantidad


# Cambio en la función leer_csv para usar DictReader
def leer_csv(ruta: Path) -> list[dict]:
    with open(ruta, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        filas = [row for row in reader]
    return filas



def normalizar_fecha(fila: dict) -> dict:

  fila["fecha"] = datetime.strptime(fila["fecha"], "%Y-%m-%d")

  return fila



def limpiar_filas(filas: list[dict]) -> list[dict]:

  limpias = []

  vistos = set()

  for fila in filas:

    clave = (fila["producto"].strip().lower())

    if clave in vistos:

      continue

    vistos.add(clave)



    fila["precio"] = float(fila["precio"])

    fila["cantidad"] = int(fila["cantidad"])



    if fila["categoria"] is not None:

      limpias.append(normalizar_fecha(fila))

  return limpias



def ingresos_por_categoria(filas: list[dict]) -> dict[str, float]:

  totales = {}

  for fila in filas:

    cat = fila["categoria"]

    if cat not in totales:

      totales[cat] = 0

    totales[cat] += fila["precio"] * fila["cantidad"]

  return totales



def main():

  if not DATA_PATH.exists():

    print("No se encontró el archivo de datos.")

    return



  filas = leer_csv(DATA_PATH)

  filas_limpias = limpiar_filas(filas)

  totales = ingresos_por_categoria(filas_limpias)



  for cat, total in totales.items():

    print(f"{cat}: {round(total, 2)}")



if __name__ == "__main__":

  main()