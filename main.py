import random
import os
import time

# Constantes
NUM_CASILLAS_EXTERNAS = 68
NUM_CASILLAS_INTERNAS = 8
NUM_FICHAS = 4
CASILLAS_SEGURO = [5, 12, 22, 29, 39, 46, 56, 63]
CARCEL = -1
META = 0

# Variables globales
modo_desarrollador = False
jugadores = []
tablero = {}
turno_actual = 0

# Colores para la consola (ANSI)
COLORES = {
    'rojo': '\033[91m',
    'verde': '\033[92m',
    'amarillo': '\033[93m',
    'azul': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'reset': '\033[0m'
}

# Posiciones iniciales de cada jugador en el tablero externo
POSICIONES_INICIALES = {
    'rojo': 5,
    'verde': 22,
    'amarillo': 39, 
    'azul': 56
}

# Función para limpiar la pantalla (compatible con diferentes OS)
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para inicializar los jugadores
def inicializar_jugadores():
    global jugadores
    jugadores = []
    
    num_jugadores = 0
    while num_jugadores < 2 or num_jugadores > 4:
        try:
            num_jugadores = int(input("Ingrese el número de jugadores (2-4): "))
            if num_jugadores < 2 or num_jugadores > 4:
                print("El número de jugadores debe estar entre 2 y 4.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    colores_disponibles = list(POSICIONES_INICIALES.keys())
    
    for i in range(num_jugadores):
        print(f"\nJugador {i+1}:")
        
        # Mostrar colores disponibles
        print("Colores disponibles:")
        for j, color in enumerate(colores_disponibles):
            print(f"{j+1}. {color}")
        
        seleccion = 0
        while seleccion < 1 or seleccion > len(colores_disponibles):
            try:
                seleccion = int(input(f"Seleccione un color (1-{len(colores_disponibles)}): "))
                if seleccion < 1 or seleccion > len(colores_disponibles):
                    print(f"Por favor, seleccione un número entre 1 y {len(colores_disponibles)}.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
        
        color_elegido = colores_disponibles.pop(seleccion-1)
        nombre = input("Ingrese su nombre: ")
        
        # Crear jugador
        jugador = {
            'nombre': nombre,
            'color': color_elegido,
            'fichas': [CARCEL, CARCEL, CARCEL, CARCEL],  # Todas las fichas comienzan en la cárcel
            'fichas_en_meta': 0
        }
        jugadores.append(jugador)

# Función para inicializar el tablero
def inicializar_tablero():
    global tablero
    tablero = {}
    
    # Inicializar casillas externas
    for i in range(1, NUM_CASILLAS_EXTERNAS + 1):
        tablero[i] = []
    
    # Inicializar casillas internas para cada jugador
    for jugador in jugadores:
        color = jugador['color']
        for i in range(1, NUM_CASILLAS_INTERNAS + 1):
            tablero[f"{color}_{i}"] = []

# Función para mostrar el tablero
def mostrar_tablero():
    limpiar_pantalla()
    
    # Crear representación del tablero con ASCII
    print("\n" + "="*70)
    print("                       PARQUÉS UN                        ")
    print("="*70 + "\n")
    
    # Mostrar información de jugadores
    for jugador in jugadores:
        color = jugador['color']
        print(f"{COLORES[color]}Jugador: {jugador['nombre']} ({color}) - Fichas en meta: {jugador['fichas_en_meta']}{COLORES['reset']}")
    
    print("\n" + "-"*70)
    
    # Dibujar tablero externo
    print("\nTablero Externo:")
    filas = 7
    columnas = 10
    
    tablero_ascii = []
    for i in range(filas):
        tablero_ascii.append([' ' for _ in range(columnas)])
    
    # Llenar el tablero con números de casilla
    casillas_en_tablero = [
        [68, 67, 66, 65, 64, 63, 62, 61, 60, 59],
        [1, 0, 0, 0, 0, 56, 0, 0, 0, 58],
        [2, 0, 0, 0, 0, 55, 0, 0, 0, 57],
        [3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        [27, 0, 0, 0, 0, 43, 0, 0, 0, 13],
        [28, 0, 0, 0, 0, 42, 0, 0, 0, 14],
        [29, 30, 31, 32, 33, 34, 35, 36, 37, 38]
    ]
    
    # Mostrar representación simplificada
    for i, fila in enumerate(casillas_en_tablero):
        linea = "|"
        for j, casilla in enumerate(fila):
            if casilla == 0:
                linea += "   |"
            else:
                # Verificar si es casilla de seguro
                es_seguro = casilla in CASILLAS_SEGURO
                
                # Obtener fichas en esta casilla
                fichas_aqui = []
                if casilla > 0:
                    fichas_aqui = tablero.get(casilla, [])
                
                if fichas_aqui:
                    # Mostrar primera ficha
                    ficha_info = fichas_aqui[0]
                    color_ficha = ficha_info['color']
                    num_ficha = ficha_info['numero']
                    
                    if es_seguro:
                        linea += f"{COLORES[color_ficha]}S{num_ficha}{COLORES['reset']}|"
                    else:
                        linea += f"{COLORES[color_ficha]}{num_ficha}{len(fichas_aqui)}{COLORES['reset']}|"
                else:
                    if es_seguro:
                        linea += " S |"
                    else:
                        linea += f"{casilla:2d} |"
        print(linea)
    
    # Mostrar casillas internas para cada jugador
    print("\nCasillas Internas:")
    for jugador in jugadores:
        color = jugador['color']
        print(f"{COLORES[color]}{color}:{COLORES['reset']}", end=" ")
        
        for i in range(1, NUM_CASILLAS_INTERNAS + 1):
            clave = f"{color}_{i}"
            fichas = tablero.get(clave, [])
            
            if fichas:
                ficha_info = fichas[0]
                print(f"{COLORES[color]}{ficha_info['numero']}{COLORES['reset']}", end=" ")
            else:
                print(f"{i}", end=" ")
        
        # Mostrar la meta
        fichas_en_meta = jugador['fichas_en_meta']
        print(f" Meta: {fichas_en_meta}")
    
    # Mostrar cárcel
    print("\nCárcel:")
    for jugador in jugadores:
        color = jugador['color']
        en_carcel = [i+1 for i, pos in enumerate(jugador['fichas']) if pos == CARCEL]
        
        if en_carcel:
            print(f"{COLORES[color]}{jugador['nombre']} ({color}): {en_carcel}{COLORES['reset']}")
    
    print("\n" + "-"*70)

# Función para simular lanzamiento de dados
def lanzar_dados():
    if modo_desarrollador:
        opcion = input("¿Desea realizar un lanzamiento real (R) o elegir valores (E)? ").upper()
        
        if opcion == 'E':
            while True:
                try:
                    dado1 = int(input("Valor del primer dado (1-6): "))
                    dado2 = int(input("Valor del segundo dado (1-6): "))
                    
                    if 1 <= dado1 <= 6 and 1 <= dado2 <= 6:
                        return (dado1, dado2)
                    else:
                        print("Los valores de los dados deben estar entre 1 y 6.")
                except ValueError:
                    print("Por favor, ingrese números válidos.")
    
    # Lanzamiento real
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    
    return (dado1, dado2)

# Función para sacar una ficha de la cárcel
def sacar_ficha_de_carcel(jugador):
    # Verificar si hay alguna ficha en la cárcel
    indices_en_carcel = [i for i, pos in enumerate(jugador['fichas']) if pos == CARCEL]
    
    if not indices_en_carcel:
        print("No hay fichas en la cárcel.")
        return False
    
    # Mostrar fichas disponibles
    print(f"Fichas en cárcel: {[i+1 for i in indices_en_carcel]}")
    
    # Seleccionar ficha
    seleccion = 0
    while seleccion not in indices_en_carcel:
        try:
            seleccion = int(input("Seleccione una ficha para sacar (número): ")) - 1
            if seleccion not in indices_en_carcel:
                print("Ficha no válida. Intente de nuevo.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    # Sacar la ficha y colocarla en la casilla inicial
    color = jugador['color']
    posicion_inicial = POSICIONES_INICIALES[color]
    
    # Verificar si hay fichas enemigas en la posición inicial
    hay_captura = False
    if posicion_inicial in tablero:
        fichas_en_posicion = tablero[posicion_inicial]
        fichas_a_eliminar = []
        
        for ficha in fichas_en_posicion:
            if ficha['color'] != color:
                # Capturar ficha enemiga
                jugador_enemigo = next(j for j in jugadores if j['color'] == ficha['color'])
                jugador_enemigo['fichas'][ficha['numero'] - 1] = CARCEL
                fichas_a_eliminar.append(ficha)
                hay_captura = True
        
        # Eliminar fichas capturadas del tablero
        for ficha in fichas_a_eliminar:
            fichas_en_posicion.remove(ficha)
    
    # Actualizar posición de la ficha
    jugador['fichas'][seleccion] = posicion_inicial
    
    # Agregar ficha al tablero
    if posicion_inicial not in tablero:
        tablero[posicion_inicial] = []
    
    tablero[posicion_inicial].append({
        'color': color,
        'numero': seleccion + 1
    })
    
    print(f"Ficha {seleccion+1} sacada de la cárcel y colocada en la posición {posicion_inicial}.")
    
    if hay_captura:
        print("¡Has capturado fichas enemigas!")
    
    return True

# Función para mover una ficha
def mover_ficha(jugador, valor_dados):
    # Obtener fichas que pueden moverse
    fichas_movibles = []
    for i, posicion in enumerate(jugador['fichas']):
        if posicion != CARCEL and posicion != META:
            fichas_movibles.append(i)
    
    if not fichas_movibles:
        print("No hay fichas para mover.")
        return False
    
    # Mostrar fichas movibles
    print("Fichas que pueden moverse:")
    for i in fichas_movibles:
        posicion_actual = jugador['fichas'][i]
        if isinstance(posicion_actual, str) and '_' in posicion_actual:
            # Ficha en casilla interna
            color, num_interno = posicion_actual.split('_')
            print(f"Ficha {i+1}: Casilla interna {color} {num_interno}")
        else:
            # Ficha en casilla externa
            print(f"Ficha {i+1}: Casilla {posicion_actual}")
    
    # Seleccionar ficha
    seleccion = -1
    while seleccion not in fichas_movibles:
        try:
            seleccion = int(input("Seleccione una ficha para mover (número): ")) - 1
            if seleccion not in fichas_movibles:
                print("Ficha no válida. Intente de nuevo.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    # Obtener posición actual de la ficha
    posicion_actual = jugador['fichas'][seleccion]
    color = jugador['color']
    
    # Calcular nueva posición
    nueva_posicion = calcular_nueva_posicion(posicion_actual, valor_dados, color)
    
    # Verificar si la nueva posición es válida
    if nueva_posicion is None:
        print("Movimiento no válido. La ficha no puede moverse.")
        return False
    
    # Verificar si hay captura
    hay_captura = False
    if isinstance(nueva_posicion, int) and nueva_posicion > 0:
        # Verificar si es un seguro
        es_seguro = nueva_posicion in CASILLAS_SEGURO
        
        if nueva_posicion in tablero:
            fichas_en_posicion = tablero[nueva_posicion]
            fichas_a_eliminar = []
            
            for ficha in fichas_en_posicion:
                if ficha['color'] != color:
                    # No se puede capturar en casillas de seguro
                    if es_seguro:
                        print("No puedes mover ahí, hay fichas enemigas en un seguro.")
                        return False
                    
                    # Capturar ficha enemiga
                    jugador_enemigo = next(j for j in jugadores if j['color'] == ficha['color'])
                    jugador_enemigo['fichas'][ficha['numero'] - 1] = CARCEL
                    fichas_a_eliminar.append(ficha)
                    hay_captura = True
            
            # Eliminar fichas capturadas del tablero
            for ficha in fichas_a_eliminar:
                fichas_en_posicion.remove(ficha)
    
    # Quitar ficha de la posición actual
    if isinstance(posicion_actual, int) and posicion_actual > 0:
        if posicion_actual in tablero:
            tablero[posicion_actual] = [f for f in tablero[posicion_actual] 
                                       if not (f['color'] == color and f['numero'] == seleccion + 1)]
    elif isinstance(posicion_actual, str) and '_' in posicion_actual:
        if posicion_actual in tablero:
            tablero[posicion_actual] = [f for f in tablero[posicion_actual] 
                                       if not (f['color'] == color and f['numero'] == seleccion + 1)]
    
    # Verificar si llegó a la meta
    if nueva_posicion == META:
        jugador['fichas_en_meta'] += 1
        jugador['fichas'][seleccion] = META
        print(f"¡La ficha {seleccion+1} ha llegado a la meta!")
        
        # Dar 10 movimientos adicionales
        print("¡Has ganado 10 movimientos adicionales!")
        for _ in range(10):
            mostrar_tablero()
            print(f"Movimientos adicionales restantes: {10 - _}")
            if not ejecutar_movimiento_adicional(jugador):
                break
        
        return True
    
    # Actualizar posición de la ficha
    jugador['fichas'][seleccion] = nueva_posicion
    
    # Agregar ficha a la nueva posición en el tablero
    if nueva_posicion not in tablero:
        tablero[nueva_posicion] = []
    
    tablero[nueva_posicion].append({
        'color': color,
        'numero': seleccion + 1
    })
    
    print(f"Ficha {seleccion+1} movida a la posición {nueva_posicion}.")
    
    if hay_captura:
        print("¡Has capturado fichas enemigas!")
    
    return True

# Función para calcular la nueva posición de una ficha
def calcular_nueva_posicion(posicion_actual, valor_dados, color):
    # Si la ficha está en una casilla externa
    if isinstance(posicion_actual, int) and posicion_actual > 0:
        nueva_posicion = posicion_actual + valor_dados
        
        # Verificar si debe entrar en casillas internas
        pos_inicial = POSICIONES_INICIALES[color]
        
        # Calcular el punto de entrada a las casillas internas (posición inicial + 51)
        punto_entrada = pos_inicial + 51
        if punto_entrada > NUM_CASILLAS_EXTERNAS:
            punto_entrada -= NUM_CASILLAS_EXTERNAS
        
        # Verificar si la ficha debe entrar a las casillas internas
        if posicion_actual <= punto_entrada and nueva_posicion > punto_entrada:
            # Calcular cuántos pasos dentro de las casillas internas
            pasos_internos = nueva_posicion - punto_entrada
            
            # Verificar que no se pase de las casillas internas disponibles
            if pasos_internos <= NUM_CASILLAS_INTERNAS:
                return f"{color}_{pasos_internos}"
            else:
                # No puede moverse, se pasaría de la meta
                return None
        
        # Ajustar si da la vuelta completa al tablero
        if nueva_posicion > NUM_CASILLAS_EXTERNAS:
            nueva_posicion -= NUM_CASILLAS_EXTERNAS
        
        return nueva_posicion
    
    # Si la ficha está en una casilla interna
    elif isinstance(posicion_actual, str) and '_' in posicion_actual:
        _, num_interno = posicion_actual.split('_')
        num_interno = int(num_interno)
        
        nueva_posicion_interna = num_interno + valor_dados
        
        # Verificar si llega exactamente a la meta
        if nueva_posicion_interna == NUM_CASILLAS_INTERNAS + 1:
            return META
        # Verificar que no se pase
        elif nueva_posicion_interna > NUM_CASILLAS_INTERNAS + 1:
            return None
        else:
            return f"{color}_{nueva_posicion_interna}"
    
    return None

# Función para ejecutar un movimiento adicional después de llegar a la meta
def ejecutar_movimiento_adicional(jugador):
    # Verificar si hay fichas que pueden moverse
    fichas_movibles = []
    for i, posicion in enumerate(jugador['fichas']):
        if posicion != CARCEL and posicion != META:
            fichas_movibles.append(i)
    
    if not fichas_movibles:
        print("No hay fichas para mover. Fin de los movimientos adicionales.")
        time.sleep(2)
        return False
    
    # Pedir valor para el movimiento
    while True:
        try:
            valor = int(input("Ingrese el valor para el movimiento adicional (1-6): "))
            if 1 <= valor <= 6:
                break
            else:
                print("El valor debe estar entre 1 y 6.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    
    # Realizar el movimiento
    return mover_ficha(jugador, valor)

# Función para verificar si un jugador ha ganado
def verificar_ganador(jugador):
    return jugador['fichas_en_meta'] == NUM_FICHAS

# Función para ejecutar un turno
def ejecutar_turno(jugador):
    print(f"\nTurno de {jugador['nombre']} ({jugador['color']})")
    input("Presione Enter para lanzar los dados...")
    
    dados = lanzar_dados()
    print(f"Resultado de los dados: {dados[0]} y {dados[1]}")
    
    # Verificar si puede sacar ficha de la cárcel
    if 5 in dados and any(pos == CARCEL for pos in jugador['fichas']):
        print("¡Puede sacar una ficha de la cárcel!")
        sacar_ficha_de_carcel(jugador)
    
    # Mover fichas según los valores de los dados
    movimientos_posibles = [dados[0], dados[1], dados[0] + dados[1]]
    
    for valor in movimientos_posibles:
        print(f"\nMovimiento con valor {valor}")
        mover_ficha(jugador, valor)
        mostrar_tablero()
    
    # Verificar si el jugador ha ganado
    if verificar_ganador(jugador):
        return True
    
    return False

# Función principal del juego
def jugar_parques():
    global turno_actual, modo_desarrollador
    
    # Configurar modo de juego
    modo = input("Seleccione el modo de juego (R: Real, D: Desarrollador): ").upper()
    modo_desarrollador = (modo == 'D')
    
    # Inicializar el juego
    inicializar_jugadores()
    inicializar_tablero()
    
    # Iniciar el juego
    hay_ganador = False
    while not hay_ganador:
        mostrar_tablero()
        jugador_actual = jugadores[turno_actual]
        
        hay_ganador = ejecutar_turno(jugador_actual)
        
        if hay_ganador:
            mostrar_tablero()
            print(f"\n¡{jugador_actual['nombre']} ({jugador_actual['color']}) ha ganado!")
            break
        
        # Pasar al siguiente jugador
        turno_actual = (turno_actual + 1) % len(jugadores)
        
        input("\nPresione Enter para continuar al siguiente turno...")
    
    print("\n¡Fin del juego!")
    input("Presione Enter para salir...")

# Función principal
def main():
    print("¡Bienvenido a Parqués UN!")
    jugar_parques()

if __name__ == "__main__":
    main()