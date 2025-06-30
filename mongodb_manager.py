from pymongo import MongoClient
import json
import time
import threading
import os

class MongoDBManager:
    def __init__(self):
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

   