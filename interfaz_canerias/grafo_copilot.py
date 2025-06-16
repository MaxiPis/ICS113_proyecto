import pygame
import sys
import math
from parametros import nodos_totales, terreno_oferta, terreno_demanda, caneria_origen_destino, canerias_operdando

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grafo Temporal")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
RED = (220, 20, 60)
GOLD = (255, 215, 0)
GRAY = (169, 169, 169)

# Fuente para etiquetas
font = pygame.font.SysFont(None, 20)

# Organizar los datos de canerias_operdando por tiempo
estado_por_tiempo = {}
for nombre, valor in canerias_operdando:
    partes = nombre.split("_")
    if len(partes) == 4:
        arco_id = int(partes[1])
        tiempo = int(partes[3])
        if tiempo not in estado_por_tiempo:
            estado_por_tiempo[tiempo] = {}
        estado_por_tiempo[tiempo][arco_id] = valor

# Obtener el número máximo de pasos de tiempo
max_tiempo = max(estado_por_tiempo.keys())

# Función para dibujar el grafo en un tiempo específico


def draw_graph(tiempo):
    screen.fill(WHITE)
    radius = 300
    center = (WIDTH // 2, HEIGHT // 2)
    angle_step = 2 * math.pi / nodos_totales
    positions = []

    # Calcular posiciones de los nodos
    for i in range(nodos_totales):
        angle = i * angle_step
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        positions.append((int(x), int(y)))

    # Dibujar aristas
    estado_actual = estado_por_tiempo.get(tiempo, {})
    for origen, destino, arco_id in caneria_origen_destino:
        color = GOLD if estado_actual.get(arco_id, 0.0) == 1.0 else GRAY
        pygame.draw.line(
            screen, color, positions[origen], positions[destino], 2)
        # Etiqueta del arco
        mid_x = (positions[origen][0] + positions[destino][0]) // 2
        mid_y = (positions[origen][1] + positions[destino][1]) // 2
        label = font.render(str(arco_id), True, BLACK)
        screen.blit(label, (mid_x, mid_y))

    # Dibujar nodos
    for i, pos in enumerate(positions):
        if i in terreno_oferta:
            color = BLUE
        elif i in terreno_demanda:
            color = RED
        else:
            color = BLACK
        pygame.draw.circle(screen, color, pos, 20)
        pygame.draw.circle(screen, BLACK, pos, 20, 2)
        label = font.render(str(i), True, BLACK)
        screen.blit(label, (pos[0] - 5, pos[1] - 5))

    # Mostrar tiempo actual
    tiempo_label = font.render(f"Tiempo: {tiempo}", True, BLACK)
    screen.blit(tiempo_label, (10, 10))

    pygame.display.flip()


# Estado inicial
tiempo_actual = 0
draw_graph(tiempo_actual)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if tiempo_actual < max_tiempo:
                    tiempo_actual += 1
                    draw_graph(tiempo_actual)
            elif event.key == pygame.K_LEFT:
                if tiempo_actual > 0:
                    tiempo_actual -= 1
                    draw_graph(tiempo_actual)

pygame.quit()
