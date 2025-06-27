from arreglo import Arreglo
from alumno import Alumno
from maestro import Maestro
import json
from mongodb_manager import MongoDBManager

class Grupo(Arreglo):
    def __init__(self, nombre=None, grado=None, turno=None, salon=None, 
                carrera=None, ciclo_escolar=None, maestro=None, id=None):
        if nombre is None and grado is None and turno is None and salon is None and \
           carrera is None and ciclo_escolar is None and maestro is None and id is None:
            Arreglo.__init__(self)
            self.es_contenedor = True
            self.mongo_manager = MongoDBManager()
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
            lista_grupos = [item.convertirADiccionario() if hasattr(item, "convertirADiccionario") else item for item in self.items]
            
            grupos_planos = []
            for grupo in lista_grupos:
                if isinstance(grupo, list):
                    grupos_planos.extend(grupo)
                else:
                    grupos_planos.append(grupo)
            
            if len(grupos_planos) == 1:
                return grupos_planos[0]
            else:
                return grupos_planos
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
    
    
    def leerJson(self, archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return Grupo.desde_json(datos)

    
    def desde_json(self, datos):
        grupos = Grupo()
        
        if isinstance(datos, dict):
            if datos.get("tipo") == "Grupo":
                maestro = None
                if datos.get("maestro"):
                    maestro_data = datos["maestro"]
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
                    nombre=datos.get("nombre"),
                    grado=datos.get("grado"),
                    turno=datos.get("turno"),
                    salon=datos.get("salon"),
                    carrera=datos.get("carrera"),
                    ciclo_escolar=datos.get("ciclo_escolar"),
                    maestro=maestro,
                    id=datos.get("id")
                )
                
                if datos.get("alumnos"):
                    for alumno_data in datos["alumnos"]:
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
        
        elif isinstance(datos, list):
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

    def guardarJson(self, archivo):
        datos = self.convertirADiccionario()
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        
        if self.es_contenedor:
            self.mongo_manager.guardar(archivo, datos, "grupos")

    
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
    grupos = Grupo()  
    grupos = grupos.leerJson("grupos.json")
    grupos.guardarJson("grupos_guardados.json")