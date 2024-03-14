# --------------------------------------------------------------
from flask import Flask, render_template, request, url_for, redirect     # Importar flask, render template
import forms                                          # Importar archivo forms
import Clientes
from collections import defaultdict
import Pizzas
from sqlalchemy import extract, text
from datetime import datetime
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g                                   # Importar variables globales
from config import DevelopmentConfig
from config import DevelopmentConfigPizza
from models import db                                 # crear instancia de clase bd
from modelsPizzeria import db
from models import Empleados
from flask import session
from modelsPizzeria import ClientesPizzeria
from modelsPizzeria import PizzasPizzeria
from sqlalchemy import func
app = Flask(__name__)                                 # Nombrar la app Flask
#app.config.from_object(DevelopmentConfig)
app.config.from_object(DevelopmentConfigPizza)
csrf = CSRFProtect()
app.secret_key = 'clave segura'

# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# Manejo de errores - mostrar pagina
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'),404

@app.route("/")         
def indexado():
  return render_template("index.html") #pagina1
""" 
@app.route("/alumnos", methods = ['GET', 'POST'])         
def alumnos():
  nom=""
  apa=""
  ama=""
  email=""
  edad=""
  alumno_clase = forms.UserForm(request.form)
  if request.method == 'POST' and alumno_clase.validate():
    nom = alumno_clase.nombre.data
    apa = alumno_clase.apaterno.data
    ama = alumno_clase.amaterno.data
    email = alumno_clase.email.data
    edad = alumno_clase.edad.data
    print("Nombre: {}".format(nom))
    print("Apaterno: {}".format(apa))
    print("Amaterno: {}".format(ama))
    print("Email: {}".format(email))
    print("Edad: {}".format(edad))
    
    mensaje='Bienvenido {}'.format(nom)
    flash(mensaje)
  
  return render_template("alumnos.html", form = alumno_clase,nom=nom,apa=apa,ama=ama, email=email, edad=edad)
"""

# Crear Empleados e insertar en BD
@app.route("/indexEmpleado", methods=['GET', 'POST'])
def indexEmpleado():
  create_form = forms.EmployeesForm(request.form)
  if request.method == 'POST':
    emp = Empleados(
      nombre = create_form.nombre.data,
      direccion = create_form.direccion.data,
      telefono = create_form.telefono.data,
      email = create_form.email.data,
      sueldo = create_form.sueldo.data
      )
    # insert empleados() values()
    db.session.add(emp)
    db.session.commit()
  return render_template("index.html", form=create_form)

# Mostrar Empleados
@app.route("/ABC_Completo_Emp", methods=['GET', 'POST'])
def ABCompleto():
  emp_form = forms.EmployeesForm(request.form)
  empleado = Empleados.query.all()
  
  return render_template("ABC_Completo_Emp.html", empleado=empleado)

# Eliminar Empleados
@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar_emp():
  create_form = forms.EmployeesForm(request.form)
  
  if request.method == 'GET':
    id = request.args.get('id')
    
    # select * from empleados where id == id
    
    emp1 = db.session.query(Empleados).filter(Empleados.id == id).first()
    
    create_form.id.data = request.args.get('id')
    create_form.nombre.data = emp1.nombre
    create_form.direccion.data = emp1.direccion
    create_form.email.data = emp1.email
    create_form.telefono.data = emp1.telefono
    create_form.sueldo.data = emp1.sueldo
  
  if request.method == 'POST':
    id = create_form.id.data
    emp = Empleados.query.get(id)
    
    # delete from empleados where id = id
    
    db.session.delete(emp)
    db.session.commit()
    return redirect(url_for('ABCompleto'))
  return render_template('eliminar.html', form=create_form)

# Modificar Empleados
@app.route('/modificar', methods=['GET', 'POST'])
def modificar():
  create_form = forms.EmployeesForm(request.form)
  
  if request.method == 'GET':
    id = request.args.get('id')
    
    # select * from empleados where id == id
    
    emp1 = db.session.query(Empleados).filter(Empleados.id == id).first()
    
    create_form.id.data = request.args.get('id')
    create_form.nombre.data = emp1.nombre
    create_form.direccion.data = emp1.direccion
    create_form.email.data = emp1.email
    create_form.telefono.data = emp1.telefono
    create_form.sueldo.data = emp1.sueldo
  
  if request.method == 'POST':
    id = create_form.id.data
    
    emp1 = db.session.query(Empleados).filter(Empleados.id == id).first()
    
    emp1.nombre = create_form.nombre.data
    emp1.direccion = create_form.direccion.data
    emp1.email = create_form.email.data
    emp1.telefono = create_form.telefono.data
    emp1.sueldo = create_form.sueldo.data
    
    # update from empleados where id == id
    
    db.session.add(emp1)
    db.session.commit()
    return redirect(url_for('ABCompleto'))
  return render_template('modificar.html', form=create_form)




