# Este archivo contiene la información modificable para cambiar
# la información del modelo
# ============= GENERAL ================
semanas = 6
comunas = 3
nodos_totales = 5
# pueblitos = 1  # Separación del la cantidad de nodos
# Nodos de una comuna: pueblito al que pertenece y [Nodos correspondientes]
nodos_demanda = [0, 1, 2]
nodos_oferta = [3, 4]
dinero_recibido = 10
periodos_sin_mantenimiento = 3
presupuesto_inicial = 100

# ================ DEMANDA ============
demanda_nodo = 40
desviacion_demanda = 0  # ! Cambiar desviación

# ============== CAÑERÍAS ============
flujo_caneria_maximo = 120
# Dice que si la cañeria cuesta x, entnonces el costo de arrelgo es x/2
proporcion_arreglo = 2
porcentaje_perdida_caneria = 0.2
desviacion_perdida = 0  # ! No hay desviación
# Costo de la construcción de cañería
# costo_mismo_pueblito = 10
# costo_distinto_pueblito = 100
# costo_arreglo = 5  # Arreglo de canerias


# =================== FUENTES ===============
tipos_fuentes = ["Tranque", "Pozo", "Plantas de Filtración"]

costos_fuentes = {
    0: 120,
    1: 100,
    2: 180
}
# Indica el máximo de fuentes que se puede construir según el tipo
diccionario_fuentes = {
    0: 2,
    1: 4,
    2: 1
}
diccionario_suministro_fuentes = {
    0: 120,
    1: 80,
    2: 160
}
diccionario_perdida_fuentes = {
    0: 0.1,
    1: 0.2,
    2: 0.4
}
