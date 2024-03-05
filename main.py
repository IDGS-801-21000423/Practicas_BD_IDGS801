# --------------------------------------------------------------
from flask import Flask, render_template, request, url_for, redirect     # Importar flask, render template
import forms                                          # Importar archivo forms
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g                                   # Importar variables globales
from config import DevelopmentConfig

from models import db                                 # crear instancia de clase bd
from models import Empleados

app = Flask(__name__)                                 # Nombrar la app Flask
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

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

if __name__ =="__main__":
  csrf.init_app(app)
  db.init_app(app)
  
  with app.app_context():
    db.create_all()
  app.run(debug=True)   # Cambios en tiempo real