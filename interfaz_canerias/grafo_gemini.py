import pygame
import math
import parametros  # Importa el archivo de parámetros


def draw_custom_circular_graph_with_time_steps():
    """
    Dibuja un grafo circular con propiedades personalizadas y permite navegar
    por los pasos de tiempo definidos en parametros.py usando las flechas.
    """

    # Inicializar Pygame
    pygame.init()

    # Configuración de la ventana
    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grafo Circular con Pasos de Tiempo")

    # Colores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)  # Nodos de oferta
    RED = (255, 0, 0)    # Nodos de demanda
    GRAY = (150, 150, 150)  # Arcos no operando
    GOLD = (255, 215, 0)  # Arcos operando (construidos)
    DARK_GRAY = (50, 50, 50)  # Color para el texto del arco

    # Fuentes para los números de los nodos y arcos
    font_node = pygame.font.Font(None, 30)  # Fuente para números de nodos
    # Fuente para números de arcos (más pequeña)
    font_arc = pygame.font.Font(None, 20)
    # Fuente para el indicador de tiempo
    font_time = pygame.font.Font(None, 40)

    # Obtener datos de parametros.py
    num_nodes = parametros.nodos_totales
    terreno_oferta = parametros.terreno_oferta
    terreno_demanda = parametros.terreno_demanda
    caneria_origen_destino = parametros.caneria_origen_destino
    all_canerias_operdando = parametros.canerias_operdando

    # --- Preprocesamiento de datos de tiempo ---
    # Agrupar los estados de las tuberías por paso de tiempo
    # Los arcos son 10 en total, así que cada 10 entradas es un nuevo paso de tiempo
    num_arcs_per_time_step = len(caneria_origen_destino)
    time_steps_data = []

    for i in range(0, len(all_canerias_operdando), num_arcs_per_time_step):
        current_time_step_data = all_canerias_operdando[i: i +
                                                        num_arcs_per_time_step]

        # Convertir a un diccionario para fácil acceso por ID de arco
        operando_status_at_time = {}
        for key_str, status_val in current_time_step_data:
            parts = key_str.split('_')
            if len(parts) >= 2:
                try:
                    # El ID del arco es parts[1] (ej. "0" de "r_0_0_0_t")
                    arc_id = int(parts[1])
                    operando_status_at_time[arc_id] = status_val
                except ValueError:
                    print(
                        f"Advertencia: No se pudo parsear el ID del arco de '{key_str}'")
        time_steps_data.append(operando_status_at_time)

    current_time_index = 0  # Empezar en el primer paso de tiempo (t=0)
    max_time_index = len(time_steps_data) - 1

    # Centro del círculo y radio
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    radius = min(WIDTH, HEIGHT) // 3

    # Calcular posiciones de los nodos (esto solo se hace una vez)
    node_positions = []
    for i in range(num_nodes):
        angle = 2 * math.pi * i / num_nodes
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))
        node_positions.append((x, y))

    # Bucle principal de Pygame
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if current_time_index < max_time_index:
                        current_time_index += 1
                elif event.key == pygame.K_LEFT:
                    if current_time_index > 0:
                        current_time_index -= 1

        # Obtener el estado actual de las tuberías para el tiempo actual
        current_operando_status = time_steps_data[current_time_index]

        # Rellenar el fondo
        screen.fill(WHITE)

        # Dibujar los arcos (líneas) y sus números
        for origen, destino, id_arco in caneria_origen_destino:
            color_arco = GRAY  # Color por defecto para arcos no operando

            # Usar el ID del arco para buscar su estado en current_operando_status
            if current_operando_status.get(id_arco) == 1.0:
                color_arco = GOLD  # Si el arco está operando, es dorado

            # Dibujar la línea del arco
            start_pos = node_positions[origen]
            end_pos = node_positions[destino]
            pygame.draw.line(screen, color_arco, start_pos, end_pos, 2)

            # Calcular la posición central del arco para el texto
            mid_x = (start_pos[0] + end_pos[0]) // 2
            mid_y = (start_pos[1] + end_pos[1]) // 2

            # Dibujar el número del arco
            text_surface_arc = font_arc.render(str(id_arco), True, DARK_GRAY)
            text_rect_arc = text_surface_arc.get_rect(center=(mid_x, mid_y))
            screen.blit(text_surface_arc, text_rect_arc)

        # Dibujar los nodos (círculos) y sus números
        for i, position in enumerate(node_positions):
            node_color = BLACK
            if i in terreno_oferta:
                node_color = BLUE
            elif i in terreno_demanda:
                node_color = RED

            pygame.draw.circle(screen, node_color, position, 20)
            pygame.draw.circle(screen, BLACK, position, 20, 2)

            # Dibujar el número del nodo
            text_surface_node = font_node.render(str(i), True, WHITE)
            text_rect_node = text_surface_node.get_rect(center=position)
            screen.blit(text_surface_node, text_rect_node)

        # Dibujar el indicador del paso de tiempo actual
        time_text = font_time.render(
            f"Tiempo: {current_time_index}", True, BLACK)
        # Posición en la esquina superior izquierda
        screen.blit(time_text, (10, 10))

        # Actualizar la pantalla
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    draw_custom_circular_graph_with_time_steps()
