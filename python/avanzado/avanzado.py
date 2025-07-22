# ================================================================
# Python AVANZADO en un solo script
# Cada bloque incluye:
#   1. ¿QUÉ es?
#   2. ¿PARA QUÉ sirve?
#   3. CÓMO funciona (con prints in-line)
#   4. CÓDIGO EJECUTABLE paso a paso
# ================================================================
from __future__ import annotations   # ❶ Postponed evaluation (PEP-563)
import asyncio
import concurrent.futures as cf
import functools
import itertools
import json
import logging
import multiprocessing as mp
import operator
import os
import pathlib
import pickle
import re
import sqlite3
import subprocess
import sys
import threading
import time
import typing
from collections import Counter, defaultdict, deque, namedtuple
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from functools import lru_cache, partial, singledispatch, wraps
from pathlib import Path
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Protocol,
    TypeVar,
    runtime_checkable,
)

# ----------------------------------------------------------
# 21. METACLASES – Crear clases “a la carta”
# ----------------------------------------------------------
print("\n=== 21. METACLASES ===")
# ¿QUÉ?  Clase cuya instancia es una clase (control total en la creación).
# ¿PARA QUÉ?  Registro automático, validación, ORM, singletons…

class AutoRegistro(type):
    registro: Dict[str, type] = {}

    def __new__(mcls, name, bases, ns):
        cls = super().__new__(mcls, name, bases, ns)
        mcls.registro[name.lower()] = cls
        return cls

class BaseModel(metaclass=AutoRegistro):
    pass

class Usuario(BaseModel):
    pass

print("  Registro de clases:", AutoRegistro.registro)

# ----------------------------------------------------------
# 22. DESCRIPTORS – Atributos con lógica
# ----------------------------------------------------------
print("\n=== 22. DESCRIPTORS ===")
# ¿QUÉ?  Clase con __get__, __set__, __delete__ que gestiona un atributo.
# ¿PARA QUÉ?  Validaciones, caché, lazy-load, ORM fields.

class Positivo:
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError("debe ser > 0")
        obj.__dict__[self.name] = value

class Producto:
    precio = Positivo("precio")

p = Producto()
p.precio = 10
print("  Precio:", p.precio)
try:
    p.precio = -5
except ValueError as e:
    print("  Error descriptor:", e)

# ----------------------------------------------------------
# 23. DECORADORES AVANZADOS (clases, parámetros, stacking)
# ----------------------------------------------------------
print("\n=== 23. DECORADORES AVANZADOS ===")
# Decorador con argumentos: necesita 3 niveles de anidación.

