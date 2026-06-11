import json
import random
from math import gcd

# Semilla fija: el banco es reproducible (misma corrida -> mismo JSON).
# Para publicar un banco distinto, cambiar la semilla y regenerar.
random.seed(20260611)

problems = []
id_counter = 1
seen_questions = set()

def lcm_list(nums):
    r = 1
    for n in nums:
        r = r * n // gcd(r, n)
    return r

def add_problem(cat, diff, question, answer, explanation, hint="", figura=None,
                template="manual", opciones=None, respuestas_aceptadas=None):
    global id_counter
    if question in seen_questions:
        return
    seen_questions.add(question)
    p = {
        "id": id_counter,
        "categoria": cat,
        "dificultad": diff,
        "enunciado": question,
        "respuesta": str(answer),
        "explicacion": explanation,
        "pista": hint,
        # Identifica la plantilla generadora; test_banco.py recalcula la
        # respuesta de cada plantilla a partir del enunciado.
        "template": template,
    }
    # Metadata de figura para que el SVG dibuje el problema concreto.
    # Solo registramos los datos DADOS en el enunciado, nunca la respuesta.
    if figura is not None:
        p["figura"] = figura
    # Opción múltiple: la app muestra botones en lugar del campo de texto.
    if opciones is not None:
        assert str(answer) in opciones, f"respuesta {answer!r} no está en las opciones"
        p["opciones"] = opciones
    # Otras formas válidas de escribir la misma respuesta.
    if respuestas_aceptadas is not None:
        p["respuestas_aceptadas"] = respuestas_aceptadas
    problems.append(p)
    id_counter += 1

# 1. Patrones (approx 35)
for i in range(15):
    # Arithmetic
    start = random.randint(2, 20)
    step = random.randint(3, 12)
    seq = [start + step*j for j in range(5)]
    ans = start + step*5
    add_problem("patrones", 1,
                f"Observá la secuencia: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ... ¿Qué número sigue?",
                ans,
                f"La secuencia aumenta sumando {step} en cada paso. {seq[4]} + {step} = {ans}",
                "Calculá la diferencia entre números consecutivos.",
                template="patrones_aritmetica")

for i in range(10):
    # Geometric / Alternating
    start = random.randint(2, 5)
    mult = random.randint(2, 4)
    seq = [start * (mult**j) for j in range(4)]
    ans = start * (mult**4)
    add_problem("patrones", 2,
                f"Descifrá el patrón: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... ¿Cuál es el próximo número?",
                ans,
                f"Cada número se multiplica por {mult} para obtener el siguiente. {seq[3]} x {mult} = {ans}",
                "Fijate si en lugar de sumar, los números se multiplican.",
                template="patrones_geometrica")

for i in range(10):
    # Double step (e.g. +2, +3, +4...)
    start = random.randint(1, 10)
    seq = [start]
    current_add = random.randint(2, 5)
    for _ in range(4):
        seq.append(seq[-1] + current_add)
        current_add += 1
    ans = seq[-1] + current_add
    add_problem("patrones", 3,
                f"Encontrá el siguiente término: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ...",
                ans,
                f"La diferencia entre los números no es fija. Primero se suma {current_add-4}, luego {current_add-3}, y así sucesivamente. Al último se le suma {current_add}.",
                "Observá las diferencias entre los números consecutivos, ¿qué patrón forman esas diferencias?",
                template="patrones_dif_creciente")

# 2. Lógica / Estrategias (approx 35)
names = ["Ana", "Beto", "Carlos", "Delfina", "Ema", "Facu", "Gaby"]

for i in range(15):
    a, b = random.sample(names, 2)
    diff = random.randint(3, 10)
    sum_ages = random.randint(20, 50)
    if (sum_ages + diff) % 2 != 0: sum_ages += 1
    age_a = (sum_ages + diff) // 2
    age_b = sum_ages - age_a
    add_problem("logica", 1,
                f"Las edades de {a} y {b} suman {sum_ages} años. Si {a} es {diff} años mayor que {b}, ¿cuántos años tiene {a}?",
                age_a,
                f"Si a la suma ({sum_ages}) le restamos la diferencia ({diff}) queda {sum_ages-diff}. Dividimos por 2 y obtenemos la edad del menor ({age_b}). El mayor tiene {age_a}.",
                "Restá la diferencia a la suma total para igualarlos.",
                template="logica_edades")

