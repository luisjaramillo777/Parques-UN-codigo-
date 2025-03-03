#### ¿Qué es Parqués UN?

Parqués UN es una implementación en consola del tradicional juego de mesa Parqués (similar al Parchís), diseñado como proyecto para la asignatura "Programación de Computadores" en la Universidad Nacional de Colombia.

#### Requisitos

Para jugar necesitas:
- Python 3.x instalado en tu sistema
- Terminal o consola que soporte colores ANSI (la mayoría de terminales modernos)

#### Cómo Iniciar el Juego

1. Abre tu terminal o consola
2. Navega hasta la carpeta donde se encuentra el archivo parques_un.py
3. Ejecuta el comando: python parques_un.py

#### Modos de Juego

El juego ofrece dos modos:
- *Modo Real (R)*: Los dados se lanzan aleatoriamente.
- *Modo Desarrollador (D)*: Puedes elegir el valor de los dados en cada turno.

#### Configuración Inicial

1. Selecciona el número de jugadores (2-4)
2. Para cada jugador:
   - Elige un color disponible (rojo, verde, amarillo o azul)
   - Ingresa tu nombre

#### Cómo Jugar

1. *Objetivo del Juego*: Ser el primer jugador en llevar todas tus fichas desde la cárcel hasta la meta.

2. *Turnos*:
   - Los jugadores se alternan en sentido horario.
   - En cada turno, el jugador lanza dos dados.
   - Puede mover sus fichas según: valor del primer dado, valor del segundo dado, o suma de ambos.

3. *Salir de la Cárcel*:
   - Para sacar una ficha de la cárcel, debes obtener un 5 en alguno de los dados.
   - Cuando sacas un 5, puedes elegir sacar una ficha o mover las existentes.

4. *Movimiento*:
   - Las fichas se mueven en sentido horario por el recorrido externo.                                                                          
