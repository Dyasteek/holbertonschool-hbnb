import uuid
from datetime import datetime

class BaseModel:
    """Clase base que define atributos comunes (id, created_at, updated_at)"""

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Actualiza la marca de tiempo cuando se modifica el objeto"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Actualiza los atributos del objeto según un diccionario"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
