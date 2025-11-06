from app.Models.Dia import Dia

class DiasController:
    
    def __init__(self):
        pass
    
    def get_dias(self):
        return Dia.all()