import json
import random
from math import gcd

problems = []
id_counter = 1
seen_questions = set()

def lcm_list(nums):
    r = 1
    for n in nums:
        r = r * n // gcd(r, n)
    return r

def add_problem(cat, diff, question, answer, explanation, hint="", figura=None):
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
        "pista": hint
    }
    # Metadata de figura para que el SVG dibuje el problema concreto.
    # Solo registramos los datos DADOS en el enunciado, nunca la respuesta.
    if figura is not None:
        p["figura"] = figura
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
                f"Observa la secuencia: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ... ¿Qué número sigue?", 
                ans, 
                f"La secuencia aumenta sumando {step} en cada paso. {seq[4]} + {step} = {ans}",
                "Calcula la diferencia entre números consecutivos.")

for i in range(10):
    # Geometric / Alternating
    start = random.randint(2, 5)
    mult = random.randint(2, 4)
    seq = [start * (mult**j) for j in range(4)]
    ans = start * (mult**4)
    add_problem("patrones", 2,
                f"Descifra el patrón: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ... ¿Cuál es el próximo número?",
                ans,
                f"Cada número se multiplica por {mult} para obtener el siguiente. {seq[3]} x {mult} = {ans}",
                "Fíjate si en lugar de sumar, los números se multiplican.")

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
                f"Encuentra el siguiente término: {seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, {seq[4]}, ...",
                ans,
                f"La diferencia entre los números no es fija. Primero se suma {current_add-4}, luego {current_add-3}, y así sucesivamente. Al último se le suma {current_add}.",
                "Observa las diferencias entre los números consecutivos, ¿qué patrón forman esas diferencias?")

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
                "Resta la diferencia a la suma total para igualarlos.")

for i in range(10):
    a, b, c = random.sample(names, 3)
    x = random.randint(5, 15)
    total = 4 * x
    add_problem("logica", 2,
                f"{a}, {b} y {c} juntaron {total} figuritas. {a} tiene el doble que {b}, y {c} tiene lo mismo que {b}. ¿Cuántas figuritas tiene {a}?",
                2 * x,
                f"Podemos pensar que {b} tiene 1 'parte', {c} tiene 1 'parte' y {a} tiene 2 'partes'. En total son 4 partes que suman {total}. Cada parte es {total}/4 = {x}. Entonces {a} tiene 2 * {x} = {2*x}.",
                "Dibuja cajitas. Si B tiene 1 cajita, C tiene 1 y A tiene 2.")

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
                f"Imagina que todos son {a1}. ¿Cuántas patas/ruedas faltarían para llegar al total?")

# 3. Geometría (approx 35)
for i in range(15):
    l1 = random.randint(4, 15)
    l2 = random.randint(4, 15)
    add_problem("geometria", 1,
                f"Se forma un rectángulo uniendo dos cuadrados iguales de lado {l1} cm. ¿Cuál es el perímetro del rectángulo formado?",
                6 * l1,
                f"Al unir los dos cuadrados por un lado, esos dos lados quedan adentro. El perímetro está formado por 3 lados de un cuadrado y 3 del otro. Total: 6 lados de {l1} cm = {6*l1} cm.",
                "Haz un dibujo. Cuenta cuántos 'lados' de los cuadrados originales quedan en el borde exterior.",
                figura={"tipo": "rect_dos_cuadrados", "lado": l1})

