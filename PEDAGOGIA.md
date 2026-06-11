# Decisiones de diseño didáctico — Misión Ñandú

Este documento explica **por qué** la app está diseñada como está. La audiencia
es un chico de primaria (9 a 12 años) que entrena para la Olimpíada Ñandú, y el
objetivo no es solo que practique cuentas: es que desarrolle el hábito de
razonar problemas de varios pasos, que es lo que el certamen evalúa.

Las decisiones se apoyan en conceptos conocidos de las ciencias del
aprendizaje (práctica de recuperación, andamiaje, feedback formativo, práctica
espaciada). No es un currículum validado académicamente: es criterio aplicado,
y cada decisión se puede revisar si en el uso real no funciona.

---

## 1. Validación de respuestas: se evalúa la matemática, no el formato

**Decisión.** `16 cm`, `1.000` y `16` valen lo mismo que `16` / `1000`. La app
interpreta unidades, separadores de miles y mayúsculas/tildes antes de
comparar. Algunos problemas aceptan varias formas de la misma respuesta
(`9:00`, `9`, `a las 9`).

**Por qué.** Para un chico, que le marquen *incorrecto* algo que resolvió bien
es la experiencia más injusta y desmotivadora posible: aprende que el juego
"está roto" o, peor, que la matemática es arbitraria. El objetivo de cada
problema es el razonamiento, no la convención de escritura. La rigurosidad de
notación se trabaja en otro lado (y en el certamen real la corrige un humano
con criterio).

**El límite.** La tolerancia es de *formato*, nunca de *valor*: `6` no vale
cuando la respuesta es `16`, y la comparación exige igualdad numérica exacta.

## 2. Respuesta escrita como regla; opción múltiple solo donde corresponde

**Decisión.** Casi todos los problemas piden escribir la respuesta. Solo el
módulo "Encuentra el Error" usa opción múltiple.

**Por qué.** Producir una respuesta desde cero (práctica de recuperación)
genera un aprendizaje más profundo que reconocerla en una lista, y es además
el formato del certamen real, donde no hay opciones. Pero "Encuentra el Error"
es distinto: su objetivo es **discriminar entre concepciones erróneas**
(¿perímetro o área? ¿sumar o multiplicar denominadores?). Ahí las opciones no
son una concesión: son el contenido. Cada distractor es un error conceptual
real que los chicos cometen, y elegir entre ellos obliga a contrastarlos.
Antes este módulo pedía tipear una frase exacta ("dividir por 2"), lo que
evaluaba adivinación de palabras, no comprensión.

## 3. Dos intentos antes de revelar la respuesta

**Decisión.** En entrenamiento, el primer error no muestra la solución:
muestra "¡Casi! Probá una vez más" y deja el problema abierto. La respuesta y
la explicación recién se revelan tras el segundo error (o al acertar).

**Por qué.** Si la solución aparece al primer fallo, la estrategia óptima para
el chico pasa a ser *responder cualquier cosa rápido para ver la respuesta*.
El esfuerzo adicional frente a un problema que "casi sale" (esfuerzo
productivo) es donde más se aprende; el segundo intento, con la pista
disponible, convierte el error en información ("algo de mi cuenta falló")
en lugar de en veredicto. Dos intentos y no más: a partir del tercero la
frustración supera al beneficio, y la explicación pasa a ser lo más valioso.

## 4. Pistas visibles, con costo suave

**Decisión.** El botón de pista está siempre disponible en entrenamiento, la
pista aparece en la pantalla (no en un popup) y usar pista reduce el XP del
problema a la mitad. El costo está avisado de antemano.

