# Este archivo contiene la información modificable para cambiar
# la información del modelo
# ============= GENERAL ================
semanas = 6
comunas = 3
nodos_totales = 40
# pueblitos = 1  # Separación del la cantidad de nodos
# Nodos de una comuna: pueblito al que pertenece y [Nodos correspondientes]
nodos_demanda = [1, 3, 4, 6, 8, 9, 10, 11, 13, 14, 16, 18, 19,
                 21, 22, 23, 24, 25, 26, 28, 29, 30, 32, 33, 34, 35, 37, 38, 39]
nodos_oferta = [0, 2, 5, 7, 12, 15, 17, 20,  27, 31, 36]
dinero_recibido = 1584000
periodos_sin_mantenimiento = 3
presupuesto_inicial = 2640000

# ================ DEMANDA ============
demanda_nodo = 65
desviacion_demanda = 0  # ! Cambiar desviación

# ============== CAÑERÍAS ============
flujo_caneria_maximo = 195
# Dice que si la cañeria cuesta x, entnonces el costo de arrelgo es x/2
proporcion_arreglo = 2
porcentaje_perdida_caneria = 0.2
desviacion_perdida = 0  # ! No hay desviación

costo_arreglo = 132000
desviacion_arreglo = 0  # ! No hay desviación
costo_instalar_caneria = 264000
desviacion_instalar_caneria = 0  # ! No hay desviación


# =================== FUENTES ===============
tipos_fuentes = ["Desalinizadora", "Tratamiento de aguas grises", "Tranques"]

costos_fuentes = {
    0: 475200000,
    1: 2112000,
    2: 316800000
}
# Indica el máximo de fuentes que se puede construir según el tipo
diccionario_fuentes = {
    0: 1,
    1: 2,
    2: 4
}
diccionario_suministro_fuentes = {
    0: 260,
    1: 130,
    2: 195
}
diccionario_perdida_fuentes = {
    0: 0.1,
    1: 0.04,
    2: 0.17
}
