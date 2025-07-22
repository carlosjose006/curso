# ==========================================================
# Python intermedio – EXPLICACIÓN LÍNEA A LÍNEA
# Cada bloque incluye:
#   1. ¿QUÉ es?
#   2. ¿PARA QUÉ sirve?
#   3. CÓMO funciona (con prints in-line)
# ==========================================================

# ----------------------------------------------------------
# 9. COMPREHENSIONS
# ----------------------------------------------------------
print("\n=== 9. COMPREHENSIONS ===")
# ¿QUÉ?  Forma concisa de crear listas, conjuntos o diccionarios
# ¿PARA QUÉ?  Reemplaza bucles largos y mejora la legibilidad

# LIST comprehension
cuadrados = [x**2 for x in range(5)]
print("Lista de cuadrados:", cuadrados)        # [0, 1, 4, 9, 16]

# SET comprehension  (elementos únicos)
vocales = {c for c in "murcielago" if c in "aeiou"}
print("Vocales únicas en 'murcielago':", vocales)

# DICT comprehension
iniciales = {fruta: fruta[0] for fruta in ["manzana", "banana"]}
print("Iniciales:", iniciales)                 # {'manzana': 'm', 'banana': 'b'}

# ----------------------------------------------------------
# 10. FUNCIONES AVANZADAS
# ----------------------------------------------------------
print("\n=== 10. FUNCIONES AVANZADAS ===")
# *args   → lista de argumentos posicionales ilimitados
# **kwargs → diccionario de argumentos nominales ilimitados

def registrar(*args, **kwargs):
    print("  Posicionales (tupla):", args)
    print("  Nominales  (dict) :", kwargs)

registrar(1, 2, 3, nombre="Guao", edad=25)

# Lambda (función anónima de una sola expresión)
usuarios = [{"nombre": "Ana", "edad": 30},
            {"nombre": "Luis", "edad": 22}]
ordenados = sorted(usuarios, key=lambda u: u["edad"])
print("Usuarios ordenados por edad:", *ordenados, sep="\n  ")

# ----------------------------------------------------------
# 11. CLASES Y OBJETOS
# ----------------------------------------------------------
print("\n=== 11. CLASES Y OBJETOS ===")
# __init__ : constructor
# self     : referencia al objeto actual
# @classmethod : método que recibe la clase, no la instancia

class Mascota:
    _registro = []                 # variable de clase compartida

    def __init__(self, nombre, especie):
        self.nombre = nombre
        self.especie = especie
        Mascota._registro.append(self)

    def __str__(self):             # representación legible
        return f"{self.nombre} ({self.especie})"

    @classmethod
    def cantidad(cls):
        return len(cls._registro)  # accede a la var. de clase

perro = Mascota("Toby", "perro")
gato  = Mascota("Michi", "gato")
print("  Mascotas creadas:", Mascota.cantidad())
print("  Lista:", [str(m) for m in Mascota._registro])

# ----------------------------------------------------------
# 12. HERENCIA Y POLIMORFISMO
# ----------------------------------------------------------
print("\n=== 12. HERENCIA Y POLIMORFISMO ===")
# Herencia → reutilizar código
# Polimorfismo → mismo método, distinto resultado según objeto

class Animal:
    def hablar(self):
        raise NotImplementedError("Subclase debe implementar")

class Perro(Animal):
    def hablar(self):
        return "Guau!"

class Gato(Animal):
    def hablar(self):
        return "Miau!"

zoo = [Perro(), Gato()]
for animal in zoo:
    print("  ", type(animal).__name__, "dice:", animal.hablar())

# ----------------------------------------------------------
# 13. MÓDULOS E IMPORTS
# ----------------------------------------------------------
print("\n=== 13. MÓDULOS E IMPORTS ===")
# Módulo = archivo .py con funciones/clases
# Se puede importar todo, con alias o solo lo que necesites

import math
import random as rd
from datetime import datetime

