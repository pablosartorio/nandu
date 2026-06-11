"""Verificador del banco de problemas (problemas_nandu.json).

Para cada plantilla generadora, RECALCULA la respuesta a partir del enunciado
(con un método independiente, p.ej. fuerza bruta) y la compara con la
respuesta guardada. Así, un enunciado que no coincide con su respuesta —el
bug histórico del banco— rompe el build en lugar de llegar al alumno.

Uso:  python3 test_banco.py   (sale con código != 0 si hay fallas)
"""
import json
import re
import sys
from itertools import permutations
from math import gcd

CATEGORIAS = {"patrones", "logica", "geometria", "conteo", "divisibilidad", "error", "olimpico"}
FIGURAS = {"rect_dos_cuadrados", "triangulo", "cuadrado_4"}
PATAS = {"gallinas": 2, "conejos": 4, "patos": 2, "vacas": 4, "triciclos": 3, "bicicletas": 2}

fallas = []


def falla(p, msg):
    fallas.append(f"id {p['id']} ({p['template']}): {msg}")


def nums(texto):
    return [int(n) for n in re.findall(r"\d+", texto)]


def lcm_list(valores):
    r = 1
    for n in valores:
        r = r * n // gcd(r, n)
    return r


# --- Recálculo por plantilla: enunciado -> respuesta esperada ---

def rc_patrones_aritmetica(p):
    seq = nums(p["enunciado"])[:5]
    pasos = {b - a for a, b in zip(seq, seq[1:])}
    assert len(pasos) == 1, f"la secuencia {seq} no tiene paso constante"
    return seq[-1] + pasos.pop()


