from datetime import datetime

class Tarea:

    def __init__(self,titulo:str,contenido:str,creada:datetime,vencimiento:int,realizada:bool,caducada:bool):
        self.titulo = titulo,
        self.contenido = contenido,
        self.creada = creada,
        self.vencimiento = vencimiento,
        self.realizada = realizada,
        self.caducada = caducada



