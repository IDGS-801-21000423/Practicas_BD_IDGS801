from flask_sqlalchemy import SQLAlchemy
import datetime                         # funcion para crear tabla

db = SQLAlchemy()
""" 
class Alumnos(db.Model):
  __tablename__ = 'alumnos'                       # nombre a tabla
  id = db.Column(db.Integer, primary_key = True)  # llave primaria tipo entero (necesario siempre)
  nombre = db.Column(db.String(50))               # columnas varchar =  string
  apaterno = db.Column(db.String(50))
  email = db.Column(db.String(50))
  created_date = db.Column(db.DateTime, default = datetime.datetime.now)  # columna de tipo fecha
 """  
class Empleados(db.Model):
  __tablename__ = 'empleados'
  id = db.Column(db.Integer, primary_key = True)
  nombre = db.Column(db.String(50))
  direccion = db.Column(db.String(50))
  telefono = db.Column(db.String(15))
  email = db.Column(db.String(50))
  sueldo = db.Column(db.Float)
  created_date = db.Column(db.DateTime, default = datetime.datetime.now)
  