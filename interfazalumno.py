from alumno import Alumno
import json
import os
from arreglo import Arreglo
from mongodb_manager import MongoDBManager

class InterfazAlumno:
    def __init__(self, contenedor_alumnos=None):
        self.contenedor_proporcionado = contenedor_alumnos is not None
        if contenedor_alumnos is None:
            self.alumnos = Alumno()
            try:
                self.alumnos = Alumno.leerJson("alumnos.json")
            except FileNotFoundError:
                pass
        else:
            self.alumnos = contenedor_alumnos

    def obtener_siguiente_id(self):
        if not self.alumnos.items:
            return 1
        return max(alumno.id for alumno in self.alumnos.items) + 1

    def guardar_cambios(self):
        if not self.contenedor_proporcionado:
            self.alumnos.guardarJson("alumnos.json")

    def crearAlumno(self):
        nombre = input("Ingrese el nombre del alumno: ")
        apellido_paterno = input("Ingrese el apellido paterno del alumno: ")
        apellido_materno = input("Ingrese el apellido materno del alumno: ")
        edad = input("Ingrese la edad del alumno: ")
        matricula = input("Ingrese la matricula del alumno: ")
        carrera = input("Ingrese la carrera del alumno: ")
        semestre = input("Ingrese el semestre del alumno: ")
        promedio = input("Ingrese el promedio del alumno: ")
        
        nuevo_id = self.obtener_siguiente_id()
        alumno = Alumno(nombre, apellido_paterno, apellido_materno, edad, matricula, carrera, semestre, promedio, nuevo_id)
        self.alumnos.agregar(alumno)
        if not self.contenedor_proporcionado:
            self.alumnos.guardarJson("alumnos.json")
            print("Cambios guardados en archivo")
        else:
            print("Los cambios se mantienen en memoria")
            
        print(f"Alumno creado correctamente con ID: {nuevo_id}")

    def mostrarAlumnos(self):
        if not self.alumnos.items:
            print("No hay alumnos registrados")
            return
        
        print("\n=== LISTA DE ALUMNOS ===")
        for alumno in self.alumnos.items:
            print(f"\nID: {alumno.id}")
            print(f"Nombre: {alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}")
            print(f"Edad: {alumno.edad}")
            print(f"Matrícula: {alumno.matricula}")
            print(f"Carrera: {alumno.carrera}")
            print(f"Semestre: {alumno.semestre}")
            print(f"Promedio: {alumno.promedio}")
            print("-" * 50)

    def actualizarAlumno(self):
        if not self.contenedor_proporcionado and not os.path.exists("alumnos.json"):
            print("Error: El archivo alumnos.json no existe")
            return
            
        self.mostrarAlumnos()
        id_alumno = input("\nIngrese el ID del alumno a actualizar: ")
        
        alumno_encontrado = None
        for alumno in self.alumnos.items:
            if str(alumno.id) == id_alumno:
                alumno_encontrado = alumno
                break
        
        if alumno_encontrado is None:
            print("Alumno no encontrado")
            return
        
        print("\nIngrese los nuevos datos (deje en blanco para mantener el valor actual):")
        alumno_encontrado.nombre = input(f"Nuevo nombre [{alumno_encontrado.nombre}]: ") or alumno_encontrado.nombre
        alumno_encontrado.apellido_paterno = input(f"Nuevo apellido paterno [{alumno_encontrado.apellido_paterno}]: ") or alumno_encontrado.apellido_paterno
        alumno_encontrado.apellido_materno = input(f"Nuevo apellido materno [{alumno_encontrado.apellido_materno}]: ") or alumno_encontrado.apellido_materno
        alumno_encontrado.edad = input(f"Nueva edad [{alumno_encontrado.edad}]: ") or alumno_encontrado.edad
        alumno_encontrado.matricula = input(f"Nueva matrícula [{alumno_encontrado.matricula}]: ") or alumno_encontrado.matricula
        alumno_encontrado.carrera = input(f"Nueva carrera [{alumno_encontrado.carrera}]: ") or alumno_encontrado.carrera
        alumno_encontrado.semestre = input(f"Nuevo semestre [{alumno_encontrado.semestre}]: ") or alumno_encontrado.semestre
        alumno_encontrado.promedio = input(f"Nuevo promedio [{alumno_encontrado.promedio}]: ") or alumno_encontrado.promedio
        
        if not self.contenedor_proporcionado:
            self.alumnos.guardarJson("alumnos.json")
        print("Alumno actualizado correctamente")

    def eliminarAlumno(self):

        self.mostrarAlumnos()
        id_alumno = input("\nIngrese el ID del alumno a eliminar: ")
        
        for i, alumno in enumerate(self.alumnos.items):
            if str(alumno.id) == id_alumno:
                del self.alumnos.items[i]
                if not self.contenedor_proporcionado:
                    self.alumnos.guardarJson("alumnos.json")
                print("Alumno eliminado correctamente")
                return
        
        print("Alumno no encontrado")

    def menu_interactivo(self):
        while True:
            print("\n=== MENÚ DE ALUMNOS ===")
            print("1. Crear alumno")
            print("2. Mostrar alumnos")
            print("3. Actualizar alumno")
            print("4. Eliminar alumno")
            print("5. Estado de cola MongoDB")
            print("6. Salir")
            opcion = input("Ingrese una opcion: ")
            
            if opcion == "1":
                self.crearAlumno()
            elif opcion == "2":
                self.mostrarAlumnos()
            elif opcion == "3":
                self.actualizarAlumno()
            elif opcion == "4":
                self.eliminarAlumno()
            elif opcion == "5":
                self.mostrar_estado_cola()
            elif opcion == "6":
                break
            else:
                print("Opción no válida")

    
if __name__ == "__main__":
    interfaz = InterfazAlumno()
    interfaz.menu_interactivo()

    # contenedor = Arreglo()
    # interfaz = InterfazAlumno(contenedor_alumnos=contenedor)
    # interfaz.menu_interactivo()
    
