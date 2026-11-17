# Space Invaders Challenges (Pygame)

Juego de esquivar obstáculos para dos jugadores hecho con Pygame, ampliado con los 12 retos de la actividad.

## Gameplay



https://github.com/user-attachments/assets/76cbab13-004f-45c5-b956-b8bd9a2848e4


## Cómo ejecutarlo

```bash
pip install pygame
python main.py
```

**Controles**

| Acción | Tecla |
|---|---|
| Jugador 1 | Flechas |
| Jugador 2 | W A S D |
| Velocidad del jugador 1 | `+` / `-` |
| Pausa | ESC |
| Reiniciar (tras Game Over) | R |

## Estructura del proyecto

| Archivo | Contenido |
|---|---|
| `config.py` | Todas las constantes del juego |
| `player.py` | Clase `Player` (movimiento, límites, vidas, efectos) |
| `obstacle.py` | Clase `Obstacle` |
| `powerup.py` | Clase `PowerUp` |
| `scores.py` | Lectura y escritura de `scores.txt` |
| `main.py` | Bucle principal, estados del juego y HUD |

## Idea clave: el reloj del juego (`game_time`)

Varios retos (pausa, temporizador, invulnerabilidad, power-ups) dependen del tiempo. Si usara directamente `pygame.time.get_ticks()`, el tiempo seguiría avanzando durante la pausa. Por eso `main.py` tiene su propio reloj, `game_time`, al que sumo `dt` (los milisegundos que devuelve `clock.tick(FPS)`) **solo cuando el juego está en marcha**: no avanza en pausa ni en Game Over. Todos los temporizadores usan este reloj.

El juego tiene cuatro estados: `menu`, `playing`, `name` (pedir nombre) y `game_over`.

---

## Parte 1 — Retos obligatorios

### 1. Player boundaries
**Qué hace:** ningún jugador puede salir de la ventana por ninguno de los cuatro lados.
**Cómo:** en `player.py` creo `SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)`. Al final de `moveArrows()` y `moveWASD()` llamo a `keep_inside_screen()`, que ejecuta `self.rect.clamp_ip(SCREEN_RECT)`. Este método mueve el rectángulo del jugador dentro del rectángulo de la pantalla si se había salido.

### 2. Random obstacle sizes
**Qué hace:** cada obstáculo mide entre 20 y 70 píxeles y siempre aparece entero dentro del ancho de la ventana.
**Cómo:** en `Obstacle.__init__` primero calculo `size = random.randint(20, 70)` y **después** `x = random.randint(0, WIDTH - size)`. Como la posición depende del tamaño ya elegido, el obstáculo nunca se sale por los lados.

### 3. Collision with Player 2
**Qué hace:** el segundo jugador también puede ser golpeado por los obstáculos.
**Cómo:** en el bucle de obstáculos recorro la lista `players = [player, player2]` y compruebo `p.rect.colliderect(obstacle.rect)` para cada uno. Como además implementé el reto 10, un impacto resta una vida; la partida termina cuando **ninguno** de los dos tiene vidas.

### 4. Pause game
**Qué hace:** ESC pausa el juego y muestra **PAUSE**; otra pulsación lo reanuda. En pausa no se mueven los jugadores, no caen obstáculos ni aparecen nuevos.
**Cómo:** una variable booleana `paused` que ESC invierte con un evento `KEYDOWN`. Toda la lógica de actualización está dentro de `if state == STATE_PLAYING and not paused:`, así que en pausa solo se dibuja la pantalla con una capa oscura y el texto.

### 5. Restart game
**Qué hace:** en Game Over, pulsar R empieza otra partida sin cerrar el programa.
**Cómo:** la función `reset_game()` pone la puntuación a 0, vacía las listas de obstáculos y power-ups, reinicia `game_time` y llama a `reset()` de cada jugador, que lo devuelve a su posición inicial (con vidas, velocidad y efectos restaurados). El récord no se toca.

### 6. Survival timer
**Qué hace:** muestra los segundos que lleva vivo el jugador; se detiene en Game Over y en pausa.
**Cómo:** se muestra `game_time // 1000`. Como `game_time` solo avanza mientras se juega (ver la idea clave de arriba), el contador se congela solo en pausa y en Game Over, y se reinicia en `reset_game()`.

### 7. Increasing difficulty
**Qué hace:** cada 10 puntos los obstáculos aparecen 50 ms antes, con un mínimo de 150 ms.
**Cómo:** la función `get_spawn_delay()` calcula `max(150, 500 - 50 * (score // 10))`. Se calcula a partir de la puntuación en cada comprobación de aparición, así no hay que guardar ni reiniciar ningún estado extra.

### 8. Change player speed
**Qué hace:** `+` sube la velocidad del jugador 1 y `-` la baja, entre 2 y 12, una vez por pulsación.
**Cómo:** uso eventos `KEYDOWN` (se disparan una vez por pulsación, aunque se mantenga la tecla) y no `get_pressed()`, que cambiaría la velocidad en cada fotograma. `Player.change_speed()` aplica `max(2, min(12, base_speed + amount))`.

### 9. High score
**Qué hace:** guarda la mejor puntuación de la ejecución y la muestra junto a la actual.
**Cómo:** la variable `high_score` se actualiza cuando `score > high_score` y no se reinicia en `reset_game()`. Se dibuja en el HUD como `Best`.

---

## Parte 2 — Retos opcionales

### 10. Lives system
**Qué hace:** cada jugador empieza con 3 vidas, pierde una por impacto y tiene 2 segundos de invulnerabilidad después. El juego acaba cuando los dos se quedan sin vidas.
**Cómo:** `Player` tiene `lives` e `invulnerable_until`. `hit(now)` solo resta una vida si el jugador está vivo y no es invulnerable, y entonces fija `invulnerable_until = now + 2000`. Durante ese tiempo el jugador parpadea. Un obstáculo que impacta se destruye, y un jugador sin vidas desaparece y deja de moverse. El HUD muestra las vidas de cada uno.

### 11. Power-ups
**Qué hace:** cada 8 segundos cae un objeto especial que los jugadores recogen al tocarlo.
**Cómo:** la clase `PowerUp` está en `powerup.py` y elige al azar uno de tres tipos:
- **Speed (S, cian):** +4 de velocidad durante 5 s.
- **Life (+, rosa):** recupera una vida, sin superar 3.
- **Shield (I, blanco):** invulnerable durante 5 s, con borde blanco alrededor del jugador.

Los efectos temporales guardan su instante de fin (`boost_until`, `shield_until`) y `update_effects()` los comprueba cada fotograma, así que desaparecen solos al terminar.

### 12. Save high scores
**Qué hace:** al terminar la partida pide un nombre y guarda la puntuación en `scores.txt`; al iniciar el juego muestra las cinco mejores.
**Cómo:** `scores.py` guarda cada línea como `nombre;puntuación`. `load_scores()` lee el fichero, ignora líneas mal formadas y ordena de mayor a menor. En Game Over el estado `name` captura el texto con eventos `KEYDOWN` (letras, BACKSPACE para borrar, ENTER para guardar, máximo 12 caracteres). Después se muestra el top 5 actualizado y se puede reiniciar con R. La pantalla de inicio también enseña el top 5.
