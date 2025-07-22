# ==========================================
# Python básico en un solo script
# ==========================================

# 1. Variables y tipos de datos
edad = 25                                   # int
altura = 1.75                               # float
nombre = "Guao"                             # str
es_programador = True                       # bool

# 2. Operaciones
suma = 10 + 5
resto = 10 % 3
es_mayor = edad > 18
puede_votar = es_mayor and es_programador

# 3. Listas y diccionarios
frutas = ["manzana", "banana", "pera"]
frutas.append("kiwi")

persona = {
    "nombre": nombre,
    "edad": edad,
    "lenguajes": ["Python", "JavaScript"]
}

# 4. Condicionales
if edad >= 18:
    mensaje_edad = "Eres mayor de edad."
elif edad >= 13:
    mensaje_edad = "Eres adolescente."
else:
    mensaje_edad = "Eres menor."

# 5. Ciclos
print("--- Frutas ---")
for fruta in frutas:
    print(f"Me gusta la {fruta}")

print("\n--- Contador ---")
contador = 0
while contador < 3:
    print(f"Contador: {contador}")
    contador += 1

# 6. Funciones
def saludar(nombre, veces=1):
    """Imprime un saludo personalizado."""
    for _ in range(veces):
        print(f"¡Hola, {nombre}!")

# 7. Input y manejo de errores
try:
    numero = int(input("\nDime un número entero: "))
    resultado = 10 / numero
    print(f"10 / {numero} = {resultado}")
except ValueError:
    print("No escribiste un número válido.")
except ZeroDivisionError:
    print("No se puede dividir entre 0.")

# 8. Resumen
print("\n--- Resumen ---")
print(mensaje_edad)
print("¿Puedes votar?:", puede_votar)
print("Persona:", persona)
saludar(nombre, veces=2)