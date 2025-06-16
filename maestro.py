from arreglo import Arreglo
import json
from mongodb_manager import MongoDBManager

class Maestro(Arreglo):
    def __init__(self, nombre=None, apellido_paterno=None, apellido_materno=None, 
                 edad=None, clave=None, carrera=None, materia=None, id=None):
        if nombre is None and apellido_paterno is None and apellido_materno is None and \
           edad is None and clave is None and carrera is None and materia is None and id is None:
            super().__init__()
            self.es_contenedor = True
            self.mongo_manager = MongoDBManager()
        else:
            self.id = id
            self.nombre = nombre
            self.apellido_paterno = apellido_paterno
            self.apellido_materno = apellido_materno
            self.edad = edad
            self.clave = clave
            self.carrera = carrera
            self.materia = materia
            self.es_contenedor = False

    def convertirADiccionario(self):
        if self.es_contenedor:
            lista_maestros = [item.convertirADiccionario()[0] if hasattr(item, "convertirADiccionario") else item for item in self.items]
            return lista_maestros[0] if len(lista_maestros) == 1 else lista_maestros
        else:
            return [{
                "id": self.id,
                "nombre": self.nombre,
                "apellido_paterno": self.apellido_paterno,
                "apellido_materno": self.apellido_materno,
                "edad": self.edad,
                "clave": self.clave,
                "carrera": self.carrera,
                "materia": self.materia,
                "tipo": "Maestro"
            }]

    @staticmethod
    def leerJson(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return Maestro.desde_json(datos)

    @staticmethod
    def desde_json(datos):
        maestros = Maestro()

        if isinstance(datos, dict) and datos.get("tipo") == "Maestro":
            maestro = Maestro(
                nombre=datos.get("nombre"),
                apellido_paterno=datos.get("apellido_paterno"),
                apellido_materno=datos.get("apellido_materno"),
                edad=datos.get("edad"),
                clave=datos.get("clave"),
                carrera=datos.get("carrera"),
                materia=datos.get("materia"),
                id=datos.get("id")
            )
            maestros.items.append(maestro)

        elif isinstance(datos, list):
            for item in datos:
                if isinstance(item, dict) and item.get("tipo") == "Maestro":
                    maestro = Maestro(
                        nombre=item.get("nombre"),
                        apellido_paterno=item.get("apellido_paterno"),
                        apellido_materno=item.get("apellido_materno"),
                        edad=item.get("edad"),
                        clave=item.get("clave"),
                        carrera=item.get("carrera"),
                        materia=item.get("materia"),
                        id=item.get("id")
                    )
                    maestros.items.append(maestro)

        return maestros

    def __str__(self):
        if self.es_contenedor:
            return f"Total de maestros: {len(self.items)}"
        return (f"Maestro: {self.nombre} {self.apellido_paterno} {self.apellido_materno}, "
                f"Edad: {self.edad}, Clave: {self.clave}, Carrera: {self.carrera}, Materia: {self.materia}")

    def buscar(self, id):
        if not self.es_contenedor:
            print("Este objeto no es un contenedor.")
            return None
        for maestro in self.items:
            if isinstance(maestro, dict):
                if maestro.get('id') == id:
                    return maestro
            elif hasattr(maestro, 'id') and maestro.id == id:
                return maestro
        print("Maestro no encontrado.")
        return None

    def cantidad_maestros(self):
        return len(self.items) if self.es_contenedor else 0

    def guardarJson(self, archivo):
        datos = self.convertirADiccionario()
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        
        if self.es_contenedor:
            self.mongo_manager.guardar(archivo, datos)

if __name__ == "__main__":
    maestros = Maestro()
    maestros = maestros.leerJson("maestros.json")
    print(f"Maestros leídos: {maestros.cantidad_maestros()}")

    maestros.guardarJson("maestros_guardados.json")
    print("Datos guardados en 'maestros_guardados.json'")