for i in range(10):
    b = random.randint(5, 10) * 2  # base par => b*h siempre par => el área es exacta y la altura se recupera sin redondeo
    h = random.randint(5, 15)
    add_problem("geometria", 2,
                f"El área de un triángulo es {b * h // 2} cm² y su base mide {b} cm. ¿Cuánto mide su altura?",
                h,
                f"El área de un triángulo es (base x altura) / 2. Entonces: {b} x altura / 2 = {b * h // 2}. Multiplicando por 2: {b} x altura = {b*h}. La altura es {h} cm.",
                "Recuerda la fórmula: Área = (base x altura) / 2.",
                figura={"tipo": "triangulo", "base": b, "area": b * h // 2})

for i in range(10):
    L = random.randint(10, 30)
    add_problem("geometria", 3,
                f"Un cuadrado grande se divide en 4 cuadrados más pequeños e iguales. El perímetro de uno de los cuadrados pequeños es {L*4}. ¿Cuál es el área del cuadrado grande?",
                (L*2)**2,
                f"El perímetro del cuadrado pequeño es {L*4}, entonces su lado es {L}. El lado del cuadrado grande es el doble, es decir {L*2}. Su área es ({L*2}) x ({L*2}) = {(L*2)**2}.",
                "Si sabes el perímetro del cuadradito, puedes saber cuánto mide su lado.",
                figura={"tipo": "cuadrado_4", "perimetro_pequeno": L * 4})

# 4. Conteo y combinatoria (approx 35)
for i in range(15):
    c = random.randint(3, 5)
    p = random.randint(2, 4)
    z = random.randint(2, 4)
    add_problem("conteo", 1,
                f"Para vestirse, un chico tiene {c} remeras, {p} pantalones y {z} pares de zapatillas. ¿De cuántas formas distintas puede vestirse usando una prenda de cada tipo?",
                c * p * z,
                f"Por el principio de multiplicación: {c} opciones de remera x {p} opciones de pantalón x {z} opciones de zapatillas = {c * p * z} formas distintas.",
                "Multiplica las opciones de cada prenda.")

for i in range(10):
    n = random.randint(4, 10)
    add_problem("conteo", 2,
                f"En un torneo participan {n} equipos. Si todos deben jugar contra todos exactamente una vez, ¿cuántos partidos se jugarán en total?",
                n * (n - 1) // 2,
                f"Cada uno de los {n} equipos juega con los {n-1} restantes. Eso da {n * (n-1)} partidos. Pero así estamos contando cada partido dos veces (A vs B y B vs A). Dividimos por 2: {n*(n-1)//2}.",
                "Imagina que son puntos en un papel unidos por líneas. ¿Cuántas líneas hay?")

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
                "Pensá cuántas opciones quedan para cada posición, descontando los dígitos ya usados.")

# 5. Divisibilidad (approx 35)
for i in range(15):
    n1 = random.choice([2, 3, 4, 5])
    n2 = random.choice([n for n in [3, 4, 5, 7] if n != n1])
    lcm = n1 * n2 # simplified since prime/coprime usually
    add_problem("divisibilidad", 1,
                f"Dos luces parpadean: una cada {n1} segundos y otra cada {n2} segundos. Si parpadearon juntas recién, ¿en cuántos segundos volverán a parpadear juntas?",
                lcm,
                f"Buscamos el mínimo común múltiplo (MCM) entre {n1} y {n2}. Los múltiplos de {n1} son {n1}, {n1*2}, {n1*3}... El primer número común es {lcm}.",
                "Busca el Mínimo Común Múltiplo.")

for i in range(10):
    m = random.randint(2, 6)
    r = random.randint(1, m-1)
    add_problem("divisibilidad", 2,
                f"Si dividimos a un número entre {m}, el resto es {r}. ¿Cuál es el número más pequeño de dos cifras que cumple esto?",
                ((10 // m) + 1) * m + r if ((10 // m) * m + r) < 10 else ((10 // m) * m + r),
                f"Los números que al dividir por {m} dan resto {r} son de la forma {m}*k + {r}. Probamos valores de k para encontrar el primero de dos cifras.",
                "Escribe los múltiplos y súmales el resto.")

mcm_sets = [[2, 3, 5], [2, 3, 4], [3, 4, 6], [2, 5, 6], [4, 6, 9], [2, 3, 7], [3, 5, 6], [4, 5, 10]]
for i in range(10):
    nums = random.choice(mcm_sets)
    ans = lcm_list(nums)
    listed = ", ".join(str(n) for n in nums[:-1]) + " y " + str(nums[-1])
    add_problem("divisibilidad", 3,
                f"¿Cuál es el menor número (distinto de cero) que es múltiplo de {listed} al mismo tiempo?",
                ans,
                f"Buscamos el Mínimo Común Múltiplo (MCM) de {listed}. Tomando los factores necesarios para que sea divisible por todos, el MCM es {ans}.",
                "Buscá el primer número que aparezca en las tablas de todos ellos a la vez.")

# 6. Encuentra el Error (10 distintos)
error_problems = [
    (
        "Resolución: 'El perímetro de un cuadrado de área 16 cm² es 8 cm, porque 16÷2=8'. Escribí la operación correcta para encontrar el lado.",
        "raiz cuadrada",
        "Si el área es 16 cm², el lado es √16 = 4 cm (no 16÷2). El perímetro correcto es 4×4 = 16 cm.",
        "¿Cómo se calcula el lado de un cuadrado si conocés el área?"
    ),
    (
        "Resolución: 'El área de un triángulo de base 8 cm y altura 5 cm es 40 cm², porque 8×5=40'. ¿Qué operación faltó?",
        "dividir por 2",
        "El área de un triángulo es (base × altura) / 2 = (8 × 5) / 2 = 20 cm². Hay que dividir por 2.",
        "¿Cuál es la fórmula del área de un triángulo?"
    ),
    (
        "Resolución: '1/2 + 1/3 = 2/5, porque sumo los numeradores y los denominadores'. ¿Qué se necesita para sumar fracciones?",
        "denominador comun",
        "Para sumar fracciones se necesita un denominador común. 1/2 + 1/3 = 3/6 + 2/6 = 5/6.",
        "¿Podés sumar fracciones con distinto denominador directamente?"
    ),
    (
        "Resolución: '2 + 3 × 4 = 20, porque primero sumo 2+3=5 y luego 5×4=20'. ¿Qué operación tiene prioridad?",
        "multiplicacion",
        "La multiplicación va antes que la suma. Primero 3×4=12, luego 2+12=14. No 20.",
        "¿Qué operación tiene mayor prioridad según el orden de operaciones?"
    ),
    (
        "Resolución: 'El 10% de 200 es 2, porque divido 200÷100=2'. ¿Por cuánto hay que dividir para calcular el 10%?",
        "10",
        "El 10% es la décima parte: 200÷10 = 20. Dividir por 100 da el 1%, no el 10%.",
        "El 10% significa '10 de cada 100', es decir, 1 de cada 10."
    ),
    (
        "Resolución: 'El área de un cuadrado de lado 5 cm es 20 cm², porque 4×5=20'. ¿Qué calculó en realidad?",
        "perimetro",
        "4×5=20 es el perímetro, no el área. El área es lado×lado = 5×5 = 25 cm².",
        "¿Cuál es la diferencia entre área y perímetro?"
    ),
    (
        "Resolución: '1/2 × 1/3 = 1/5, porque multiplico los numeradores y sumo los denominadores'. ¿Qué se hace con los denominadores al multiplicar fracciones?",
        "multiplicar",
        "Al multiplicar fracciones se multiplican numeradores y denominadores. 1/2 × 1/3 = (1×1)/(2×3) = 1/6.",
        "¿Cómo se multiplican dos fracciones?"
    ),
    (
        "Resolución: 'Hay 3 camisetas y 2 pantalones, así que hay 5 combinaciones posibles porque 3+2=5'. ¿Cuál es la operación correcta?",
        "multiplicar",
        "Por el principio de multiplicación: 3 × 2 = 6 combinaciones. Cada camiseta se combina con cada pantalón.",
        "¿Cuántas combinaciones tiene cada camiseta con los pantalones?"
    ),
    (
        "Resolución: 'La suma de los ángulos de un triángulo es 360° como la de cualquier figura'. ¿Cuántos grados suman los ángulos de un triángulo?",
        "180",
        "Los ángulos interiores de un triángulo suman 180°. Los 360° corresponden a los cuadriláteros.",
        "¿Cuánto suman los ángulos de un triángulo?"
    ),
    (
        "Resolución: 'El MCM de 4 y 6 es 24, porque 4×6=24'. ¿Cuál es el Mínimo Común Múltiplo correcto?",
        "12",
        "El MCM de 4 y 6 es 12. Múltiplos de 4: 4,8,12... y de 6: 6,12... El primero en común es 12.",
        "Busca el primer número que sea múltiplo de ambos."
    ),
]
for q, a, expl, hint in error_problems:
    add_problem("error", 2, q, a, expl, hint)

# 7. Olímpico (approx 30) - Combina temas
for i in range(15):
    pages = random.randint(50, 150)
    add_problem("olimpico", 3,
                f"Para numerar las páginas de un libro de {pages} páginas, ¿cuántos dígitos se utilizan en total?",
                9 + (pages - 9) * 2 if pages < 100 else 9 + 90*2 + (pages - 99)*3,
                f"De la página 1 a la 9 se usan 9 dígitos. De la 10 a la {min(pages, 99)} se usan {(min(pages, 99)-9)*2} dígitos. Y si hay más de 99, las páginas de 3 cifras usan 3 dígitos cada una.",
                "Separa por cantidad de cifras: de 1 cifra, de 2 cifras, etc.")

for i in range(15):
    azules = random.randint(3, 12)
    rojas = azules + 5
    verdes = rojas - 3
    total = azules + rojas + verdes
    add_problem("olimpico", 3,
                f"En una caja hay bolitas rojas, azules y verdes. Hay 5 rojas más que azules, y 3 verdes menos que rojas. En total hay {total} bolitas. ¿Cuántas bolitas azules hay?",
                azules,
                f"Si A son las azules: R = A+5 y V = R-3 = A+2. Total: A + (A+5) + (A+2) = 3A+7 = {total}. Entonces 3A = {total-7}, A = {azules}.",
                "Usa una letra para las bolitas azules y expresa el resto en función de ellas.")

# Generate JSON
with open("problemas_nandu.json", "w", encoding="utf-8") as f:
    json.dump(problems, f, ensure_ascii=False, indent=2)

print(f"Generated {len(problems)} problems.")
