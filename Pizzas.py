# ------------------------------------------------
from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField
from wtforms import EmailField, TelField, FloatField, BooleanField, SelectMultipleField, RadioField, DateTimeField

# Aqui de los validadores importamos el dato obligatorio y el email
from wtforms import validators

class pizzas(Form):
  id_pizza = IntegerField('id_pizza', [validators.number_range(min=1, max=50, message='Valor no valido')])
  tamanio_pizza = RadioField('tamanio_pizza', choices=[
    (1, "Chica"),
    (2, "Mediana"),
    (3, "Grande")
  ])
  jamon = BooleanField('Jamon', default=False)
  pina = BooleanField('Piña', default=False)
  champinones = BooleanField('Champiñones', default=False)
  numero_pizza = IntegerField('numero_pizza', [validators.number_range(min=1, max=50, message='Valor no valido')])
  subtotal_pizza = FloatField('subtotal')
  fecha_de_compra = DateTimeField('fecha_de_compra')
