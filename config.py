# Configuracion BD ----------------------------------------------------
import os
from sqlalchemy import create_engine
import urllib

class Config(object):
  SECRET_KEY = 'Clave nueva'          # Clave
  SESSION_COOKIE_SECURE = False       # Conexion a bd, manejo sesiones


class DevelopmentConfig(Config):
  DEBUG=True
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://angel:ramirezangel1234@127.0.0.1/prueba'
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  

class DevelopmentConfigPizza(Config):
  DEBUG=True
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://angel:ramirezangel1234@127.0.0.1/pizzeria'
  SQLALCHEMY_TRACK_MODIFICATIONS=False