@app.route("/clientes", methods=['GET', 'POST'])
def detalles_cliente():
  ingredientes= []
  costo_tamanio = 0
  costo_ingredientes = 0
  pizzas_cliente_actual = 0
  create_form_cl = Clientes.clientes(request.form)
  create_form_pz = Pizzas.pizzas(request.form)
  if request.method == 'POST':
    id_eliminar = request.form.get('eliminar_pizza')
    if id_eliminar:
      pizza = PizzasPizzeria.query.get(id_eliminar)
      if pizza:
        db.session.delete(pizza)
        db.session.commit()
    else:
      clPizza = ClientesPizzeria(
        nombre_cliente = create_form_cl.nombre_cliente.data,
        direccion_cliente = create_form_cl.direccion_cliente.data,
        telefono_cliente = create_form_cl.telefono_cliente.data,
      )
    
      # verificar si el cliente ya existe en la tabla clientes
      cliente_existente = (
        db.session.query(ClientesPizzeria)
        .filter(
          ClientesPizzeria.nombre_cliente == create_form_cl.nombre_cliente.data,
          ClientesPizzeria.direccion_cliente == create_form_cl.direccion_cliente.data,
          ClientesPizzeria.telefono_cliente == create_form_cl.telefono_cliente.data
        )
        .first()
      )
    
      if cliente_existente:
        session['id_cliente'] = cliente_existente.id_cliente
        #id_cliente_nuevo = cliente_existente.id_cliente
      else:
        #insertar nuevo id y obtenerlo
        db.session.add(clPizza)
        db.session.commit()
        session['id_cliente'] = clPizza.id_cliente
    
        # Calcular costo por tamaño
    
      if create_form_pz.tamanio_pizza.data == 'Chica':
        costo_tamanio = 40
      elif create_form_pz.tamanio_pizza.data == 'Mediana':
        costo_tamanio = 80
      elif create_form_pz.tamanio_pizza.data == 'Grande':
        costo_tamanio = 120
    
      if create_form_pz.jamon.data:
        ingredientes.append('jamon')
      if create_form_pz.pina.data:
        ingredientes.append('piña')
      if create_form_pz.champinones.data:
        ingredientes.append('champiñones')
    
      if 'jamon' in ingredientes:
        costo_ingredientes += 10
      if 'piña' in ingredientes:
        costo_ingredientes += 10
      if 'champiñones' in ingredientes:
        costo_ingredientes += 10

      numero_pizzas = create_form_pz.numero_pizza.data
      if numero_pizzas is None or numero_pizzas == '':
        numero_pizzas = 0
      subtotal_pizza = (costo_tamanio + costo_ingredientes) * int(numero_pizzas)

      fecha_de_compra_str = request.form.get('fecha_de_compra')
      if fecha_de_compra_str is not None:
        fecha_de_compra = datetime.strptime(fecha_de_compra_str, "%Y-%m-%d")
      else:
        fecha_de_compra = datetime.now()
        
      pzPizza = PizzasPizzeria(
        tamanio_pizza = create_form_pz.tamanio_pizza.data,
        ingredientes_pizza =', '.join(ingredientes),
        numero_pizza = create_form_pz.numero_pizza.data,
        id_cliente_pz = session['id_cliente'],
        subtotal_pizza = subtotal_pizza,
        fecha_de_compra = fecha_de_compra
      )
      # INSERT pizzas() values()
      db.session.add(pzPizza)
      db.session.commit()

      
    # Obtener pizzas del cliente query
    pizzas_cliente_actual = PizzasPizzeria.query.filter_by(id_cliente_pz=session['id_cliente']).all()   
    #return redirect(url_for('detalles_cliente', _anchor='pizzas'))
    return render_template("pizzeria.html", clientes=create_form_cl, pizzas=create_form_pz, registros_pizzas=pizzas_cliente_actual)
  elif 'id_cliente' in session:
    total = db.session.query(func.sum(PizzasPizzeria.subtotal_pizza)).filter_by(id_cliente_pz=session['id_cliente']).scalar()
    pizzas_cliente_actual = PizzasPizzeria.query.filter_by(id_cliente_pz=session['id_cliente']).all()  
    #return render_template("pizzeria.html", clientes=create_form_cl, pizzas=create_form_pz, registros_pizza=pizzas_cliente_actual, registro_pizzas = [])
  return render_template("pizzeria.html", clientes=create_form_cl, pizzas=create_form_pz, registros_pizza=[], registro_pizzas = [])


