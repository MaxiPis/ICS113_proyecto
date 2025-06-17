import pandas as pd
from gurobipy import Model, GRB, quicksum
import os
import csv
from dataset.constructor_dataset import run

# ==== CREACIÓN DE LOS DATASET ======
run()
ruta_carpeta = "dataset"

# Diccionario general de datos
datos = {}
# === INFORMACION ===
datos["dimensiones"] = pd.read_csv(ruta_carpeta+"/"+"dimensiones.csv")
datos["terrenos"] = pd.read_csv(ruta_carpeta+"/"+"terrenos.csv")
datos["canerias"] = pd.read_csv(ruta_carpeta+"/"+"canerias.csv")

# === COSTOS ===
datos["costo_arreglar_canerias"] = pd.read_csv(
    ruta_carpeta+"/"+"costo_arreglar_canerias.csv")
datos["costo_fuentes"] = pd.read_csv(ruta_carpeta+"/"+"costo_fuentes.csv")
datos["costo_instalar_canerias"] = pd.read_csv(
    ruta_carpeta+"/"+"costo_instalar_canerias.csv")

# === DEMANDA Y FLUJO ===
datos["demanda"] = pd.read_csv(ruta_carpeta+"/"+"demanda.csv")
datos["flujos_canerias"] = pd.read_csv(ruta_carpeta+"/"+"flujos_canerias.csv")
datos["flujo_fuente"] = pd.read_csv(ruta_carpeta+"/"+"flujo_fuentes.csv")

# === PÉRDIDAS ===
datos["perdidas_canerias"] = pd.read_csv(
    ruta_carpeta+"/"+"perdidas_canerias.csv")
datos["perdidas_fuentes"] = pd.read_csv(
    ruta_carpeta+"/"+"perdidas_fuentes.csv")

# === PARÁMETROS ECONÓMICOS ===
datos["dinero_recibido"] = pd.read_csv(ruta_carpeta+"/"+"dinero_recibido.csv")
datos["presupuesto"] = pd.read_csv(ruta_carpeta+"/"+"presupuesto.csv")

# === RESTRICCIONES ===
datos["maximo_fuentes"] = pd.read_csv(ruta_carpeta+"/"+"maximo_fuentes.csv")
datos["periodos_maximos"] = pd.read_csv(
    ruta_carpeta+"/"+"periodos_maximos.csv")
#################


# d(n, s, t): demanda
def d(n, s, t):
    df = datos["demanda"]
    resultado = df[(df.iloc[:, 0] == n) &
                   (df.iloc[:, 1] == s) &
                   (df.iloc[:, 2] == t)]
    return float(resultado.iloc[0, 3]) if not resultado.empty else 0.0

# k(a, s): capacidad cañerías


def k(a, s):
    df = datos["flujos_canerias"]
    resultado = df[(df.iloc[:, 0] == a) & (df.iloc[:, 1] == s)]
    return float(resultado.iloc[0, 2])

# m(f): flujo máximo fuente


def m(f):
    df = datos["flujo_fuente"]
    resultado = df[df.iloc[:, 0] == f]
    return float(resultado.iloc[0, 1])

# alpha(a, s): pérdida cañería


def alpha(a, s):
    df = datos["perdidas_canerias"]
    resultado = df[(df.iloc[:, 0] == a) & (df.iloc[:, 1] == s)]
    return float(resultado.iloc[0, 2])

# beta(f): pérdida fuente


def beta(f):
    df = datos["perdidas_fuentes"]
    resultado = df[df.iloc[:, 0] == f]
    return float(resultado.iloc[0, 1])

# c(f, s): costo construir fuente


def c(f, s):
    df = datos["costo_fuentes"]
    resultado = df[(df.iloc[:, 0] == f) & (df.iloc[:, 1] == s)]
    return float(resultado.iloc[0, 2])

# c_1(a, s): costo instalar cañería


def c_1(a, s):
    df = datos["costo_instalar_canerias"]
    resultado = df[(df.iloc[:, 0] == a) & (df.iloc[:, 1] == s)]
    return float(resultado.iloc[0, 2])

