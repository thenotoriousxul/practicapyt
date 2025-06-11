from maestro import Maestro
import json
import os

class InterfazMaestro:
    def __init__(self, contenedor_maestros=None):
        if contenedor_maestros is None:
            try:
                self.maestros = Maestro.leerJson("maestros.json")
            except FileNotFoundError:
                self.maestros = Maestro()
            self.contenedor_proporcionado = False
        else:
            self.maestros = contenedor_maestros
            self.contenedor_proporcionado = True

    def obtener_siguiente_id(self):
        if not self.maestros.items:
            return 1
        return max(maestro.id for maestro in self.maestros.items) + 1

    def crearMaestro(self):
        if not self.contenedor_proporcionado and not os.path.exists("maestros.json"):
            print("Error: El archivo maestros.json no existe")
            return
            
        nombre = input("Ingrese el nombre del maestro: ")
        apellido_paterno = input("Ingrese el apellido paterno del maestro: ")
        apellido_materno = input("Ingrese el apellido materno del maestro: ")
        edad = input("Ingrese la edad del maestro: ")
        numero_empleado = input("Ingrese el número de empleado del maestro: ")
        materia = input("Ingrese la materia del maestro: ")
        grado_academico = input("Ingrese el grado académico del maestro: ")
        
        nuevo_id = self.obtener_siguiente_id()
        maestro = Maestro(nombre, apellido_paterno, apellido_materno, edad, numero_empleado, materia, grado_academico, nuevo_id)
        self.maestros.agregar(maestro)
        
        if not self.contenedor_proporcionado:
            self.maestros.guardarJson("maestros.json")
            print("Cambios guardados en archivo")
        else:
            print("Los cambios se mantienen en memoria")
            
        print(f"Maestro creado correctamente con ID: {nuevo_id}")

    def mostrarMaestros(self):
        if not self.maestros.items:
            print("No hay maestros registrados")
            return
        
        print("\n=== LISTA DE MAESTROS ===")
        for maestro in self.maestros.items:
            print(f"\nID: {maestro.id}")
            print(f"Nombre: {maestro.nombre} {maestro.apellido_paterno} {maestro.apellido_materno}")
            print(f"Edad: {maestro.edad}")
            print(f"Número de empleado: {maestro.numero_empleado}")
            print(f"Materia: {maestro.materia}")
            print(f"Grado académico: {maestro.grado_academico}")
            print("-" * 50)

    def actualizarMaestro(self):
        if not self.contenedor_proporcionado and not os.path.exists("maestros.json"):
            print("Error: El archivo maestros.json no existe")
            return
            
        self.mostrarMaestros()
        id_maestro = input("\nIngrese el ID del maestro a actualizar: ")
        
        maestro_encontrado = None
        for maestro in self.maestros.items:
            if str(maestro.id) == id_maestro:
                maestro_encontrado = maestro
                break
        
        if maestro_encontrado is None:
            print("Maestro no encontrado")
            return
        
        print("\nIngrese los nuevos datos (deje en blanco para mantener el valor actual):")
        maestro_encontrado.nombre = input(f"Nuevo nombre [{maestro_encontrado.nombre}]: ") or maestro_encontrado.nombre
        maestro_encontrado.apellido_paterno = input(f"Nuevo apellido paterno [{maestro_encontrado.apellido_paterno}]: ") or maestro_encontrado.apellido_paterno
        maestro_encontrado.apellido_materno = input(f"Nuevo apellido materno [{maestro_encontrado.apellido_materno}]: ") or maestro_encontrado.apellido_materno
        maestro_encontrado.edad = input(f"Nueva edad [{maestro_encontrado.edad}]: ") or maestro_encontrado.edad
        maestro_encontrado.numero_empleado = input(f"Nuevo número de empleado [{maestro_encontrado.numero_empleado}]: ") or maestro_encontrado.numero_empleado
        maestro_encontrado.materia = input(f"Nueva materia [{maestro_encontrado.materia}]: ") or maestro_encontrado.materia
        maestro_encontrado.grado_academico = input(f"Nuevo grado académico [{maestro_encontrado.grado_academico}]: ") or maestro_encontrado.grado_academico
        
        if not self.contenedor_proporcionado:
            self.maestros.guardarJson("maestros.json")
            print("Cambios guardados en archivo")
        else:
            print("Los cambios se mantienen en memoria")
            
        print("Maestro actualizado correctamente")

    def eliminarMaestro(self):
        if not self.contenedor_proporcionado and not os.path.exists("maestros.json"):
            print("Error: El archivo maestros.json no existe")
            return
            
        self.mostrarMaestros()
        id_maestro = input("\nIngrese el ID del maestro a eliminar: ")
        
        for i, maestro in enumerate(self.maestros.items):
            if str(maestro.id) == id_maestro:
                del self.maestros.items[i]
                if not self.contenedor_proporcionado:
                    self.maestros.guardarJson("maestros.json")
                    print("Cambios guardados en archivo")
                else:
                    print("Los cambios se mantienen en memoria")
                print("Maestro eliminado correctamente")
                return
        
        print("Maestro no encontrado")

    def menu_interactivo(self):
        while True:
            print("\n=== MENÚ DE MAESTROS ===")
            print("1. Crear maestro")
            print("2. Mostrar maestros")
            print("3. Actualizar maestro")
            print("4. Eliminar maestro")
            print("5. Salir")
            opcion = input("Ingrese una opcion: ")
            
            if opcion == "1":
                self.crearMaestro()
            elif opcion == "2":
                self.mostrarMaestros()
            elif opcion == "3":
                self.actualizarMaestro()
            elif opcion == "4":
                self.eliminarMaestro()
            elif opcion == "5":
                break
            else:
                print("Opción no válida")

if __name__ == "__main__":
    interfaz = InterfazMaestro()
    interfaz.menu_interactivo() 