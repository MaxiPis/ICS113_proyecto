import pygame
import sys
import csv
import math
from random import randint

imagenes = ['comuna_andacollo.jpg', 'comuna_salamanca.jpg']
escala_comunas = {
    0: 0.005,   # 1 px = 5 m en Andacollo
    1: 0.066,   # 1 px = 66 m en Salamanca
    2: 0.05     # Placeholder
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
lista_fuentes_maximas = []
lista_flujo_canerias = []

for comuna_idx, image_path in enumerate(imagenes):
    # === ZOOM: aplicar solo en comuna 0 ===
    factor_zoom = 2 if comuna_idx == 0 else 1
    imagen_original = pygame.image.load(image_path)
    ancho, alto = imagen_original.get_size()
    image = pygame.transform.scale(imagen_original, (ancho * factor_zoom, alto * factor_zoom))
    screen = pygame.display.set_mode((ancho * factor_zoom, alto * factor_zoom))
    pygame.display.set_caption(f'Comuna {comuna_idx} - Agrega puntos y presiona S para guardar')

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

                se_solapa = any(math.hypot(x_real - p[0], y_real - p[1]) < distancia_entre_puntos for p in puntos_comuna)
                if not se_solapa:
                    puntos_comuna.append(nuevo_punto)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    current_label = 'B'
                elif event.key == pygame.K_r:
                    current_label = 'R'
                elif event.key == pygame.K_s:
                    for local_id, punto in enumerate(puntos_comuna):
                        x, y, label = punto
                        todos_los_puntos.append((x, y, label, comuna_idx))
                        lista_terrenos.append((comuna_idx, local_id))
                        demanda = 0 if label == 'B' else 40 + randint(-5, 5)
                        for t in range(5):
                            lista_demanda.append((comuna_idx, local_id, t, demanda))
                            lista_demanda.sort(key=lambda x: (x[2], x[0]))
                        for fuentes in range(3):
                            fuentes_maximas = 0 if label == 'R' else randint(1, 3)
                            lista_fuentes_maximas.append((fuentes, local_id, comuna_idx, fuentes_maximas))

                    # === CALCULAR CANERÍAS ===
                    id_caneria_local = 0
                    distancias_reales = []

                    for i in range(len(puntos_comuna)):
                        for j in range(i + 1, len(puntos_comuna)):
                            x1, y1 = puntos_comuna[i][0], puntos_comuna[i][1]
                            x2, y2 = puntos_comuna[j][0], puntos_comuna[j][1]
                            distancia_px = math.hypot(x2 - x1, y2 - y1)
                            distancia_real = distancia_px * escala_comunas[comuna_idx]
                            distancias_reales.append(distancia_real)

                    min_real = min(distancias_reales)
                    max_real = max(distancias_reales)
                    rango_real = max_real - min_real if max_real != min_real else 1

                    idx = 0
                    for i in range(len(puntos_comuna)):
                        for j in range(i + 1, len(puntos_comuna)):
                            distancia_real = distancias_reales[idx]
                            norm = (distancia_real - min_real) / rango_real
                            costo = int(10 + 990 * (math.exp(2.5 * norm) - 1) / (math.exp(5) - 1))
                            arreglo = costo // 2
                            porcentaje_perdida = 0.08 + randint(-1, 1) / 100

                            lista_canas.append((comuna_idx, i, j, id_caneria_local))
                            lista_costos.append((id_caneria_local, comuna_idx, costo))
                            lista_costos_arreglo.append((id_caneria_local, comuna_idx, arreglo))
                            lista_perdidas.append((id_caneria_local, comuna_idx, porcentaje_perdida))
                            lista_flujo_canerias.append((id_caneria_local,comuna_idx, randint(130, 150)))
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
with open('datasets/terrenos.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['comuna', 'terreno'])
    csv.writer(f).writerows(lista_terrenos)

with open('datasets/demanda.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['comuna', 'terreno', 'tiempo', 'demanda'])
    csv.writer(f).writerows(lista_demanda)

with open('datasets/canerias.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['comuna', 'origen', 'destino', 'ID'])
    csv.writer(f).writerows(lista_canas)

with open('datasets/costo_instalar_canerias.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['ID', 'comuna', 'costo'])
    csv.writer(f).writerows(lista_costos)

with open('datasets/costo_arreglar_canerias.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['ID', 'comuna', 'costo'])
    csv.writer(f).writerows(lista_costos_arreglo)

with open('datasets/perdidas_canerias.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['caneria', 'comuna', 'porcentaje_perdida'])
    csv.writer(f).writerows(lista_perdidas)

with open('datasets/maximo_fuentes.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['Fuente', 'Terreno', 'Comuna', 'Maximo'])
    csv.writer(f).writerows(lista_fuentes_maximas)

with open('datasets/flujos_canerias.csv', 'w', newline='') as f:
    csv.writer(f).writerow(['caneria', 'comuna', 'flujo_maximo'])
    csv.writer(f).writerows(lista_flujo_canerias)


pygame.quit()
sys.exit()