# c_2(a, s): costo arreglo cañería


def c_2(a, s):
    df = datos["costo_arreglar_canerias"]
    resultado = df[(df.iloc[:, 0] == a) & (df.iloc[:, 1] == s)]
    return float(resultado.iloc[0, 2])

# I_0(): presupuesto inicial


def I_0():
    df = datos["presupuesto"]
    return float(df.iloc[0, 0])

# e(t): dinero recibido


def e(t):
    df = datos["dinero_recibido"]
    resultado = df[df.iloc[:, 0] == t]
    return float(resultado.iloc[0, 1])

# g(f, n, s): máximo fuentes por terreno


def g(f, n, s):
    df = datos["maximo_fuentes"]
    resultado = df[
        (df.iloc[:, 0] == f) & (df.iloc[:, 1] == n) & (df.iloc[:, 2] == s)
    ]
    return int(resultado.iloc[0, 3])

# phi(): periodos máximos sin mantenimiento


def phi():
    df = datos["periodos_maximos"]
    return int(df.iloc[0, 0])


def pruebas():
    """
    Llamar esta función para ver los conjunto de datos generados.
    """
    # =====================
    # === Dimensiones ===
    # =====================
    cantidad_de_comunidades = int(datos["dimensiones"].iloc[0]["comunidades"])
    cantidad_de_semanas = int(datos["dimensiones"].iloc[0]["semanas"])
    cantidad_de_terrenos = int(datos["dimensiones"].iloc[0]["terrenos"])
    cantidad_de_fuentes = int(datos["dimensiones"].iloc[0]["fuentes"])
    cantidad_de_canerias = int(datos["dimensiones"].iloc[0]["canerias"])

    # =====================
    # === Conjuntos ===
    # =====================
    comunas = list(range(cantidad_de_comunidades))
    semanas = list(range(cantidad_de_semanas))
    fuentes = list(range(cantidad_de_fuentes))

    terrenos = {
        c: list(datos["terrenos"][datos["terrenos"]["comuna"] == c]["terreno"])
        for c in comunas
    }

    canerias = {
        c: [(int(f["origen"]), int(f["destino"]))
            for _, f in datos["canerias"][datos["canerias"]["comuna"] == c].iterrows()]
        for c in comunas
    }
    print(canerias)
    # ================================
    # === Parámetros de prueba ===
    # ================================

    # Variables para pruebas
    n = 0  # terreno
    s = 0  # comuna
    t = 0  # semana
    a = 0  # caneria
    f = 0  # fuente

    print("\n--- PARÁMETROS DEL MODELO ---")
    print(
        f"Demanda en terreno n={n}, comuna s={s}, semana t={t}: {d(n, s, t)} m³/s")
    print(f"Capacidad cañería a={a}, comuna s={s}: {k(a, s)} m³/s")
    print(f"Flujo máximo de fuente f={f}: {m(f)} m³/s")
    print(f"Pérdida en cañería a={a}, comuna s={s}: {alpha(a, s)} %")
    print(f"Pérdida en fuente f={f}: {beta(f)} %")
    print(f"Costo construir fuente f={f}, comuna s={s}: {c(f, s)} CLP")
    print(f"Costo instalar cañería a={a}, comuna s={s}: {c_1(a, s)} CLP")
    print(f"Costo arreglar cañería a={a}, comuna s={s}: {c_2(a, s)} CLP")
    print(f"Presupuesto inicial (t={t}): {I_0()} CLP")
    print(f"Dinero recibido en semana t={t}: {e(t)} CLP·s/m³")
    print(
        f"Máx. fuentes tipo f={f} en terreno n={n}, comuna s={s}: {g(f, n, s)}")
    print(f"Periodo máximo sin mantenimiento: {phi()} semanas")

    # ===============================
    # === Información estructural ===
    # ===============================
    print("\n--- DIMENSIONES DEL MODELO ---")
    print(f"Cantidad de Comunidades: {cantidad_de_comunidades}")
    print(f"Cantidad de Semanas: {cantidad_de_semanas}")
    print(f"Cantidad de Terrenos: {cantidad_de_terrenos}")
    print(f"Cantidad de Fuentes: {cantidad_de_fuentes}")
    print(f"Cantidad de Cañerías: {cantidad_de_canerias}")

    print("\n--- CONJUNTOS GENERADOS ---")
    print(f"Comunas: {comunas}")
    print(f"Semanas: {semanas}")
    print(f"Fuentes: {fuentes}")

    print("\nTerrenos por Comuna:")
    for comuna, lista_terrenos in terrenos.items():
        print(f"  Comuna {comuna}: {lista_terrenos}")

    print("\nCañerías por Comuna (origen → destino):")
    for comuna, lista_canerias in canerias.items():
        print(f"  Comuna {comuna}: {lista_canerias}")


