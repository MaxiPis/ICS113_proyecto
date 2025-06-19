import pygame
import sys
import csv
import math
from random import randint, seed, uniform
from parametros import demanda_nodo, desviacion_demanda, semanas
from parametros import proporcion_arreglo, porcentaje_perdida_caneria, desviacion_perdida
import os

# Semilla para setear lo aleatorio
seed(1000)
path_directorio = "comunas_img"
imagenes = ['canela.jpg', 'illapel.jpg', 'salamanca.jpg']
escala_comunas = {
    0: 0.005,  # 1px = 5 m en Canela
    1: 0.005,  # 1px = 10 m en Illapel
    2: 0.005  # 1px = 50 m en Salamanca
}

distancia_entre_puntos = 5
radio_punto = 5

pygame.init()
font = pygame.font.SysFont(None, 18)

todos_los_puntos = []
lista_terrenos = []
lista_demanda = []
lista_canas = []
lista_costos = []
lista_costos_arreglo = []
lista_perdidas = []

for comuna_idx, image_path in enumerate(imagenes):
    # === ZOOM: aplicar solo en comuna 0 ===
    image_path = os.path.join(path_directorio, image_path)
    factor_zoom = 0.5  # 2 if comuna_idx == 0 else 1
    imagen_original = pygame.image.load(image_path)
    ancho, alto = imagen_original.get_size()
    image = pygame.transform.scale(
        imagen_original, (ancho * factor_zoom, alto * factor_zoom))
    screen = pygame.display.set_mode((ancho * factor_zoom, alto * factor_zoom))
    pygame.display.set_caption(
        f'Comuna {comuna_idx} - Agrega puntos y presiona S para guardar')

    puntos_comuna = []
    running = True
    current_label = 'R'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Convertir a coordenadas reales (sin zoom)
                x_real = event.pos[0] / factor_zoom
                y_real = event.pos[1] / factor_zoom
                nuevo_punto = [x_real, y_real, current_label]

                se_solapa = any(math.hypot(
                    x_real - p[0], y_real - p[1]) < distancia_entre_puntos for p in puntos_comuna)
                if not se_solapa:
                    puntos_comuna.append(nuevo_punto)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    current_label = 'B'
                elif event.key == pygame.K_r:
                    current_label = 'R'
                elif event.key == pygame.K_s:
                    for s in range(semanas):
                        for local_id, punto in enumerate(puntos_comuna):
                            x, y, label = punto
                            todos_los_puntos.append((x, y, label, comuna_idx))
                            lista_terrenos.append((comuna_idx, local_id))
                            demanda = 0 if label == 'B' else demanda_nodo + \
                                randint(-desviacion_demanda,
                                        desviacion_demanda)
                            lista_demanda.append(
                                (comuna_idx, local_id, s, demanda))

                    # === CALCULAR CANERÍAS ===
                    id_caneria_local = 0
                    distancias_reales = []

                    for i in range(len(puntos_comuna)):
                        for j in range(i + 1, len(puntos_comuna)):
                            x1, y1 = puntos_comuna[i][0], puntos_comuna[i][1]
                            x2, y2 = puntos_comuna[j][0], puntos_comuna[j][1]
                            distancia_px = math.hypot(x2 - x1, y2 - y1)
                            distancia_real = distancia_px * \
                                escala_comunas[comuna_idx]
                            distancias_reales.append(distancia_real)

                    min_real = min(distancias_reales)
                    max_real = max(distancias_reales)
                    rango_real = max_real - min_real if max_real != min_real else 1

                    idx = 0
                    for i in range(len(puntos_comuna)):
                        for j in range(i + 1, len(puntos_comuna)):
                            distancia_real = distancias_reales[idx]
                            norm = (distancia_real - min_real) / rango_real
                            costo = int(
                                10 + 990 * (math.exp(2.5 * norm) - 1) / (math.exp(5) - 1))
                            arreglo = costo // proporcion_arreglo
                            porcentaje_perdida = porcentaje_perdida_caneria + \
                                round(uniform(-desviacion_perdida,
                                              desviacion_perdida), 2)

                            lista_canas.append(
                                (comuna_idx, i, j, id_caneria_local))
                            lista_costos.append(
                                (id_caneria_local, comuna_idx, costo))
                            lista_costos_arreglo.append(
                                (id_caneria_local, comuna_idx, arreglo))
                            lista_perdidas.append(
                                (id_caneria_local, comuna_idx, porcentaje_perdida))
                            id_caneria_local += 1
                            idx += 1

                    running = False

        # === DIBUJAR IMAGEN ESCALADA Y PUNTOS ===
        screen.blit(image, (0, 0))
        for idx, (x, y, label) in enumerate(puntos_comuna):
            x_vis = int(x * factor_zoom)
            y_vis = int(y * factor_zoom)
            color = (255, 20, 147) if label == 'R' else (0, 0, 255)
            pygame.draw.circle(screen, color, (x_vis, y_vis), radio_punto)
            texto = font.render(str(idx), True, (0, 0, 0))
            screen.blit(texto, (x_vis + 5, y_vis - 5))

        pygame.display.flip()

# === GUARDAR ARCHIVOS ===
with open('dataset/terrenos.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['comuna', 'terreno'])
    csv.writer(f).writerows(lista_terrenos)

with open('dataset/demanda.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['comuna', 'terreno', 'tiempo', 'demanda'])
    csv.writer(f).writerows(lista_demanda)

with open('dataset/canerias.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['comuna', 'origen', 'destino', 'ID'])
    csv.writer(f).writerows(lista_canas)

with open('dataset/costo_instalar_canerias.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['ID', 'comuna', 'costo'])
    csv.writer(f).writerows(lista_costos)

with open('dataset/costo_arreglar_canerias.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['ID', 'comuna', 'costo'])
    csv.writer(f).writerows(lista_costos_arreglo)

with open('dataset/perdidas_canerias.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['caneria', 'comuna', 'porcentaje_perdida'])
    csv.writer(f).writerows(lista_perdidas)

pygame.quit()
sys.exit()