@app.route('/modificar_pizza', methods=['GET', 'POST'])
def modificar_pizza():
  ingredientesGuardados = []
  create_form_pz = Pizzas.pizzas(request.form)
  
  if request.method == 'GET':
    id_pizza = request.args.get('id_pizza')
    session['id_pizza'] = id_pizza
    # select from pizzas where id_pizza = id_pizza
    pza1 = db.session.query(PizzasPizzeria).filter(PizzasPizzeria.id_pizza == id_pizza).first()
    
    create_form_pz.id_pizza.data = request.args.get('id_pizza')
    create_form_pz.tamanio_pizza.data = pza1.tamanio_pizza
    create_form_pz.numero_pizza.data = pza1.numero_pizza
    create_form_pz.subtotal_pizza.data = pza1.subtotal_pizza
    ingredientesGuardados = pza1.ingredientes_pizza.split(', ')
    create_form_pz.fecha_de_compra.data = pza1.fecha_de_compra
    
  if request.method == 'POST':
    ingredientesGuardados = []
    id_pizza = create_form_pz.id_pizza.data
    pza1 = db.session.query(PizzasPizzeria).filter(PizzasPizzeria.id_pizza == id_pizza).first()  
    pza1.tamanio_pizza = create_form_pz.tamanio_pizza.data
    pza1.numero_pizza = create_form_pz.numero_pizza.data
    fecha_de_compra_str = request.form.get('fecha_de_compra')
    fecha_de_compra = datetime.strptime(fecha_de_compra_str, "%Y-%m-%d")
    pza1.fecha_de_compra = fecha_de_compra
    if create_form_pz.jamon.data:
      ingredientesGuardados.append('jamon')
    if create_form_pz.pina.data:
      ingredientesGuardados.append('piña')
    if create_form_pz.champinones.data:
      ingredientesGuardados.append('champiñones')
    pza1.ingredientes_pizza =', '.join(ingredientesGuardados)
    
    # calcular el subtotal de la pizza y actualizar 
    
    costo_tamanio = {
      'Chica': 40,
      'Mediana': 80,
      'Grande': 120
    }
    
    costo_ingredientes = {
      'jamon': 10,
      'piña': 10,
      'champiñones': 10
    }
    
    costo_tamanio_pizza = costo_tamanio.get(pza1.tamanio_pizza, 0)
    costo_ingredientes_pizza = sum(costo_ingredientes.get(ingrediente, 0)
    for ingrediente in pza1.ingredientes_pizza.split(', '))
    
    pza1.subtotal_pizza = (costo_tamanio_pizza + costo_ingredientes_pizza) * pza1.numero_pizza
    
    db.session.add(pza1)
    db.session.commit()
    pizzas_cliente_actual = PizzasPizzeria.query.filter_by(id_cliente_pz=session['id_cliente']).all()
    #pizzas_cliente_actual = PizzasPizzeria.query.filter_by(id_cliente_pz = session['id_cliente']).all()
    return redirect(url_for('detalles_cliente'))
  return render_template('modificar_pizza.html', pizzas=create_form_pz, ingredientesGuardados =ingredientesGuardados)


       
