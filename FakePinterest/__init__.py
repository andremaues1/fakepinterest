#Aqui onde a gente define o app e precia ter o nome __init__ pra funcionar

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt # faz criptografia da senha
import os

app = Flask(__name__) #importar o app é importar o arquivo __init__

if os.getenv("DEGUB") == 0:
    link_banco = os.getenv("_DATABASE_URI")
else:
    link_banco = "sqlite:///comunidade.db"

app.config["SQLALCHEMY_DATABASE_URI"] = link_banco
app.config["SECRET_KEY"] = "ca7f77263d0186ce1e8962ab89a5725f"
app.config["UPLOAD FOLDER"] = "static/fotos_posts"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager._user_callback = "yes"
login_manager.login_view = "/homepage" # caso a senha fale ele te leva pra homepage

from FakePinterest import routes




# import secrets

# print(secrets.token_hex(16)) -> gera códigos