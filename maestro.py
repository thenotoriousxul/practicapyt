from arreglo import Arreglo

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
            if maestro.id == id:
                return maestro
        print("Maestro no encontrado.")
        return None
    
    def cantidad_maestros(self):
        if self.es_contenedor:
            return len(self.items)
        return 0

if __name__ == "__main__":
    maestro1 = Maestro("Ramiro", "Esquivel", "Gómez", 35, "M001", "Bases de Datos en la nube", "TI", 1)
    maestro2 = Maestro("Ana", "Lilia", "Hernández", 40, "M002", "Bases de Datos para aplicaciones", "TI", 2)
    maestro3 = Maestro("Delia", "Tarango", "Pérez", 50, "M003", "Desarrollo integral", "CM", 3)
    
    maestros = Maestro()
    maestros.agregar(maestro1, maestro2, maestro3)
    
    print("\nLista de maestros:")
    for maestro in maestros.items:
        print(maestro)
    
    print("\nResultado de búsqueda del maestro con id 1:")
    encontrado = maestros.buscar(1)
    if encontrado:
        print(encontrado)
    
    maestros.actualizar(maestro1, "nombre", "Ramiro")
    maestros.actualizar(maestro1, "materia", "Bases de Datos para aplicaciones")
    maestros.actualizar(maestro1, "carrera", "Mecatrónica")
    
    print("\nSe actualizó el maestro con id 1:")
    print(maestro1)
    
    maestros.eliminar(maestro2)
    print("\nDespués de eliminar el maestro con id 2:")
    for maestro in maestros.items:
        print(maestro)
    
    print(f"\nCantidad de maestros: {maestros.cantidad_maestros()}")