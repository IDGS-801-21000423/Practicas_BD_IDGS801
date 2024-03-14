# ------------------------------------------------
from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField
from wtforms import EmailField, TelField, FloatField, BooleanField, SelectMultipleField, RadioField
# Aqui de los validadores importamos el dato obligatorio y el email
from wtforms import validators

# Formularios para la pizzeria
class clientes(Form):
  id_cliente = IntegerField('id_cliente', [validators.number_range(min=1, max=50, message='Valor no valido')])
  nombre_cliente = StringField('nombre_cliente', validators=[
    validators.DataRequired(message='El nombre es requerido'),
    validators.length(min=4, max=50, message='Requiere min=4, max=50')
  ])
  direccion_cliente = StringField('direccion_cliente', validators=[
    validators.DataRequired(message='La direccion es requerida')
  ])
  telefono_cliente = StringField('telefono_cliente', validators=[
    validators.DataRequired(message='El telefono es requerido')
  ])
