from arreglo import Arreglo
from alumno import Alumno
from maestro import Maestro
import json

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
    
    def convertirADiccionario(self):
        if self.es_contenedor:
            return [item.convertirADiccionario() if hasattr(item, "convertirADiccionario") else item for item in self.items]
        else:
            maestro_dict = self.maestro.convertirADiccionario()[0] if self.maestro and hasattr(self.maestro, "convertirADiccionario") else None
            alumnos_list = []
            if hasattr(self.alumnos, "items"):
                for alumno in self.alumnos.items:
                    if isinstance(alumno, dict):
                        alumnos_list.append(alumno)
                    elif hasattr(alumno, "convertirADiccionario"):
                        alumnos_list.append(alumno.convertirADiccionario()[0])
                    else:
                        alumnos_list.append(alumno)
            
            grupo_dict = {
                "id": self.id,
                "nombre": self.nombre,
                "grado": self.grado,
                "turno": self.turno,
                "salon": self.salon,
                "carrera": self.carrera,
                "ciclo_escolar": self.ciclo_escolar,
                "maestro": maestro_dict,
                "alumnos": alumnos_list,
                "tipo": "Grupo"
            }
            
            return [grupo_dict]
    
    def leerJson(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return Grupo.desde_json(datos)
        

    def desde_json(datos):
        grupos = Grupo()
        
        for item in datos:
            if isinstance(item, dict) and item.get("tipo") == "Grupo":
                maestro = None
                if item.get("maestro"):
                    maestro_data = item["maestro"]
                    maestro = Maestro(
                        nombre=maestro_data.get("nombre"),
                        apellido_paterno=maestro_data.get("apellido_paterno"),
                        apellido_materno=maestro_data.get("apellido_materno"),
                        edad=maestro_data.get("edad"),
                        clave=maestro_data.get("clave"),
                        carrera=maestro_data.get("carrera"),
                        materia=maestro_data.get("materia"),
                        id=maestro_data.get("id")
                    )
                
                grupo = Grupo(
                    nombre=item.get("nombre"),
                    grado=item.get("grado"),
                    turno=item.get("turno"),
                    salon=item.get("salon"),
                    carrera=item.get("carrera"),
                    ciclo_escolar=item.get("ciclo_escolar"),
                    maestro=maestro,
                    id=item.get("id")
                )
                
                if item.get("alumnos"):
                    for alumno_data in item["alumnos"]:
                        if isinstance(alumno_data, dict):
                            alumno = Alumno(
                                nombre=alumno_data.get("nombre"),
                                apellido_paterno=alumno_data.get("apellido_paterno"),
                                apellido_materno=alumno_data.get("apellido_materno"),
                                edad=alumno_data.get("edad"),
                                matricula=alumno_data.get("matricula"),
                                carrera=alumno_data.get("carrera"),
                                semestre=alumno_data.get("semestre"),
                                promedio=alumno_data.get("promedio"),
                                id=alumno_data.get("id")
                            )
                            grupo.alumnos.items.append(alumno)
                
                grupos.items.append(grupo)
        
        return grupos
    
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
    a3 = Alumno("Carlos", "Ramírez", "López", 20, "23170130", "TI", 2, 10, 3)
    a4 = Alumno("Fernanda", "Gomez", "Vega", 21, "23170133", "TI", 2, 10, 4)
    a5 = Alumno("Luis", "Perez", "Cruz", 22, "23170144", "TI", 1, 10, 5)
    a6 = Alumno("Sofia", "Lopez", "Ramos", 20, "23170148", "TI", 1, 10, 6)

    m1 = Maestro("Ramiro", "Esquivel", "Nuñez", 40, "M001", "TI", "Aplicaciones Web", 1)
    m2 = Maestro("María", "Hernández", "Silva", 38, "M002", "TI", "Base de Datos", 2)

    grupo1 = Grupo("Desarrollo Web", "Tercero", "Matutino", "301", "TI", "2023-2024", m1, 1)
    grupo1.alumnos.items.append(a1)
    grupo1.alumnos.items.append(a2)

    grupo2 = Grupo("Base de Datos", "Segundo", "Vespertino", "201", "TI", "2023-2024", m2, 2)
    grupo2.alumnos.items.append(a3)
    grupo2.alumnos.items.append(a4)

    grupo3 = Grupo("Redes", "Primero", "Matutino", "101", "TI", "2023-2024", m2, 3)
    grupo3.alumnos.items.append(a5)
    grupo3.alumnos.items.append(a6)

    print("=== GUARDANDO GRUPOS ===")
    todos_los_grupos = Arreglo()
    todos_los_grupos.items.append(grupo1)
    todos_los_grupos.items.append(grupo2)
    todos_los_grupos.items.append(grupo3)

    with open("grupos.json", "w", encoding="utf-8") as archivo:
        json.dump([dic for g in todos_los_grupos.items for dic in g.convertirADiccionario()], archivo, indent=4, ensure_ascii=False)
    print("Grupos guardados en grupos.json")

    print("\n=== LEYENDO GRUPOS ===")
    grupos_leidos = Grupo.leerJson("grupos.json")
    print("Grupos leídos del archivo:")
    for grupo_leido in grupos_leidos.items:
        print(f"\nGrupo: {grupo_leido}")
        print("Alumnos en el grupo:")
        for alumno in grupo_leido.alumnos.items:
            print(f"  - {alumno}")
        if grupo_leido.maestro:
            print(f"Maestro del grupo: {grupo_leido.maestro}")
