from arreglo import Arreglo

class Alumno(Arreglo):
    def __init__(self, nombre=None, apellido_paterno=None, apellido_materno=None, 
                edad=None, matricula=None, carrera=None, semestre=None, promedio=None, id=None):
        if nombre is None and apellido_paterno is None and apellido_materno is None and \
           edad is None and matricula is None and carrera is None and semestre is None and \
           promedio is None and id is None:
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
            self.promedio = promedio
            self.es_contenedor = False
    
    def actualizarMatricula(self, matricula):
        self.matricula = matricula
    
    def __str__(self):
        if self.es_contenedor:
            return f"Total de alumnos: {len(self.items)}"
        return (f"Alumno: {self.nombre} {self.apellido_paterno} {self.apellido_materno}, {self.edad} años, "
                f"Matrícula: {self.matricula}, Carrera: {self.carrera}, Semestre: {self.semestre}, "
                f"Promedio: {self.promedio if hasattr(self, 'promedio') else 'No asignado'}")
    
    def cantidad_alumnos(self):
        if self.es_contenedor:
            return len(self.items)
        return 0

if __name__ == "__main__":
    a1 = Alumno("Saul", "Sanchez", "Lopez", 20, "23170093", "Desarrollo y gestion de software", 3, 10, 1)
    print(a1)
    
    a2 = Alumno("Misael", "Trejo", "Perez", 19, "23170115", "Desarrollo y gestion de software", 4, 10, 2)
    a2.actualizarMatricula("23170125")
    print(a2)
    
    alumnos = Alumno()
    alumnos.agregar(a1)
    alumnos.eliminar(indice=0)
    alumnos.agregar(a2)
    alumnos.agregar(Alumno("Azael", "Garcia", "Candela", 20, "23170022", "Desarrollo y gestion de software", 2, 10, 3))
    
    print("\nLista de alumnos:")
    for alumno in alumnos.items:
        print(alumno)
    
    alumnos.actualizar(a2, "carrera", "Redes y telecomunicaciones")
    print("\nDespués de actualizar carrera:")
    print(a2)
    
    print(f"\nCantidad de alumnos: {alumnos.cantidad_alumnos()}")