#### Creacion de modelo, conjuntos y definicion de variables####
def construir_modelo():
    """
    Esta función debe construir el modelo de optimización utilizando Gurobi
    y los datos provistos en el diccionario `data`.
    """
    cantidad_de_comunidades = int(datos["dimensiones"].iloc[0]["comunas"])
    cantidad_de_semanas = int(datos["dimensiones"].iloc[0]["semanas"])
    cantidad_de_terrenos = int(datos["dimensiones"].iloc[0]["terrenos"])
    cantidad_de_fuentes = int(datos["dimensiones"].iloc[0]["fuentes"])
    cantidad_de_canerias = int(datos["dimensiones"].iloc[0]["canerias"])

    comunas = [e for e in range(cantidad_de_comunidades)]
    semanas = [e for e in range(cantidad_de_semanas)]
    fuentes = [e for e in range(cantidad_de_fuentes)]

    # Terrenos por comuna desde datos
    terrenos = {
        c: list(datos["terrenos"][datos["terrenos"]["comuna"] == c]["terreno"])
        for c in comunas
    }

    # Cañerías por comuna como tuplas (origen, destino)
    canerias = {
        c: [(int(f["origen"]), int(f["destino"]))
            for _, f in datos["canerias"][datos["canerias"]["comuna"] == c].iterrows()]
        for c in comunas
    }

    # Modelo
    w = {}
    x = {}
    y = {}
    p = {}
    q = {}
    r = {}
    v = {}
    l = {}
    u = {}

    modelo = Model()
    for tt in semanas:
        # Dinero al final de la semana t
        p[tt] = modelo.addVar(vtype=GRB.CONTINUOUS, name=f"p_{tt}")
        for ss in comunas:
            for nn in terrenos[ss]:
                # terrenos[ss]= [0,1,2]
                # nn = 0
                for ff in fuentes:
                    # Numero de fuentes totales tipo f en terreno n , comuna s ,semana t
                    x[ff, nn, ss, tt] = modelo.addVar(
                        vtype=GRB.INTEGER, lb=0, name=f"x_{ff}_{nn}_{ss}_{tt}")

                    # Numero de fuentes nuevas tipo f en terreno n , comuna s ,semana t
                    w[ff, nn, ss, tt] = modelo.addVar(
                        vtype=GRB.INTEGER, lb=0, name=f"w_{ff}_{nn}_{ss}_{tt}")

            # Recorremos el diccionario de cañerias
            for aa in canerias[ss]:
                # canerias[ss]=[(2, 3), (1, 2)]
                # aa =(2,3)
                # buscamos la posicion de las tuplas de las cañerias
                ind = canerias[ss].index(aa)
                # hasta aqui ta bien

                # flujo de agua de caneria a, comuna s, semana t
                y[ind, ss, tt] = modelo.addVar(
                    vtype=GRB.CONTINUOUS, lb=0, name=f"y_{ind}_{ss}_{tt}")

                # Se construye caneria a en la comuna s en la semana t
                q[ind, ss, tt] = modelo.addVar(
                    vtype=GRB.BINARY, name=f"q_{ind}_{ss}_{tt}")

                # Esta operando la caneria a en la comuna s en la semana t
                r[ind, ss, tt] = modelo.addVar(
                    vtype=GRB.BINARY, name=f"r_{ind}_{ss}_{tt}")

                # Se encuentra instalada la caneria a en la comuna s en la semana t
                v[ind, ss, tt] = modelo.addVar(
                    vtype=GRB.BINARY, name=f"v_{ind}_{ss}_{tt}")

                # Se arregla la caneria a en la comuna s en la semana t
                l[ind, ss, tt] = modelo.addVar(
                    vtype=GRB.BINARY, name=f"l_{ind}_{ss}_{tt}")

                # Se encuentra rota la caneria a en la comuna s en la semana t
                u[ind, ss, tt] = modelo.addVar(
                    vtype=GRB.BINARY, name=f"u_{ind}_{ss}_{tt}")
    modelo.update()

    # ========== RESTRICCIONES ==========
    # R1 Ecuacion de flujo
    for t in semanas:
        for s in comunas:
            canerias_de_s = canerias[s]

            for n in terrenos[s]:
                # terrenos[s] = [0,1,2]
                # n = 2
                canerias_entrada = []  # [0]
                canerias_salida = []  # [2]
                for caneria in canerias_de_s:
                    # caneria=(2,0)
                    index_of_caneria = canerias_de_s.index(caneria)  # 2
                    # print('indice de cañerias:', index_of_caneria)
                    if n in caneria:  # El terreno esta involucrado en esta conexion?
                        # En cual de la posicion de la tupla esta
                        # (x,y) donde x es entrada e y salida
                        pos_terreno = caneria.index(n)
                        if pos_terreno == 0:  # es de salida
                            canerias_salida.append(index_of_caneria)
                        elif pos_terreno == 1:   # pos_terreno == 1 , es de entrada
                            canerias_entrada.append(index_of_caneria)

                modelo.addConstr(
                    quicksum((1-beta(f))*m(f)*x[f, n, s, t] for f in fuentes)
                    + quicksum((1-alpha(a_in, s)) * y[a_in, s, t]
                               for a_in in canerias_entrada)
                    - quicksum((y[a_out, s, t]
                               for a_out in canerias_salida))
                    >= d(s, n, t), name=f"R1_flujo_{s}_{n}_{t}"
                )

    # R2 Capacidad maxima de flujo
    for t in semanas:
        for s in comunas:
            canerias_de_s = canerias[s]
            for a in range(len(canerias_de_s)):
                modelo.addConstr(y[a, s, t] <= k(a, s) * r[a, s, t],
                                 name=f"R2_capacidad_{a}_{s}_{t}")

    # R3 Activacion de caneria
    for s in comunas:
        canerias_de_s = canerias[s]
        for a in range(len(canerias_de_s)):
            modelo.addConstr(quicksum(q[a, s, t] for t in semanas) <= 1,
                             name=f"R3_activacion_{a}_{s}")

    # R5 Caneria previamente instalada, sigue instala
    for t in semanas:
        for s in comunas:
            canerias_de_s = canerias[s]
            for a in range(len(canerias_de_s)):
                modelo.addConstr(q[a, s, t] <= v[a, s, t],
                                 name=f"R5_instalada_{a}_{s}_{t}")

    for t in range(0, len(semanas)-1):
        for s in comunas:
            canerias_de_s = canerias[s]
            for a in range(len(canerias_de_s)):
                modelo.addConstr(v[a, s, t] <= v[a, s, t+1],
                                 name=f"R5_instalada_persistencia_{a}_{s}_{t}")

    #! Restricciones nuevas
    # Restricción que obliga que si no se ha construido en el periodo 0
    # una cañería, entonces esta no esta operando
    for s in comunas:
        canerias_de_s = canerias[s]
        for a in range(len(canerias_de_s)):
            modelo.addConstr(v[a, s, 0] <= q[a, s, 0],
                             name=f"R5_1_instalada_{a}_{s}_{1}")

    # Restricicón que indica que sólo puede operar una cañería si se compró en ese periodo
    # o esta operando desde el periodo anteior
    for t in semanas:
        if t != 0:
            for s in comunas:
                canerias_de_s = canerias[s]
                for a in range(len(canerias_de_s)):
                    modelo.addConstr(v[a, s, t] <= q[a, s, t] + v[a, s, t-1],
                                     name=f"R5_2_instalada_{a}_{s}_{t}")
    #! Fin de las restricciones nuevas

    # R6 Solo puede operar una caneria que esta instalada
    for s in comunas:
        for a in range(len(canerias[s])):
            for t in semanas:
                modelo.addConstr(r[a, s, t] <= v[a, s, t],
                                 name=f"R6_operando_{a}_{s}_{t}")

    # R7: Persistencia de la falla
    #  U[a,s,t+1] >= U[a,s,t] - L[a,s,t]   ∀ t=0…T-2
    for t in range(len(semanas)-1):
        for s in comunas:
            for a in range(len(canerias[s])):
                modelo.addConstr(
                    u[a, s, t+1] >= u[a, s, t] - l[a, s, t],
                    name=f"R7_persistencia_falla_{a}_{s}_{t}")

    # R8 Condicion ruptura caneria
    #  U[a,s,t] >= r[a,s,t] - ∑_{τ=t..t+φ} L[a,s,τ]   ∀ t=0…T−φ−1
    horizonte = len(semanas)
    for t in range(0, horizonte - phi()):
        for s in comunas:
            for a in range(len(canerias[s])):
                modelo.addConstr(
                    u[a, s, t + phi()]
                    >= r[a, s, t]
                    - quicksum(l[a, s, tau]
                               for tau in range(t, t + phi())),
                    name=f"R8_condicion_ruptura_{a}_{s}_{t}")

    # R9 Flujo de caja
    modelo.addConstr(I_0()
                     - quicksum(c_1(a, s)*q[a, s, 0]
                                for s in comunas for a in range(len(canerias[s])))
                     - quicksum(c(f, s)*w[f, n, s, 0]
                                for s in comunas for f in fuentes for n in terrenos[s])
                     + e(0) * quicksum(d(n, s, 0)
                                       for s in comunas for n in terrenos[s])
                     # – coste de reparar cañerías en t
                     - quicksum(c_2(a, s) * l[a, s, 0]
                                for s in comunas for a in range(len(canerias[s])))
                     == p[0],
                     name="R9_flujo_caja_inicial")

    # R10 Flujo de caja para tiempos posteriores
    for t in semanas:
        if t != 0:
            modelo.addConstr(p[t-1]
                             # + ingresos esta semana:
                             + e(t) * quicksum(d(n, s, t)
                                               for s in comunas for n in terrenos[s])
                             # – coste de construir cañerías en t
                             - quicksum(c_1(a, s) * q[a, s, t]
                                        for s in comunas for a in range(len(canerias[s])))
                             # – coste de construir fuentes en t
                             - quicksum(c(f, s) * w[f, n, s, t]
                                        for s in comunas for f in fuentes for n in terrenos[s])
                             # – coste de reparar cañerías en t
                             - quicksum(c_2(a, s) * l[a, s, t]
                                        for s in comunas for a in range(len(canerias[s])))
                             == p[t],
                             name=f"R10_flujo_caja_{t}")

    # R11 No se permite saldo negativo
    for t in semanas:
        modelo.addConstr(p[t] >= 0,
                         name=f"R11_saldo_no_negativo_{t}")

    # R12 Acumulacion de fuentes instaladas
    # R12.1 Caso base (t = 1): X = W
    for f in fuentes:
        for s in comunas:
            for n in terrenos[s]:
                modelo.addConstr(x[f, n, s, 0] == w[f, n, s, 0],
                                 name=f"R12.1_caso_base_{f}_{n}_{s}_0")

    # R12.2 Acumulación (t = 2,...,T): X_t = W_t + X_{t-1}
    for t in semanas:
        if t == 0:
            continue
        for f in fuentes:
            for s in comunas:
                for n in terrenos[s]:
                    modelo.addConstr(x[f, n, s, t] == w[f, n, s, t] + x[f, n, s, t-1],
                                     name=f"R12.2_acumulacion_{f}_{n}_{s}_{t}")

    # R13: Una cañería rota no está operando
    for t in semanas:
        for s in comunas:
            for a in range(len(canerias[s])):
                modelo.addConstr(u[a, s, t] + r[a, s, t] <= 1,
                                 name=f"R13_caneria_rota_no_operando_{a}_{s}_{t}")

    # R14 Arreglar una caneria
    # R14: Si una cañería rota se arregla, deja de estar rota en la misma semana
    for t in semanas:
        for s in comunas:
            for a in range(len(canerias[s])):
                modelo.addConstr(l[a, s, t] + u[a, s, t] <= 1,
                                 name=f"R14_arreglar_caneria_{a}_{s}_{t}")

    # R15 Fuentes maximas por terreno
    for t in semanas:
        for s in comunas:
            for n in terrenos[s]:
                for f in fuentes:
                    modelo.addConstr(x[f, n, s, t] <= g(f, n, s),
                                     name=f"R15_fuentes_maximas_{f}_{n}_{s}_{t}")

    #! Restricciones nuevas
    # R16 Sólo es posible romper cañerías que estan instaladas
    for t in semanas:
        for s in comunas:
            for a in range(len(canerias[s])):
                modelo.addConstr(v[a, s, t] >= u[a, s, t],
                                 name=f"R16_{a}_{s}_{t}")

    # R17 Sólo es posible arreglar cañerías instaladas
    for t in semanas:
        for s in comunas:
            for a in range(len(canerias[s])):
                modelo.addConstr(l[a, s, t] <= v[a, s, t],
                                 name=f"R17_{a}_{s}_{t}")

    # Funcion Objetivo
    modelo.setObjective(
        quicksum(alpha(a, s) * y[a, s, t]
                 for t in semanas for s in comunas for a in range(len(canerias[s])))
        + quicksum(beta(f) * m(f) * x[f, n, s, t]
                   for t in semanas for s in comunas for n in terrenos[s] for f in fuentes),
        GRB.MINIMIZE
    )

    return modelo


