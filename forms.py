# ------------------------------------------------
from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField
from wtforms import EmailField, TelField, FloatField
# Aqui de los validadores importamos el dato obligatorio y el email
from wtforms import validators

"""   
class UserForm2(Form):
  id = IntegerField('id', [validators.number_range(min=1, max=20, message='Valor no valido')])
  nombre = StringField('nombre', validators=[
    validators.DataRequired(message='El nombre es requerido'),
    validators.length(min=4, max=20, message='Requiere min=4, max=10')
  ])
  apaterno = StringField('apaterno', validators=[
    validators.DataRequired(message='El apellido es requerido')
  ])
  email = EmailField('correo', validators=[ 
    validators.Email(message='El email es requerido')
  ])
 """
class EmployeesForm(Form):
  id = IntegerField('id', [validators.number_range(min=1, max=20, message='Valor no valido')])
  nombre = StringField('nombre', validators=[
    validators.DataRequired(message='El nombre es requerido'),
    validators.length(min=4, max=20, message='Requiere min=4, max=20')
  ])
  direccion = StringField('direccion', validators=[
    validators.DataRequired(message='La direccion es requerida')
  ])
  email = EmailField('email', validators=[ 
    validators.Email(message='El email es requerido')
  ])
  telefono = StringField('telefono', validators=[
    validators.DataRequired(message='El telefono es requerido')
  ])
  sueldo = FloatField('sueldo', validators=[
    validators.DataRequired(message='El sueldo es requerido')
  ])
  
