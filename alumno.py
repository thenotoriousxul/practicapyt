from arreglo import Arreglo
import json

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
    
    def convertirADiccionario(self):
        if self.es_contenedor:
            return [item.convertirADiccionario()[0] if hasattr(item, "convertirADiccionario") else item for item in self.items]
        else:
            alumno_dict = {
                "id": self.id,
                "nombre": self.nombre,
                "apellido_paterno": self.apellido_paterno,
                "apellido_materno": self.apellido_materno,
                "edad": self.edad,
                "matricula": self.matricula,
                "carrera": self.carrera,
                "semestre": self.semestre,
                "promedio": self.promedio,
                "tipo": "Alumno"
            }
            
            return [alumno_dict]
    
    def leerJson(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
        return Alumno.desde_json(datos)
    
    def desde_json(datos):
        alumnos = Alumno()
        for item in datos:
            if isinstance(item, dict) and item.get("tipo") == "Alumno":
                alumno = Alumno(
                    nombre=item.get("nombre"),
                    apellido_paterno=item.get("apellido_paterno"),
                    apellido_materno=item.get("apellido_materno"),
                    edad=item.get("edad"),
                    matricula=item.get("matricula"),
                    carrera=item.get("carrera"),
                    semestre=item.get("semestre"),
                    promedio=item.get("promedio"),
                    id=item.get("id")
                )
                alumnos.items.append(alumno)
        return alumnos

    
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
    a2 = Alumno("Misael", "Trejo", "Perez", 19, "23170115", "Desarrollo y gestion de software", 4, 10, 2)
    a3 = Alumno("Azael", "Garcia", "Candela", 20, "23170022", "Desarrollo y gestion de software", 2, 10, 3)
    
    alumnos = Alumno()
    alumnos.agregar(a1, a2, a3)
    
    print("=== GUARDANDO ALUMNOS ===")
    with open("alumnos.json", "w", encoding="utf-8") as archivo:
        json.dump(alumnos.convertirADiccionario(), archivo, indent=4, ensure_ascii=False)
    print("Alumnos guardados en alumnos.json")
    
    print("\n=== LEYENDO ALUMNOS ===")
    alumnos_leidos = Alumno.leerJson("alumnos.json")
    print("Alumnos leídos del archivo:")
    for alumno_leido in alumnos_leidos.items:
        print(alumno_leido)
    
    print(f"\nCantidad de alumnos leídos: {alumnos_leidos.cantidad_alumnos()}")