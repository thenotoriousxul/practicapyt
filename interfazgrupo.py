from grupo import Grupo
from maestro import Maestro
from alumno import Alumno
import json
import os

class InterfazGrupo:
    def __init__(self, contenedor_grupos=None, contenedor_alumnos=None):
        if contenedor_grupos is None:
            try:
                self.grupos = Grupo.leerJson("grupos.json")
            except FileNotFoundError:
                self.grupos = Grupo()
            self.contenedor_proporcionado = False
        else:
            self.grupos = contenedor_grupos
            self.contenedor_proporcionado = True
            
        self.contenedor_alumnos = contenedor_alumnos

    def obtener_siguiente_id(self):
        if not self.grupos.items:
            return 1
        return max(grupo.id for grupo in self.grupos.items) + 1

    def crearGrupo(self):
        if not self.contenedor_proporcionado and not os.path.exists("grupos.json"):
            print("Error: El archivo grupos.json no existe")
            return
            
        nombre = input("Ingrese el nombre del grupo: ")
        capacidad = input("Ingrese la capacidad del grupo: ")
        horario = input("Ingrese el horario del grupo: ")
        aula = input("Ingrese el aula del grupo: ")
        
        nuevo_id = self.obtener_siguiente_id()
        grupo = Grupo(nombre, capacidad, horario, aula, nuevo_id)
        self.grupos.agregar(grupo)
        
        if not self.contenedor_proporcionado:
            self.grupos.guardarJson("grupos.json")
            print("Cambios guardados en archivo")
        else:
            print("Los cambios se mantienen en memoria")
            
        print(f"Grupo creado correctamente con ID: {nuevo_id}")

    def mostrarGrupos(self):
        if not self.grupos.items:
            print("No hay grupos registrados")
            return
        
        print("\n=== LISTA DE GRUPOS ===")
        for grupo in self.grupos.items:
            print(f"\nID: {grupo.id}")
            print(f"Nombre: {grupo.nombre}")
            print(f"Capacidad: {grupo.capacidad}")
            print(f"Horario: {grupo.horario}")
            print(f"Aula: {grupo.aula}")
            print("Alumnos:")
            for alumno in grupo.alumnos.items:
                print(f"  - {alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}")
            print("-" * 50)

    def actualizarGrupo(self):
        if not self.contenedor_proporcionado and not os.path.exists("grupos.json"):
            print("Error: El archivo grupos.json no existe")
            return
            
        self.mostrarGrupos()
        id_grupo = input("\nIngrese el ID del grupo a actualizar: ")
        
        grupo_encontrado = None
        for grupo in self.grupos.items:
            if str(grupo.id) == id_grupo:
                grupo_encontrado = grupo
                break
        
        if grupo_encontrado is None:
            print("Grupo no encontrado")
            return
        
        print("\nIngrese los nuevos datos (deje en blanco para mantener el valor actual):")
        grupo_encontrado.nombre = input(f"Nuevo nombre [{grupo_encontrado.nombre}]: ") or grupo_encontrado.nombre
        grupo_encontrado.capacidad = input(f"Nueva capacidad [{grupo_encontrado.capacidad}]: ") or grupo_encontrado.capacidad
        grupo_encontrado.horario = input(f"Nuevo horario [{grupo_encontrado.horario}]: ") or grupo_encontrado.horario
        grupo_encontrado.aula = input(f"Nueva aula [{grupo_encontrado.aula}]: ") or grupo_encontrado.aula
        
        if not self.contenedor_proporcionado:
            self.grupos.guardarJson("grupos.json")
            print("Cambios guardados en archivo")
        else:
            print("Los cambios se mantienen en memoria")
            
        print("Grupo actualizado correctamente")

    def eliminarGrupo(self):
        if not self.contenedor_proporcionado and not os.path.exists("grupos.json"):
            print("Error: El archivo grupos.json no existe")
            return
            
        self.mostrarGrupos()
        id_grupo = input("\nIngrese el ID del grupo a eliminar: ")
        
        for i, grupo in enumerate(self.grupos.items):
            if str(grupo.id) == id_grupo:
                del self.grupos.items[i]
                if not self.contenedor_proporcionado:
                    self.grupos.guardarJson("grupos.json")
                    print("Cambios guardados en archivo")
                else:
                    print("Los cambios se mantienen en memoria")
                print("Grupo eliminado correctamente")
                return
        
        print("Grupo no encontrado")

    def agregarAlumnoAGrupo(self):
        if not self.contenedor_proporcionado and not os.path.exists("grupos.json"):
            print("Error: El archivo grupos.json no existe")
            return
            
        self.mostrarGrupos()
        id_grupo = input("\nIngrese el ID del grupo al que desea agregar un alumno: ")
        
        grupo_encontrado = None
        for grupo in self.grupos.items:
            if str(grupo.id) == id_grupo:
                grupo_encontrado = grupo
                break
        
        if grupo_encontrado is None:
            print("Grupo no encontrado")
            return

        alumnos = None
        if self.contenedor_alumnos is not None:
            alumnos = self.contenedor_alumnos
        else:
            try:
                alumno = Alumno()
                alumnos = alumno.leerJson("alumnos.json")
            except FileNotFoundError:
                print("No hay alumnos registrados. Primero debe registrar alumnos.")
                return

        if not alumnos.items:
            print("No hay alumnos registrados. Primero debe registrar alumnos.")
            return
        
        print("\nAlumnos disponibles:")
        for alumno in alumnos.items:
            print(f"ID: {alumno.id} - {alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}")
        
        id_alumno = input("\nIngrese el ID del alumno a agregar al grupo: ")
        alumno_encontrado = None
        for alumno in alumnos.items:
            if str(alumno.id) == id_alumno:
                alumno_encontrado = alumno
                break
        
        if alumno_encontrado is None:
            print("Alumno no encontrado")
            return

        for alumno in grupo_encontrado.alumnos.items:
            if str(alumno.id) == id_alumno:
                print("Este alumno ya está en el grupo")
                return

        grupo_encontrado.alumnos.agregar(alumno_encontrado)
        if not self.contenedor_proporcionado:
            self.grupos.guardarJson("grupos.json")
            print("Cambios guardados en archivo")
        else:
            print("Los cambios se mantienen en memoria")
        print("Alumno agregado al grupo correctamente")

    def eliminarAlumnoDeGrupo(self):
        if not self.contenedor_proporcionado and not os.path.exists("grupos.json"):
            print("Error: El archivo grupos.json no existe")
            return
            
        self.mostrarGrupos()
        id_grupo = input("\nIngrese el ID del grupo del que desea eliminar un alumno: ")
        
        grupo_encontrado = None
        for grupo in self.grupos.items:
            if str(grupo.id) == id_grupo:
                grupo_encontrado = grupo
                break
        
        if grupo_encontrado is None:
            print("Grupo no encontrado")
            return

        if not grupo_encontrado.alumnos.items:
            print("Este grupo no tiene alumnos")
            return

        print("\nAlumnos en el grupo:")
        for alumno in grupo_encontrado.alumnos.items:
            print(f"ID: {alumno.id} - {alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}")
        
        id_alumno = input("\nIngrese el ID del alumno a eliminar del grupo: ")
        
        for i, alumno in enumerate(grupo_encontrado.alumnos.items):
            if str(alumno.id) == id_alumno:
                del grupo_encontrado.alumnos.items[i]
                if not self.contenedor_proporcionado:
                    self.grupos.guardarJson("grupos.json")
                    print("Cambios guardados en archivo")
                else:
                    print("Los cambios se mantienen en memoria")
                print("Alumno eliminado del grupo correctamente")
                return
        
        print("Alumno no encontrado en el grupo")

    def menu_interactivo(self):
        while True:
            print("\n=== MENÚ DE GRUPOS ===")
            print("1. Crear grupo")
            print("2. Mostrar grupos")
            print("3. Actualizar grupo")
            print("4. Eliminar grupo")
            print("5. Agregar alumno a grupo")
            print("6. Eliminar alumno de grupo")
            print("7. Salir")
            opcion = input("Ingrese una opcion: ")
            
            if opcion == "1":
                self.crearGrupo()
            elif opcion == "2":
                self.mostrarGrupos()
            elif opcion == "3":
                self.actualizarGrupo()
            elif opcion == "4":
                self.eliminarGrupo()
            elif opcion == "5":
                self.agregarAlumnoAGrupo()
            elif opcion == "6":
                self.eliminarAlumnoDeGrupo()
            elif opcion == "7":
                break
            else:
                print("Opción no válida")

if __name__ == "__main__":
    interfaz = InterfazGrupo()
    interfaz.menu_interactivo() 