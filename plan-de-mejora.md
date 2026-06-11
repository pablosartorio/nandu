# Plan de mejora — Misión Ñandú

## ✅ Hecho

**Tanda 1 (junio 2026, primeras fases):** validación estricta de respuestas,
problemas olímpicos consistentes, banco deduplicado, 10 errores distintos en
"Encuentra el Error", dificultad progresiva en competencia, IDs únicos,
progreso por categoría, anti-repetición inmediata, SVG de geometría con los
datos del problema.

**Tanda 2 (2026-06-11):** las cinco mejoras grandes — el porqué de cada
decisión está en [`PEDAGOGIA.md`](PEDAGOGIA.md):

1. **Validación justa:** comparación numérica tolerante a unidades y
   separadores de miles, `respuestas_aceptadas` por problema, y opción
   múltiple en "Encuentra el Error" (4 opciones con distractores
   conceptuales).
2. **UX sin `alert()`:** modales y toasts propios, pista inline con costo de
   medio XP, segunda oportunidad antes de revelar la respuesta, teclado
   numérico en mobile.
3. **Competencia fiel al certamen:** "Intercolegial" (nombre oficial), sin
   corrección hasta terminar los 3 problemas, resumen de etapa con la
   corrección completa, contrarreloj opcional de 15 min, confirmación al
   abandonar, sin pistas.
4. **Revancha + Panel del Entrenador:** cola de problemas fallados que se
   redime al acertar, precisión por módulo, racha diaria y sugerencia de qué
   entrenar.
5. **Contenido y calidad:** semilla fija (banco reproducible), 24 problemas
   manuales estilo certamen (4 por categoría), voseo consistente, y
   `test_banco.py` que recalcula cada respuesta desde el enunciado por un
   método independiente (185/195 verificadas; el resto son los de opción
   múltiple, con control estructural).

---

## Ideas futuras (por orden de retorno estimado)

- **Selector de nivel Ñandú (1/2/3 según grado):** requiere etiquetar el
  banco por grado con criterio curricular real (temario oficial de cada
  nivel), no "a ojo".
- **Más problemas manuales:** es la mejora de mayor valor por hora invertida;
  el mecanismo ya está (lista `manuales` en `generate_problems.py` + control
  en `MANUALES_ESPERADOS` de `test_banco.py`).
- **Práctica de justificación escrita:** un modo donde el alumno escribe su
  razonamiento y un adulto lo revisa (la app no puede corregirlo sola).
- **Multi-perfil:** dos hermanos en el mismo dispositivo hoy comparten
  progreso.
- **PWA / ícono en pantalla de inicio:** el HTML único ya funciona offline
  una vez descargado; faltaría manifest para instalarlo como app.

## Lo que NO hacer

- No migrar a frameworks (React, Vue) — el valor del proyecto es ser un único
  HTML portable.
- No separar en múltiples archivos.
- No agregar backend ni servidor.
- No agregar mecánicas punitivas (perder XP, rankings, presión de tiempo
  obligatoria) — ver PEDAGOGIA.md §8.
