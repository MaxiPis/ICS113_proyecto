# Librerías
import pygame
import math
import pandas as pd
from pathlib import Path
import sys
import os
from procesador_dataset.parametros import nodos_totales, nodos_oferta, nodos_demanda, comunas
# Funciones


def tratamiento___var___terrenos_fuentes_comunas_tiempo(lista_valores_variables):
    dicc_arcos_por_t = {}
    for nombre, valor in lista_valores_variables:
        partes = nombre.split("_")
        if len(partes) == 5:
            _, fuente_id, terreno_id, comuna_id, t = partes
            t = int(t)
            if t not in dicc_arcos_por_t:
                dicc_arcos_por_t[t] = {}
            dicc_arcos_por_t[t][nombre] = valor
    return dicc_arcos_por_t


def tratamiento___var___arcos_comunas_tiempo(lista_valores_variables):
    dicc_arcos_por_t = {}
    for nombre, valor in lista_valores_variables:
        partes = nombre.split("_")
        if len(partes) == 4:
            _, arc_id, _, t = partes
            t = int(t)
            if t not in dicc_arcos_por_t:
                dicc_arcos_por_t[t] = {}
            dicc_arcos_por_t[t][nombre] = valor
    return dicc_arcos_por_t


def colorear_binarias(variable, booleano):
    color = GRAY
    if variable == "l" and booleano:
        color = YELLOW
    elif variable == "q" and booleano:
        pass
    elif variable == "r" and booleano:
        color = ORANGE
    elif variable == "u" and booleano:
        color = VIOLET
    elif variable == "v" and booleano:
        color = GREEN
    return color


# Parámetros
# nodos_totales = 5
# nodos_oferta = [0, 2]
# nodos_demanda = [1, 3, 4]
# cantidad_de_comunas = 3

# Rutas
current_path = Path.cwd()
# parent_path = current_path.parent
csv_folder = current_path.joinpath("procesador_dataset")
csv_s = csv_folder.joinpath("dataset")
resultados = current_path.joinpath("resultados")

# Leer CSV
csv_canerias = csv_s.joinpath("canerias.csv")
df_canerias = pd.read_csv(csv_canerias)
caneria_origen_destino = df_canerias.values.tolist()

csv_demandas = csv_s.joinpath("demanda.csv")
demandas_ldl = pd.read_csv(csv_demandas).values.tolist()

csv_plata = resultados.joinpath("p.csv")
plata_ldl = pd.read_csv(csv_plata).values.tolist()

# Visuales
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (212, 175, 55)
GRAY = (160, 160, 160)
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

BLUE = (100, 100, 255)

INDIGO = (75, 0, 130)
VIOLET = (148, 0, 211)

# Ventana
ESCALA_VENTANA = 2
WIDTH, HEIGHT = 1920/ESCALA_VENTANA, 1080/ESCALA_VENTANA

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grafo dinámico por tiempo")

# Fuente
font = pygame.font.SysFont(None, 32)