for i in range(10):
    a, b, c = random.sample(names, 3)
    x = random.randint(5, 15)
    total = 4 * x
    add_problem("logica", 2,
                f"{a}, {b} y {c} juntaron {total} figuritas. {a} tiene el doble que {b}, y {c} tiene lo mismo que {b}. ¿Cuántas figuritas tiene {a}?",
                2 * x,
                f"Podemos pensar que {b} tiene 1 'parte', {c} tiene 1 'parte' y {a} tiene 2 'partes'. En total son 4 partes que suman {total}. Cada parte es {total}/4 = {x}. Entonces {a} tiene 2 * {x} = {2*x}.",
                "Dibujá cajitas. Si B tiene 1 cajita, C tiene 1 y A tiene 2.",
                template="logica_partes")

for i in range(10):
    animals = random.choice([("gallinas", "conejos", 2, 4), ("patos", "vacas", 2, 4), ("triciclos", "bicicletas", 3, 2)])
    a1, a2, p1, p2 = animals
    qty1 = random.randint(5, 15)
    qty2 = random.randint(5, 15)
    total_heads = qty1 + qty2
    total_legs = qty1*p1 + qty2*p2
    add_problem("logica", 3,
                f"En una granja hay {a1} y {a2}. Si contamos las cabezas (o vehículos) hay {total_heads}, y si contamos las patas (o ruedas) hay {total_legs}. ¿Cuántos {a2} hay?",
                qty2,
                f"Si todos fueran {a1}, habría {total_heads * p1} patas/ruedas. Pero hay {total_legs}, una diferencia de {total_legs - total_heads * p1}. Cada {a2} aporta {p2 - p1} extra. { (total_legs - total_heads * p1) } / {p2 - p1} = {qty2}.",
                f"Imaginate que todos son {a1}. ¿Cuántas patas/ruedas faltarían para llegar al total?",
                template="logica_patas")

# 3. Geometría (approx 35)
for i in range(15):
    l1 = random.randint(4, 15)
    add_problem("geometria", 1,
                f"Se forma un rectángulo uniendo dos cuadrados iguales de lado {l1} cm. ¿Cuál es el perímetro del rectángulo formado?",
                6 * l1,
                f"Al unir los dos cuadrados por un lado, esos dos lados quedan adentro. El perímetro está formado por 3 lados de un cuadrado y 3 del otro. Total: 6 lados de {l1} cm = {6*l1} cm.",
                "Hacé un dibujo. Contá cuántos 'lados' de los cuadrados originales quedan en el borde exterior.",
                figura={"tipo": "rect_dos_cuadrados", "lado": l1},
                template="geo_dos_cuadrados")