def resolver_modelo(modelo):
    """
    Esta función debe llamar al solver de Gurobi para resolver el modelo.
    """
    modelo.optimize()

    if modelo.status == GRB.OPTIMAL:
        print("Valor óptimo:", modelo.ObjVal)
    elif modelo.status == GRB.INFEASIBLE:
        print('toi aqui')
        print("El modelo es infactible.")
        modelo.computeIIS()
        modelo.write("modelo_inviable.ilp")

    elif modelo.status == GRB.UNBOUNDED:
        print("El modelo es no acotado.")
    else:
        print(f"Estado del modelo: {modelo.status} (no óptimo)")
    return modelo


def guardar_resultados(model):
    """
    Guarda los valores de las variables del modelo en archivos CSV separados,
    agrupados por tipo de variable (x, w, y, etc.), dentro de una carpeta 'resultados'.
    """
    # Crear carpeta 'resultados' si no existe
    carpeta_resultados = "resultados"
    os.makedirs(carpeta_resultados, exist_ok=True)

    # Diccionario para agrupar variables por prefijo
    variables_por_tipo = {}

    # Recorrer todas las variables del modelo
    for var in model.getVars():
        nombre = var.varName  # Ejemplo: x_1_0_Illapel_2
        valor = var.x
        if "_" in nombre:
            prefijo = nombre.split("_")[0]  # x, w, y, etc.
            if prefijo not in variables_por_tipo:
                variables_por_tipo[prefijo] = []
            variables_por_tipo[prefijo].append((nombre, valor))

    # Guardar cada grupo en un CSV
    for tipo, variables in variables_por_tipo.items():
        ruta_csv = os.path.join(carpeta_resultados, f"{tipo}.csv")
        with open(ruta_csv, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Nombre", "Valor"])
            for nombre, valor in variables:
                escritor.writerow([nombre, valor])


def main():
    # pruebas()
    model = construir_modelo()
    resultado = resolver_modelo(model)
    guardar_resultados(resultado)


if __name__ == "__main__":
    main()
