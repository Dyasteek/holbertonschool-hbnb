from datetime import datetime
from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if not first_name or len(first_name) > 50:
            raise ValueError("El nombre es obligatorio y no puede superar los 50 caracteres")
        if not last_name or len(last_name) > 50:
            raise ValueError("El apellido es obligatorio y no puede superar los 50 caracteres")
        if not email or "@" not in email:
            raise ValueError("Debe proporcionar un correo electrónico válido")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
