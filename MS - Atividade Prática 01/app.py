from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import UserMixin, LoginManager, logout_user, login_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

#Configuração de App e Banco de Dados
app = Flask(__name__,)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///registros.sqlite3"
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager(app)
db = SQLAlchemy(app)

#Definição de Banco de dados
@login_manager.user_loader
def get_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(86), nullable=False, unique=True)
    username = db.Column(db.String(86), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password, email):
        self.email = email
        self.username= username
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    

#Configuração de rotas
#Rota Inicial
@app.route('/')
def index():
    return render_template('index.html')

#Rota de Login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd= request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not user.verify_password(pwd):
            flash
            return redirect(url_for('login'))        

        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')

#Rota de Registro
@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['username']
        pwd = request.form['password']
        user = User(name, pwd, email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

#Rota com funação de Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#Rota da Tela principal
@app.route('/home', methods=['GET', 'POST'])
def home():
    
    return render_template('home.html')

#Inicialização de App
if __name__ == '__main__':
    app.run(debug=True)