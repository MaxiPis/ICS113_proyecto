import pygame
import math
from parametros import nodos_totales, terreno_oferta, terreno_demanda, caneria_origen_destino, canerias_operdando

# Inicializar pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
RED = (255, 0, 0)
GOLD = (212, 175, 55)
GRAY = (160, 160, 160)

# Ventana
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grafo dinámico por tiempo")

# Fuente
font = pygame.font.SysFont(None, 24)

# Posiciones circulares
center = (WIDTH // 2, HEIGHT // 2)
radius = WIDTH // 3
node_radius = 20

positions = []
for i in range(nodos_totales):
    angle = 2 * math.pi * i / nodos_totales
    x = center[0] + radius * math.cos(angle)
    y = center[1] + radius * math.sin(angle)
    positions.append((int(x), int(y)))

# === Preprocesar los datos por paso de tiempo ===
estado_arcos_por_t = {}
for nombre, valor in canerias_operdando:
    partes = nombre.split("_")
    if len(partes) == 4:
        _, arc_id, _, t = partes
        t = int(t)
        if t not in estado_arcos_por_t:
            estado_arcos_por_t[t] = {}
        estado_arcos_por_t[t][nombre] = valor

# Obtener valores de tiempo
tiempos_disponibles = sorted(estado_arcos_por_t.keys())
t_actual = tiempos_disponibles[0]
max_t = tiempos_disponibles[-1]

# === Bucle principal ===
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Estado actual
    estado_actual = estado_arcos_por_t.get(t_actual, {})

    # Dibujar aristas
    for origen, destino, arc_id in caneria_origen_destino:
        key = f"r_{arc_id}_0_{t_actual}"
        construida = estado_actual.get(key, 0.0) == 1.0
        color = GOLD if construida else GRAY
        pygame.draw.line(
            screen, color, positions[origen], positions[destino], 3)

        # ID en el medio
        mid_x = (positions[origen][0] + positions[destino][0]) // 2
        mid_y = (positions[origen][1] + positions[destino][1]) // 2
        text = font.render(str(arc_id), True, BLACK)
        screen.blit(text, (mid_x - 10, mid_y - 10))

    # Dibujar nodos
    for i, pos in enumerate(positions):
        color = BLUE if i in terreno_oferta else RED if i in terreno_demanda else BLACK
        pygame.draw.circle(screen, color, pos, node_radius)
        pygame.draw.circle(screen, BLACK, pos, node_radius, 2)
        num_text = font.render(str(i), True, BLACK)
        screen.blit(num_text, (pos[0] - 7, pos[1] - 7))

    # Mostrar tiempo actual
    t_text = font.render(f"t = {t_actual}", True, BLACK)
    screen.blit(t_text, (20, 20))

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and t_actual < max_t:
                t_actual += 1
            elif event.key == pygame.K_LEFT and t_actual > 0:
                t_actual -= 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
