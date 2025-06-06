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
            lista_alumnos = [item.convertirADiccionario()[0] if hasattr(item, "convertirADiccionario") else item for item in self.items]
            
            if len(lista_alumnos) == 1:
                return lista_alumnos[0]
            else:
                return lista_alumnos
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

        if isinstance(datos, dict):
            if datos.get("tipo") == "Alumno":
                alumno = Alumno(
                    nombre=datos.get("nombre"),
                    apellido_paterno=datos.get("apellido_paterno"),
                    apellido_materno=datos.get("apellido_materno"),
                    edad=datos.get("edad"),
                    matricula=datos.get("matricula"),
                    carrera=datos.get("carrera"),
                    semestre=datos.get("semestre"),
                    promedio=datos.get("promedio"),
                    id=datos.get("id")
                )
                alumnos.items.append(alumno)

        elif isinstance(datos, list): 
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

    def guardarJson(self, archivo):
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(self.convertirADiccionario(), f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    alumnos = Alumno()  

    alumnos = Alumno.leerJson("alumnos.json")
    print(f"Alumnos leídos: {alumnos.cantidad_alumnos()}")

    alumnos.guardarJson("alumnos_guardados.json")
    print("Datos guardados en 'alumnos_guardados.json'")

    
    # print("=== CASO 1: UN SOLO ALUMNO ===")
    # a1 = Alumno("Saul", "Sanchez", "Lopez", 20, "23170093", "Desarrollo y gestion de software", 3, 10, 1)
    # alumnos_uno = Alumno()
    # alumnos_uno.agregar(a1)

    # with open("un_alumno.json", "w", encoding="utf-8") as archivo:
    #     json.dump(alumnos_uno.convertirADiccionario(), archivo, indent=4, ensure_ascii=False)
    # print("Un alumno guardado en un_alumno.json (como diccionario)")

    # print("\n=== CASO 2: VARIOS ALUMNOS ===")
    # a1 = Alumno("Saul", "Sanchez", "Lopez", 20, "23170093", "Desarrollo y gestion de software", 3, 10, 1)
    # a2 = Alumno("Misael", "Trejo", "Perez", 19, "23170115", "Desarrollo y gestion de software", 4, 10, 2)
    # a3 = Alumno("Azael", "Garcia", "Candela", 20, "23170022", "Desarrollo y gestion de software", 2, 10, 3)

    # alumnos_varios = Alumno()
    # alumnos_varios.agregar(a1, a2, a3)

    # with open("varios_alumnos.json", "w", encoding="utf-8") as archivo:
    #     json.dump(alumnos_varios.convertirADiccionario(), archivo, indent=4, ensure_ascii=False)
    # print("Varios alumnos guardados en varios_alumnos.json (como lista de diccionarios)")

    # print("\n=== LEYENDO ARCHIVOS ===")
    # alumnos_leidos_uno = Alumno.leerJson("un_alumno.json")
    # print(f"Un alumno leído: {alumnos_leidos_uno.cantidad_alumnos()} alumno(s)")
    
    # alumnos_leidos_varios = Alumno.leerJson("varios_alumnos.json")
    # print(f"Varios alumnos leídos: {alumnos_leidos_varios.cantidad_alumnos()} alumno(s)")

    