# Posiciones circulares
center = (WIDTH // 2, HEIGHT // 2)
radius = HEIGHT // 2.35
node_radius = 15  # ! Este cambie

positions = []
for i in range(nodos_totales):
    angle = 2 * math.pi * i / nodos_totales
    x = center[0] + radius * math.cos(angle)
    y = center[1] + radius * math.sin(angle)
    positions.append((int(x), int(y)))

# Variables
variables_modelo = [["w", "x"], ["l", "q", "r", "u", "v", "y"], ["p"]]
variables_binarias = ["q", "r", "l", "u", "v"]
variables_estacionarias = ["x", "y", "p", "demanda"]
variables_modelo_listas = ["r", "l", "u", "v"]

tecla_variable_map = {
    pygame.K_l: "l",
    pygame.K_q: "q",
    pygame.K_r: "r",
    pygame.K_u: "u",
    pygame.K_v: "v"
}

entrada = "v"

# Y
estado_variable_y = {}
lectura_y = resultados.joinpath(f"y.csv")
ldl_y = pd.read_csv(lectura_y).values.tolist()
estado_variable_y = tratamiento___var___arcos_comunas_tiempo(ldl_y)

# X
estado_variable_x = {}
lectura_x = resultados.joinpath(f"x.csv")
ldl_x = pd.read_csv(lectura_x).values.tolist()
estado_variable_x = tratamiento___var___terrenos_fuentes_comunas_tiempo(ldl_x)

# Variables binarias iniciales
lectura_variable = resultados.joinpath(f"{entrada}.csv")
ldl_variable = pd.read_csv(lectura_variable).values.tolist()
estado_por_t_bin = tratamiento___var___arcos_comunas_tiempo(ldl_variable)

# Tiempo y comuna
tiempos_disponibles = sorted(estado_por_t_bin.keys())
comunas_disponibles = [i for i in range(comunas)]
t_actual = tiempos_disponibles[0]
max_t = tiempos_disponibles[-1]
comuna_actual = comunas_disponibles[0]
max_comuna = comunas_disponibles[-1]

# Loop principal
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    estado_actual_binarias = estado_por_t_bin.get(t_actual, {})

    # Aristas
    for _, origen, destino, arc_id in caneria_origen_destino:
        key = f"{entrada}_{arc_id}_{comuna_actual}_{t_actual}"
        key_for_y = f"y_{arc_id}_{comuna_actual}_{t_actual}"

        estado_variable_y_values = estado_variable_y.get(t_actual, {})
        flujo = estado_variable_y_values.get(key_for_y, 0.0)

        booleano = estado_actual_binarias.get(key, 0.0) == 1.0
        mostrar_linea = (flujo > 0.0) or booleano

        if mostrar_linea:
            color = colorear_binarias(
                entrada, booleano) if entrada in variables_binarias else GRAY
            grosor = max(2, min(6, int(flujo * 0.8)))
            pygame.draw.line(
                screen, color, positions[origen], positions[destino], grosor)

            if flujo > 0.0:
                mid_x = (positions[origen][0] + positions[destino][0]) // 2
                mid_y = (positions[origen][1] + positions[destino][1]) // 2
                text = font.render(f"{round(flujo, 1)}", True, BLACK)
                screen.blit(text, (mid_x - 10, mid_y - 10))

    # Nodos
    for i, pos in enumerate(positions):
        color = BLUE if i in nodos_oferta else RED if i in nodos_demanda else BLACK
        pygame.draw.circle(screen, color, pos, node_radius)
        pygame.draw.circle(screen, BLACK, pos, node_radius, 2)

        # Texto centrado dentro del nodo (ID del nodo)
        id_text = font.render(str(i), True, BLACK)
        id_rect = id_text.get_rect(center=pos)
        screen.blit(id_text, id_rect)

        # Buscar demanda asociada
        valor_demanda = 0
        for fila in demandas_ldl:
            if fila[:3] == [comuna_actual, i, t_actual]:
                valor_demanda = fila[3]
                break

        # Mostrar demanda debajo del nodo (si hay)
        if valor_demanda > 0:
            demanda_text = font.render(f"dem: {valor_demanda}", True, BLACK)
            demanda_rect = demanda_text.get_rect(
                midtop=(pos[0], pos[1] + node_radius + 5))
            screen.blit(demanda_text, demanda_rect)

    # Título centrado
    titulo = f"Variable: {entrada.upper()}  |  t = {t_actual}  |  comuna = {comuna_actual}  |  dinero = {plata_ldl[t_actual][1]}"
    titulo_render = font.render(titulo, True, BLACK)
    titulo_rect = titulo_render.get_rect(center=(WIDTH // 2, 30))
    screen.blit(titulo_render, titulo_rect)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT and t_actual < max_t:
                t_actual += 1
            elif event.key == pygame.K_LEFT and t_actual > 0:
                t_actual -= 1
            elif event.key == pygame.K_DOWN and comuna_actual > 0:
                comuna_actual -= 1
            elif event.key == pygame.K_UP and comuna_actual < max_comuna:
                comuna_actual += 1

            elif event.key in tecla_variable_map:
                nueva_entrada = tecla_variable_map[event.key]
                lectura_variable = resultados.joinpath(f"{nueva_entrada}.csv")
                ldl_variable = pd.read_csv(lectura_variable).values.tolist()
                estado_por_t_bin = tratamiento___var___arcos_comunas_tiempo(
                    ldl_variable)
                entrada = nueva_entrada
                print(f"Cambiando a variable '{entrada}' para visualización.")

            elif event.key == pygame.K_x:
                estado_x_t = estado_variable_x.get(t_actual, {})
                print(
                    f"--- Estado de 'x' en t={t_actual}, comuna={comuna_actual} ---")
                for k, v in estado_x_t.items():
                    partes = k.split("_")
                    if len(partes) == 5:
                        _, fuente_id, terreno_id, comuna_id, tiempo = partes
                        if int(comuna_id) == comuna_actual and int(tiempo) == t_actual:
                            print(f"{k} : {v}")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
