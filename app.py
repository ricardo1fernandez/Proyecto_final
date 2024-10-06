from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import session
# Inicializa la aplicación Flask
app = Flask(__name__)

# Configura la URI de la base de datos (actualiza según tu preferencia)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tu_base_de_datos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Opcional, para suprimir advertencias

# Inicializa la base de datos
db = SQLAlchemy(app)

# Define tus modelos de base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Define rutas
@app.route('/')
def home():
    return render_template('home.html')  # Asegúrate de crear esta plantilla

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html')  # Crea esta plantilla también

@app.route('/mail_template/<username>')
def mail_template(username):
    return render_template('mail_template.html', username=username)  # Pasa el nombre de usuario a la plantilla

@app.route('/template_view/<username>')
def template_view(username):
    return render_template('template.html', username=username)  # Pasa el nombre de usuario a la plantilla


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('template_view', username=username))  # Redirige a la plantilla de correo
    return render_template('login.html')  # Crea esta plantilla también


@app.route('/logout')
def logout():
    session.clear()  # Clear the session to log out the user
    return redirect(url_for('home'))  # Redirect to the login page
# Bloque principal para ejecutar la aplicación
if __name__ == "__main__":
    with app.app_context():  # Crea el contexto de la aplicación
        db.create_all()  # Crea las tablas de la base de datos
    app.run(debug=True)  # Ejecuta la aplicación en modo de depuración