def repetir(n: int):
    def decorador(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def envoltura(*args, **kwargs):
            for i in range(n):
                print(f"  Rep {i+1}/{n}", end=" → ")
                func(*args, **kwargs)
        return envoltura
    return decorador

@repetir(3)
def hola():
    print("¡Hola!")

hola()

# ----------------------------------------------------------
# 24. SINGLE DISPATCH – Polimorfismo ad-hoc
# ----------------------------------------------------------
print("\n=== 24. SINGLE DISPATCH ===")
# ¿QUÉ?  Función genérica que cambia de comportamiento según tipo.

@singledispatch
def serializar(obj):
    return json.dumps(obj)

@serializar.register
def _(obj: dict):
    return json.dumps(obj, sort_keys=True)

@serializar.register
def _(obj: set):
    return json.dumps(list(obj))

print("  str:", serializar("abc"))
print("  dict:", serializar({"z": 1, "a": 2}))
print("  set:", serializar({3, 1, 2}))

# ----------------------------------------------------------
# 25. TYPING AVANZADO – Protocols, generics, bounded types
# ----------------------------------------------------------
print("\n=== 25. TYPING AVANZADO ===")
T = TypeVar("T", bound=float | int)

class Sumable(Protocol):
    def __add__(self, other: typing.Self) -> typing.Self: ...

def suma_generica(a: T, b: T) -> T:
    return a + b  # type: ignore

print("  1.2 + 2.3 (float) =", suma_generica(1.2, 2.3))

# ----------------------------------------------------------
# 26. ASYNC / AWAIT – Concurrencia cooperativa
# ----------------------------------------------------------
print("\n=== 26. ASYNC/AWAIT ===")

async def tarea(n: int) -> str:
    await asyncio.sleep(n)
    return f"Tarea {n}s finalizada"

async def main_async():
    resultados = await asyncio.gather(tarea(1), tarea(2))
    print("  Async resultados:", resultados)

asyncio.run(main_async())

# ----------------------------------------------------------
# 27. THREADING vs MULTIPROCESSING
# ----------------------------------------------------------
print("\n=== 27. PARALELISMO REAL vs CONCURRENCIA ===")

def cpu_bound(n):
    return sum(i * i for i in range(n))

# 27a. Multiprocessing (aprovecha múltiples núcleos)
if __name__ == "__main__":
    with mp.Pool() as pool:
        print("  Multiprocessing:", pool.map(cpu_bound, [10_000, 20_000]))

# 27b. Threading (I/O bound)
def io_bound():
    time.sleep(0.2)
    return "I/O ok"

with cf.ThreadPoolExecutor() as ex:
    futuros = [ex.submit(io_bound) for _ in range(3)]
    print("  Threading:", [f.result() for f in futuros])

# ----------------------------------------------------------
# 28. CONTEXT MANAGERS PERSONALIZADOS
# ----------------------------------------------------------
print("\n=== 28. CONTEXT MANAGERS ===")

@contextmanager
def cronometro():
    t0 = time.perf_counter()
    yield
    print(f"  Tiempo: {time.perf_counter() - t0:.4f}s")

with cronometro():
    time.sleep(0.1)

# ----------------------------------------------------------
# 29. CONTEXTOS ASÍNCRONOS
# ----------------------------------------------------------
print("\n=== 29. ASYNC CONTEXT MANAGER ===")

@asynccontextmanager
async def db_con():
    print("  Conectando DB...")
    yield "conexión"
    print("  Cerrando DB...")

async def usar_db():
    async with db_con() as conn:
        print("  Usando", conn)

asyncio.run(usar_db())

# ----------------------------------------------------------
# 30. C EXTENSIONS – Cython, ctypes, cffi (demo conceptual)
# ----------------------------------------------------------
print("\n=== 30. C EXTENSIONS (simulado) ===")
# En la práctica usarías Cython o escribirías un .c/.cpp y lo compilas.
# Aquí usamos subprocess para compilar y ejecutar un módulo C toy.

c_code = """
#include <Python.h>
static PyObject* suma_c(PyObject* self, PyObject* args){
    long a, b;
    if(!PyArg_ParseTuple(args, "ll", &a, &b)) return NULL;
    return PyLong_FromLong(a + b);
}
static PyMethodDef methods[] = {
    {"suma", suma_c, METH_VARARGS, "Suma en C"},
    {NULL, NULL, 0, NULL}
};
static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT, "ext", NULL, -1, methods
};
PyMODINIT_FUNC PyInit_ext(void){ return PyModule_Create(&module); }
"""

with open("ext.c", "w") as f:
    f.write(c_code)

# Compilar (requiere compilador y python-dev)
try:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", ".", "--quiet"],
        cwd=Path.cwd(),
        check=True,
        capture_output=True,
    )
except Exception:
    print("  Compilación C omitida (necesitas setuptools y compilador).")

# ----------------------------------------------------------
# 31. OPTIMIZACIONES – LRU CACHE & JIT
# ----------------------------------------------------------
print("\n=== 31. LRU CACHE & NUMBA (simulado) ===")

@lru_cache(maxsize=None)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print("  Fib 30 cached:", fib(30))

