import requests

print("🧪 Conversor universal sin clave (Frankfurter API)")

try:
    monto = float(input("Monto a convertir: "))
    moneda_origen = input("Moneda origen (ej: USD, EUR, DOP): ").upper()
    moneda_destino = input("Moneda destino (ej: USD, EUR, DOP): ").upper()

    url = f"https://api.frankfurter.app/latest?amount={monto}&from={moneda_origen}&to={moneda_destino}"
    resp = requests.get(url)
    datos = resp.json()

    if "error" in datos:
        raise Exception(datos["error"])

    tasa = datos["rates"].get(moneda_destino)
    if tasa is None:
        raise Exception("Moneda destino no válida o no soportada.")

    resultado = tasa
    print(f"\n💱 {monto} {moneda_origen} = {resultado:.2f} {moneda_destino}")
    print(f"🔁 1 {moneda_origen} ≈ {resultado / monto:.4f} {moneda_destino}")

except ValueError:
    print("❌ Debes ingresar un número válido.")
except Exception as e:
    print(f"❌ Error: {e}")