def rc_patrones_geometrica(p):
    seq = nums(p["enunciado"])[:4]
    assert all(b % a == 0 for a, b in zip(seq, seq[1:])), f"{seq} no es geométrica"
    razones = {b // a for a, b in zip(seq, seq[1:])}
    assert len(razones) == 1, f"la secuencia {seq} no tiene razón constante"
    return seq[-1] * razones.pop()


def rc_patrones_dif_creciente(p):
    seq = nums(p["enunciado"])[:5]
    difs = [b - a for a, b in zip(seq, seq[1:])]
    assert difs == list(range(difs[0], difs[0] + 4)), f"las diferencias {difs} no crecen de a 1"
    return seq[-1] + difs[-1] + 1


def rc_logica_edades(p):
    suma, dif = nums(p["enunciado"])[:2]
    assert (suma + dif) % 2 == 0, "suma+diferencia impar: la edad no es entera"
    return (suma + dif) // 2


def rc_logica_partes(p):
    total = nums(p["enunciado"])[0]
    assert total % 4 == 0, f"el total {total} no se divide en 4 partes"
    return total // 2  # A se lleva 2 de las 4 partes


def rc_logica_patas(p):
    m = re.search(r"hay (\w+) y (\w+)\.", p["enunciado"])
    p1, p2 = PATAS[m.group(1)], PATAS[m.group(2)]
    cabezas, patas = nums(p["enunciado"])[:2]
    resto = patas - cabezas * p1
    assert resto % (p2 - p1) == 0, "la cuenta de patas no da entera"
    return resto // (p2 - p1)


def rc_geo_dos_cuadrados(p):
    return 6 * nums(p["enunciado"])[0]


def rc_geo_triangulo_altura(p):
    area, base = nums(p["enunciado"])[:2]
    assert (2 * area) % base == 0, "la altura no es entera"
    return 2 * area // base


def rc_geo_cuadrado_4(p):
    perimetro = nums(p["enunciado"])[-1]  # el primer número del texto es el "4 cuadrados"
    assert perimetro % 4 == 0, "el perímetro no es múltiplo de 4"
    return (2 * (perimetro // 4)) ** 2


def rc_conteo_vestimenta(p):
    c, pant, z = nums(p["enunciado"])[:3]
    return c * pant * z


def rc_conteo_torneo(p):
    n = nums(p["enunciado"])[0]
    return n * (n - 1) // 2


def rc_conteo_cifras(p):
    valores = nums(p["enunciado"])
    L, digitos = valores[0], valores[1:]
    assert len(set(digitos)) == len(digitos), "dígitos repetidos en el enunciado"
    # Fuerza bruta: contamos las variaciones reales.
    return sum(1 for _ in permutations(digitos, L))


def rc_div_mcm2(p):
    n1, n2 = nums(p["enunciado"])[:2]
    return lcm_list([n1, n2])


def rc_div_resto(p):
    m, r = nums(p["enunciado"])[:2]
    return next(x for x in range(10, 100) if x % m == r)


def rc_div_mcm3(p):
    return lcm_list(nums(p["enunciado"]))


def rc_olimpico_paginas(p):
    paginas = nums(p["enunciado"])[0]
    return sum(len(str(i)) for i in range(1, paginas + 1))


def rc_olimpico_bolitas(p):
    total = nums(p["enunciado"])[-1]
    # Fuerza bruta sobre las azules: R = A+5, V = R-3.
    return next(a for a in range(0, total + 1) if a + (a + 5) + (a + 2) == total)


RECALCULOS = {
    "patrones_aritmetica": rc_patrones_aritmetica,
    "patrones_geometrica": rc_patrones_geometrica,
    "patrones_dif_creciente": rc_patrones_dif_creciente,
    "logica_edades": rc_logica_edades,
    "logica_partes": rc_logica_partes,
    "logica_patas": rc_logica_patas,
    "geo_dos_cuadrados": rc_geo_dos_cuadrados,
    "geo_triangulo_altura": rc_geo_triangulo_altura,
    "geo_cuadrado_4": rc_geo_cuadrado_4,
    "conteo_vestimenta": rc_conteo_vestimenta,
    "conteo_torneo": rc_conteo_torneo,
    "conteo_cifras": rc_conteo_cifras,
    "div_mcm2": rc_div_mcm2,
    "div_resto": rc_div_resto,
    "div_mcm3": rc_div_mcm3,
    "olimpico_paginas": rc_olimpico_paginas,
    "olimpico_bolitas": rc_olimpico_bolitas,
}

# --- Recálculo independiente de los problemas manuales (por fragmento único
# del enunciado). Si se agrega un problema manual, agregar acá su control. ---

def caracol():
    altura, dia = 0, 0
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    while True:
        altura += 5
        if altura >= 16:
            return dias[dia % 7]
        altura -= 3
        dia += 1


def fibonacci_decimo():
    a, b = 1, 1
    for _ in range(8):
        a, b = b, a + b
    return b


def mago():
    monedas = 5
    for _ in range(3):  # lun->mar, mar->mié, mié->jue
        monedas = monedas * 2 - 2
    return monedas


def carrera():
    for orden in permutations(["Ana", "Bruno", "Carla"]):
        ana_no_ultima = orden[-1] != "Ana"
        carla_tras_ana = orden.index("Carla") == orden.index("Ana") + 1
        bruno_no_gano = orden[0] != "Bruno"
        if ana_no_ultima and carla_tras_ana and bruno_no_gano:
            return orden[0]


MANUALES_ESPERADOS = {
    "7 mesas en hilera": 6 + 4 * 6,
    "décimo número": fibonacci_decimo(),
    "jueves a la mañana": mago(),
    "guarda de 12 cuadrados": 4 + 3 * 11,
    "¿Quién ganó la carrera?": carrera(),
    "30 frutas": next(n for n in range(31) if n + (n + 8) == 30),
    "¿Cuántos caramelos tiene Sofía?": next(3 * v for v in range(55) if v + 3 * v + v + 4 == 54),
    "¿qué día llega a la punta?": caracol(),
    "¿Cuántos centímetros mide la base?": next(2 * h for h in range(37) if 2 * (h + 2 * h) == 36),
    "¿Cuántas baldosas se necesitan?": (200 // 20) * (300 // 20),
    "se le recorta, en cada esquina": 4 * 12,  # recortar esquinas no cambia el perímetro
    "¿Cuál es el área del cuadrado?": ((2 * (14 + 6)) // 4) ** 2,
    "sus dos cifras iguales": sum(1 for n in range(10, 100) if n // 10 == n % 10),
    "¿Cuántos helados diferentes": 2 * sum(1 for i in range(4) for j in range(i + 1, 4)),
    "Fede no quiere sentarse en el medio": sum(
        1 for orden in permutations(["F", "G", "H"]) if orden[1] != "F"),
    "al menos un dígito 7": sum(1 for n in range(1, 101) if "7" in str(n)),
    "¿Cuántas figuritas tiene?": next(
        n for n in range(30, 41) if n % 5 == 0 and n % 4 == 3),
    "menor número de tres cifras que es divisible por 2, por 3 y por 5": next(
        n for n in range(100, 1000) if n % 2 == 0 and n % 3 == 0 and n % 5 == 0),
    "¿A qué hora vuelven a salir los tres juntos?": f"{8 + lcm_list([12, 15, 20]) // 60}:00",
    "decenas es el doble": next(
        n for n in range(10, 100) if n % 9 == 0 and n // 10 == 2 * (n % 10)),
    "¿Cuánto cuesta un alfajor?": next(
        2 * c for c in range(1051) if 2 * (2 * c) + 3 * c == 1050),
    "¿Cuántas veces escribe el dígito 4?": sum(str(i).count("4") for i in range(1, 51)),
    "¿Cuántas carpas de 3 personas hay?": next(
        t for t in range(14) if 3 * t + 2 * (13 - t) == 31),
    "página de la derecha": next(n + 1 for n in range(1, 145) if n + (n + 1) == 145),
}


def main():
    with open("problemas_nandu.json", encoding="utf-8") as f:
        problemas = json.load(f)

    # --- Invariantes globales ---
    ids = [p["id"] for p in problemas]
    if ids != list(range(1, len(problemas) + 1)):
        fallas.append("los ids no son únicos y consecutivos desde 1")
    enunciados = [p["enunciado"] for p in problemas]
    if len(set(enunciados)) != len(enunciados):
        fallas.append("hay enunciados duplicados")

    recalculados = 0
    manuales_controlados = set()
    for p in problemas:
        if p["categoria"] not in CATEGORIAS:
            falla(p, f"categoría desconocida: {p['categoria']}")
        if p["dificultad"] not in (1, 2, 3):
            falla(p, f"dificultad inválida: {p['dificultad']}")
        for campo in ("enunciado", "respuesta", "explicacion", "pista"):
            if not str(p.get(campo, "")).strip():
                falla(p, f"campo vacío: {campo}")
        if "figura" in p:
            if p["categoria"] != "geometria":
                falla(p, "figura en un problema que no es de geometría")
            if p["figura"].get("tipo") not in FIGURAS:
                falla(p, f"tipo de figura desconocido: {p['figura'].get('tipo')}")
        if "opciones" in p:
            ops = p["opciones"]
            if len(ops) != len(set(ops)) or len(ops) < 3:
                falla(p, "opciones repetidas o insuficientes")
            if p["respuesta"] not in ops:
                falla(p, "la respuesta no figura entre las opciones")

        # --- Recálculo de la respuesta ---
        template = p.get("template")
        if template in RECALCULOS:
            try:
                esperado = RECALCULOS[template](p)
            except (AssertionError, StopIteration, AttributeError, KeyError) as e:
                falla(p, f"no se pudo recalcular: {e}")
                continue
            if str(esperado) != p["respuesta"]:
                falla(p, f"respuesta {p['respuesta']!r} != recalculada {esperado!r} | {p['enunciado'][:70]}")
            recalculados += 1
        elif template == "manual":
            coincidencias = [k for k in MANUALES_ESPERADOS if k in p["enunciado"]]
            if len(coincidencias) != 1:
                falla(p, f"problema manual sin control único en MANUALES_ESPERADOS ({coincidencias})")
                continue
            clave = coincidencias[0]
            manuales_controlados.add(clave)
            esperado = MANUALES_ESPERADOS[clave]
            if str(esperado).lower() != p["respuesta"].lower():
                falla(p, f"respuesta {p['respuesta']!r} != recalculada {esperado!r}")
            recalculados += 1
        elif template == "error_manual":
            if "opciones" not in p:
                falla(p, "problema de 'Encuentra el Error' sin opciones")
        else:
            falla(p, f"template desconocido: {template}")

    sin_control = set(MANUALES_ESPERADOS) - manuales_controlados
    if sin_control:
        fallas.append(f"controles manuales sin problema asociado: {sorted(sin_control)}")

    print(f"{len(problemas)} problemas | {recalculados} respuestas recalculadas desde el enunciado")
    if fallas:
        print(f"\n{len(fallas)} FALLAS:")
        for f_ in fallas:
            print(" -", f_)
        sys.exit(1)
    print("BANCO OK")


if __name__ == "__main__":
    main()
