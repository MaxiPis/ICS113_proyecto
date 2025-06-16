import csv
import os

"""
No ejecutar este código directamente desde \dataset.
Este código se ejecuta desde main.py
"""
##################### PARAMETROS MODIFICABLES #####################
semanas = 6
comunas = 1
nodos_totales = 5
pueblitos = 1  # Separación del la cantidad de nodos
# Nodos de una comuna: pueblito al que pertenece y [Nodos correspondientes]
terreno_oferta = [0, 2]
terreno_demanda = [1, 3, 4]
tipos_fuentes = ["Tranque"]
# Variables para el máximo de fuentes
numero_fuentes = 1
# Indica el máximo de fuentes que se puede construir según el tipo
diccionario_fuentes = {
    0: 1,
}
diccionario_suministro_fuentes = {
    0: 120
}
diccionario_perdida_fuentes = {
    0: 0.1,
}
demanda_nodo = 40
flujo_caneria_maximo = 120
porcentaje_caneria = 0.2
costos_fuentes = 20
# Costo de la construcción de cañería
costo_mismo_pueblito = 10
costo_distinto_pueblito = 100
costo_arreglo = 5  # Arreglo de canerias
dinero_recibido = 250  # No lo estamos tocando por ahora
periodos_sin_mantenimiento = 3
presupuesto_inicial = 100

# terreno_oferta = [0, 2, 5, 7, 12, 14]
# pueblitos = 3
# nodos_oferta = [[0, 2], [5, 7], [12, 14]]
# No modificar pero mover a parametros.py


def divisor_terrenos(lista, pueblitos):
    nodos = []
    subterrenos = []
    for pueblito in range(pueblitos):
        for elemento in range(int(len(terreno_oferta)/pueblitos)):
            indice = elemento + int(pueblito*len(lista)/pueblitos)
            subterrenos.append(lista[indice])
        nodos.append(subterrenos)
        subterrenos = []
    return nodos


nodos_oferta = divisor_terrenos(terreno_oferta, pueblitos)
nodos_demanda = divisor_terrenos(terreno_demanda, pueblitos)


######################### NO MODIFICAR #########################

cant_canerias = nodos_totales * (nodos_totales-1)
cant_canerias /= 2
cant_canerias = int(cant_canerias)


# Esta parte hace la separación por pueblitos
# terreno_oferta = [0, 2, 5, 7, 12, 14]
# pueblitos = 3
# nodos_oferta = [[0, 2], [5, 7], [12, 14]]


################################ FUNCIONES#########################


def leer_csv(ruta):
    lista = []
    carpeta = 'dataset'
    ruta = os.path.join(carpeta, ruta)

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
    l = []
    l2 = []
    for c in range(pueblitos):
        for i in range(nodos_totales):
            for j in range(nodos_totales):
                if not i == j:
                    l.append([c, i, j])
    for caneria_index in range(len(l)):
        l[caneria_index][1:] = sorted(l[caneria_index][1:])
    for e in l:
        if not e in l2:
            l2.append(e)
    for indice in range(len(l2)):
        l2[indice] = l2[indice] + [indice]
    return l2


def demanda_csv(demanda):
    l = []
    for t in range(semanas):
        for c in range(pueblitos):
            for i in range(nodos_totales):
                if i in terreno_oferta:
                    l.append([c, i, t, 0])
                else:
                    l.append([c, i, t, demanda])
    return l


def flujo_caneria_csv(flujo_max):
    l = []
    for c in range(pueblitos):
        for caneria in range(cant_canerias):
            l.append([caneria, c, flujo_max])
    return l


def perdidas_canerias_csv(perdida):
    l = []
    for comuna in range(pueblitos):
        for caneria in range(cant_canerias):
            l.append([caneria, comuna, perdida])
    return l


def terrenos_csv():
    l = []
    for comuna in range(pueblitos):
        for i in range(nodos_totales):
            l.append([comuna, i])
    return l


def costos_cañeria(costo_mismo_pueblito, costo_distinto_pueblito):
    lista = leer_csv('canerias.csv')
    costos = []
    for l in lista:
        id_nodo = l[3]
        comuna = l[0]
        nodo_origen = l[1]
        nodo_destino = l[2]
        for pueblito in nodos_demanda:
            if nodo_origen in pueblito:
                pueblito_nodo_origen = nodos_demanda.index(pueblito)
            if nodo_destino in pueblito:
                pueblito_nodo_destino = nodos_demanda.index(pueblito)
        for pueblito in nodos_oferta:
            if nodo_origen in pueblito:
                pueblito_nodo_origen = nodos_oferta.index(pueblito)
            if nodo_destino in pueblito:
                pueblito_nodo_destino = nodos_oferta.index(pueblito)
        if pueblito_nodo_origen == pueblito_nodo_destino:
            costos.append([id_nodo, comuna, costo_mismo_pueblito])
        else:
            costos.append([id_nodo, comuna, costo_distinto_pueblito])

    return costos


def costos_tipos_fuente(precio):
    costos = []
    indice = 0
    for comuna in range(comunas):
        for tipo in tipos_fuentes:
            id = tipos_fuentes.index(tipo)
            costos.append([id, comuna, precio])
            indice += 1
    return costos


def construir_maximo_fuentes():
    lista = []
    for comuna in range(comunas):
        for fuente in range(numero_fuentes):
            for terreno in range(nodos_totales):
                if terreno in terreno_oferta:
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
    for fuente in range(numero_fuentes):
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
        "ID", "comuna", "costo"], costos_cañeria(costo_mismo_pueblito, costo_distinto_pueblito))

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
                  perdidas_canerias_csv(porcentaje_caneria))

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