**Por qué.** Pedir ayuda es una conducta que queremos *permitir sin castigar*
— la pista es andamiaje: una pregunta orientadora, nunca la solución. Pero si
la pista fuera gratis, abusar de ella sería la jugada dominante ("apretás el
botón antes de pensar"). El medio XP mantiene el incentivo de intentar primero
sin convertir la ayuda en penitencia. Importante: el XP nunca se descuenta,
solo se gana menos — en ningún caso jugar deja al chico peor que no jugar.

## 5. Feedback inmediato al entrenar, diferido al competir

**Decisión.** En los módulos de entrenamiento la corrección es inmediata y
con explicación ("Estrategia Olímpica"). En Modo Competencia no: las
respuestas se registran y la corrección completa llega al terminar los 3
problemas de la etapa, como en el certamen real. En competencia tampoco hay
pistas ni segundo intento.

**Por qué.** Son dos momentos de aprendizaje distintos. Entrenando, el
feedback inmediato y explicado es de lo más efectivo que existe (feedback
formativo: no solo "bien/mal" sino *por qué*). Compitiendo, el objetivo es
otro: ensayar las condiciones reales del certamen, donde nadie te confirma
nada y tenés que autoevaluarte, manejar la ansiedad y seguir. El resumen de
etapa al final reintroduce el feedback con la corrección completa de los 3
problemas, que es exactamente el ritual de revisar la prueba al salir.

## 6. Contrarreloj opcional, y más corto que el real

**Decisión.** El timer de competencia es una opción que se elige al
inscribirse (apagado por defecto): 15 minutos por etapa de 3 problemas. Si se
acaba el tiempo, lo no respondido cuenta como incorrecto.

**Por qué.** La presión de tiempo es una habilidad entrenable, pero también la
principal fuente de ansiedad en esta edad; imponerla siempre haría que los
chicos más ansiosos eviten el modo competencia, que es justo lo que más los
prepara. Por eso es opt-in. Los 15 minutos (y no las ~2 horas del certamen
real) responden a que los problemas del banco son más cortos que los del
certamen: el ratio tiempo/problema queda exigente pero alcanzable, y una
sesión de juego completa sigue durando lo que un chico tolera.

## 7. Revancha: los errores propios son el mejor plan de estudio

**Decisión.** Todo problema fallado entra en una cola de "Revancha". El módulo
los repite (primero el fallado hace más tiempo) y acertarlos los saca de la
cola, con celebración explícita ("¡Revancha ganada!").

**Por qué.** Volver sobre el propio error pasado un tiempo es de las prácticas
con más evidencia a favor (práctica espaciada + recuperación), y es además lo
que un entrenador humano haría: insistir donde flaqueás. El diseño cuida dos
cosas: la cola **se redime** (acertar limpia, la lista se achica, hay
sensación de progreso) y el módulo se presenta como *revancha* — un desquite
deportivo — y no como "tus errores", que sería un castigo con nombre propio.

## 8. XP, racha y mascota: motivación dosificada

**Decisión.** El XP escala con la dificultad (20/40/60), la mascota evoluciona
por nivel, y hay racha de días entrenando. No hay tabla de posiciones, no hay
comparación con otros, no se pierde nunca XP ni se "baja" de nivel.

**Por qué.** A esta edad la motivación extrínseca (puntos, mascota) es una
puerta de entrada legítima, siempre que premie el *esfuerzo y la dificultad
elegida* y no la velocidad — por eso un problema difícil vale el triple que
uno fácil, y por eso no hay bonus por responder rápido. La racha premia la
consistencia (que es la variable que de verdad predice la mejora) y se basa en
días, no en horas jugadas: 10 minutos por día alimentan la racha igual que una
hora. Todo lo punitivo quedó afuera deliberadamente: perder XP, rachas que
humillan al cortarse, rankings.

## 9. Tono y lenguaje: voseo, y el error como detalle a revisar

**Decisión.** Toda la app habla en voseo rioplatense ("Probá", "Fijate",
"¡Vos podés!"). El mensaje de error es "Hay un detalle para revisar... 🤔" y
el de reintento "¡Casi! Probá una vez más 💪". Las soluciones se llaman
"Estrategia Olímpica".

**Por qué.** El voseo es el registro real de un chico argentino: la app le
habla como le habla su maestra, no como un libro español. Los mensajes de
error están redactados desde la mentalidad de crecimiento: señalan que *la
resolución* tiene un detalle, no que *el chico* está mal — nunca "MAL",
"INCORRECTO" ni rojo a pantalla completa. Y llamar "Estrategia Olímpica" a la
explicación reencuadra leer la solución: no es el premio consuelo del que
falló, es material de entrenamiento de campeones.

## 10. Contenido: plantillas para volumen, problemas manuales para profundidad

**Decisión.** El banco mezcla ~170 problemas generados por plantillas
paramétricas con 24 problemas escritos a mano, de varios pasos, al estilo de
los certámenes Ñandú (más los 10 de "Encuentra el Error", también manuales).
El Modo Competencia mezcla categorías (práctica intercalada) y sube la
dificultad por instancia: Escolar/Intercolegial nivel 1, Zonal/Regional nivel
2, Nacional nivel 3.

**Por qué.** Las plantillas dan volumen para automatizar técnicas (un alumno
que vio 15 secuencias aritméticas distintas ya no calcula: *ve* el paso), pero
tienen un riesgo conocido: el chico aprende a reconocer la plantilla en lugar
de razonar. Los problemas manuales atacan justo eso: números elegidos a
propósito, contexto narrativo, más de una idea encadenada y algún resultado
sorprendente (recortar las esquinas **no** cambia el perímetro). Que la
competencia mezcle categorías también es deliberado: identificar *qué tipo de
problema es* es la primera habilidad que pide un certamen, y la práctica por
bloques (todo patrones, todo geometría) no la entrena.

**Calidad como requisito pedagógico:** cada problema del banco pasa por
`test_banco.py`, que recalcula la respuesta desde el enunciado por un método
independiente. Un solo problema con respuesta incorrecta le enseña al alumno
a desconfiar de todo el sistema (o de sí mismo); acá eso rompe el build.

## 11. El Panel del Entrenador es para el adulto

**Decisión.** Las estadísticas finas (precisión por módulo, intentos,
sugerencia de qué entrenar) viven en una pantalla aparte, no en la pantalla
de juego. El chico ve barras de progreso que solo crecen; el panel muestra
porcentajes que pueden ser bajos.

**Por qué.** Un 45% de precisión es información valiosísima para el adulto
que acompaña ("conviene practicar divisibilidad esta semana") y un golpe
gratuito para el chico si se lo cruza después de cada problema. Separar las
vistas permite que cada número le llegue a quien puede hacer algo útil con él.
La sugerencia de entrenamiento pide un mínimo de 5 intentos por módulo antes
de opinar, para no diagnosticar sobre ruido.

---

## Límites conocidos y posibles próximos pasos

- **Sin niveles por grado.** La Ñandú real tiene 3 niveles (5º, 6º y 7º
  grado) y la app no distingue: la dificultad 1–3 es transversal. Un selector
  de nivel exigiría etiquetar el banco por grado con criterio curricular real;
  hacerlo "a ojo" daría precisión falsa.
- **Sin justificación escrita.** En el certamen real no alcanza la respuesta:
  hay que justificar. Practicar eso requiere corrección humana (o un adulto
  que revise); la app entrena la parte automatizable.
- **Un solo perfil.** El progreso vive en `localStorage` del navegador. Si
  dos hermanos comparten dispositivo, comparten ñandú (se puede borrar el
  progreso desde el Panel del Entrenador).
- **La racha es local del dispositivo**: jugar en la tablet y en la compu
  cuenta como dos entrenamientos separados.
