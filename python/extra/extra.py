# ================================================================
# Python AVANZADO – CONCEPTOS “EXTRA” que faltaban
# Cada bloque incluye:
#   1. ¿QUÉ es?
#   2. ¿PARA QUÉ sirve?
#   3. CÓMO funciona (con prints in-line)
# ================================================================
import gc
import secrets
import statistics
import weakref
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from functools import cached_property, total_ordering
from itertools import islice, tee
from operator import attrgetter
from typing import Any, Dict, List, NamedTuple, Tuple, TypedDict, Union

# ----------------------------------------------------------
# 41. DATA CLASSES AVANZADAS (post-init, frozen, slots)
# ----------------------------------------------------------
print("\n=== 41. DATACLASSES AVANZADAS ===")
# ¿QUÉ?  @dataclass genera __init__, __repr__, __eq__, etc.
# EXTRAS: frozen=True → inmutable, slots=True → menos RAM, post_init.

@dataclass(slots=True, frozen=True)
class Punto3D:
    x: float
    y: float
    z: float = 0.0
    norma: float = field(init=False)

    def __post_init__(self):
        # A pesar de frozen=True, podemos modificar vía object.__setattr__
        super().__setattr__('norma', (self.x**2 + self.y**2 + self.z**2)**0.5)

p = Punto3D(3, 4, 12)
print("  Punto:", p, "norma:", p.norma)

# ----------------------------------------------------------
# 42. TYPEDDICT vs NAMEDTUPLE vs @dataclass(slots=True)
# ----------------------------------------------------------
print("\n=== 42. TYPEDDICT & NAMEDTUPLE ===")

class ConfigDict(TypedDict, total=False):
    host: str
    port: int
    debug: bool

config: ConfigDict = {"host": "0.0.0.0", "port": 8000}

class Coord(NamedTuple):
    lat: float
    lon: float

c = Coord(40.4, -3.7)
print("  TypedDict:", config, "NamedTuple:", c)

# ----------------------------------------------------------
# 43. CACHED_PROPERTY – cálculo on-demand y caché
# ----------------------------------------------------------
print("\n=== 43. CACHED_PROPERTY ===")

class Circulo:
    def __init__(self, r):
        self.r = r

    @cached_property
    def area(self):
        print("  (Calculando área...)")
        return 3.1416 * self.r ** 2

circle = Circulo(10)
print("  Área 1ª:", circle.area)
print("  Área 2ª (cached):", circle.area)  # No recalcula

# ----------------------------------------------------------
# 44. WEAKREF – referencias débiles para evitar leaks
# ----------------------------------------------------------
print("\n=== 44. WEAKREF ===")

class BigObject:
    def __del__(self):
        print("    BigObject borrado")

obj = BigObject()
wref = weakref.ref(obj)
print("  Referencia débil existe:", wref() is obj)
del obj
gc.collect()  # fuerza recolección
print("  ¿Aún existe?:", wref() is None)

# ----------------------------------------------------------
# 45. SECRETS – generación criptográficamente segura
# ----------------------------------------------------------
print("\n=== 45. SECRETS ===")

token = secrets.token_urlsafe(32)
pwd = ''.join(secrets.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(12))
print("  Token seguro:", token)
print("  Contraseña aleatoria:", pwd)

# ----------------------------------------------------------
# 46. STATISTICS – funciones rápidas de estadística
# ----------------------------------------------------------
print("\n=== 46. STATISTICS ===")

data = [2.75, 1.75, 1.25, 0.25, 0.5, 1.25, 3.5]
print("  Media:", statistics.mean(data))
print("  Mediana:", statistics.median(data))
print("  Desv. estándar:", statistics.stdev(data))

# ----------------------------------------------------------
# 47. TOTAL_ORDERING – generar comparaciones automáticamente
# ----------------------------------------------------------
print("\n=== 47. TOTAL_ORDERING ===")

@total_ordering
class Version:
    def __init__(self, major, minor=0, patch=0):
        self.major, self.minor, self.patch = major, minor, patch

    def __eq__(self, other):
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other):
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

v1, v2 = Version(1, 9), Version(1, 10)
print("  v1 < v2:", v1 < v2, "v1 <= v2:", v1 <= v2, "v1 == v2:", v1 == v2)

# ----------------------------------------------------------
# 48. ISLICE & TEE – cortar y duplicar iteradores sin gastar RAM
# ----------------------------------------------------------
print("\n=== 48. ISLICE & TEE ===")

def naturals():
    n = 0
    while True:
        yield n
        n += 1

# tomar solo 5 elementos sin lista intermedia
primeros = list(islice(naturals(), 5))
print("  Primeros 5 naturales:", primeros)

# duplicar iterador
it1, it2 = tee(naturals(), 2)
print("  it1[0:3]:", list(islice(it1, 3)), "it2[0:3]:", list(islice(it2, 3)))

# ----------------------------------------------------------
# 49. PARTIAL & ATTRGETTER – funciones pre-configuradas
# ----------------------------------------------------------
print("\n=== 49. PARTIAL & ATTRGETTER ===")