for i in range(10):
    b = random.randint(5, 10) * 2  # base par => b*h siempre par => el área es exacta y la altura se recupera sin redondeo
    h = random.randint(5, 15)
    add_problem("geometria", 2,
                f"El área de un triángulo es {b * h // 2} cm² y su base mide {b} cm. ¿Cuánto mide su altura?",
                h,
                f"El área de un triángulo es (base x altura) / 2. Entonces: {b} x altura / 2 = {b * h // 2}. Multiplicando por 2: {b} x altura = {b*h}. La altura es {h} cm.",
                "Acordate de la fórmula: Área = (base x altura) / 2.",
                figura={"tipo": "triangulo", "base": b, "area": b * h // 2},
                template="geo_triangulo_altura")

for i in range(10):
    L = random.randint(10, 30)
    add_problem("geometria", 3,
                f"Un cuadrado grande se divide en 4 cuadrados más pequeños e iguales. El perímetro de uno de los cuadrados pequeños es {L*4}. ¿Cuál es el área del cuadrado grande?",
                (L*2)**2,
                f"El perímetro del cuadrado pequeño es {L*4}, entonces su lado es {L}. El lado del cuadrado grande es el doble, es decir {L*2}. Su área es ({L*2}) x ({L*2}) = {(L*2)**2}.",
                "Si sabés el perímetro del cuadradito, podés saber cuánto mide su lado.",
                figura={"tipo": "cuadrado_4", "perimetro_pequeno": L * 4},
                template="geo_cuadrado_4")

# 4. Conteo y combinatoria (approx 35)
for i in range(15):
    c = random.randint(3, 5)
    p = random.randint(2, 4)
    z = random.randint(2, 4)
    add_problem("conteo", 1,
                f"Para vestirse, un chico tiene {c} remeras, {p} pantalones y {z} pares de zapatillas. ¿De cuántas formas distintas puede vestirse usando una prenda de cada tipo?",
                c * p * z,
                f"Por el principio de multiplicación: {c} opciones de remera x {p} opciones de pantalón x {z} opciones de zapatillas = {c * p * z} formas distintas.",
                "Multiplicá las opciones de cada prenda.",
                template="conteo_vestimenta")

for i in range(10):
    n = random.randint(4, 10)
    add_problem("conteo", 2,
                f"En un torneo participan {n} equipos. Si todos deben jugar contra todos exactamente una vez, ¿cuántos partidos se jugarán en total?",
                n * (n - 1) // 2,
                f"Cada uno de los {n} equipos juega con los {n-1} restantes. Eso da {n * (n-1)} partidos. Pero así estamos contando cada partido dos veces (A vs B y B vs A). Dividimos por 2: {n*(n-1)//2}.",
                "Imaginate que son puntos en un papel unidos por líneas. ¿Cuántas líneas hay?",
                template="conteo_torneo")

digit_sets = [[1, 2, 3], [2, 4, 6], [5, 6, 7], [1, 3, 5, 7], [1, 2, 3, 4], [2, 3, 4, 5]]
for i in range(10):
    digits = random.choice(digit_sets)
    L = random.randint(2, min(3, len(digits)))
    factors = [len(digits) - k for k in range(L)]
    ans = 1
    for fct in factors:
        ans *= fct
    listed = ", ".join(str(d) for d in digits)
    add_problem("conteo", 3,
                f"¿Cuántos números de {L} cifras distintas se pueden formar usando solamente los dígitos {listed}?",
                ans,
                f"Para la 1ª cifra hay {len(digits)} opciones; en cada posición siguiente queda una opción menos porque no se repiten. {' x '.join(str(fct) for fct in factors)} = {ans}.",
                "Pensá cuántas opciones quedan para cada posición, descontando los dígitos ya usados.",
                template="conteo_cifras")

# 5. Divisibilidad (approx 35)
for i in range(15):
    n1 = random.choice([2, 3, 4, 5])
    n2 = random.choice([n for n in [3, 4, 5, 7] if n != n1])
    lcm = n1 * n2 # simplified since prime/coprime usually
    add_problem("divisibilidad", 1,
                f"Dos luces parpadean: una cada {n1} segundos y otra cada {n2} segundos. Si parpadearon juntas recién, ¿en cuántos segundos volverán a parpadear juntas?",
                lcm,
                f"Buscamos el mínimo común múltiplo (MCM) entre {n1} y {n2}. Los múltiplos de {n1} son {n1}, {n1*2}, {n1*3}... El primer número común es {lcm}.",
                "Buscá el mínimo común múltiplo (MCM).",
                template="div_mcm2")

for i in range(10):
    m = random.randint(2, 6)
    r = random.randint(1, m-1)
    add_problem("divisibilidad", 2,
                f"Si dividimos a un número entre {m}, el resto es {r}. ¿Cuál es el número más pequeño de dos cifras que cumple esto?",
                ((10 // m) + 1) * m + r if ((10 // m) * m + r) < 10 else ((10 // m) * m + r),
                f"Los números que al dividir por {m} dan resto {r} son de la forma {m}*k + {r}. Probamos valores de k para encontrar el primero de dos cifras.",
                "Escribí los múltiplos y sumales el resto.",
                template="div_resto")

mcm_sets = [[2, 3, 5], [2, 3, 4], [3, 4, 6], [2, 5, 6], [4, 6, 9], [2, 3, 7], [3, 5, 6], [4, 5, 10]]
for i in range(10):
    nums = random.choice(mcm_sets)
    ans = lcm_list(nums)
    listed = ", ".join(str(n) for n in nums[:-1]) + " y " + str(nums[-1])
    add_problem("divisibilidad", 3,
                f"¿Cuál es el menor número (distinto de cero) que es múltiplo de {listed} al mismo tiempo?",
                ans,
                f"Buscamos el Mínimo Común Múltiplo (MCM) de {listed}. Tomando los factores necesarios para que sea divisible por todos, el MCM es {ans}.",
                "Buscá el primer número que aparezca en las tablas de todos ellos a la vez.",
                template="div_mcm3")

# 6. Encuentra el Error (10 distintos, opción múltiple)
# La respuesta correcta debe coincidir EXACTAMENTE con una de las opciones.
error_problems = [
    (
        "Resolución: 'El perímetro de un cuadrado de área 16 cm² es 8 cm, porque 16÷2=8'. ¿Qué operación permite encontrar el lado?",
        "Sacar la raíz cuadrada de 16",
        ["Sacar la raíz cuadrada de 16", "Dividir 16 por 2", "Dividir 16 por 4", "Restar 8 a 16"],
        "Si el área es 16 cm², el lado es √16 = 4 cm (no 16÷2). El perímetro correcto es 4×4 = 16 cm.",
        "¿Qué operación deshace 'lado × lado'?"
    ),
    (
        "Resolución: 'El área de un triángulo de base 8 cm y altura 5 cm es 40 cm², porque 8×5=40'. ¿Qué operación faltó?",
        "Dividir por 2",
        ["Dividir por 2", "Multiplicar por 2", "Sumar la base y la altura", "Restar la altura"],
        "El área de un triángulo es (base × altura) / 2 = (8 × 5) / 2 = 20 cm². Hay que dividir por 2.",
        "¿Cuál es la fórmula del área de un triángulo?"
    ),
    (
        "Resolución: '1/2 + 1/3 = 2/5, porque sumo los numeradores y los denominadores'. ¿Qué se necesita para sumar fracciones?",
        "Buscar un denominador común",
        ["Buscar un denominador común", "Sumar numeradores y denominadores", "Multiplicar las dos fracciones", "Restar los denominadores"],
        "Para sumar fracciones se necesita un denominador común. 1/2 + 1/3 = 3/6 + 2/6 = 5/6.",
        "¿Podés sumar fracciones con distinto denominador directamente?"
    ),
    (
        "Resolución: '2 + 3 × 4 = 20, porque primero sumo 2+3=5 y luego 5×4=20'. ¿Qué operación tiene prioridad?",
        "La multiplicación",
        ["La multiplicación", "La suma", "La que aparece primero", "Las dos valen igual"],
        "La multiplicación va antes que la suma. Primero 3×4=12, luego 2+12=14. No 20.",
        "¿Qué operación tiene mayor prioridad según el orden de operaciones?"
    ),
    (
        "Resolución: 'El 10% de 200 es 2, porque divido 200÷100=2'. ¿Por cuánto hay que dividir para calcular el 10%?",
        "Por 10",
        ["Por 10", "Por 100", "Por 20", "Por 5"],
        "El 10% es la décima parte: 200÷10 = 20. Dividir por 100 da el 1%, no el 10%.",
        "El 10% significa '10 de cada 100', es decir, 1 de cada 10."
    ),
    (
        "Resolución: 'El área de un cuadrado de lado 5 cm es 20 cm², porque 4×5=20'. ¿Qué calculó en realidad?",
        "El perímetro",
        ["El perímetro", "El área", "La diagonal", "El doble del lado"],
        "4×5=20 es el perímetro, no el área. El área es lado×lado = 5×5 = 25 cm².",
        "¿Cuál es la diferencia entre área y perímetro?"
    ),
    (
        "Resolución: '1/2 × 1/3 = 1/5, porque multiplico los numeradores y sumo los denominadores'. ¿Qué se hace con los denominadores al multiplicar fracciones?",
        "Se multiplican entre sí",
        ["Se multiplican entre sí", "Se suman entre sí", "Se restan", "Se deja el más grande"],
        "Al multiplicar fracciones se multiplican numeradores y denominadores. 1/2 × 1/3 = (1×1)/(2×3) = 1/6.",
        "¿Cómo se multiplican dos fracciones?"
    ),
    (
        "Resolución: 'Hay 3 camisetas y 2 pantalones, así que hay 5 combinaciones posibles porque 3+2=5'. ¿Cuál es la operación correcta?",
        "Multiplicar 3 × 2",
        ["Multiplicar 3 × 2", "Sumar 3 + 2", "Restar 3 − 2", "Elevar 3 al cuadrado"],
        "Por el principio de multiplicación: 3 × 2 = 6 combinaciones. Cada camiseta se combina con cada pantalón.",
        "¿Cuántas combinaciones tiene cada camiseta con los pantalones?"
    ),
    (
        "Resolución: 'La suma de los ángulos de un triángulo es 360° como la de cualquier figura'. ¿Cuántos grados suman los ángulos interiores de un triángulo?",
        "180°",
        ["180°", "360°", "90°", "270°"],
        "Los ángulos interiores de un triángulo suman 180°. Los 360° corresponden a los cuadriláteros.",
        "Cortá las tres puntas de un triángulo de papel y juntalas: forman un ángulo llano."
    ),
    (
        "Resolución: 'El MCM de 4 y 6 es 24, porque 4×6=24'. ¿Cuál es el Mínimo Común Múltiplo correcto?",
        "12",
        ["12", "24", "6", "48"],
        "El MCM de 4 y 6 es 12. Múltiplos de 4: 4,8,12... y de 6: 6,12... El primero en común es 12.",
        "Buscá el primer número que sea múltiplo de ambos."
    ),
]
for q, a, ops, expl, hint in error_problems:
    add_problem("error", 2, q, a, expl, hint, template="error_manual", opciones=ops)

# 7. Olímpico (approx 30) - Combina temas
for i in range(15):
    pages = random.randint(50, 150)
    add_problem("olimpico", 3,
                f"Para numerar las páginas de un libro de {pages} páginas, ¿cuántos dígitos se utilizan en total?",
                9 + (pages - 9) * 2 if pages < 100 else 9 + 90*2 + (pages - 99)*3,
                f"De la página 1 a la 9 se usan 9 dígitos. De la 10 a la {min(pages, 99)} se usan {(min(pages, 99)-9)*2} dígitos. Y si hay más de 99, las páginas de 3 cifras usan 3 dígitos cada una.",
                "Separá por cantidad de cifras: de 1 cifra, de 2 cifras, etc.",
                template="olimpico_paginas")

for i in range(15):
    azules = random.randint(3, 12)
    rojas = azules + 5
    verdes = rojas - 3
    total = azules + rojas + verdes
    add_problem("olimpico", 3,
                f"En una caja hay bolitas rojas, azules y verdes. Hay 5 rojas más que azules, y 3 verdes menos que rojas. En total hay {total} bolitas. ¿Cuántas bolitas azules hay?",
                azules,
                f"Si A son las azules: R = A+5 y V = R-3 = A+2. Total: A + (A+5) + (A+2) = 3A+7 = {total}. Entonces 3A = {total-7}, A = {azules}.",
                "Usá una letra para las bolitas azules y expresá el resto en función de ellas.",
                template="olimpico_bolitas")

# 8. Problemas estilo certamen (escritos a mano, varios pasos)
# A diferencia de las plantillas, acá los números están elegidos a propósito y
# cada problema pide encadenar más de una idea, como en los certámenes Ñandú.
manuales = [
    # --- Patrones ---
    ("patrones", 2,
     "En una fiesta se arman mesas en hilera. Una mesa sola permite sentar 6 personas, y cada mesa que se agrega a la hilera suma 4 lugares más. ¿Cuántas personas se pueden sentar con 7 mesas en hilera?",
     6 + 4 * 6,
     "La primera mesa sienta 6 personas. Las otras 6 mesas agregan 4 lugares cada una: 6 + 6×4 = 6 + 24 = 30 personas.",
     "Probá con 2 y 3 mesas, anotá cuántos lugares hay y buscá el patrón."),
    ("patrones", 2,
     "Lucía escribe una lista que empieza con 1, 1 y donde cada número siguiente se obtiene sumando los dos anteriores: 1, 1, 2, 3, 5, 8, ... ¿Cuál es el décimo número de la lista?",
     55,
     "Siguiendo la regla: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55. El décimo es 55.",
     "Escribí la lista completa hasta el décimo lugar, sumando siempre los dos últimos."),
    ("patrones", 3,
     "Un mago tiene un cofre con monedas. Cada noche duplica las monedas del cofre y, después de duplicar, saca 2 para pagar a su ayudante. Si el lunes a la mañana hay 5 monedas, ¿cuántas hay el jueves a la mañana?",
     26,
     "Pasan 3 noches. Lunes: 5. Martes: 5×2−2 = 8. Miércoles: 8×2−2 = 14. Jueves: 14×2−2 = 26 monedas.",
     "Andá día por día: primero duplicá, después restá 2."),
    ("patrones", 3,
     "Se arma una guarda con palitos de helado: el primer cuadrado usa 4 palitos, y cada cuadrado siguiente, pegado al anterior, usa solo 3 palitos más. ¿Cuántos palitos hacen falta para una guarda de 12 cuadrados?",
     4 + 3 * 11,
     "El primer cuadrado usa 4 palitos y los 11 siguientes usan 3 cada uno (comparten un lado con el anterior): 4 + 11×3 = 37 palitos.",
     "Dibujá los primeros 3 cuadrados pegados y contá los palitos: 4, 7, 10..."),

    # --- Lógica ---
    ("logica", 2,
     "Ana, Bruno y Carla corren una carrera. Ana no llegó última, Carla llegó justo detrás de Ana y Bruno no ganó. ¿Quién ganó la carrera?",
     "Ana",
     "Como Carla llegó justo detrás de Ana, van pegadas en ese orden. Si Bruno no ganó, la única opción es Ana 1ª, Carla 2ª y Bruno 3º. Ganó Ana.",
     "Probá los órdenes posibles y tachá los que rompen alguna de las tres condiciones."),
    ("logica", 2,
     "En un canasto hay 30 frutas entre manzanas y naranjas. Hay 8 manzanas más que naranjas. ¿Cuántas naranjas hay?",
     (30 - 8) // 2,
     "Si sacamos las 8 manzanas 'de más', quedan 22 frutas repartidas en partes iguales: 11 naranjas y 11 manzanas. Hay 11 naranjas (y 19 manzanas: 11+19 = 30).",
     "Sacá la diferencia del total y repartí lo que queda en partes iguales."),
    ("logica", 3,
     "Tres amigas juntan caramelos. Sofía tiene el triple que Valen, y Mora tiene 4 caramelos más que Valen. Entre las tres tienen 54 caramelos. ¿Cuántos caramelos tiene Sofía?",
     3 * ((54 - 4) // 5),
     "Si Valen tiene V: Sofía tiene 3V y Mora tiene V+4. Entonces V + 3V + V + 4 = 54, es decir 5V = 50, V = 10. Sofía tiene 3×10 = 30 caramelos.",
     "Usá 'cajitas': Valen 1 caja, Sofía 3 cajas, Mora 1 caja y 4 sueltos."),
    ("logica", 3,
     "Un caracol sube por un poste de 16 metros. De día sube 5 metros, pero de noche resbala 3. Si empieza un lunes a la mañana desde el piso, ¿qué día llega a la punta?",
     "domingo",
     "Cada día completo avanza 5−3 = 2 metros. Al terminar el sábado de noche está a 12 metros. El domingo sube 5 y llega a 17: ¡alcanza la punta el domingo, y ya no resbala!",
     "Ojo con el final: el día que llega arriba, ya no resbala a la noche."),

    # --- Geometría ---
    ("geometria", 2,
     "Un rectángulo tiene 36 cm de perímetro y su base mide el doble que su altura. ¿Cuántos centímetros mide la base?",
     12,
     "Base + altura = 36÷2 = 18 cm. Como la base es el doble, son 3 partes iguales: 18÷3 = 6. La altura mide 6 cm y la base 2×6 = 12 cm.",
     "La base y la altura juntas suman la mitad del perímetro."),
    ("geometria", 2,
     "Con baldosas cuadradas de 20 cm de lado se quiere cubrir por completo un patio rectangular de 2 metros por 3 metros, sin cortar ninguna baldosa. ¿Cuántas baldosas se necesitan?",
     (200 // 20) * (300 // 20),
     "2 m = 200 cm y 3 m = 300 cm. Entran 200÷20 = 10 baldosas a lo ancho y 300÷20 = 15 a lo largo: 10 × 15 = 150 baldosas.",
     "Pasá todo a centímetros y fijate cuántas baldosas entran por lado."),
    ("geometria", 3,
     "A una hoja cuadrada de 12 cm de lado se le recorta, en cada esquina, un cuadradito de 2 cm de lado. ¿Cuál es el perímetro de la figura que queda?",
     4 * 12,
     "¡Sorpresa! El perímetro no cambia: en cada esquina se quitan dos pedacitos de 2 cm del borde, pero aparecen dos lados nuevos de 2 cm hacia adentro. Sigue siendo 4×12 = 48 cm.",
     "Dibujalo y seguí el borde con el dedo: por cada pedacito que sacás, aparece otro igual."),
    ("geometria", 3,
     "Un cuadrado tiene el mismo perímetro que un rectángulo de 14 cm de base y 6 cm de altura. ¿Cuál es el área del cuadrado?",
     ((2 * (14 + 6)) // 4) ** 2,
     "El perímetro del rectángulo es 2×(14+6) = 40 cm. El lado del cuadrado es 40÷4 = 10 cm, y su área es 10×10 = 100 cm².",
     "Primero el perímetro del rectángulo, después el lado del cuadrado."),

    # --- Conteo ---
    ("conteo", 2,
     "¿Cuántos números de dos cifras tienen sus dos cifras iguales?",
     9,
     "Son 11, 22, 33, 44, 55, 66, 77, 88 y 99: uno por cada dígito del 1 al 9. Hay 9 (el 00 no es un número de dos cifras).",
     "Escribilos todos: empiezan en 11."),
    ("conteo", 2,
     "Para armar un helado se elige un envase (vasito o cucurucho) y dos gustos distintos entre chocolate, frutilla, vainilla y limón (no importa el orden de los gustos). ¿Cuántos helados diferentes se pueden armar?",
     12,
     "Las parejas de gustos distintos son 6: Ch-F, Ch-V, Ch-L, F-V, F-L, V-L. Con 2 envases posibles: 6 × 2 = 12 helados.",
     "Primero anotá todas las parejas de gustos, con cuidado de no repetir Ch-F y F-Ch."),
    ("conteo", 3,
     "Fede, Gime y Hugo se sientan en 3 butacas juntas del cine. Fede no quiere sentarse en el medio. ¿De cuántas maneras distintas pueden ubicarse?",
     4,
     "En total hay 6 maneras de sentarse (3×2×1). Con Fede en el medio hay 2 (Gime y Hugo se intercambian). Quedan 6 − 2 = 4 maneras.",
     "Contá todas las formas posibles y restá las que tienen a Fede en el medio."),
    ("conteo", 3,
     "¿Cuántos números entre 1 y 100 tienen al menos un dígito 7?",
     19,
     "Con 7 en las unidades: 7, 17, 27, ..., 97 (son 10). Con 7 en las decenas: 70 a 79 (son 10). El 77 está en las dos listas, así que son 10 + 10 − 1 = 19.",
     "Armá dos listas (7 en las unidades y 7 en las decenas) y ojo con contar el 77 dos veces."),

    # --- Divisibilidad ---
    ("divisibilidad", 2,
     "Caro tiene entre 30 y 40 figuritas. Si las agrupa de a 5 no le sobra ninguna, y si las agrupa de a 4 le sobran 3. ¿Cuántas figuritas tiene?",
     35,
     "Entre 30 y 40, los múltiplos de 5 son 30, 35 y 40. Al dividir por 4: 30 deja resto 2, 35 deja resto 3 ✓ y 40 deja resto 0. Tiene 35 figuritas.",
     "Empezá por los múltiplos de 5 entre 30 y 40: son solo tres candidatos."),
    ("divisibilidad", 2,
     "¿Cuál es el menor número de tres cifras que es divisible por 2, por 3 y por 5 a la vez?",
     120,
     "Ser divisible por 2, 3 y 5 a la vez es ser múltiplo de 30. Los múltiplos de 30 son 30, 60, 90, 120... El primero de tres cifras es 120.",
     "¿De qué número tiene que ser múltiplo? Buscá el primero que llegue a tres cifras."),
    ("divisibilidad", 3,
     "Tres colectivos salen juntos de la terminal a las 8:00. Uno sale cada 12 minutos, otro cada 15 y otro cada 20. ¿A qué hora vuelven a salir los tres juntos?",
     "9:00",
     "Hay que buscar el MCM de 12, 15 y 20, que es 60. Los tres coinciden cada 60 minutos: vuelven a salir juntos a las 9:00.",
     "Buscá cada cuántos minutos coinciden los tres (MCM) y sumalo a las 8:00.",
     {"respuestas_aceptadas": ["9", "09:00", "a las 9", "las 9", "9 hs"]}),
    ("divisibilidad", 3,
     "Un número de dos cifras es múltiplo de 9, y su cifra de las decenas es el doble que la de las unidades. ¿Qué número es?",
     63,
     "Los números con la decena doble que la unidad son 21, 42, 63 y 84. El único múltiplo de 9 (sus cifras suman 9) es 63.",
     "Anotá los números cuya decena es el doble de la unidad: son poquitos."),

    # --- Olímpico ---
    ("olimpico", 3,
     "En un quiosco, 2 alfajores y 3 caramelos cuestan $1050. Un alfajor cuesta el doble que un caramelo. ¿Cuánto cuesta un alfajor?",
     300,
     "Como cada alfajor vale 2 caramelos, 2 alfajores + 3 caramelos equivalen a 7 caramelos. Entonces un caramelo cuesta 1050÷7 = $150, y el alfajor 2×150 = $300.",
     "Convertí los alfajores en caramelos: ¿a cuántos caramelos equivale todo?"),
    ("olimpico", 3,
     "Martina escribe todos los números del 1 al 50. ¿Cuántas veces escribe el dígito 4?",
     15,
     "En las unidades aparece en 4, 14, 24, 34 y 44 (5 veces). En las decenas, en 40 a 49 (10 veces). En total: 5 + 10 = 15 veces (el 44 lo tiene dos veces y se cuenta en ambas).",
     "Contá por separado: el 4 en las unidades y el 4 en las decenas."),
    ("olimpico", 3,
     "En el campamento hay carpas de 2 personas y carpas de 3 personas. En total hay 13 carpas y duermen 31 personas, sin lugares vacíos. ¿Cuántas carpas de 3 personas hay?",
     5,
     "Si las 13 carpas fueran de 2, dormirían 26 personas. Sobran 31−26 = 5 personas, y cada carpa de 3 aloja exactamente 1 persona más: hay 5 carpas de 3 (y 8 de 2: 5×3 + 8×2 = 31 ✓).",
     "Imaginá que todas las carpas son de 2: ¿cuántas personas quedan sin lugar?"),
    ("olimpico", 3,
     "Un libro se abre al azar y la suma de los números de las dos páginas enfrentadas es 145. ¿Qué número tiene la página de la derecha?",
     73,
     "Las páginas enfrentadas son consecutivas: n + (n+1) = 145, así que n = 72. Son la 72 y la 73. En los libros, la página de la derecha lleva el número impar: es la 73.",
     "Las dos páginas son números consecutivos que suman 145."),
]
for item in manuales:
    cat, diff, q, a, expl, hint = item[:6]
    extra = item[6] if len(item) > 6 else {}
    add_problem(cat, diff, q, a, expl, hint, template="manual",
                respuestas_aceptadas=extra.get("respuestas_aceptadas"))

# Generate JSON
with open("problemas_nandu.json", "w", encoding="utf-8") as f:
    json.dump(problems, f, ensure_ascii=False, indent=2)

print(f"Generated {len(problems)} problems.")
