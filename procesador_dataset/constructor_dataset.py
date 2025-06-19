import csv
import os
from parametros import semanas, comunas, nodos_totales, nodos_demanda, nodos_oferta
from parametros import tipos_fuentes, diccionario_fuentes, diccionario_suministro_fuentes
from parametros import diccionario_suministro_fuentes, diccionario_perdida_fuentes, periodos_sin_mantenimiento, presupuesto_inicial
from parametros import flujo_caneria_maximo, dinero_recibido, costos_fuentes
from parametros import demanda_nodo, porcentaje_perdida_caneria, costo_arreglo, costo_instalar_caneria

######################### Calculos previos #########################

cant_canerias = nodos_totales * (nodos_totales-1)
cant_canerias /= 2
cant_canerias = int(cant_canerias)
numero_fuentes = len(diccionario_fuentes)

################### DECLARACIÓN DE FUNCIONES #########################


def leer_csv(ruta):
    lista = []
    carpeta = 'dataset'
    ruta = os.path.join(carpeta, ruta)
    # ruta = os.path.join(ruta)
    # Crear carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)

    with open(ruta, newline='') as f:
        reader = csv.reader(f)
        next(reader)  # Encabezado
        for fila in reader:
            comuna, origen, destino, id = int(fila[0]), int(
                fila[1]), int(fila[2]), int(fila[3])
            lista.append([comuna, origen, destino, id])
    return lista


def canerias_csv():
    l2 = []
    for comuna in range(comunas):
        conexiones = []
        for i in range(nodos_totales):
            for j in range(nodos_totales):
                if i != j:
                    conexiones.append([i, j])
        conexiones_unicas = []
        for con in conexiones:
            con_ordenada = sorted(con)
            if con_ordenada not in conexiones_unicas:
                conexiones_unicas.append(con_ordenada)
        for id_local, (origen, destino) in enumerate(conexiones_unicas):
            l2.append([comuna, origen, destino, id_local])
    return l2


def demanda_csv(demanda):
    l = []
    for t in range(semanas):
        for c in range(comunas):
            for i in range(nodos_totales):
                if i in nodos_oferta:
                    l.append([c, i, t, 0])
                else:
                    l.append([c, i, t, demanda])
    return l


def flujo_caneria_csv(flujo_max):
    l = []
    for c in range(comunas):
        for caneria in range(cant_canerias):
            l.append([caneria, c, flujo_max])
    return l


def perdidas_canerias_csv(perdida):
    l = []
    for comuna in range(comunas):
        for caneria in range(cant_canerias):
            l.append([caneria, comuna, perdida])
    return l


def terrenos_csv():
    l = []
    for comuna in range(comunas):
        for i in range(nodos_totales):
            l.append([comuna, i])
    return l


def costos_cañeria():
    canerias_lista = []
    for c in range(comunas):
        for a in range(cant_canerias):
            costo_caneria = costo_instalar_caneria
            canerias_lista.append([a, c, costo_caneria])

    return canerias_lista


def costos_tipos_fuente(diccionario_precios):
    costos = []
    indice = 0
    for comuna in range(comunas):
        for tipo in tipos_fuentes:
            id = tipos_fuentes.index(tipo)
            precio = diccionario_precios[id]
            costos.append([id, comuna, precio])
            indice += 1
    return costos


def construir_maximo_fuentes():
    lista = []
    retornan = []
    for comuna in range(comunas):
        for fuente in range(numero_fuentes):
            for terreno in range(nodos_totales):
                if terreno in nodos_oferta:
                    # aquí debe ser por fuente
                    maximo_fuentes = diccionario_fuentes[fuente]
                    sublista = [fuente, terreno, comuna, maximo_fuentes]
                else:
                    sublista = [fuente, terreno, comuna, 0]

                lista.append(sublista)
    return lista


def costo_arreglar_canerias(cant_canerias, comunas, costo_arreglo):
    lista_final = []

    for comu in range(comunas):
        for caneria in range(cant_canerias):
            lista_final.append([caneria, comu, costo_arreglo])
    return lista_final


def dimensiones_crear(comuna, semana, nodos_totale, numero_fuente, cant_caneria):
    lista = [comuna, semana, nodos_totale,
             numero_fuente, cant_caneria]
    return [lista]


