from . import db
from . import bcrypt


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    direccion = db.Column(db.String, nullable=True)
    edad = db.Column(db.Integer, nullable=True)

    def __init__(self, **kwargs):
        super(Usuario, self).__init__(**kwargs)
        self.password = self.generar_password(**kwargs)

    def generar_password(self, **kwargs):
        if 'password' not in kwargs:
            return None

        return bcrypt.generate_password_hash(kwargs['password']).decode()
