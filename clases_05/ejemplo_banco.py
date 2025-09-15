import threading
import time

# Recurso compartido
inventario = 5
lock = threading.Lock()

def retirar_producto(cantidad, cliente):
    global inventario
    for i in range(3):  # Cada cliente intenta retirar 3 veces
        print(f"[{cliente}] Intentando retirar {cantidad} producto(s)... (Intento {i+1})")

        # Bloqueo con lock
        with lock:
            print(f"[{cliente}] 🔑 Entró a la sección crítica.")

            if inventario >= cantidad:
                print(f"[{cliente}] Retirando {cantidad} producto(s)...")
                inventario -= cantidad
                time.sleep(1)  # Simula el tiempo de transacción
                print(f"[{cliente}] ✅ Retiro completado. Inventario actual: {inventario}")
            else:
                print(f"[{cliente}] ❌ No hay suficiente stock. Inventario actual: {inventario}")

            print(f"[{cliente}] 🚪 Saliendo de la sección crítica.\n")

        time.sleep(1)  # Pausa para que otros hilos actúen

# Crear varios hilos simulando clientes
clientes = [
    threading.Thread(target=retirar_producto, args=(4, "Cliente-1")),
    threading.Thread(target=retirar_producto, args=(6, "Cliente-2")),
    threading.Thread(target=retirar_producto, args=(3, "Cliente-3")),
]

# Iniciar hilos
for c in clientes:
    c.start()

# Esperar que todos finalicen
for c in clientes:
    c.join()

print(f"🏁 Todas las operaciones finalizaron. Inventario final: {inventario}")