base_url = "https://api.example.com/v1"
get_users = partial(f"{base_url}/users".format)  # currying
print("  URL users:", get_users())

usuarios = [
    {"nombre": "Ana", "puntos": 120},
    {"nombre": "Luis", "puntos": 95},
]
# Ordenar por "puntos" sin lambda
usuarios.sort(key=attrgetter("puntos"), reverse=True)
print("  Ranking:", usuarios)

# ----------------------------------------------------------
# 50. MULTIPROCESSING con POOL + MAP CHUNKED
# ----------------------------------------------------------
print("\n=== 50. MULTIPROCESSING CHUNKED ===")

def heavy(n):
    return sum(i * i for i in range(n))

if __name__ == "__main__":  # Necesario en Windows
    with ProcessPoolExecutor() as ex:
        grandes = [500_000] * 4
        # chunksize automático
        resultados = list(ex.map(heavy, grandes))
    print("  Resultados:", resultados)

# ----------------------------------------------------------
# 51. GC (GARBAGE COLLECTOR) – inspección manual
# ----------------------------------------------------------
print("\n=== 51. GARBAGE COLLECTOR ===")

class Nodo:
    def __init__(self, val, next=None):
        self.val, self.next = val, next

a = Nodo(1)
b = Nodo(2)
a.next, b.next = b, a  # ciclo
del a, b
print("  Objetos inalcanzables antes de GC:", gc.collect())
print("  Generaciones:", gc.get_count())

# ----------------------------------------------------------
# 52. MATCH-CASE (Python 3.10+) – pattern matching
# ----------------------------------------------------------
print("\n=== 52. MATCH-CASE ===")

def procesar(data):
    match data:
        case {"type": "point", "x": x, "y": y}:
            return f"Punto({x},{y})"
        case [x, y, *_]:
            return f"Lista empieza por {x},{y}"
        case str(s) if len(s) < 5:
            return f"String corto: {s}"
        case _:
            return "Sin coincidencia"

print("  procesar({'type':'point','x':1,'y':2}):", procesar({"type": "point", "x": 1, "y": 2}))
print("  procesar([10,20,30]):", procesar([10, 20, 30]))
print("  procesar('Hi'):", procesar("Hi"))

# ----------------------------------------------------------
# 53. FUNCTOOLS.REDUCE – reducir iterable a valor único
# ----------------------------------------------------------
print("\n=== 53. REDUCE ===")

from functools import reduce
# Producto de lista
producto = reduce(operator.mul, [1, 2, 3, 4, 5], 1)
print("  Producto de lista:", producto)

# ----------------------------------------------------------
# 54. ANY/ALL con short-circuit
# ----------------------------------------------------------
print("\n=== 54. ANY/ALL ===")

print("  ¿Hay algún par?:", any(n % 2 == 0 for n in [1, 3, 5, 7, 8]))
print("  ¿Todos positivos?:", all(n > 0 for n in [1, 2, 3]))

# ----------------------------------------------------------
# 55. VALORES POR DEFECTO MUTABLES – trampa y solución
# ----------------------------------------------------------
print("\n=== 55. TRAMPA DE MUTABLES ===")

def mal(a: List[int] = []):  # NO HAGAS ESTO
    a.append(1)
    return a

def bien(a: Optional[List[int]] = None):
    if a is None:
        a = []
    a.append(1)
    return a

print("  Mal después de 3 llamadas:", mal(), mal(), mal())
print("  Bien después de 3 llamadas:", bien(), bien(), bien())

# ----------------------------------------------------------
# 56. OPERADOR WALRUS := – asignación en expresión (3.8+)
# ----------------------------------------------------------
print("\n=== 56. WALRUS OPERATOR ===")

lineas = ["  hola", "", "  mundo"]
while (l := lineas.pop(0)) != "":
    print("  No vacía:", l)

# ----------------------------------------------------------
# 57. ZIP con *strict=True (3.10+) – detectar longitudes distintas
# ----------------------------------------------------------
print("\n=== 57. ZIP STRICT ===")

try:
    for a, b in zip([1, 2, 3], [10, 20], strict=True):
        print(a, b)
except ValueError as e:
    print("  Error zip strict:", e)

# ----------------------------------------------------------
# 58. ENUMERATE con START
# ----------------------------------------------------------
print("\n=== 58. ENUMERATE START ===")

for idx, nombre in enumerate(["Ana", "Luis", "Carlos"], start=1):
    print(f"  {idx}. {nombre}")

# ----------------------------------------------------------
# 59. DEQUE – cola de doble extremo rápida
# ----------------------------------------------------------
print("\n=== 59. DEQUE ===")

q = deque(maxlen=3)
for i in range(5):
    q.append(i)
    print("  Estado deque:", list(q))

# ----------------------------------------------------------
# 60. CIERRE FINAL
# ----------------------------------------------------------
if __name__ == "__main__":
    print("\n🚀 ¡Extras ejecutados! Combínalos con los bloques anteriores.")