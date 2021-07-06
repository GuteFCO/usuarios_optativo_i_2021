from sqlalchemy.orm import load_only
from marshmallow import post_load
from . import ma
from .models import Usuario


class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_only = ('password',)
        load_instance = True

    @post_load
    def update_password(self, model, **kwargs):
        if model.id:
            model.password = model.generar_password(password=model.password)

        return model




