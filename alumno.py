from arreglo import Arreglo

class Alumno(Arreglo):
    def __init__(self, nombre=None, apellido_paterno=None, apellido_materno=None,
                 edad=None, matricula=None, carrera=None, semestre=None, id=None):
        if nombre is None and apellido_paterno is None and apellido_materno is None \
           and edad is None and matricula is None and carrera is None and semestre is None and id is None:
            Arreglo.__init__(self)  
            self.es_contenedor = True
        else:
            self.id = id
            self.nombre = nombre
            self.apellido_paterno = apellido_paterno
            self.apellido_materno = apellido_materno
            self.edad = edad
            self.matricula = matricula
            self.carrera = carrera
            self.semestre = semestre
            self.es_contenedor = False

    

    def __str__(self):
        if self.es_contenedor:
            return "Contenedor de alumnos"
        return (f"Alumno {self.nombre} {self.apellido_paterno} {self.apellido_materno}, "
                f"Edad: {self.edad}, Matrícula: {self.matricula}, Carrera: {self.carrera}, Semestre: {self.semestre}")

    def cantidad_alumnos(self):
        if self.es_contenedor:
            return len(self.items)
        return 0

if __name__ == "__main__":
    alumnos = Alumno()  

    alumno1 = Alumno("Saul", "Pérez", "Gómez", 20, "A001", "TI", 3, 1)
    alumnos.agregar(alumno1)  

    alumno2 = Alumno("Ana", "López", "Martínez", 21, "A002", "TI", 4, 2)
    alumnos.agregar(alumno2) 

    print("\nLista de alumnos:")
    for alumno in alumnos.items:
        print(alumno)

    alumnos.actualizar(1, nombre="Saul Sanchez", matricula="A001-2023", semestre=4)
    print("\nSe actualizó el alumno 1:")
    print(alumno1)

    alumnos.eliminar(alumno2)
    print("\nDespués de eliminar el alumno 2:")
    for alumno in alumnos.items:
        print(alumno)
    

    print(f"\nCantidad de alumnos: {alumnos.cantidad_alumnos()}")
