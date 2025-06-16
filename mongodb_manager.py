from pymongo import MongoClient
import json
import time
import threading
import os

class MongoDBManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.cola_archivo = "cola_guardado.json"
        self.tiempo_espera = 20  
        self.timer = None
        self.lock = threading.Lock()
        self.iniciar_cola()

    def iniciar_cola(self):
        if not os.path.exists(self.cola_archivo):
            with open(self.cola_archivo, "w", encoding="utf-8") as f:
                json.dump([], f)

    def intentar_conexion(self):
        try:
            self.client = MongoClient("mongodb+srv://thenotoriousxul:albertomarica@dbclass.txaumqu.mongodb.net/")
            self.db = self.client["dbclass"]
            return True
        except Exception as e:
            print(f"Error de conexión a MongoDB: {e}")
            return False

    def guardar_en_cola(self, archivo, datos):
        with self.lock:
            try:
                with open(self.cola_archivo, "r", encoding="utf-8") as f:
                    cola = json.load(f)
                
                cola.append({
                    "archivo": archivo,
                    "datos": datos,
                    "timestamp": time.time()
                })
                
                with open(self.cola_archivo, "w", encoding="utf-8") as f:
                    json.dump(cola, f, indent=4)
                
                if not self.timer:
                    self.iniciar_timer()
            except Exception as e:
                print(f"Error al guardar en cola: {e}")

    def iniciar_timer(self):
        self.timer = threading.Timer(self.tiempo_espera, self.procesar_cola)
        self.timer.start()

    def procesar_cola(self):
        with self.lock:
            try:
                if not self.intentar_conexion():
                    self.iniciar_timer()
                    return

                with open(self.cola_archivo, "r", encoding="utf-8") as f:
                    cola = json.load(f)

                if not cola:
                    self.timer = None
                    return

                for item in cola:
                    coleccion = os.path.splitext(item["archivo"])[0]
                    self.db[coleccion].insert_many(item["datos"])

                # Limpiar cola después de procesar
                with open(self.cola_archivo, "w", encoding="utf-8") as f:
                    json.dump([], f)

                self.timer = None
                print("Cola procesada exitosamente")

            except Exception as e:
                print(f"Error al procesar cola: {e}")
                self.iniciar_timer()

    def guardar(self, archivo, datos):
        if self.intentar_conexion():
            try:
                coleccion = os.path.splitext(archivo)[0]
                self.db[coleccion].insert_many(datos)
                print(f"Datos guardados en MongoDB - Colección: {coleccion}")
            except Exception as e:
                print(f"Error al guardar en MongoDB: {e}")
                self.guardar_en_cola(archivo, datos)
        else:
            self.guardar_en_cola(archivo, datos) 