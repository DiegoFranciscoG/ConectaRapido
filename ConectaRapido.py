import numpy as np

# Constantes para el juego
FILAS = 6
COLUMNAS = 7

def crear_tablero():
    """Crea un tablero vacío de tamaño FILAS x COLUMNAS."""
    return np.zeros((FILAS, COLUMNAS), dtype=int)

def imprimir_tablero(tablero):
    """Imprime el estado actual del tablero."""
    print("\nTablero actual:")
    print(np.flip(tablero, 0))
    print()

def columna_valida(tablero, columna):
    """Verifica si una columna tiene espacio disponible."""
    return tablero[FILAS - 1][columna] == 0

def obtener_fila_disponible(tablero, columna):
    """Retorna la fila más baja disponible en una columna dada."""
    for fila in range(FILAS):
        if tablero[fila][columna] == 0:
            return fila

def colocar_ficha(tablero, fila, columna, ficha):
    """Coloca una ficha en la posición especificada del tablero."""
    tablero[fila][columna] = ficha

def verificar_victoria(tablero, ficha):
    """Verifica si la ficha especificada ha ganado."""
    # Verificar filas
    for fila in range(FILAS):
        for col in range(COLUMNAS - 3):
            if all(tablero[fila, col + i] == ficha for i in range(4)):
                return True

    # Verificar columnas
    for col in range(COLUMNAS):
        for fila in range(FILAS - 3):
            if all(tablero[fila + i, col] == ficha for i in range(4)):
                return True

    # Verificar diagonales positivas
    for fila in range(FILAS - 3):
        for col in range(COLUMNAS - 3):
            if all(tablero[fila + i, col + i] == ficha for i in range(4)):
                return True

    # Verificar diagonales negativas
    for fila in range(3, FILAS):
        for col in range(COLUMNAS - 3):
            if all(tablero[fila - i, col + i] == ficha for i in range(4)):
                return True

    return False

def jugar_conecta_cuatro():
    """Función principal que gestiona el flujo del juego Conecta 4."""
    while True:
        tablero = crear_tablero()
        imprimir_tablero(tablero)

        # Contadores de victorias
        victorias_rojas = 0
        victorias_amarillas = 0

        # Bandera para determinar el turno inicial
        turno_rojo = True
        juego_activo = True

        while juego_activo:
            # Determinar el jugador actual
            jugador = "Rojo" if turno_rojo else "Amarillo"
            ficha = 1 if turno_rojo else 2

            # Solicitar al jugador que elija una columna
            while True:
                try:
                    columna = int(input(f"Jugador {jugador}, elija una columna (0-{COLUMNAS-1}): "))
                    if 0 <= columna < COLUMNAS:
                        break
                    else:
                        print("Columna no válida. Intente de nuevo.")
                except ValueError:
                    print("Por favor ingrese un número válido.")

            # Verificar si la columna es válida
            if not columna_valida(tablero, columna):
                print("La columna está llena. Intente otra columna.")
                continue

            # Colocar la ficha en el tablero
            fila = obtener_fila_disponible(tablero, columna)
            colocar_ficha(tablero, fila, columna, ficha)
            imprimir_tablero(tablero)

            # Verificar si el jugador actual ha ganado
            if verificar_victoria(tablero, ficha):
                print(f"¡Jugador {jugador} ha ganado!")
                if turno_rojo:
                    victorias_rojas += 1
                else:
                    victorias_amarillas += 1

                print(f"Victorias - Rojas: {victorias_rojas}, Amarillas: {victorias_amarillas}")
                juego_activo = False
                break

            # Cambiar de turno
            turno_rojo = not turno_rojo

            # Verificar empate
            if not any(columna_valida(tablero, col) for col in range(COLUMNAS)):
                print("El juego termina en empate.")
                juego_activo = False
                break

        # Reiniciar el juego sin preguntar al usuario
        print("\nIniciando una nueva partida...\n")

# Pruebas automatizadas
def pruebas_conecta_cuatro():
    """Realiza pruebas automáticas de las funciones principales del juego."""
    resultados = {}
    
    # Prueba 1: Verificar tablero vacío
    tablero = crear_tablero()
    resultados['Tablero vacío'] = np.all(tablero == 0)
    
    # Prueba 2: Colocar ficha y verificar validez
    fila = obtener_fila_disponible(tablero, 0)
    colocar_ficha(tablero, fila, 0, 1)  # Colocar ficha del jugador 1 en la columna 0
    resultados['Colocar ficha y validez'] = tablero[0][0] == 1 and columna_valida(tablero, 0)
    
    # Prueba 3: Verificar victoria horizontal
    tablero = crear_tablero()
    for col in range(4):
        fila = obtener_fila_disponible(tablero, col)
        colocar_ficha(tablero, fila, col, 1)
    resultados['Victoria horizontal'] = verificar_victoria(tablero, 1)
    
    # Prueba 4: Verificar victoria vertical
    tablero = crear_tablero()
    for _ in range(4):
        fila = obtener_fila_disponible(tablero, 0)
        colocar_ficha(tablero, fila, 0, 2)
    resultados['Victoria vertical'] = verificar_victoria(tablero, 2)
    
    # Prueba 5: Verificar victoria diagonal positiva
    tablero = crear_tablero()
    movimientos = [(0, 0), (1, 1), (2, 2), (3, 3)]
    for fila, col in movimientos:
        colocar_ficha(tablero, fila, col, 1)
    resultados['Victoria diagonal positiva'] = verificar_victoria(tablero, 1)
    
    # Prueba 6: Verificar victoria diagonal negativa
    tablero = crear_tablero()
    movimientos = [(3, 0), (2, 1), (1, 2), (0, 3)]
    for fila, col in movimientos:
        colocar_ficha(tablero, fila, col, 2)
    resultados['Victoria diagonal negativa'] = verificar_victoria(tablero, 2)
    
    return resultados

if __name__ == "__main__":
    # Ejecutar las pruebas automáticas
    resultados_pruebas = pruebas_conecta_cuatro()
    for prueba, resultado in resultados_pruebas.items():
        print(f"{prueba}: {'Éxito' if resultado else 'Fallo'}")
    
    # Iniciar el juego
    jugar_conecta_cuatro()
