import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Leer la imagen y asumir que se ha escalado a 800x800
img = mpimg.imread('comuna_andacollo.jpg')  # Usa PNG, JPG, etc.

# Leer puntos desde el archivo
points = []
with open('puntos.txt', 'r') as f:
    for line in f:
        parts = line.strip().split(',')
        x = float(parts[0])
        y = float(parts[1])
        label = parts[2].strip()  # 'R' o 'B'
        radio = int(parts[3])
        cercanos = int(parts[4]) if len(parts) > 4 else 0
        points.append([x, y, label, radio, cercanos])


# Separar coordenadas
x_coords = [p[0] for p in points]
y_coords = [p[1] for p in points]

# Crear figura
fig, ax = plt.subplots(figsize=(6, 6))

# Mostrar imagen en el fondo (con origen en esquina superior izquierda)
ax.imshow(img, extent=[0, 600, 400, 0])  # ← invertimos el extent en Y aquí

# Graficar puntos en verde
ax.scatter(x_coords, y_coords, color='yellow', s=25)

# Escalas
ax.set_xlim(0, 600)
ax.set_ylim(400, 0)

# Etiquetas
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
#plt.gca().invert_yaxis()
plt.title('Grafico de Nodos finales')
plt.tight_layout()
plt.show()

