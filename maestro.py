from arreglo import Arreglo
import json

class Maestro(Arreglo):
    def __init__(self, nombre=None, apellido_paterno=None, apellido_materno=None, 
                edad=None, clave=None, carrera=None, materia=None, id=None):
        if nombre is None and apellido_paterno is None and apellido_materno is None and \
           edad is None and clave is None and carrera is None and materia is None and id is None:
            Arreglo.__init__(self)
            self.es_contenedor = True
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
            return [item.convertirADiccionario()[0] if hasattr(item, "convertirADiccionario") else item for item in self.items]
        else:
            maestro_dict = {
                "id": self.id,
                "nombre": self.nombre,
                "apellido_paterno": self.apellido_paterno,
                "apellido_materno": self.apellido_materno,
                "edad": self.edad,
                "clave": self.clave,
                "carrera": self.carrera,
                "materia": self.materia,
                "tipo": "Maestro"
            }
            
            return [maestro_dict]
    
    def leerJson(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return Maestro.desde_json(datos)
    
    def desdeJson(datos):
        maestros = Maestro()
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
        if self.es_contenedor:
            return len(self.items)
        return 0

if __name__ == "__main__":
    maestro1 = Maestro("Ramiro", "Esquivel", "Gómez", 35, "M001", "TI", "Bases de Datos en la nube", 1)
    maestro2 = Maestro("Ana", "Lilia", "Hernández", 40, "M002", "TI", "Bases de Datos para aplicaciones", 2)
    maestro3 = Maestro("Delia", "Tarango", "Pérez", 50, "M003", "CM", "Desarrollo integral", 3)
    
    maestros = Maestro()
    maestros.agregar(maestro1, maestro2, maestro3)
    
    print("=== GUARDANDO MAESTROS ===")
    with open("maestros.json", "w", encoding="utf-8") as archivo:
        json.dump(maestros.convertirADiccionario(), archivo, indent=4, ensure_ascii=False)
    print("Maestros guardados en maestros.json")
    
    print("\n=== LEYENDO MAESTROS ===")
    maestros_leidos = Maestro.leerJson("maestros.json")
    print("Maestros leídos del archivo:")
    for maestro_leido in maestros_leidos.items:
        print(maestro_leido)
    
    print(f"\nCantidad de maestros leídos: {maestros_leidos.cantidad_maestros()}")
    
    print("\n=== PROBANDO BÚSQUEDA ===")
    encontrado = maestros_leidos.buscar(2)
    if encontrado:
        print(f"Maestro encontrado: {encontrado}")