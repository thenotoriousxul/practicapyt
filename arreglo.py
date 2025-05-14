class Arreglo:
    def __init__(self):
        self.items = []

    def agregar(self, item):
        self.items.append(item)

    def eliminar(self, item=None, indice=None):
        try:
            if indice is not None:
                del self.items[indice]
            else:
                self.items.remove(item)
            return True
        except (IndexError, ValueError):
            return False
    
    def actualizar(self, id, **nuevos_valores):
        for elem in self.items:
            if hasattr(elem, 'id') and elem.id == id:
                for attr, val in nuevos_valores.items():
                    setattr(elem, attr, val)
                return True
        return False
    
    def obtener(self, indice=None):
        if indice is not None:
            try:
                return self.items[indice]
            except IndexError:
                return None
        return self.items

    