# ----------------------------------------------------------
# 32. SERIALIZACIÓN AVANZADA – Pickle, JSON, ORJSON
# ----------------------------------------------------------
print("\n=== 32. SERIALIZACIÓN ===")

class Punto:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __reduce__(self):
        return (self.__class__, (self.x, self.y))

p = Punto(3, 4)
data = pickle.dumps(p)
p2 = pickle.loads(data)
print("  Pickle Punto:", p2.x, p2.y)

# ----------------------------------------------------------
# 33. PATRONES DE DISEÑO – Lazy Singleton, Factory, Observer
# ----------------------------------------------------------
print("\n=== 33. PATRONES ===")

class SingletonMeta(type):
    _instancias: dict[type, Any] = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            cls._instancias[cls] = super().__call__(*args, **kwargs)
        return cls._instancias[cls]

class Config(metaclass=SingletonMeta):
    def __init__(self):
        self.debug = True

c1 = Config()
c2 = Config()
print("  Misma instancia:", c1 is c2, c1.debug)

# ----------------------------------------------------------
# 34. TESTING – unittest & pytest estilo
# ----------------------------------------------------------
print("\n=== 34. TESTING ===")

def add(a: int, b: int) -> int:
    return a + b

# Test simple sin frameworks
assert add(2, 3) == 5
print("  ✓ Test unitario básico pasó")

# ----------------------------------------------------------
# 35. PROFILE & OPTIMIZACIÓN – cProfile & line_profiler
# ----------------------------------------------------------
print("\n=== 35. PROFILING ===")

import cProfile
import pstats
from io import StringIO

pr = cProfile.Profile()
pr.enable()
_ = [cpu_bound(5000) for _ in range(100)]
pr.disable()
s = StringIO()
pstats.Stats(pr, stream=s).strip_dirs().sort_stats("cumulative").print_stats(3)
print("  Top funciones CPU:", s.getvalue().splitlines()[4:7])

# ----------------------------------------------------------
# 36. PAQUETES & PUBLICACIÓN – pyproject.toml
# ----------------------------------------------------------
print("\n=== 36. EMPAQUETADO ===")
# pyproject.toml (mínimo)
toml = """
[build-system]
requires = ["setuptools>=61", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mipkg"
version = "0.1.0"
description = "Demo avanzada"
"""
Path("pyproject.toml").write_text(toml)
print("  pyproject.toml creado ✓")

# ----------------------------------------------------------
# 37. PLUGINS DINÁMICOS – importlib.metadata & entry points
# ----------------------------------------------------------
print("\n=== 37. PLUGINS ===")

# Simula descubrimiento de plugins
def descubrir_plugins():
    # En la práctica se usa importlib.metadata.entry_points()
    return ["plugin_csv", "plugin_json"]

print("  Plugins encontrados:", descubrir_plugins())

# ----------------------------------------------------------
# 38. METAPROGRAMACIÓN – ast & inspect
# ----------------------------------------------------------
print("\n=== 38. AST & INSPECT ===")

import ast, inspect

cod = """
def foo(x):
    return x + 1
"""
tree = ast.parse(cod)
print("  Nombres AST:", [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])

# ----------------------------------------------------------
# 39. TYPING RUNTIME – runtime_checkable & get_type_hints
# ----------------------------------------------------------
print("\n=== 39. TYPING EN TIEMPO DE EJECUCIÓN ===")

@runtime_checkable
class Ejecutable(Protocol):
    def run(self) -> None: ...

class TareaEjecutable:
    def run(self):
        print("  Tarea ejecutándose ✓")

obj = TareaEjecutable()
print("  Cumple protocolo:", isinstance(obj, Ejecutable))

# ----------------------------------------------------------
# 40. CIERRE & LLAMADA FINAL
# ----------------------------------------------------------
if __name__ == "__main__":
    print("\n🎉 Script avanzado ejecutado. Explora cada bloque y profundiza!")