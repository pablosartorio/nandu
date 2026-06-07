# Plan de mejora — Misión Ñandú

## Fase 1 — Bugs que rompen la experiencia

**a. Validación de respuesta permisiva**
- Archivo: `mision_nandu.html` línea ~717
- Cambiar `input === correct || input.includes(correct)` por `input === correct`
- Actualmente "16" o "600" pasan como respuesta correcta cuando la respuesta es "6"

**b. Problemas olímpicos con respuesta incorrecta**
- Archivo: `generate_problems.py` líneas 218-223
- El enunciado muestra un total aleatorio (25/34/40/52) pero la respuesta siempre es 6 (calculada para 25)
- Solución: escribirlos como datos fijos en lugar de generación paramétrica

**c. Deduplicar el banco de problemas**
- Archivo: `generate_problems.py`
- Usar un set de enunciados vistos y skipear antes de hacer `append`
- Actualmente hay problemas idénticos (ej: "3, 9, 27, 81..." aparece 3 veces)

---

## Fase 2 — Calidad del contenido

**d. Módulo "Encuentra el Error" con variedad real**
- Actualmente: 15 problemas idénticos (mismo enunciado, misma respuesta)
- Escribir ~10 errores distintos: perímetro vs área, fracciones, orden de operaciones, unidades, etc.
- No aplica generación paramétrica, hay que escribirlos a mano

**e. Dificultad progresiva en Modo Competencia**
- En lugar de problemas aleatorios, subir dificultad por etapa
- Escolar → dificultad 1, Zonal → dificultad 2, Nacional → dificultad 3

**f. IDs únicos globales**
- Archivo: `generate_problems.py` líneas 82-83
- Eliminar el reset de `id_counter` y de `problems` a mitad del script
- Actualmente los problemas de lógica reutilizan IDs 26-35 (ya usados por patrones)

---

## Fase 3 — Features de valor

**g. Tracking de progreso por categoría**
- Guardar en estado cuántos problemas resolvió por módulo
- Mostrar barras de progreso en el dashboard

**h. Anti-repetición inmediata**
- Guardar el id del último problema mostrado y excluirlo del sorteo siguiente
- Evita que el mismo problema salga dos veces seguidas

**i. SVG de geometría útil**
- Dibujar la figura con las medidas del problema concreto (base, altura, lado)
- Requiere agregar metadata de figura al JSON de cada problema de geometría
- Actualmente el SVG es siempre el mismo cuadrado decorativo independiente del problema

---

## Lo que NO hacer

- No migrar a frameworks (React, Vue) — el valor del proyecto es ser un único HTML portable
- No separar en múltiples archivos
- No agregar backend ni servidor

## Orden recomendado por retorno

1c (deduplicar) → 1a (validación) → 1b (olímpicos) → 2d (errores) → 3h (anti-repetición)