def crear_dinero(semana, dinero):
    lista = []
    for sem in range(semana):
        lista.append([sem, dinero])
    return lista


def flujo_fuente_crear():
    lista = []
    for fuente in range(numero_fuentes):
        lista.append([fuente, diccionario_suministro_fuentes[fuente]])

    return lista


def perdidas_fuente_crear():
    lista = []
    for fuente in range(len(tipos_fuentes)):
        lista.append([fuente, diccionario_perdida_fuentes[fuente]])
    return lista


def periodos_sin_mantenimiento_crear():
    lista = [periodos_sin_mantenimiento]
    return [lista]


def presupuesto_crear():
    return [[presupuesto_inicial]]


def construir_csv(nombre_archivo, encabezados, datos):
    """
    Crea un archivo CSV con los encabezados y datos proporcionados.

    Parámetros:
    - nombre_archivo (str): Nombre del archivo CSV a crear.
    - encabezados (list): Lista de strings para los encabezados del CSV.
    - datos (list of lists): Lista de filas, cada una es una lista de valores.

    Ejemplo:
    construir_csv("salida.csv", ["Nombre", "Edad"], [
                  ["Ana", 30], ["Luis", 25]])
    """
    carpeta = 'dataset'
    nombre_archivo = os.path.join(carpeta, nombre_archivo)
    # nombre_archivo = os.path.join(nombre_archivo)

    # Crear carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)

    try:
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
            escritor = csv.writer(archivo_csv)
            escritor.writerow(encabezados)
            escritor.writerows(datos)
        print(f"Archivo '{nombre_archivo}' creado exitosamente.")
    except Exception as e:
        print(f"Error al crear el archivo CSV: {e}")

    """# Escribir a CSV
    with open("maximo_fuentes.csv", mode="w", newline="") as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(["Fuente", "Terreno", "Comuna",
                           "maximo"])  # encabezado
        escritor.writerows(lista)"""


def run():
    construir_csv("canerias.csv", [
                  "comuna", "origen", "destino", "ID"], canerias_csv())

    construir_csv("costo_instalar_canerias.csv", [
        "ID", "comuna", "costo"], costos_cañeria())

    construir_csv("costo_fuentes.csv", [
                  "ID", "comuna", "costo"], costos_tipos_fuente(costos_fuentes))

    construir_csv("demanda.csv",
                  ["comuna", "terreno", "tiempo", "demanda"],
                  demanda_csv(demanda_nodo)
                  )

    construir_csv("flujos_canerias.csv",
                  ["caneria", "comuna", "flujo_maximo"],
                  flujo_caneria_csv(flujo_caneria_maximo)
                  )

    construir_csv("perdidas_canerias.csv",
                  ["caneria", "comuna", "porcentaje_perdida"],
                  perdidas_canerias_csv(porcentaje_perdida_caneria))

    construir_csv("terrenos.csv",
                  ["comuna", "terreno"],
                  terrenos_csv())

    construir_csv("costo_arreglar_canerias.csv",
                  ["caneria", "comuna", "costo_arreglo"],
                  costo_arreglar_canerias(cant_canerias, comunas, costo_arreglo))

    construir_csv("dimensiones.csv", ["comunas", "semanas", "terrenos", "fuentes", "canerias"],
                  dimensiones_crear(comunas, semanas, nodos_totales, numero_fuentes, cant_canerias))

    construir_csv("dinero_recibido.csv",
                  ["semana", "dinero_recibido"],
                  crear_dinero(semanas, dinero_recibido))

    construir_csv("flujo_fuentes.csv",
                  ["fuente", "suministro_entregado_fuente"],
                  flujo_fuente_crear())

    construir_csv("maximo_fuentes.csv",
                  ["Fuente", "Terreno", "Comuna", "maximo"],
                  construir_maximo_fuentes())

    construir_csv("perdidas_fuentes.csv",
                  ["fuente", "porcentaje_perdida"],
                  perdidas_fuente_crear())

    construir_csv("periodos_maximos.csv",
                  ["periodos_sin_mantenimiento"],
                  periodos_sin_mantenimiento_crear())

    construir_csv("presupuesto.csv",
                  ["presupuesto_inicial"],
                  presupuesto_crear())


if __name__ == "__main__":
    run()
