from arreglo import Arreglo
class Grupo(Arreglo):
    def __init__(self, nombre=None, grado=None, turno=None, salon=None, carrera=None, ciclo_escolar=None, alumnos=None, maestros=None, id=None):
        if id is None and nombre is None and grado is None and turno is None and salon is None and carrera is None and ciclo_escolar is None and alumnos is None and maestros is None:
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
            self.alumnos = alumnos
            self.maestro = None 
            self.es_contenedor = False

    def __str__(self):
        if self.es_contenedor:
            return "Contenedor de grupos"
        return (f"Grupo: {self.nombre}, Grado: {self.grado}, Turno: {self.turno}, "
                f"Salón: {self.salon}, Carrera: {self.carrera}, Ciclo Escolar: {self.ciclo_escolar}, "
                f"Maestro: {self.maestro if self.maestro else 'No asignado'}, "
                f"Alumnos: {len(self.alumnos)}")

    def cantidad_grupos(self):
        return len(self.items) if self.es_contenedor else 0

    def asignar_maestro(self, maestro):
        self.maestro = maestro

    def agregar_alumnos(self, lista_alumnos):
        self.alumnos.extend(lista_alumnos)

if __name__ == "__main__":
    from alumno import Alumno

    alumnos = Alumno()
    
    alumno1 = Alumno("Saul", "Pérez", "Gómez", 20, "A001", "TI", 3, 1)
    alumno2 = Alumno("Ana", "López", "Martínez", 21, "A002", "TI", 4, 2)
    alumno3 = Alumno("Luis", "Ramírez", "Santos", 19, "A003", "TI", 1, 3)

    alumnos.agregar(alumno1)
    alumnos.agregar(alumno2)
    alumnos.agregar(alumno3)

    grupos = Grupo()  

    grupo1 = Grupo("Grupo A", "Primero", "Matutino", "101", "TI", "2023-2024", alumnos=[alumno1, alumno2, alumno3])
    grupos.agregar(grupo1)

    grupo2 = Grupo("Grupo B", "Segundo", "Vespertino", "202", "TI", "2023-2024", alumnos=[alumno1])
    grupos.agregar(grupo2)

    print("\nLista de grupos:")
    for grupo in grupos.items:
        print(grupo)

    grupo1.asignar_maestro("Mtro. Juan Pérez")

    print("\nSe asignó el maestro al grupo con id 1:")
    print(grupo1)

    grupos.actualizar(1, nombre="Grupo A - Actualizado", grado="Cuarto", maestro="Mtro. Juan Pérez")
    print("\nSe actualizó el grupo con id 1:")
    print(grupo1)

    grupos.eliminar(grupo2)
    print("\nDespués de eliminar el grupo con id 2:")
    for grupo in grupos.items:
        print(grupo)

    print(f"\nCantidad de grupos: {grupos.cantidad_grupos()}")