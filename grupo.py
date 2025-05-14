from arreglo import Arreglo
from alumno import Alumno
from maestro import Maestro

class Grupo(Arreglo):
    def __init__(self, nombre=None, grado=None, turno=None, salon=None, 
                carrera=None, ciclo_escolar=None, maestro=None, id=None):
        if nombre is None and grado is None and turno is None and salon is None and \
           carrera is None and ciclo_escolar is None and maestro is None and id is None:
            Arreglo.__init__(self)
            self.es_contenedor = True
        else:
            self.id = id
            self.nombre = nombre
            self.grado = grado
            self.turno = turno
            self.salon = salon
            self.carrera = carrera
            self.ciclo_escolar = ciclo_escolar
            self.maestro = maestro
            self.alumnos = Alumno()
            self.es_contenedor = False
    
    def asignar_maestro(self, maestro):
        self.maestro = maestro
    
    def cambiarNombre(self, nombre):
        self.nombre = nombre
    
    def __str__(self):
        if self.es_contenedor:
            return f"Total de grupos: {len(self.items)}"
        
        maestro_info = f"{self.maestro.nombre} {self.maestro.apellido_paterno}" if self.maestro else "Falta asignar"
        
        return (
            f"Grupo: {self.nombre}, Grado: {self.grado}, Turno: {self.turno}\n"
            f"Salón: {self.salon}, Carrera: {self.carrera}, Ciclo Escolar: {self.ciclo_escolar}\n"
            f"Maestro: {maestro_info}\n"
            f"Total de alumnos: {len(self.alumnos.items)}"
        )
    
    def cantidad_grupos(self):
        return len(self.items) if self.es_contenedor else 0

if __name__ == "__main__":
    a1 = Alumno("Saul", "Sanchez", "Lopez", 18, "23170125", "TI", 3, 10, 1)
    a2 = Alumno("Diana", "Ochoa", "Martínez", 19, "23170119", "TI", 4, 10, 2)
    
    m1 = Maestro("Ramiro", "Esquivel", "Nuñez", 40, "M001", "TI", "Aplicaciones Web", 1)
    
    grupo = Grupo("Desarrollo Web", "Tercero", "Matutino", "301", "TI", "2023-2024", m1, 1)
    grupo.alumnos.agregar(a1, a2)
    
    print(grupo)
    
    grupo.alumnos.actualizar(a1, "matricula", "23170126")
    print("\nDespués de actualizar matricula:")
    print(a1)
    
    grupos = Grupo()
    grupos.agregar(grupo)
    
    grupo2 = Grupo("Desarrollo Web", "Cuarto", "Vespertino", "402", "TI", "2023-2024", None, 2)
    grupos.agregar(grupo2)
    
    m2 = Maestro("Laura", "Gómez", "Sánchez", 38, "M002", "Computación", "Frameworks", 2)
    grupo2.asignar_maestro(m2)
    
    print("\nLista de grupos:")
    for grupo in grupos.items:
        print(grupo)
    
    print(f"\nCantidad de grupos: {grupos.cantidad_grupos()}")