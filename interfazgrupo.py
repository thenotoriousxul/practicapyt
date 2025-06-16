from grupo import Grupo
from maestro import Maestro
from alumno import Alumno
from arreglo import Arreglo
import json
import os

class InterfazGrupo:
    def __init__(self, contenedor_grupos=None):
        self.contenedor_proporcionado = contenedor_grupos is not None
        if contenedor_grupos is None:
            self.grupos = Grupo()
            try:
                self.grupos = Grupo.leerJson("grupos.json")
            except FileNotFoundError:
                pass

    def obtener_siguiente_id(self):
        if not self.grupos.items:
            return 1
        return max(grupo.id for grupo in self.grupos.items) + 1
    
    def asignar_alumnos(self, grupo):
        try:
            alumno = Alumno()
            alumnos = alumno.leerJson("alumnos.json")
            if not alumnos.items:
                print("No hay alumnos registrados.")
                return

            print("\nAlumnos disponibles:")
            for alumno in alumnos.items:
                print(f"ID: {alumno.id} - {alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}")

            while True:
                id_alumno = input("Ingrese el ID del alumno a asignar (o presione Enter para terminar): ")
                if id_alumno == "":
                    break

                alumno_encontrado = next((a for a in alumnos.items if str(a.id) == id_alumno), None)
                if alumno_encontrado:
                    grupo.alumnos.items.append(alumno_encontrado)
                    print("Alumno asignado con éxito.")
                else:
                    print("Alumno no encontrado.")
        except FileNotFoundError:
            print("Archivo de alumnos no encontrado.")


    def crearGrupo(self):
        nombre = input("Ingrese el nombre del grupo: ")
        grado = input("Ingrese el grado del grupo: ")
        turno = input("Ingrese el turno del grupo: ")
        salon = input("Ingrese el salón del grupo: ")
        carrera = input("Ingrese la carrera del grupo: ")
        ciclo_escolar = input("Ingrese el ciclo escolar del grupo: ")
        
        try:
            maestro = Maestro()
            maestros = maestro.leerJson("maestros.json")
            if not maestros.items:
                print("No hay maestros registrados. Primero debe registrar maestros.")
                return
            
            print("\nMaestros disponibles:")
            for maestro in maestros.items:
                print(f"ID: {maestro.id} - {maestro.nombre} {maestro.apellido_paterno} {maestro.apellido_materno}")
            
            id_maestro = input("\nIngrese el ID del maestro para el grupo: ")
            maestro_encontrado = next((m for m in maestros.items if str(m.id) == id_maestro), None)
            
            if maestro_encontrado is None:
                print("Maestro no encontrado")
                return
        except FileNotFoundError:
            print("No hay maestros registrados. Primero debe registrar maestros.")
            return
        
        nuevo_id = self.obtener_siguiente_id()
        grupo = Grupo(nombre, grado, turno, salon, carrera, ciclo_escolar, maestro_encontrado, nuevo_id)

        self.asignar_alumnos(grupo)

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
            print(f"Grado: {grupo.grado}")
            print(f"Turno: {grupo.turno}")
            print(f"Salón: {grupo.salon}")
            print(f"Carrera: {grupo.carrera}")
            print(f"Ciclo Escolar: {grupo.ciclo_escolar}")
            if grupo.maestro:
                print(f"Maestro: {grupo.maestro.nombre} {grupo.maestro.apellido_paterno} {grupo.maestro.apellido_materno}")
            print("Alumnos:")
            for alumno in grupo.alumnos.items:
                print(f"  - {alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}")
            print("-" * 50)

    def actualizarGrupo(self):
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
        grupo_encontrado.grado = input(f"Nuevo grado [{grupo_encontrado.grado}]: ") or grupo_encontrado.grado
        grupo_encontrado.turno = input(f"Nuevo turno [{grupo_encontrado.turno}]: ") or grupo_encontrado.turno
        grupo_encontrado.salon = input(f"Nuevo salón [{grupo_encontrado.salon}]: ") or grupo_encontrado.salon
        grupo_encontrado.carrera = input(f"Nueva carrera [{grupo_encontrado.carrera}]: ") or grupo_encontrado.carrera
        grupo_encontrado.ciclo_escolar = input(f"Nuevo ciclo escolar [{grupo_encontrado.ciclo_escolar}]: ") or grupo_encontrado.ciclo_escolar

        try:
            maestro = Maestro()
            maestros = maestro.leerJson("maestros.json")
            if maestros.items:
                print("\nMaestros disponibles:")
                for maestro in maestros.items:
                    print(f"ID: {maestro.id} - {maestro.nombre} {maestro.apellido_paterno} {maestro.apellido_materno}")
                
                id_maestro = input("\nIngrese el ID del nuevo maestro (deje en blanco para mantener el actual): ")
                if id_maestro:
                    maestro_encontrado = None
                    for maestro in maestros.items:
                        if str(maestro.id) == id_maestro:
                            maestro_encontrado = maestro
                            break
                    
                    if maestro_encontrado:
                        grupo_encontrado.maestro = maestro_encontrado
                    else:
                        print("Maestro no encontrado")
        except FileNotFoundError:
            print("No hay maestros registrados")

        if not self.contenedor_proporcionado:
            self.grupos.guardarJson("grupos.json")
            print("Cambios guardados en archivo")
        else:
            print("Los cambios se mantienen en memoria")
        
    def eliminarGrupo(self):
        self.mostrarGrupos()
        id_grupo = input("\nIngrese el ID del grupo a eliminar: ")
        
        for i, grupo in enumerate(self.grupos.items):
            if str(grupo.id) == id_grupo:
                del self.grupos.items[i]
                self.grupos.guardarJson("grupos.json")
                print("Grupo eliminado correctamente")
                return
        
        print("Grupo no encontrado")



    def eliminarAlumnoDeGrupo(self):
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
                self.grupos.guardarJson("grupos.json")
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
            elif opcion == "6":
                self.eliminarAlumnoDeGrupo()
            elif opcion == "7":
                break
            else:
                print("Opción no válida")

if __name__ == "__main__":
    interfaz = InterfazGrupo()
    interfaz.menu_interactivo()

    #contenedor = Arreglo()
    #interfaz = InterfazGrupo(contenedor_grupos=contenedor)
    #interfaz.menu_interactivo()