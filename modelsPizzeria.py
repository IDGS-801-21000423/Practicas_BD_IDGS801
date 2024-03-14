from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import datetime                         # funcion para crear tabla

db = SQLAlchemy()


class ClientesPizzeria(db.Model):
  __tablename__ = 'clientes_pizzeria'
  id_cliente = db.Column(db.Integer, primary_key = True)
  nombre_cliente = db.Column(db.String(50))
  direccion_cliente = db.Column(db.String(50))
  telefono_cliente = db.Column(db.String(15))
  
  # Relacion inversa
  pizzas = relationship('PizzasPizzeria', back_populates='cliente')


class PizzasPizzeria(db.Model):
  __tablename__ = 'detalle_pizza'
  id_pizza  = db.Column(db.Integer, primary_key = True)
  tamanio_pizza = db.Column(db.String(50))
  ingredientes_pizza = db.Column(db.String(50))
  numero_pizza = db.Column(db.Integer)
  subtotal_pizza = db.Column(db.Float)
  fecha_de_compra = db.Column(db.Date)
  #fecha_de_compra = db.Column(db.DateTime, default = datetime.datetime.now)
  
  # Especificar la relacion como clave foranea con la tabla clientes_pizzeria
  id_cliente_pz = db.Column(db.Integer, ForeignKey('clientes_pizzeria.id_cliente'))
  
  # Definir la relacion con la tabla 'clientes_pizzeria'
  cliente = relationship('ClientesPizzeria', back_populates='pizzas')
  
  #subtotal = db.Column(db.Float)
  
