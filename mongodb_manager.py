from pymongo import MongoClient
import json
import time
import threading
import os


class MongoDBManager:
    def _init_(self):
        self.client = None
        self.db = None
        self.tiempo_espera = 20
        self.timers = {}
        self.lock = threading.Lock()
        self.estado_conexion = False
        self.iniciar_colas()

    def iniciar_colas(self):
        clases = ["alumnos", "maestros", "grupos"]
        for clase in clases:
            archivo_cola = f"cola_{clase}.json"
            if not os.path.exists(archivo_cola):
                with open(archivo_cola, "w", encoding="utf-8") as f:
                    json.dump([], f)

    def intentar_conexion(self):
        try:
            self.client = MongoClient("mongodb+srv://thenotoriousxul:albertomarica@dbclass.txaumqu.mongodb.net/")
            self.db = self.client["dbclass"]
            if not self.estado_conexion:
                print("Conexión a MongoDB establecida exitosamente")
                self.estado_conexion = True
            return True
        except Exception as e:
            if self.estado_conexion:
                print(f"Error de conexión a MongoDB: {e}")
                print("Los datos se guardarán en cola local hasta que se restablezca la conexión")
                self.estado_conexion = False
            return False

    def guardar_en_cola(self, archivo, datos, clase_origen):
        with self.lock:
            try:
                archivo_cola = f"cola_{clase_origen}.json"

                with open(archivo_cola, "r", encoding="utf-8") as f:
                    cola = json.load(f)

                item_cola = {
                    "archivo": archivo,
                    "datos": datos,
                    "timestamp": time.time()
                }

                cola.append(item_cola)

                with open(archivo_cola, "w", encoding="utf-8") as f:
                    json.dump(cola, f, indent=4)

                print(f"Datos agregados a cola de {clase_origen} - Archivo: {archivo}")

                if clase_origen not in self.timers:
                    self.iniciar_timer(clase_origen)
            except Exception as e:
                print(f"Error al guardar en cola de {clase_origen}: {e}")

    def iniciar_timer(self, clase):
        if clase in self.timers and self.timers[clase]:
            self.timers[clase].cancel()

        self.timers[clase] = threading.Timer(self.tiempo_espera, self.procesar_cola, args=[clase])
        self.timers[clase].start()
        print(f"Timer iniciado para {clase} - Procesando cola en {self.tiempo_espera} segundos")

    def procesar_cola(self, clase):
        with self.lock:
            try:
                print(f"Intentando procesar cola de {clase}...")
                if not self.intentar_conexion():
                    print(f"Sin conexión a MongoDB - Reintentando cola de {clase} en 20 segundos")
                    self.iniciar_timer(clase)
                    return

                archivo_cola = f"cola_{clase}.json"
                with open(archivo_cola, "r", encoding="utf-8") as f:
                    cola = json.load(f)

                if not cola:
                    if clase in self.timers:
                        self.timers[clase] = None
                    print(f"Cola de {clase} vacía - No hay datos pendientes")
                    return

                print(f"Procesando {len(cola)} elementos de la cola de {clase}...")

                for i, item in enumerate(cola, 1):
                    coleccion = os.path.splitext(item["archivo"])[0]

                    try:
                        self.db[coleccion].insert_many(item["datos"])
                        print(f"Elemento {i}/{len(cola)} - Colección: {coleccion} (desde {clase})")
                    except Exception as e:
                        print(f"Error en elemento {i}/{len(cola)} de {clase} - {e}")

                with open(archivo_cola, "w", encoding="utf-8") as f:
                    json.dump([], f)

                if clase in self.timers:
                    self.timers[clase] = None
                print(f"Cola de {clase} procesada exitosamente - Todos los datos subidos a MongoDB")

            except Exception as e:
                print(f"Error al procesar cola de {clase}: {e}")
                print(f"Reintentando cola de {clase} en 20 segundos...")
                self.iniciar_timer(clase)

    def guardar(self, archivo, datos, clase_origen):
        if self.intentar_conexion():
            try:
                coleccion = os.path.splitext(archivo)[0]
                self.db[coleccion].insert_many(datos)
                print(f"Datos guardados directamente en MongoDB - Colección: {coleccion}")
                print(f"   Clase origen: {clase_origen}")
            except Exception as e:
                print(f"Error al guardar en MongoDB: {e}")
                print(f"Guardando en cola de {clase_origen}...")
                self.guardar_en_cola(archivo, datos, clase_origen)
        else:
            print(f"Sin conexión a MongoDB - Guardando en cola de {clase_origen}...")
            self.guardar_en_cola(archivo, datos, clase_origen)

    def obtener_estado_cola(self):
        try:
            clases = ["alumnos", "maestros", "grupos"]
            estado = "Estado de colas por clase:\n"

            for clase in clases:
                archivo_cola = f"cola_{clase}.json"
                try:
                    with open(archivo_cola, "r", encoding="utf-8") as f:
                        cola = json.load(f)

                    if not cola:
                        estado += f"   • {clase.capitalize()}: Cola vacía\n"
                    else:
                        estado += f"   • {clase.capitalize()}: {len(cola)} elementos pendientes\n"

                        for i, item in enumerate(cola[:3], 1):
                            archivo = item["archivo"]
                            timestamp = time.strftime("%H:%M:%S", time.localtime(item["timestamp"]))
                            estado += f"     - {i}. {archivo} ({timestamp})\n"

                        if len(cola) > 3:
                            estado += f"     ... y {len(cola) - 3} elementos más\n"

                except Exception as e:
                    estado += f"   • {clase.capitalize()}: Error al leer cola - {e}\n"

            if self.estado_conexion:
                estado += "\n✅ Conexión a MongoDB activa"
            else:
                estado += "\n❌ Sin conexión a MongoDB"

            return estado
        except Exception as e:
            return f"Error al leer estado de colas: {e}"