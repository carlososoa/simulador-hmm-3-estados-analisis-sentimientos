Arquitectura: MVC

Librerías sugeridas: pygame, numpy, matplotlib.

Para las graficas usa matplotlib, luego las mostramos dentro la simulación pygame.

Objetivo: Desarrollar un simulador de HMM (modelos ocultos de markov) para análisis de sentimientos de tweets.
La interfaz será únicamente a través de pygame creando un "juego", desde el cual se iniciaría la simulación, y el posterior a análisis de resultados.

### Pantalla 1: 
Muestra el titulo del proyecto "Simulador HMM Análisis de Sentimientos en Redes Sociales"
Integrantes del equipo: 
Estefania Martinez Guzman
Valentina Pérez Flórez
Carlos Andrés Osorio Agudelo
Botón de avanzar a la siguiente pantalla.

### Pantalla 2:
Muestra el titulo del proyecto, muestra la información inicial para la simulación: 
3 Estados ocultos(hardcodeado)
3 Observaciones (hardcodeado)
Matriz de transición: el código tiene por defecto una matriz de transición ( pero permite ser editada en la interfaz)
Matriz de emisión: el código tiene por defecto una matriz de emisión ( pero permite ser editada en la interfaz)
Distribución inicial: el código tiene por defecto una Distribución inicial ( pero permite ser editada en la interfaz)

Numero de publicaciones/tweets, permite seleccionar el numero de tweets con 4 opciones 10, 100, 500.

Botón de iniciar simulación.

### Pantalla de simulación:

Muestra un mensaje de simulando... con un contador de las transiciones vs las esperadas.
Muestra en grande el ultimo tweet(numerado) simulado, con su "Estado" y un emoji y color que lo diferencia de los otros. 
Muestra un listado de los tweets con color, numeración, emoji, texto del tweet

Los datos simulados se deben guardar para poder realizar el análisis posterior.

Una vez finalizada la simulación, se mostrara una **pantalla resumen**, que muestra las estadísticas observadas, y la distribución de los sentimientos. Para las graficas usamos matplotlib para generarlas y luego las renderizamos en el "juego" esta pantalla debe tener botón para ir a la siguiente

### Pantalla 5
Tiene botón de retroceder y botón de avanzar a la siguiente o anterior pantalla.
Análisis de tendencia
Evolución de los estados a lo largo de las iteraciones
Grafico muestra la evolución temporal del sentimiento 

### Pantalla 6

Muestra la evolución del vector estacionario a lo largo de las iteraciones, el objetivo es poder ver en que momento se estabiliza. De acuerdo al teorema de Perron-Frobenius.


Para tu simulación de un HMM con **3 estados ocultos** y **3 observaciones** aplicado a análisis de sentimientos, aquí tienes una configuración inicial coherente:

---

### 1. Definición de estados y observaciones
- **Estados ocultos (sentimientos):**  
  S₁ = Positivo, S₂ = Neutral, S₃ = Negativo  
- **Observaciones (tokens simplificados):**  
  v₁ = palabra positiva (ej. “genial”), v₂ = palabra neutra (ej. “hoy”), v₃ = palabra negativa (ej. “odio”)

---

### 2. Matriz de transición A (probabilidades de cambio de sentimiento)

| A     | S₁ (Pos) | S₂ (Neu) | S₃ (Neg) |
|-------|----------|----------|----------|
| **S₁** | 0.6      | 0.3      | 0.1      |
| **S₂** | 0.2      | 0.6      | 0.2      |
| **S₃** | 0.1      | 0.3      | 0.6      |

*Justificación:* Los sentimientos tienden a persistir, con mayor probabilidad de moverse gradualmente que de saltar de un extremo al otro.

---

### 3. Matriz de emisión B (probabilidad de observar cada tipo de palabra según el estado)

| B     | v₁ (pal. positiva) | v₂ (pal. neutra) | v₃ (pal. negativa) |
|-------|--------------------|------------------|--------------------|
| **S₁** | 0.7                | 0.2              | 0.1                |
| **S₂** | 0.2                | 0.6              | 0.2                |
| **S₃** | 0.1                | 0.2              | 0.7                |

*Justificación:* Un estado positivo emite mayoritariamente palabras positivas, pero admite cierto ruido (neutral e incluso negativa). El estado neutral es más equilibrado.

---

### 4. Distribución inicial π (probabilidades del primer sentimiento en una secuencia)

**Opción realista** (arranque usualmente neutro en redes sociales):
```
π = [0.2, 0.6, 0.2]   →   P(Positivo)=0.2, P(Neutral)=0.6, P(Negativo)=0.2
```







