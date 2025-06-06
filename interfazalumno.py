from alumno import Alumno
import json

class InterfazAlumno:
    def __init__(self, contenedor_alumnos=None):
        if contenedor_alumnos is None:
            self.alumnos = Alumno()  
        else:
            self.alumnos = contenedor_alumnos

    def crear_alumno(self, nombre, apellido_paterno, apellido_materno, edad, matricula, carrera, semestre, promedio, id=None):
        """Crea un nuevo alumno y lo agrega al contenedor"""
        try:
            nuevo_alumno = Alumno(
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                edad=edad,
                matricula=matricula,
                carrera=carrera,
                semestre=semestre,
                promedio=promedio,
                id=id
            )
            self.alumnos.agregar(nuevo_alumno)
            print(f"✓ Alumno {nombre} {apellido_paterno} creado exitosamente.")
            return nuevo_alumno
        except Exception as e:
            print(f"✗ Error al crear alumno: {e}")
            return None

    def mostrar_todos_los_alumnos(self):
        """Muestra información de todos los alumnos"""
        if self.alumnos.cantidad_alumnos() == 0:
            print("No hay alumnos registrados.")
            return
        
        print(f"\n=== LISTA DE ALUMNOS ({self.alumnos.cantidad_alumnos()}) ===")
        for i, alumno in enumerate(self.alumnos.items, 1):
            print(f"\n{i}. {alumno}")

    def buscar_alumno_por_matricula(self, matricula):
        """Busca un alumno por su matrícula"""
        for alumno in self.alumnos.items:
            if alumno.matricula == matricula:
                return alumno
        return None

    def buscar_alumno_por_id(self, id):
        """Busca un alumno por su ID"""
        for alumno in self.alumnos.items:
            if alumno.id == id:
                return alumno
        return None

    def mostrar_alumno_por_matricula(self, matricula):
        """Muestra información de un alumno específico por matrícula"""
        alumno = self.buscar_alumno_por_matricula(matricula)
        if alumno:
            print(f"\n=== INFORMACIÓN DEL ALUMNO ===")
            print(alumno)
        else:
            print(f"✗ No se encontró alumno con matrícula: {matricula}")

    def actualizar_alumno(self, matricula, **kwargs):
        """Actualiza información de un alumno por matrícula"""
        alumno = self.buscar_alumno_por_matricula(matricula)
        if not alumno:
            print(f"✗ No se encontró alumno con matrícula: {matricula}")
            return False

        campos_actualizados = []
        if 'nombre' in kwargs and kwargs['nombre']:
            alumno.nombre = kwargs['nombre']
            campos_actualizados.append('nombre')
        if 'apellido_paterno' in kwargs and kwargs['apellido_paterno']:
            alumno.apellido_paterno = kwargs['apellido_paterno']
            campos_actualizados.append('apellido_paterno')
        if 'apellido_materno' in kwargs and kwargs['apellido_materno']:
            alumno.apellido_materno = kwargs['apellido_materno']
            campos_actualizados.append('apellido_materno')
        if 'edad' in kwargs and kwargs['edad']:
            alumno.edad = kwargs['edad']
            campos_actualizados.append('edad')
        if 'nueva_matricula' in kwargs and kwargs['nueva_matricula']:
            alumno.actualizarMatricula(kwargs['nueva_matricula'])
            campos_actualizados.append('matrícula')
        if 'carrera' in kwargs and kwargs['carrera']:
            alumno.carrera = kwargs['carrera']
            campos_actualizados.append('carrera')
        if 'semestre' in kwargs and kwargs['semestre']:
            alumno.semestre = kwargs['semestre']
            campos_actualizados.append('semestre')
        if 'promedio' in kwargs and kwargs['promedio']:
            alumno.promedio = kwargs['promedio']
            campos_actualizados.append('promedio')

        if campos_actualizados:
            print(f"✓ Alumno actualizado. Campos modificados: {', '.join(campos_actualizados)}")
            return True
        else:
            print("No se proporcionaron campos válidos para actualizar.")
            return False

    def eliminar_alumno_por_matricula(self, matricula):
        """Elimina un alumno por su matrícula"""
        alumno = self.buscar_alumno_por_matricula(matricula)
        if not alumno:
            print(f"✗ No se encontró alumno con matrícula: {matricula}")
            return False

        nombre_completo = f"{alumno.nombre} {alumno.apellido_paterno} {alumno.apellido_materno}"
        
        try:
            self.alumnos.items.remove(alumno)
            print(f"✓ Alumno {nombre_completo} eliminado exitosamente.")
            return True
        except Exception as e:
            print(f"✗ Error al eliminar alumno: {e}")
            return False

    def eliminar_todos_los_alumnos(self):
        """Elimina todos los alumnos del contenedor"""
        cantidad = self.alumnos.cantidad_alumnos()
        if cantidad == 0:
            print("No hay alumnos para eliminar.")
            return False
        
        confirmacion = input(f"¿Estás seguro de eliminar {cantidad} alumno(s)? (s/n): ").lower()
        if confirmacion == 's' or confirmacion == 'si':
            self.alumnos.items.clear()
            print(f"✓ {cantidad} alumno(s) eliminado(s) exitosamente.")
            return True
        else:
            print("Operación cancelada.")
            return False

    def cargar_desde_archivo(self, archivo):
        """Carga alumnos desde un archivo JSON"""
        try:
            self.alumnos = Alumno.leerJson(archivo)
            print(f"✓ {self.alumnos.cantidad_alumnos()} alumno(s) cargado(s) desde {archivo}")
        except Exception as e:
            print(f"✗ Error al cargar archivo {archivo}: {e}")

    def guardar_en_archivo(self, archivo):
        """Guarda alumnos en un archivo JSON"""
        try:
            self.alumnos.guardarJson(archivo)
            print(f"✓ {self.alumnos.cantidad_alumnos()} alumno(s) guardado(s) en {archivo}")
        except Exception as e:
            print(f"✗ Error al guardar archivo {archivo}: {e}")

    def obtener_estadisticas(self):
        """Obtiene estadísticas de los alumnos"""
        if self.alumnos.cantidad_alumnos() == 0:
            print("No hay alumnos para mostrar estadísticas.")
            return

        promedios = [alumno.promedio for alumno in self.alumnos.items if alumno.promedio is not None]
        carreras = {}
        
        for alumno in self.alumnos.items:
            if alumno.carrera in carreras:
                carreras[alumno.carrera] += 1
            else:
                carreras[alumno.carrera] = 1

        print(f"\n=== ESTADÍSTICAS ===")
        print(f"Total de alumnos: {self.alumnos.cantidad_alumnos()}")
        if promedios:
            print(f"Promedio general: {sum(promedios) / len(promedios):.2f}")
            print(f"Promedio más alto: {max(promedios)}")
            print(f"Promedio más bajo: {min(promedios)}")
        
        print(f"\nAlumnos por carrera:")
        for carrera, cantidad in carreras.items():
            print(f"  {carrera}: {cantidad}")

    def menu_interactivo(self):
        """Menu interactivo para el CRUD"""
        while True:
            print(f"\n{'='*50}")
            print("           SISTEMA DE GESTIÓN DE ALUMNOS")
            print(f"         Alumnos registrados: {self.alumnos.cantidad_alumnos()}")
            print(f"{'='*50}")
            print("1. Crear nuevo alumno")
            print("2. Mostrar todos los alumnos")
            print("3. Buscar alumno por matrícula")
            print("4. Actualizar información de alumno")
            print("5. Eliminar alumno por matrícula")
            print("6. Eliminar todos los alumnos")
            print("7. Cargar alumnos desde archivo")
            print("8. Guardar alumnos en archivo")
            print("9. Mostrar estadísticas")
            print("0. Salir")
            print(f"{'='*50}")

            try:
                opcion = input("Seleccione una opción (0-9): ").strip()
                
                if opcion == "1":
                    self.menu_crear_alumno()
                elif opcion == "2":
                    self.mostrar_todos_los_alumnos()
                elif opcion == "3":
                    matricula = input("Ingrese la matrícula a buscar: ").strip()
                    self.mostrar_alumno_por_matricula(matricula)
                elif opcion == "4":
                    self.menu_actualizar_alumno()
                elif opcion == "5":
                    matricula = input("Ingrese la matrícula del alumno a eliminar: ").strip()
                    self.eliminar_alumno_por_matricula(matricula)
                elif opcion == "6":
                    self.eliminar_todos_los_alumnos()
                elif opcion == "7":
                    archivo = input("Ingrese el nombre del archivo a cargar: ").strip()
                    self.cargar_desde_archivo(archivo)
                elif opcion == "8":
                    archivo = input("Ingrese el nombre del archivo donde guardar: ").strip()
                    self.guardar_en_archivo(archivo)
                elif opcion == "9":
                    self.obtener_estadisticas()
                elif opcion == "0":
                    print("¡Hasta luego!")
                    break
                else:
                    print("✗ Opción no válida. Por favor, seleccione una opción del 0 al 9.")
                    
                input("\nPresione Enter para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego!")
                break
            except Exception as e:
                print(f"✗ Error inesperado: {e}")

    def menu_crear_alumno(self):
        """Submenú para crear un alumno"""
        print("\n=== CREAR NUEVO ALUMNO ===")
        try:
            nombre = input("Nombre: ").strip()
            apellido_paterno = input("Apellido Paterno: ").strip()
            apellido_materno = input("Apellido Materno: ").strip()
            edad = int(input("Edad: "))
            matricula = input("Matrícula: ").strip()
            carrera = input("Carrera: ").strip()
            semestre = int(input("Semestre: "))
            promedio = float(input("Promedio: "))
            id_input = input("ID (opcional, presione Enter para omitir): ").strip()
            id_alumno = int(id_input) if id_input else None
            
            self.crear_alumno(nombre, apellido_paterno, apellido_materno, edad, 
                            matricula, carrera, semestre, promedio, id_alumno)
        except ValueError as e:
            print(f"✗ Error en los datos ingresados: {e}")
        except Exception as e:
            print(f"✗ Error al crear alumno: {e}")

    def menu_actualizar_alumno(self):
        """Submenú para actualizar un alumno"""
        print("\n=== ACTUALIZAR ALUMNO ===")
        matricula = input("Ingrese la matrícula del alumno a actualizar: ").strip()
        
        alumno = self.buscar_alumno_por_matricula(matricula)
        if not alumno:
            print(f"✗ No se encontró alumno con matrícula: {matricula}")
            return
        
        print(f"\nAlumno encontrado: {alumno}")
        print("\nDeje en blanco los campos que no desea modificar:")
        
        try:
            campos = {}
            nuevo_nombre = input(f"Nuevo nombre [{alumno.nombre}]: ").strip()
            if nuevo_nombre:
                campos['nombre'] = nuevo_nombre
                
            nuevo_ap_paterno = input(f"Nuevo apellido paterno [{alumno.apellido_paterno}]: ").strip()
            if nuevo_ap_paterno:
                campos['apellido_paterno'] = nuevo_ap_paterno
                
            nuevo_ap_materno = input(f"Nuevo apellido materno [{alumno.apellido_materno}]: ").strip()
            if nuevo_ap_materno:
                campos['apellido_materno'] = nuevo_ap_materno
                
            nueva_edad = input(f"Nueva edad [{alumno.edad}]: ").strip()
            if nueva_edad:
                campos['edad'] = int(nueva_edad)
                
            nueva_matricula = input(f"Nueva matrícula [{alumno.matricula}]: ").strip()
            if nueva_matricula:
                campos['nueva_matricula'] = nueva_matricula
                
            nueva_carrera = input(f"Nueva carrera [{alumno.carrera}]: ").strip()
            if nueva_carrera:
                campos['carrera'] = nueva_carrera
                
            nuevo_semestre = input(f"Nuevo semestre [{alumno.semestre}]: ").strip()
            if nuevo_semestre:
                campos['semestre'] = int(nuevo_semestre)
                
            nuevo_promedio = input(f"Nuevo promedio [{alumno.promedio}]: ").strip()
            if nuevo_promedio:
                campos['promedio'] = float(nuevo_promedio)
            
            self.actualizar_alumno(matricula, **campos)
            
        except ValueError as e:
            print(f"✗ Error en los datos ingresados: {e}")
        except Exception as e:
            print(f"✗ Error al actualizar alumno: {e}")


if __name__ == "__main__":
    interfaz = InterfazAlumno()
    
    try:
        interfaz.cargar_desde_archivo("alumnos.json")
    except:
        print("No se encontró archivo de alumnos existente. Iniciando con lista vacía.")
    
    interfaz.menu_interactivo()