@app.route('/confirmar_terminar', methods=['POST'])
def confirmar_terminar():
  
  create_form_cl = Clientes.clientes(request.form)
  create_form_pz = Pizzas.pizzas(request.form)
  total = db.session.query(func.sum(PizzasPizzeria.subtotal_pizza)).filter_by(id_cliente_pz=session['id_cliente']).scalar()
  if request.method == 'POST':
    action = request.form.get('action')
    
    if action == 'aceptar':
      return redirect(url_for('detalles_cliente'))
    elif action == 'cancelar':
      registros_pizzas = PizzasPizzeria.query.filter_by(id_cliente_pz=session['id_cliente']).all()
      cliente = ClientesPizzeria.query.filter_by(id_cliente=session['id_cliente']).first()
      
      nombre_cliente = create_form_cl.nombre_cliente
      direccion_cliente = create_form_cl.direccion_cliente
      telefono_cliente = create_form_cl.telefono_cliente
      return render_template('pizzeria.html',registros_pizzas=registros_pizzas, clientes=create_form_cl, pizzas=create_form_pz, nombre_cliente=nombre_cliente, direccion_cliente=direccion_cliente, telefono_cliente=telefono_cliente)
  return render_template('terminar.html', total=total)
                                                                                                                                                                                                                                                              
@app.route('/ventas', methods=['GET'])
def ventas():
  create_form_cl = Clientes.clientes(request.form)
  create_form_pz = Pizzas.pizzas(request.form)
  dia = request.args.get('dia')
  mes = request.args.get('mes')
  
  dias = {
    'Lunes': 2,
    'Martes': 3,
    'Miercoles': 4,
    'Jueves': 5,
    'Viernes': 6,
    'Sabado': 7,
    'Domingo': 1
  }
  
  meses = {
    'Enero': 1,
    'Febrero': 2,
    'Marzo': 3,
    'Abril': 4,
    'Mayo': 5,
    'Junio': 6,
    'Julio': 7,
    'Agosto': 8,
    'Septiembre': 9,
    'Octubre': 10,
    'Noviembre': 11,
    'Diciembre': 12,
  }
  if dia and dia not in dias:
    return "El dia ingresado no es valido. Ingresa un dia de la semana.", 400
  if mes and mes not in meses:
    return "El mes ingresado no es valido. Ingresa un mes del año.", 400

  if dia:
    
    dia_numero = list(dias.values())[list(dias.keys()).index(dia)]
    
    ventas_dia = db.session.query(func.sum(PizzasPizzeria.subtotal_pizza)).filter(text("DAYOFWEEK(fecha_de_compra) =:dow")).params(dow=dias[dia]).scalar()
    registros_dia = db.session.query(PizzasPizzeria, ClientesPizzeria).join(ClientesPizzeria).filter(text("DAYOFWEEK(fecha_de_compra) = :dow")).params(dow=dia_numero).all()
    #registros_dia = db.session.query(PizzasPizzeria, ClientesPizzeria).join(ClientesPizzeria).filter(((func.dayofweek(PizzasPizzeria.fecha_de_compra) - 1) % 7) + 1 == dia_numero).all()
    #registros_dia = db.session.query(PizzasPizzeria, ClientesPizzeria).join(ClientesPizzeria).filter(text("DAYOFWEEK(fecha_de_compra) =:dow")).params(dow=dias[dia]).all()
    #totales_por_cliente = defaultdict(float)
    #for registro_pizza, registro_cliente in registros_dia:
     # totales_por_cliente[registro_cliente.nombre_cliente]+= registro_pizza.subtotal_pizza
    return render_template('pizzeria.html', ventas_dia=ventas_dia, clientes=create_form_cl, pizzas=create_form_pz, registros_dia=registros_dia)
  if mes:
    ventas_mes = db.session.query(func.sum(PizzasPizzeria.subtotal_pizza)).filter(extract('month', PizzasPizzeria.fecha_de_compra) == meses[mes]).scalar()
    registros_mes = db.session.query(PizzasPizzeria, ClientesPizzeria).filter(PizzasPizzeria.id_cliente_pz == ClientesPizzeria.id_cliente).filter(extract('month', PizzasPizzeria.fecha_de_compra) == meses[mes]).all()
    return render_template('pizzeria.html', ventas_mes=ventas_mes, clientes=create_form_cl, pizzas=create_form_pz, registros_mes=registros_mes) 

    #registros_mes = db.session.query(PizzasPizzeria, ClientesPizzeria).join(ClientesPizzeria).filter(extract('month', PizzasPizzeria.fecha_de_compra) == meses[mes]).all()
    #registros_dia = db.session.query(PizzasPizzeria, ClientesPizzeria).join(ClientesPizzeria).filter(text("DAYOFWEEK(fecha_de_compra) = : dow")).params(dow=dias[dia]).all()
if __name__ =="__main__":
  csrf.init_app(app)
  db.init_app(app)
  
  with app.app_context():
    db.create_all()
  app.run(debug=True)   # Cambios en tiempo real