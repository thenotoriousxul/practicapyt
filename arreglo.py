class Arreglo:
    def __init__(self):
        self.items = []
    
    def agregar(self, *items):
        for item in items:
            if hasattr(item, "convertirADiccionario"):
                self.items.append(item.convertirADiccionario())
            else:
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
    
    def actualizar(self, objeto, atributo, nuevo_valor):
        if hasattr(objeto, "convertirADiccionario"):
            objeto_dict = objeto.convertirADiccionario()
            for i, elem in enumerate(self.items):
                if isinstance(elem, dict) and elem.get('id') == objeto_dict.get('id'):
                    self.items[i][atributo] = nuevo_valor
                    setattr(objeto, atributo, nuevo_valor)
                    return True
        else:
            for elem in self.items:
                if elem == objeto:
                    if hasattr(elem, atributo):
                        setattr(elem, atributo, nuevo_valor)
                        return True
        return False
    
    def obtener(self, indice=None):
        if indice is not None:
            try:
                return self.items[indice]
            except IndexError:
                return None
        return self.items
    
    def __str__(self):
        if not self.items:
            return "No hay elementos"
        return str(len(self.items))
    
    