print("  √16 =", math.sqrt(16))
print("  Aleatorio 1-10:", rd.randint(1, 10))
print("  Hora actual:", datetime.now().strftime("%H:%M:%S"))

# ----------------------------------------------------------
# 14. MANEJO DE ARCHIVOS
# ----------------------------------------------------------
print("\n=== 14. MANEJO DE ARCHIVOS ===")
# with abre y cierra el archivo automáticamente (mejor práctica)

archivo = "datos.txt"
with open(archivo, "w", encoding="utf-8") as f:
    f.write("Primera línea\nSegunda línea\n")

with open(archivo, encoding="utf-8") as f:
    print("  Contenido del archivo:")
    print("   ", f.read().replace("\n", "\n    "))

# ----------------------------------------------------------
# 15. EXCEPCIONES PERSONALIZADAS
# ----------------------------------------------------------
print("\n=== 15. EXCEPCIONES PERSONALIZADAS ===")
# Crear tu propio tipo de error heredando de Exception/ValueError

class EdadNegativaError(ValueError):
    pass

def set_edad(e):
    if e < 0:
        raise EdadNegativaError("Edad negativa no tiene sentido")
    return e

try:
    set_edad(-5)
except EdadNegativaError as exc:
    print("  Capturado:", exc)

# ----------------------------------------------------------
# 16. GENERADORES (ITERADORES PEREZOSOS)
# ----------------------------------------------------------
print("\n=== 16. GENERADORES ===")
# yield retorna un valor y pausa la función; se reanuda en la siguiente llamada

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a            # devuelve y suspende
        a, b = b, a + b

print("  Primeros 6 Fibonacci:", list(fibonacci(6)))

# ----------------------------------------------------------
# 17. DECORADORES
# ----------------------------------------------------------
print("\n=== 17. DECORADORES ===")
# Función que recibe otra función y le añade comportamiento sin modificarla

from time import perf_counter, sleep

def medir(func):
    def envoltura(*args, **kwargs):
        t0 = perf_counter()
        resultado = func(*args, **kwargs)
        print(f"  {func.__name__} tardó {perf_counter()-t0:.6f}s")
        return resultado
    return envoltura

@medir
def pausa(seg):
    sleep(seg)

pausa(0.25)

# ----------------------------------------------------------
# 18. ENUMERACIONES Y DATACLASSES
# ----------------------------------------------------------
print("\n=== 18. ENUM & DATACLASS ===")
# Enum → conjunto de constantes con nombre
# dataclass → genera __init__, __repr__, __eq__, etc. automáticamente

from enum import Enum
from dataclasses import dataclass

class Estado(Enum):
    PENDIENTE = 1
    EN_CURSO = 2
    COMPLETADO = 3

@dataclass
class Tarea:
    titulo: str
    estado: Estado = Estado.PENDIENTE

t = Tarea("Aprender Python intermedio")
print("  Tarea nueva:", t)
t.estado = Estado.COMPLETADO
print("  Tarea finalizada:", t)

# ----------------------------------------------------------
# 19. PRUEBAS RÁPIDAS CON ASSERT
# ----------------------------------------------------------
print("\n=== 19. ASSERT ===")
# assert condición, mensaje  → lanza AssertionError si la condición es False

def area_circulo(r):
    import math
    return math.pi * r ** 2

assert abs(area_circulo(1) - math.pi) < 1e-10
print("  ✓ Prueba de área pasó")

# ----------------------------------------------------------
# 20. BLOQUE __main__ (PUNTO DE ENTRADA)
# ----------------------------------------------------------
print("\n=== 20. __name__ ===")
# Este bloque solo se ejecuta cuando el archivo corre como script,
# NO cuando se importa.

if __name__ == "__main__":
    print("  Este archivo se ejecutó directamente. ¡Fin del tour!")

# ==========================================================
# Ejecuta este archivo y observa la salida paso a paso.
# ==========================================================